import re
import shlex

def filter_git_diff(diff_text):
    # Split the diff into sections starting with 'diff --git'
    sections = re.split(r'(^diff)', diff_text, flags=re.MULTILINE)
    filtered_sections = []
    
    # Process each section (the first element may be a preamble)
    for i in range(1, len(sections), 2):
        separator = sections[i]
        content = sections[i + 1]
        full_section = separator + content
        
        # Split the section into lines to extract paths
        lines = full_section.split('\n', 1)  # Split into first line and the rest
        first_line = lines[0]
        
        try:
            parts = shlex.split(first_line)
        except ValueError:
            parts = first_line.split()
        
        if len(parts) < 4:
            # Malformed 'diff --git' line; include as-is
            filtered_sections.append(full_section)
            continue
        
        old_path_part = parts[2]
        new_path_part = parts[3]
        old_path = old_path_part[2:] if old_path_part.startswith('a/') else old_path_part
        new_path = new_path_part[2:] if new_path_part.startswith('b/') else new_path_part
        
        # Check if either path contains 'test'
        if 'test' not in old_path and 'test' not in new_path:
            filtered_sections.append(full_section)
    
    # Combine the preamble (if any) and filtered sections
    result = []
    if sections[0].strip():
        result.append(sections[0].rstrip('\n'))
    result.extend(filtered_sections)
    return '\n'.join(result).strip()

# import os
# def generate_line_mappings_after_to_bef(diff_text):
#     line_mappings = {}
#     # Use 'diff --git' to split sections for accuracy
#     file_sections = re.split(r'(^diff)', diff_text, flags=re.MULTILINE)
    
#     for i in range(1, len(file_sections), 2):
#         separator = file_sections[i]
#         content = file_sections[i + 1]
#         full_section = separator + content
        
#         # Extract file paths
#         first_line = full_section.split('\n', 1)[0].strip()
#         parts = re.split(r'\s+', first_line)
#         if len(parts) < 4:
#             continue
        
#         old_path = parts[2][2:] if parts[2].startswith('a/') else parts[2]
#         new_path = parts[3][2:] if parts[3].startswith('b/') else parts[3]
        
#         # Process hunks
#         file_mapping = {}
#         hunks = re.split(r'(^@@ -\d+,\d+ \+\d+,\d+ @@)', content, flags=re.MULTILINE)
#         pending_deletions = []  # Track deletions for modifications
        
#         with open(new_path, "r") as f:
#             after_line_count = len(f.readlines())
        
            
#         current_new = 1
#         current_old = 1
        
#         for j in range(1, len(hunks), 2):
#             hunk_header = hunks[j].strip()
#             hunk_content = hunks[j + 1]
            
#             header_match = re.match(r'@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@', hunk_header)
#             if not header_match:
#                 continue
            
#             old_start = int(header_match.group(1))
#             new_start = int(header_match.group(3))
            
#             while current_new < new_start and current_old < old_start:
#                 # Fill in the gaps for lines that are unchanged
#                 file_mapping[current_new] = current_old
#                 current_new += 1
#                 current_old += 1
            
#             current_old = old_start
#             current_new = new_start
            
#             for line in hunk_content.split('\n'):
#                 # line = line.strip()  # Handle trailing whitespace
#                 if not line:
#                     continue
                
#                 line_type = line[0] if line[0] in (' ', '-', '+') else ' '
#                 if line_type == ' ':
#                     # Context line: map directly
#                     pending_deletions = []  # Reset on context
#                     file_mapping[current_new] = current_old
#                     current_old += 1
#                     current_new += 1
#                 elif line_type == '-':
#                     # Track deletion's original line
#                     pending_deletions.append(current_old)
#                     current_old += 1
#                 elif line_type == '+':
#                     # Link to earliest pending deletion or mark as new
#                     if pending_deletions:
#                         file_mapping[current_new] = pending_deletions.pop(0)
#                     else:
#                         file_mapping[current_new] = None
#                     current_new += 1
#             while current_new <= after_line_count:
#                 # Fill in the gaps for lines that are unchanged
#                 file_mapping[current_new] = current_old
#                 current_new += 1
#                 current_old += 1
        
#         composite_key = f"{new_path}_{old_path}"
#         line_mappings[composite_key] = file_mapping
    
#     return line_mappings
def generate_line_mappings_after_to_bef(diff_text):
    line_mappings = {}

    # Detect diff format
    if 'diff --git' in diff_text:
        # Git-style diff — split per file section
        file_sections = re.split(r'(^diff)', diff_text, flags=re.MULTILINE)
        file_chunks = [file_sections[i] + file_sections[i + 1] for i in range(1, len(file_sections), 2)]
    else:
        # Plain unified diff — single file
        file_chunks = [diff_text]

    for chunk in file_chunks:
        # --- File Path Detection ---
        if chunk.startswith("diff"):
            # Git-style
            first_line = chunk.split('\n', 1)[0].strip()
            parts = re.split(r'\s+', first_line)
            if len(parts) < 4:
                continue
            old_path = parts[2][2:] if parts[2].startswith('a/') else parts[2]
            new_path = parts[3][2:] if parts[3].startswith('b/') else parts[3]
        else:
            # Plain unified diff
            old_line = re.search(r'^---\s+([^\t\n]+)', chunk, re.MULTILINE)
            new_line = re.search(r'^\+\+\+\s+([^\t\n]+)', chunk, re.MULTILINE)
            if not old_line or not new_line:
                continue
            old_path = old_line.group(1).strip()
            new_path = new_line.group(1).strip()
            if old_path.startswith('a/'):
                old_path = old_path[2:]
            if new_path.startswith('b/'):
                new_path = new_path[2:]
            

        # --- Read the new file (after version) ---
        try:
            with open(new_path, "r") as f:
                after_line_count = len(f.readlines())
        except FileNotFoundError:
            # Skip if the new file does not exist
            continue

        file_mapping = {}
        hunks = re.split(r'(^@@ -\d+(?:,\d+)? \+\d+(?:,\d+)? @@)', chunk, flags=re.MULTILINE)
        pending_deletions = []

        current_new = 1
        current_old = 1

        for j in range(1, len(hunks), 2):
            hunk_header = hunks[j].strip()
            hunk_content = hunks[j + 1]

            header_match = re.match(r'@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@', hunk_header)
            if not header_match:
                continue

            old_start = int(header_match.group(1))
            new_start = int(header_match.group(3))

            # Fill in unchanged lines before this hunk
            while current_new < new_start and current_old < old_start:
                file_mapping[current_new] = current_old
                current_new += 1
                current_old += 1

            current_old = old_start
            current_new = new_start

            for line in hunk_content.split('\n'):
                if not line:
                    continue
                line_type = line[0] if line[0] in (' ', '-', '+') else ' '

                if line_type == ' ':
                    pending_deletions = []
                    file_mapping[current_new] = current_old
                    current_old += 1
                    current_new += 1
                elif line_type == '-':
                    pending_deletions.append(current_old)
                    current_old += 1
                elif line_type == '+':
                    if pending_deletions:
                        file_mapping[current_new] = pending_deletions.pop(0)
                    else:
                        file_mapping[current_new] = None
                    current_new += 1

        # Fill in remaining unchanged lines after last hunk
        while current_new <= after_line_count:
            file_mapping[current_new] = current_old
            current_new += 1
            current_old += 1

        composite_key = f"{new_path}_{old_path}"
        line_mappings[composite_key] = file_mapping

    return line_mappings

import re

def generate_line_mappings_bef_to_prev(diff_text):
    line_mappings = {}
    # Use 'diff --git' to split sections for accuracy
    file_sections = re.split(r'(^diff --git)', diff_text, flags=re.MULTILINE)
    
    for i in range(1, len(file_sections), 2):
        separator = file_sections[i]
        content = file_sections[i + 1]
        full_section = separator + content
        
        # Extract file paths
        first_line = full_section.split('\n', 1)[0].strip()
        parts = re.split(r'\s+', first_line)
        if len(parts) < 4:
            continue
        
        old_path = parts[2][2:] if parts[2].startswith('a/') else parts[2]
        new_path = parts[3][2:] if parts[3].startswith('b/') else parts[3]
        
        # Process hunks
        file_mapping = {}
        hunks = re.split(r'(^@@ -\d+,\d+ \+\d+,\d+ @@)', content, flags=re.MULTILINE)
        pending_deletions = []  # Track deletions for modifications
        
        for j in range(1, len(hunks), 2):
            hunk_header = hunks[j].strip()
            hunk_content = hunks[j + 1]
            
            header_match = re.match(r'@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@', hunk_header)
            if not header_match:
                continue
            
            old_start = int(header_match.group(1))
            new_start = int(header_match.group(3))
            current_old = old_start
            current_new = new_start
            
            for line in hunk_content.split('\n'):
                # line = line.strip()  # Handle trailing whitespace
                if not line:
                    continue
                
                line_type = line[0] if line[0] in (' ', '-', '+') else ' '
                if line_type == ' ':
                    if pending_deletions:
                        # Mapping lost
                        for pending in pending_deletions:
                            file_mapping[pending] = None
                            
                    # Context line: map directly
                    pending_deletions = []  # Reset on context
                    file_mapping[current_old] = current_new
                    current_old += 1
                    current_new += 1
                elif line_type == '-':
                    # Track addition's original line
                    pending_deletions.append(current_old)
                    current_old += 1
                elif line_type == '+':
                    # Link to earliest pending deletion or mark as new
                    if pending_deletions:
                        file_mapping[pending_deletions.pop(0)] = current_new
                    # else:
                    #     file_mapping[current_old] = None
                    current_new += 1
        
        composite_key = f"{new_path}_{old_path}"
        line_mappings[composite_key] = file_mapping
    
    return line_mappings

### MARK - Patch Correction
PATCH_PATTERN = re.compile(
    r"(?:diff[\w\_\.\ \/\-]+\n)?\-\-\-\s+a\/(?:.*?)\n\+\+\+\s+b\/(?:.*?)(?=diff\ |\-\-\-\ a\/|\Z)",
    re.DOTALL,
)
PATCH_FILE_PATTERN = re.compile(r"\-\-\-\s+a\/(?:.+)\n\+\+\+\s+b\/(?:.+)")
PATCH_HUNK_PATTERN = re.compile(
    r"\@\@\s+\-(\d+),(\d+)\s+\+(\d+),(\d+)\s+\@\@(.+?)(?=diff\ |\-\-\-\ a\/|\@\@\ \-|\Z)",
    re.DOTALL,
)


def get_first_idx(charlist):
    """Get index of first occurrence of "-" or "+" in charlist"""
    first_min = charlist.index("-") if "-" in charlist else len(charlist)
    first_plus = charlist.index("+") if "+" in charlist else len(charlist)
    return min(first_min, first_plus)


def get_last_idx(charlist):
    """Get index of last occurrence of "-" or "+" in charlist"""
    char_idx = get_first_idx(charlist[::-1])
    last_idx = len(charlist) - char_idx
    return last_idx + 1


def strip_content(hunk):
    """Remove trailing non +/- lines and trailing whitespace per line per hunk"""
    first_chars = list(map(lambda x: None if not len(x) else x[0], hunk.split("\n")))
    first_idx = get_first_idx(first_chars)
    last_idx = get_last_idx(first_chars)
    new_lines = list(map(lambda x: x.rstrip(), hunk.split("\n")[first_idx:last_idx]))
    new_hunk = "\n" + "\n".join(new_lines) + "\n"
    return new_hunk, first_idx - 1


def get_hunk_stats(pre_start, pre_len, post_start, post_len, hunk, total_delta):
    """Recalculate hunk start/end position and diff delta"""
    stats = {"context": 0, "added": 0, "subtracted": 0}
    hunk = hunk.split("\n", 1)[-1].strip("\n")
    for line in hunk.split("\n"):
        if line.startswith("-"):
            stats["subtracted"] += 1
        elif line.startswith("+"):
            stats["added"] += 1
        else:
            stats["context"] += 1
    context = stats["context"]
    added = stats["added"]
    subtracted = stats["subtracted"]
    pre_len = context + subtracted
    post_start = pre_start + total_delta
    post_len = context + added
    total_delta = total_delta + (post_len - pre_len)
    return pre_start, pre_len, post_start, post_len, total_delta


def extract_minimal_patch(model_patch):
    """
    Wrapper function that takes hunk and
    * Removes trailing non +/- lines and trailing whitespace per line per hunk
    * Recalculates hunk start/end position and diff delta
    * Returns new patch
    """
    model_patch = model_patch.lstrip("\n")
    new_patch = ""
    for patch in PATCH_PATTERN.findall(model_patch):
        total_delta = 0
        patch_header = PATCH_FILE_PATTERN.findall(patch)[0]
        if patch_header:
            new_patch += patch_header + "\n"
        for hunk in PATCH_HUNK_PATTERN.findall(patch):
            pre_start, pre_len, post_start, post_len, content = hunk
            pre_start, pre_len, post_start, post_len, content = list(
                map(lambda x: int(x) if x.isnumeric() else x, hunk)
            )
            content, adjust_pre_start = strip_content(content)
            pre_start += adjust_pre_start
            pre_start, pre_len, post_start, post_len, total_delta = get_hunk_stats(
                pre_start, pre_len, post_start, post_len, content, total_delta
            )
            new_patch += (
                f"@@ -{pre_start},{pre_len} +{post_start},{post_len} @@{content}"
            )
    return new_patch