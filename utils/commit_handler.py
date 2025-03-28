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

def generate_line_mappings(diff_text):
    line_mappings = {}
    # Use 'diff --git' to split sections for accuracy
    file_sections = re.split(r'(^diff)', diff_text, flags=re.MULTILINE)
    
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
                line = line.strip()  # Handle trailing whitespace
                if not line:
                    continue
                
                line_type = line[0] if line[0] in (' ', '-', '+') else ' '
                if line_type == ' ':
                    # Context line: map directly
                    pending_deletions = []  # Reset on context
                    file_mapping[current_new] = current_old
                    current_old += 1
                    current_new += 1
                elif line_type == '-':
                    # Track deletion's original line
                    pending_deletions.append(current_old)
                    current_old += 1
                elif line_type == '+':
                    # Link to earliest pending deletion or mark as new
                    if pending_deletions:
                        file_mapping[current_new] = pending_deletions.pop(0)
                    else:
                        file_mapping[current_new] = None
                    current_new += 1
        
        composite_key = f"{new_path}_{old_path}"
        line_mappings[composite_key] = file_mapping
    
    return line_mappings