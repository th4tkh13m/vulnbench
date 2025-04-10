#!/usr/bin/env python3

"""Get Testcases"""
import argparse
import asyncio
import hashlib
import logging
import os


from swebench_docker.constants import (
    KEY_INSTANCE_ID,
    KEY_MODEL,
    KEY_PREDICTION, MAP_REPO_TO_TEST_FRAMEWORK,
)
from swebench_docker.run_docker import run_docker_evaluation
from swebench_docker.utils.evaluation import get_instances, get_eval_refs

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("get_testcases")


async def main(
    swe_bench_tasks: str,
    namespace: str,
    log_dir: str,
    log_suffix: str = "",
    skip_existing: bool = False,
    timeout: int = 900,
    num_processes: int = -1,
):
    """
    Runs evaluation on predictions for each model/repo/version combination.

    Args:
        swe_bench_tasks (str): Path to the SWE-bench tasks file OR HF dataset name.
        namespace (str): Docker repository namespace.
        log_dir (str): Path to the directory where logs will be saved.
        log_suffix (str): Suffix to append to log file names.
        skip_existing (bool): Whether to skip evaluations for predictions that already have logs.
        timeout (int): Timeout for each evaluation.
        num_processes (int): Number of processes to run in parallel (-1 = unlimited)

    Raises:
        ValueError: If log_dir is not a directory, testbed is not a directory, or swe_bench_tasks does not exist.
    """
    # Validate arguments
    if not os.path.exists(log_dir) or not os.path.isdir(log_dir):
        raise ValueError("--log_dir must exist and point at a directory")

    tasks = list(get_eval_refs(swe_bench_tasks).values())

    # Verify arguments are formatted correctly
    if not isinstance(tasks, list):
        raise ValueError(f"{swe_bench_tasks} must contain an array of tasks")
    tasks_map = {t[KEY_INSTANCE_ID]: t for t in tasks}

    # Remove predictions that have already been evaluated
    if skip_existing:
        # Skip logs that already exist
        predictions_filtered = []
        for p in predictions:
            dir_name = f"{p[KEY_INSTANCE_ID]}.{p[KEY_MODEL]}"
            if log_suffix:
                dir_name = f"{p[KEY_INSTANCE_ID]}.{p[KEY_MODEL]}"
            dir_path = os.path.join(log_dir, dir_name)
            if not os.path.exists(dir_path):
                predictions_filtered.append(p)
        if len(predictions_filtered) == 0:
            logger.info(f"All predictions already exist, skipping")
            return
        else:
            logger.info(
                f"# of predictions to evaluate: {len(predictions_filtered)} " +
                f"({len(predictions) - len(predictions_filtered)} already evaluated)"
            )
            predictions = predictions_filtered
    else:
        logger.info(
            f"# of predictions to evaluate: {len(predictions)}"
        )

    task_instances = []
    repo_set = set()
    for task_instance in tasks:
        if task_instance["repo"] not in repo_set:
            repo_set.add(task_instance["repo"])
            # Add the repo to the task instance
            
            test_cmd = MAP_REPO_TO_TEST_FRAMEWORK[task_instance["repo"]]
            
            task_instances.append({
                "repo": task_instance["repo"],
                "base_commit": task_instance["base_commit"],
                "test_cmd": test_cmd,
                KEY_INSTANCE_ID: task_instance[KEY_INSTANCE_ID],
            })


    # Set the relevant data on task_instances
    # for prediction in predictions:
    #     task = tasks_map[prediction[KEY_INSTANCE_ID]]

    #     test_cmd = MAP_REPO_TO_TEST_FRAMEWORK[task["repo"]]

    #     task_instances.append({
    #         "repo": task["repo"],
    #         # "version": task["version"],
    #         "base_commit": task["base_commit"],
    #         KEY_INSTANCE_ID: prediction[KEY_INSTANCE_ID],
    #         "test_cmd": test_cmd
    #     })

    task_instances = sorted(task_instances, key=lambda x: x[KEY_INSTANCE_ID])

    sem = asyncio.Semaphore(num_processes if num_processes > 0 else len(task_instances))
    async with asyncio.TaskGroup() as tg:
        for task_instance in task_instances:
            if task_instance[KEY_PREDICTION]:
                # Create each log directory
                dir_name = f"{task_instance['repo'].replace('/', '__')}"
                dir_path = os.path.join(log_dir, dir_name)
                os.makedirs(dir_path, exist_ok=True)
                
                async def run_docker_throttled(*args, **kwargs):
                    async with sem:
                        return await run_docker_evaluation(*args, **kwargs)

                tg.create_task(run_docker_throttled(task_instance, namespace, dir_path, timeout, log_suffix, curate_data=False))
            else:
                logger.info(f"[{task_instance['repo'].replace('/', '__')}] No prediction found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log_dir", type=str, help="Path to log directory", required=True)
    parser.add_argument("--swe_bench_tasks", type=str, help="Path to dataset file or HF datasets name", required=True)
    parser.add_argument("--namespace", type=str, help="Docker repository namespace", required=False, default="aorwall")
    parser.add_argument("--log_suffix", type=str, help="(Optional) Suffix to append to log file names", default="")
    parser.add_argument("--skip_existing", action="store_true", help="(Optional) Skip existing logs")
    parser.add_argument("--timeout", type=int, help="(Optional) Timeout in seconds (default: 900)", default=1800)
    parser.add_argument("--num_processes", type=int, help="(Optional) Number of processes to run in parallel (-1 for unlimited)", default=-1)
    args = parser.parse_args()
    asyncio.run(main(**vars(args)))