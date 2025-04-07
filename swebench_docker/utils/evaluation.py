# Copyright (c) Meta Platforms, Inc. and affiliates.
# Adapted from: https://github.com/aorwall/SWE-bench-docker/blob/main/swebench_docker/utils.py

import glob
import json
import os
import re
from enum import Enum
from typing import Callable, Dict, Optional, Tuple

from datasets import load_dataset, load_from_disk
from swebench_docker.constants import (
    INSTALL_FAIL,
    KEY_ID,
    KEY_INSTANCE_ID,
    NON_TEST_EXTS,
    RESET_FAILED,
    TESTS_CONFIG,
    TESTS_ERROR,
    TESTS_FAILED,
    TESTS_PASSED,
    TESTS_TIMEOUT,
    UNFILTERED_TESTS_FAILED,
    UNFILTERED_TESTS_PASSED,
    VALID_K,
    RULES,
    CWE_LIST
)

from swebench_docker.utils.testcase_handler import TestStatus, TESTCASE_HANDLER

from swebench_docker.utils.vulnerabilities_handler import get_vulnerability_type, get_vulnerabilities_type_count, get_vulnerabilities_info
from swebench_docker.utils.commit_handler import generate_line_mappings_after_to_bef


def classify_error(test_str: str) -> str:
    if TESTS_PASSED in test_str:
        return "Success"
    elif "Error" in test_str:
        error_type = test_str.rsplit("Error")[0].split()[-1].split(".")[-1] + "Error"
        if "Test" in error_type:
            return "Other"
        return error_type
    elif "Val..." in test_str:
        return "ValueError"
    elif "Test script run timed out" in test_str:
        return "TimeoutError"
    elif "ass..." in test_str:
        return "AssertionError"
    elif "Ass" in test_str:
        return "AssertionError"
    elif "test" not in test_str:
        return "PostprocessingError"
    else:
        return "Other"

def get_line_coverage(coverage_json: Dict) -> Dict[str, dict]:
    """
    
    """
    
    results = {}
        
    for file_name, result in coverage_json["files"].items():
        if "test" in file_name.lower():
            continue
        else:
            results[file_name] = result["executed_lines"]
    return results
    
def check_resolved_vulnerability(vulnerability: Dict, old_report: list, new_report: Dict, patch_str: str) -> bool:
    
    # with open(new_report_fp, "r") as f:
    #     new_report = json.load(f)
    
    new_vulnerabilities = get_vulnerabilities_info(new_report)
    old_vulnerabilities = old_report
    


    # Get the target vulnerability CWE and locations
    cwe_id = get_vulnerability_type(vulnerability)[0]
    file_location_set = set()
    distinct_location_set = set()
    
    # Get the file locations and line numbers of the vulnerability in the old report
    for location in vulnerability["locations"]:
        file_location = location["physicalLocation"]["artifactLocation"]["uri"]
        start_line = location["physicalLocation"]["region"]["startLine"]
        
        file_location_set.add(file_location)
        distinct_location_set.add(
            (file_location, start_line)
        )
        
    # Check if there is reduction in the number of vulnerabilities
    # in the new report compared to the old report for the same CWE
    # and file locations
    lower_vuln_file_count = False
    vulns_at_locations_and_cwe = {}
    for location in file_location_set:
        new_type_count = get_vulnerabilities_type_count(
            new_vulnerabilities, cwe_id, location
        )
        old_type_count = get_vulnerabilities_type_count(
            old_vulnerabilities, cwe_id, location
        )
        if len(new_type_count[cwe_id]) < len(old_type_count[cwe_id]):
            lower_vuln_file_count = True
        vulns_at_locations_and_cwe[location] = new_type_count
    
    
    # Check if there is reduction in the number of vulnerabilities
    # in the new report compared to the old report for all files
    # for the same CWE
    new_type_count_all = get_vulnerabilities_type_count(
        new_vulnerabilities, cwe_id, "all"
    )
    old_type_count_all = get_vulnerabilities_type_count(
        old_vulnerabilities, cwe_id, "all"
    )
    if len(new_type_count_all[cwe_id]) < len(old_type_count_all[cwe_id]):
        lower_vuln_count = True
    else:
        lower_vuln_count = False
    
    # If there is reduction in the number of vulnerabilities
    # check if the reduced vulnerabilities contains the target vulnerability
    if lower_vuln_count and lower_vuln_file_count:
        # Check mapping lines
        file_line_mapping = generate_line_mappings_after_to_bef(patch_str)
        
        # resolving = T
        for location in distinct_location_set:
            mapping = file_line_mapping.get(location[0], None)
            if mapping is None:
                # The patch did not change the file that includes the vulnerability
                # Thus, the vulnerability is not resolved
                return False
            if location[1] in mapping:
                # Check if the line number of the vulnerability is in the mapping
                # If it is, then the vulnerability is resolved
                # Get the vulnerabilities at the location
                vulns_at_location = vulns_at_locations_and_cwe[location[0]][cwe_id]
                for vuln in vulns_at_location:
                    if mapping[vuln["locations"][0]["physicalLocation"]["region"]["startLine"]] == location[1]:
                        # The vulnerability is resolved
                        return True
    # If there is no reduction in the number of vulnerabilities
    # in the new report compared to the old report for the same CWE
    # and file locations, then the vulnerability is not resolved
    return False

def check_testcase_statuses(bef_testcase_status: Dict[str, list[str]], after_testcase_status: Dict[str, list[str]]) -> bool:
    """
    Check if the test cases that passed before the patch are still passing after the patch
    and the test cases that failed before either passed or failed after the patch.
    """
    # Check if:
    # 1. The test cases that passed before the patch are still passing after the patch
    # 2. The test cases that failed before either passed or failed after the patch
    # 3. The test cases skipped either passed or skipped after the patch
    
    for test_case in bef_testcase_status:
        if bef_testcase_status[test_case] == TestStatus.PASSED.value:
            if test_case not in after_testcase_status or after_testcase_status[test_case] != TestStatus.PASSED.value:
                print(f"Test case {test_case} failed after patch")
                return False
        elif bef_testcase_status[test_case] == TestStatus.FAILED.value:
            if test_case not in after_testcase_status:
                print(f"Test case {test_case} not found after patch")
                return False
        elif bef_testcase_status[test_case] == TestStatus.SKIPPED.value:
            if test_case not in after_testcase_status or after_testcase_status[test_case] == TestStatus.FAILED.value:
                print(f"Test case {test_case} failed after patch")
                return False
        elif bef_testcase_status[test_case] == TestStatus.ERROR.value:
            if test_case not in after_testcase_status:
                print(f"Test case {test_case} not found after patch")
                return False
        elif bef_testcase_status[test_case] == TestStatus.XFAIL.value:
            if test_case not in after_testcase_status or after_testcase_status[test_case] != TestStatus.XFAILED.value:
                print(f"Test case {test_case} failed after patch")
                return False
    
    return True
    
                

def get_dir_eval(dir_path: str, task_instance: Dict) -> Dict[str, dict]:
    """
    Retrieve evaluation results for a task instance from its corresponding dir log file

    Args:
        dir_path (str): path to dir log file
    Returns:
        bool: whether the patch applied successfully
        dict: status map
    """
    repo = task_instance["repo"]
    # Get the test case status
    before_testcase_status = task_instance["testcase_status"]
    # Get the vulnerability status
    before_all_vulnerabilities = task_instance["vulnerability_report"]
    # Get target vulnerability
    target_vulnerability = task_instance["target_vulnerability"]

    # print(task_instance[KEY_INSTANCE_ID])
    results: Dict[str, dict] = {}
    
    # There should be 5 files in the directory
    # 1. .log
    # 2. test_case.json
    # 3. test_case.log
    # 4. vulnerability.json
    # 5. .patch
    
    # If there are not 5 files, return empty dict
    # TODO: validate this later, but return empty dict for now
    files = os.listdir(dir_path)
    if len(files) != 5:
        return results
    
    # Open the 4 files
    # Based on the file name, get the file type
    for file in files:
        if file.endswith(".log") and "test_case" not in file:
            log_fp = os.path.join(dir_path, file)
        if file.endswith(".log") and "test_case" in file:
            testcase_fp = os.path.join(dir_path, file)
        if file.endswith(".json") and "vulnerability" in file:
            vulnerability_fp = os.path.join(dir_path, file)
        if file.endswith(".json") and "coverage" in file:
            coverage_fp = os.path.join(dir_path, file)
        if file.endswith(".patch"):
            patch_fp = os.path.join(dir_path, file)
            
    # Open files
    with open(log_fp, "r") as f:
        log_content = f.read()
        
    with open(testcase_fp, "r") as f:
        testcase_log_content = f.read()
    
    with open(vulnerability_fp, "r") as f:
        vulnerability_content = json.load(f)
        
    with open(coverage_fp, "r") as f:
        coverage_content = json.load(f)
        
    # Get the patch content
    with open(patch_fp, "r") as f:
        patch_content = f.read()
        
    # Check if the patch applied successfully
    result = {
        "patch_applied": False,
        "testcase_status": False,
        "all_testcases_statuses": {},
        "vulnerability_resolved": False,
        "vulnerabilities_found": {},
        "coverage": {}
    }
    
    # Check if the patch applied successfully
    if INSTALL_FAIL in log_content:
        result["patch_applied"] = False
    elif RESET_FAILED in log_content:
        result["patch_applied"] = False
    else:
        result["patch_applied"] = True
        
    # Get the test case status
    test_case_handler = TESTCASE_HANDLER.get(repo, None)
    # print(repo)
    if test_case_handler is None:
        raise ValueError(f"Test case handler not found for repo {repo}")
    after_testcase_status = test_case_handler(testcase_log_content)
    
    result["testcase_status_compare"] = check_testcase_statuses(
        before_testcase_status, after_testcase_status
    )
    
    result["all_testcases_statuses"] = after_testcase_status
    
    # Get the vulnerability status
    result["vulnerability_resolved"] = check_resolved_vulnerability(
        target_vulnerability, before_all_vulnerabilities, vulnerability_content, patch_content
    )
    
    # Get the vulnerabilities found
    vulnerabilities_found = get_vulnerabilities_info(vulnerability_content)
    result["vulnerabilities_found"] = vulnerabilities_found
    
    result["coverage"] = get_line_coverage(coverage_content)
    return result
  


def get_eval_reports_for_instance_dir(
    eval_dirs: list,
    swe_bench_instances: dict,
    callback: Optional[Callable[[str], bool]] = None,
    # verbose: bool = False,
    raw_only: bool = False,
    is_baseline: bool = False,
) -> Dict[str, dict]:
    """
    Wrapper for getting eval report for a list of evaluation log paths.

    Args:
        eval_dirs (list): list of paths to evaluation log dirs
        swe_bench_instances (str): path to eval task instances (swe-bench.json)
        callback (callable): callback function for evaluation logs
        verbose (bool): whether to print verbose output
    Returns:
        reports_patch_success (dict): dict of eval reports for patch apply successes
        reports_patch_failure (dict): dict of eval reports for patch apply failures
    """
    report_tests = {}

    from tqdm import tqdm

    for eval_dir in tqdm(eval_dirs):
        # Remove task instances that do not satisfy callback
        if callback is not None and not callback(eval_dir):
            continue
        try:
            # Get eval logs
            # print(eval_dir)
            instance_id = eval_dir.split("/")[-1].split(".")[0]
            print(instance_id)
            eval_sm = get_dir_eval(eval_dir, task_instance=swe_bench_instances[instance_id])
            if eval_sm != {}:
                print("Has Report")
            else:
                print("No Report") 
            # report = (
            #     get_eval_report(eval_sm, swe_bench_instances, instance_id, is_baseline)
            #     if not raw_only
            #     else eval_sm
            # )
            
            report_tests[get_file_name_from_lp(eval_dir)] = eval_sm
        except Exception as e:
            print("error in instance", instance_id)
            print(e)
            raise e
            print(f"Skipping instance {get_file_name_from_lp(eval_log)}")

    report_final = {}

    # Merge settings
    for eval_dir in eval_dirs:
        instance_id = eval_dir.split("/")[-1].split(".")[0]
        # print(instance_id)
        # print(get_file_name_from_lp(eval_dir))
        if instance_id not in report_final:
            # print("Add")
            report_final[instance_id] = report_tests[get_file_name_from_lp(eval_dir)]
        else:
            # print("Update")
            report_final[instance_id].update(
                report_tests[get_file_name_from_lp(eval_dir)]
            )

    return report_final



# def get_eval_report(
#     eval_sm: dict,
#     swe_bench_instances: dict,
#     instance_id: str,
#     is_baseline: bool = False,
# ) -> dict:
#     """
#     Create a report based on failure/pass change from gold results to eval results.

#     Args:
#         eval_sm (dict): evaluation status map
#     Returns:
#         report (dict): report of metrics
#     """
#     # Calculate resolution metrics

#     final_results: Dict[str, float] = {}

#     for setting in eval_sm:
#         tests_passed = eval_sm[setting]["tests_passed"]
#         unfiltered_tests_passed = (
#             eval_sm[setting]["unfiltered_tests_passed"]
#             if "unfiltered_tests_passed" in eval_sm[setting]
#             else []
#         )

#         if not is_baseline:
#             baseline_cov_info = swe_bench_instances[instance_id]["baseline_covs"]

#             add_execution_metric(
#                 eval_sm, final_results, setting, baseline_cov_info, "coverage"
#             )
#             if setting == "full":
#                 add_execution_metric(
#                     eval_sm, final_results, setting, {}, "mutation_score"
#                 )
#         else:
#             final_results[f"{setting}_av_coverage"] = eval_sm[setting]["coverage"][0]

#         for k in VALID_K:
#             if len(tests_passed) >= k:
#                 final_results[f"{setting}_pass_at_{k}"] = any(tests_passed[:k])
#             if len(tests_passed) >= k:
#                 final_results[f"{setting}_avg_pass_at_{k}"] = sum(
#                     tests_passed[:k]
#                 ) / len(tests_passed[:k])
#             if len(unfiltered_tests_passed) >= k:
#                 final_results[f"{setting}_unfiltered_pass_at_{k}"] = any(
#                     unfiltered_tests_passed[:k]
#                 )

#         for metric in eval_sm[setting]:
#             if metric not in [
#                 "tests_passed",
#                 "tests_compiled",
#                 "unfiltered_tests_passed",
#                 "unfiltered_tests_compiled",
#                 "coverage",
#                 "mutation_score",
#                 "test_error",
#             ]:
#                 met_non_negative = [
#                     eval_sm[setting][metric][i]
#                     for i in range(len(eval_sm[setting][metric]))
#                     if eval_sm[setting][metric][i] >= 0
#                 ]
#                 if len(met_non_negative) == 0:
#                     final_results[f"{setting}_av_{metric}"] = -1
#                 else:
#                     final_results[f"{setting}_av_{metric}"] = sum(
#                         eval_sm[setting][metric]
#                     ) / len(eval_sm[setting][metric])
#     return final_results


get_file_name_from_lp = lambda x: x.rsplit("/", 1)[-1]


get_id_from_lp = lambda x: get_file_name_from_lp(x).split(".")[0]


get_repo_from_lp = lambda x: get_id_from_lp(x).rsplit("-", 1)[0].replace("__", "/")


test_passed = lambda case, sm: case in sm and sm[case] == TestStatus.PASSED.value

test_failed = lambda case, sm: case not in sm or any(
    [sm[case] == status for status in [TestStatus.FAILED.value, TestStatus.ERROR.value]]
)


def get_eval_reports_for_dir(
    eval_dir: str,
    swe_bench_instances: dict,
    model_name,
    callback: Optional[Callable[[str], bool]] = None,
    raw_only=False,
    is_baseline=False,
) -> dict:
    """
    Wrapper for getting eval report for a directory of evaluation logs.

    Args:
        eval_dir (str): path to directory of evaluation logs
        (See get_eval_reports_for_logs for other args)
    """
    if not os.path.exists(eval_dir):
        raise ValueError(f"Path {eval_dir} does not exist")
    # logs_list = [x for x in glob.glob(os.path.join(eval_dir, f"*{model_name}*.log"))]
    
    repo_dirs = [os.path.join(eval_dir, x) for x in os.listdir(eval_dir)]
    return get_eval_reports_for_instance_dir(
        repo_dirs, swe_bench_instances, callback, raw_only, is_baseline
    )


### MARK - Model Evaluation Summary


def get_model_eval_summary(
    predicts_path: str,
    eval_dir: str,
    swe_bench_instances: dict,
    model_name: str,
    repo: Optional[str] = None,
    is_baseline: bool = False,
) -> dict:
    """
    Generate a summary of model evaluation results.

    Args:
        predicts_path (str): path to predictions file
        eval_dir (str): path to directory of evaluation logs
        swe_bench_instances (str): path to eval references (swe-bench-eval-refs.json)
        repo (str): if given, repo name to limit evaluation to
    """
    # Load Predictions
    preds = []
    if len(predicts_path) > 0:
        with open(predicts_path) as f:
            for line in f.readlines():
                preds.append(json.loads(line))

        # Filter by repo if provided
        criteria_eval_sm = None
        if repo is not None:
            criteria_pred = lambda pred: repo in pred[KEY_ID]
            criteria_eval_sm = lambda eval_log: repo in eval_log
            preds = [x for x in preds if criteria_pred(x)]
        # print("HERE")
        # Get reports
        report_net = get_eval_reports_for_dir(
            eval_dir,
            swe_bench_instances,
            is_baseline=is_baseline,
            callback=criteria_eval_sm,
            model_name=model_name,
        )
    else:
        # print("else")
        report_net = get_eval_reports_for_dir(
            eval_dir,
            swe_bench_instances,
            is_baseline=is_baseline,
            model_name=model_name,
        )

    # Print reports for different granularities of patch success/failure
    summary = {
        "repo": repo if repo is not None else "all",
        "total_predictions": len(preds),
    }

    format_dec = lambda x: round(x * 100, 2)

    total_metrics: Dict[str, list] = {}
    print("Ở ĐÂY")
    i = 0
    for fn in report_net:
        # print(i)
        # print(fn)
        # print(report_net[fn])
        i += 1
        for key in report_net[fn]:
            # print(key)
            if key in ["patch_applied", "testcase_status_compare", "vulnerability_resolved"]:
                if key not in total_metrics:
                    total_metrics[key] = []
                total_metrics[key].append(report_net[fn][key])
    for met in total_metrics:
        cleansed_metrics = [e for e in total_metrics[met] if e != -1]
        if len(cleansed_metrics) == 0:
            summary[met] = -1
        else:
            summary[met] = sum(cleansed_metrics) / len(cleansed_metrics)

    return summary


# def get_model_report(
#     model: str,
#     predictions_path: str,
#     log_dir: str,
#     verbose: bool = False,
# ) -> dict:
#     """
#     Generate a report of model evaluation results from predictions, task instances,
#     and evaluation logs.

#     Args:
#         model (str): model name
#         predictions_path (str): path to predictions file
#         log_dir (str): path to directory of evaluation logs
#         verbose (bool): show tqdm to track progress
#     Returns:
#         report_map (dict): map of repo to report
#     """
#     from tqdm import tqdm

#     # Get predictions
#     predictions = []
#     if predictions_path.endswith("jsonl"):
#         with open(predictions_path) as f:
#             for line in f.readlines():
#                 predictions.append(json.loads(line))
#     elif predictions_path.endswith("json"):
#         predictions = json.load(open(predictions_path))
#     else:
#         raise ValueError("Predictions file must be in json or jsonl format")
#     report_map: Dict[str, list] = {}

#     # Iterate through predictions
#     report_map = {
#         "no_generation": [],
#         "generated": [],
#         "with_logs": [],
#         "install_fail": [],
#         "reset_failed": [],
#         "test_errored": [],
#         "test_timeout": [],
#         "mutation_timeout": [],
#     }
#     for p in tqdm(predictions, desc="Processing predictions new", disable=not verbose):
#         report_map["generated"].append(p[KEY_ID])

#         # Get log file
#         log_path = os.path.join(log_dir, f"{p[KEY_ID]}.{model}.eval.log")
#         if not os.path.exists(log_path):
#             continue
#         report_map["with_logs"].append(p[KEY_ID])
#         log_content = open(log_path).read()

#         # Check if there is a reset failure
#         if RESET_FAILED in log_content:
#             report_map["reset_failed"].append(p[KEY_ID])
#             continue

#         # Get evaluation logs
#         eval_sm = get_logs_eval(log_path)

#         # Check if any tests errored or timed out
#         for status in [
#             ("test_errored", TESTS_ERROR),
#             ("test_timeout", TESTS_TIMEOUT),
#             ("mutation_timeout", "MutationTimeout"),
#         ]:
#             if status[1] in log_content:
#                 report_map[status[0]].append(p[KEY_ID])
#                 continue

#     return report_map


def get_instances(instance_path: str) -> list:
    """
    Get task instances from given path

    Args:
        instance_path (str): Path to task instances
    Returns:
        task_instances (list): List of task instances
    """
    if any([instance_path.endswith(x) for x in [".jsonl", ".jsonl.all"]]):
        task_instances = list()
        with open(instance_path) as f:
            for line in f.readlines():
                task_instances.append(json.loads(line))
        return task_instances

    with open(instance_path) as f:
        task_instances = json.load(f)
    return task_instances


def get_eval_refs(data_path_or_name):
    decode_keys = False
    if os.path.isfile(data_path_or_name):
        if data_path_or_name.endswith(".jsonl"):
            data = [json.loads(l) for l in open(data_path_or_name).readlines()]
        elif data_path_or_name.endswith(".json"):
            data = json.load(open(data_path_or_name, "r"))
    elif os.path.isdir(data_path_or_name):
        data = load_from_disk(data_path_or_name)
        decode_keys = True
    else:
        data = load_dataset(data_path_or_name)
        decode_keys = True
    if isinstance(data, dict):
        all_data = list()
        all_data.extend(data["test"])
        data = all_data

    return {d[KEY_INSTANCE_ID]: d for d in data}
