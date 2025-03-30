from swebench_docker.constants import RULES, CWE_LIST



def get_vulnerabilities_info(codeql_result):
    """
    Extracts vulnerabilities information from the CodeQL result.
    
    Args:
        codeql_result (dict): The CodeQL result dictionary.
        
    Returns:
        list: A list of dictionaries containing vulnerability information.
    """
    vulnerabilities = []
    for vuln in codeql_result["runs"][0]["results"]:
        # Don't include the vulnerability if it include the "test" keyword
        is_test = False
        for location in vuln["locations"]:
            if "test" in location["physicalLocation"]["artifactLocation"]["uri"].lower():
                is_test = True
                break
        if is_test:
            continue
        vulnerabilities.append(vuln)
    return vulnerabilities

def get_vulnerabilities_type_count(vulnerabilities, cwe_id: str = "all", location: str = "all"):
    """
    Count the number of vulnerabilities by type.
    
    Args:
        vulnerabilities (list): A list of vulnerabilities.
        
    Returns:
        dict: A dictionary with vulnerability types as keys and their counts as values.
    """
    type_count = {}

    for vuln in vulnerabilities:
        if location != "all":
            if location not in vuln["locations"][0]["physicalLocation"]["artifactLocation"]["uri"]:
                continue
        if cwe != "all":
            cwes = [cwe_id]
        else:
            cwes = [_id for _id in RULES[vuln["ruleId"]] if _id in CWE_LIST]
        for cwe in cwes:
            if cwe not in type_count:
                type_count[cwe] = []
            type_count[cwe].append(vuln)
    return type_count

def get_vulnerability_type(vulnerability):
    """
    Get the type of a vulnerability.
    
    Args:
        vulnerability (dict): A vulnerability dictionary.
        
    Returns:
        str: The type of the vulnerability.
    """
    return RULES[vulnerability["ruleId"]]
            
   
