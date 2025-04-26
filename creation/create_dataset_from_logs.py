from swebench_docker.utils.testcase_handler import TESTCASE_HANDLER
from swebench_docker.constants import RULES, CWE_LIST
import os
import json
import argparse
from typing import List, Dict
from datasets import DatasetDict, Dataset


def get_test_case(
    log_dir: str
):
    """
    Get test cases for a single project from the log directory.

    Args:
        log_dir (str): Path to the log directory.

    Returns:
        dict: A dictionary containing the test cases.
    """
    # Get all log files in the directory
    # Get the folder name from the log_dir
    folder_name = os.path.basename(log_dir)
    
    repo_name = "/".join(folder_name.split("__")[:2])
    test_case_log_file = None
    for file in os.listdir(log_dir):
        if "test_case" in file:
            test_case_log_file = os.path.join(log_dir, file)
            break
    

    # Initialize an empty dictionary to store test cases
    test_cases = None
    test_case_list = []

    with open(test_case_log_file, "r") as f:
        log_content = f.read()
        test_cases = TESTCASE_HANDLER.get(repo_name)(log_content)
        # if "litellm" in repo_name:
        #     print(log_content)
        #     print(test_cases)
    if test_cases is None:
        # print(f"No test cases found for {repo_name}")
        raise ValueError(f"No test cases found for {repo_name}")
    else:
        for tc_name, status in test_cases.items():
            test_case_list.append(
                {
                    "test_case_name": tc_name,
                    "status": status,
                }
            )
            
    return test_case_list


def get_vulnerabilities(
    log_dir: str,
):
    """
    Get vulnerabilities for a single project from the log directory.

    Args:
        log_dir (str): Path to the log directory.

    Returns:
        dict: A dictionary containing the vulnerabilities.
    """
    # Get all log files in the directory
    # Get the folder name from the log_dir
    folder_name = os.path.basename(log_dir)
    vulnerabilities = []
    
    repo_name = "/".join(folder_name.split("__")[:2])
    vulnerabilities_log_file = None
    for file in os.listdir(log_dir):
        if "vulnerability" in file:
            vulnerabilities_log_file = os.path.join(log_dir, file)
            break
    

    # Initialize an empty dictionary to store vulnerabilities
    vulnerability_json = None

    # It is a JSON file
    with open(vulnerabilities_log_file, "r") as f:
        log_content = f.read()
        vulnerability_json = json.loads(log_content)
    if vulnerability_json is None:
        # print(f"No vulnerabilities found for {repo_name}")
        raise ValueError(f"No vulnerabilities found for {repo_name}")
    
    for vuln in vulnerability_json["runs"][0]["results"]:
        should_skip = False
        for location in vuln["locations"]:
            if "test" in location["physicalLocation"]["artifactLocation"]["uri"].lower():
                should_skip = True
                break
            # else:
            if repo_name == "red-hat-storage/ocs-ci":
                if "src/ocp-network-split" in location["physicalLocation"]["artifactLocation"]["uri"]:
                    should_skip = True
                    break

        if should_skip:
            continue
        if vuln["ruleId"] not in RULES:
            continue
        if vuln["ruleId"] in RULES:
            vulnerabilities.append(
                vuln
            )
    
    return vulnerabilities
    
    

def create_dataset(
    log_dir: str,
    output_dir: str,
    dataset_name: str,
    # vulnerabilities_json_path: str = None,
):
    datapoints = []
    
    for folder in os.listdir(log_dir):
        try:
            folder_path = os.path.join(log_dir, folder)
            if os.path.isdir(folder_path):
                print(f"Processing folder: {folder}")
                owner, repo, base_commit = folder.split("__")
                repo = f"{owner}/{repo}"  
                testcase_status = get_test_case(folder_path)
                vulnerability_report = get_vulnerabilities(folder_path)

                    # print(vulnerability_report)
                for i, vuln in enumerate(vulnerability_report):
                    instance_repo = repo
                    instance_base_commit = base_commit
                    instance_id = f"{repo.replace('/', '__')}__{i}"
                    instance_target_vulnerability = vuln
                    instance_vulnerability_report = vulnerability_report
                    instance_testcase_status = testcase_status
                    # import pprint
                    # pprint.pprint(instance_testcase_status)
                    # print(type(list(instance_testcase_status.values())[0]))
                    # exit(0)
                    datapoints.append(
                        {
                            "repo": instance_repo,
                            "base_commit": instance_base_commit,
                            "instance_id": instance_id,
                            "target_vulnerability": instance_target_vulnerability,
                            "vulnerability_report": instance_vulnerability_report,
                            "testcase_status": instance_testcase_status,
                        }
                    )
                    # if "litellm" in repo:
                    #     print(testcase_status)
        except Exception as e:
            print(f"Error processing folder {folder}: {e}")
            continue
    # Create a DatasetDict
    dataset = Dataset.from_list(datapoints)
    # print(datapoints[0]["testcase_status"])
    # print(type(datapoints[0]["testcase_status"]))
    # print(dataset[0]["testcase_status"])
    dataset_dict = DatasetDict(
        {
            "test": dataset
        }
    )
    # print(datapoints[0])
    # Save the dataset
    dataset_dict.save_to_disk(os.path.join(output_dir, dataset_name))
    print(f"Dataset saved to {os.path.join(output_dir, dataset_name)}")
            
            
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create dataset from logs")
    parser.add_argument(
        "--log_dir", type=str, help="Path to the log directory", required=True
    )
    parser.add_argument(
        "--output_dir", type=str, help="Path to the output directory", required=True
    )
    parser.add_argument(
        "--dataset_name",
        type=str,
        help="Name of the dataset to be created",
        required=True,
    )
    args = parser.parse_args()

    create_dataset(args.log_dir, args.output_dir, args.dataset_name)
