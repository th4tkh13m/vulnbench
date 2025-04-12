# Copyright (c) Meta Platforms, Inc. and affiliates.
# Adapted from: https://github.com/aorwall/SWE-bench-docker/blob/main/swebench_docker/evaluate_instance.py

import base64
import json
import logging
import os
import re
import subprocess
import sys
from typing import Optional, Tuple

from swebench_docker.constants import (
    KEY_BASELINES,
    KEY_MODEL,
    KEY_PREDICTIONS,
    MAP_REPO_TO_TEST_FRAMEWORK,
    SETTING_PROMPT_MAP,
    TESTS_CONFIG,
    TESTS_FAILED,
    UNFILTERED_TESTS_FAILED,
    UNFILTERED_TESTS_PASSED,
    PatchType,
    KEY_PREDICTION
)
from swebench_docker.context_manager import TaskEnvContextManager
from swebench_docker.utils.commit_handler import extract_minimal_patch

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger("evaluate_instance")


def main(
    task_instance: dict,
    testbed_name: str,
    repo_dir: str,
    log_dir: str,
    timeout: Optional[int],
    image_type: str = "python",
    curate_data: bool = False,
):
    
    
    logger.info(
        "Instance ID: "
        + task_instance["instance_id"]
        + "\nTestbed: "
        + testbed_name
        + "\nLog dir: "
        + log_dir
        + "\nCurated data: "
        + str(curate_data)
    )

    # if only_baseline:
    #     task_instance[KEY_MODEL] = "baseline"
    #     test_type = MAP_REPO_TO_TEST_FRAMEWORK[task_instance["repo"]]
    #     test_directives = get_test_directives(task_instance)
    #     test_cmd = f"{test_type} {' '.join(test_directives)}"
    #     task_instance["test_directives"] = test_directives
    #     task_instance["test_cmd"] = test_cmd

    with TaskEnvContextManager(
        task_instance,
        testbed_name,
        repo_dir,
        log_dir,
        timeout=timeout,
        image_type=image_type,
        curate_data=curate_data,
    ) as tcm:
        
        if not curate_data:
            # Attempt to apply prediction
            patch_type = PatchType.PATCH_PRED_TRY.value

            # If prediction patch doesn't apply, try to do some minor patch refactoring and try again
            if not tcm.apply_patch(task_instance[KEY_PREDICTION], patch_type=patch_type, revert=True) \
                    and task_instance[KEY_PREDICTION] is not None \
                    and task_instance[KEY_PREDICTION] != "":
                task_instance[KEY_PREDICTION] = extract_minimal_patch(task_instance[KEY_PREDICTION])
                patch_type = PatchType.PATCH_PRED_MINIMAL_TRY.value
                if not tcm.apply_patch(task_instance[KEY_PREDICTION], patch_type=patch_type, revert=True):
                    logger.warning("Failed to apply prediction patch")
                    sys.exit(1)

            tcm.apply_patch(task_instance[KEY_PREDICTION], patch_type=patch_type)
            # Set prediction patch label based on whether patch was edited
            if patch_type == PatchType.PATCH_PRED_MINIMAL_TRY.value:
                patch_type = PatchType.PATCH_PRED_MINIMAL.value
            else:
                patch_type = PatchType.PATCH_PRED.value     
            
            
            # Print the file after patch: File path: /app/vulnerable.py

        # Run tests
        logger.info("Start testing")
        _, success = tcm.run_tests_task(
            task_instance)
        
        # if not success:
        #     logger.error("Tests failed")
        #     sys.exit(1)
            
        # if not curate_data:
        # Scan vulnerabilities
        logger.info("Start vulnerability scan")
        _, success = tcm.run_vulnerability_check(
            task_instance)
        
        # if not success:
        #     logger.error("Vulnerability scan failed")
        #     sys.exit(1)
        
        logger.info("Evaluation succeeded")
        
        if curate_data:
            logger.info("Curated data succeeded")
        
        
if __name__ == "__main__":
    TASK_INSTANCE_JSON = "/vulnbench/task_instance.json"
    if os.path.exists(TASK_INSTANCE_JSON):
        with open(TASK_INSTANCE_JSON, "r") as f:
            task_instance = json.load(f)
    else:
        instance_encoded = os.getenv("INSTANCE")
        if instance_encoded is None:
            raise ValueError("INSTANCE environment variable is not set")
        task_instance = json.loads(base64.b64decode(instance_encoded).decode("utf-8"))
    log_dir = os.getenv("LOG_DIR", "/log")
    if log_dir is None:
        raise ValueError("LOG_DIR environment variable is not set")

    testbed_name = os.getenv("TESTBED_NAME")
    if testbed_name is None:
        raise ValueError("TESTBED_NAME environment variable is not set")

    repo_dir = os.getenv("REPO_DIR", "/app") if os.getenv("REPO_DIR", "/app") else os.getenv("TESTBED")
    if repo_dir is None:
        raise ValueError("REPO_DIR environment variable is not set")

    timeout = os.getenv("TIMEOUT", 600)
    int_timeout: Optional[int] = None
    if timeout is not None:
        try:
            int_timeout = int(timeout)
        except ValueError:
            raise ValueError("TIMEOUT environment variable must be an integer or None")


    main(
        task_instance=task_instance,
        testbed_name=testbed_name,
        repo_dir=repo_dir,
        log_dir=log_dir,
        timeout=int_timeout,
        image_type=os.getenv("IMAGE_TYPE", "python"),
        curate_data=os.getenv("CURATE_DATA", "false").lower() == "true",
    )