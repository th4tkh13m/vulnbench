# Copyright (c) Meta Platforms, Inc. and affiliates.
# Adapted from: https://github.com/aorwall/SWE-bench-docker/blob/main/generate_report.py

import argparse
import json
import re
import os

from swebench_docker.utils.evaluation import (
    get_eval_reports_for_dir,
    get_instances,
    get_model_eval_summary,
    get_eval_refs
    # get_model_report,
)



def generate_report(
    swe_bench_tasks: str, predictions_path: str, log_dir: str, output_dir: str
):
    instances = get_eval_refs(swe_bench_tasks)

    predictions = get_instances(predictions_path)
    model_name_or_path = predictions[0]["model_name_or_path"]

    report_net = get_eval_reports_for_dir(
        log_dir, instances, raw_only=True, model_name=model_name_or_path
    )
    filename = os.path.basename(predictions_path).replace(".jsonl", "")
    with open(f"{output_dir}/{filename}_full.json", "w") as f:
        f.write(json.dumps(report_net, indent=4))

    summary = get_model_eval_summary(
        predicts_path=predictions_path,
        eval_dir=log_dir,
        swe_bench_instances=instances,
        model_name=model_name_or_path,
    )


    with open(f"{output_dir}/{filename}_summary.json", "w") as f:
        f.write(json.dumps(summary, indent=4))

    # report = get_model_report(
    #     verbose=True,
    #     model=model_name_or_path,
    #     predictions_path=predictions_path,
    #     log_dir=log_dir,
    # )

    # with open(f"{output_dir}/{model_name_or_path}_report.json", "w") as f:
    #     f.write(json.dumps(report, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--predictions_path", type=str, help="Path to predictions file", required=True
    )
    parser.add_argument(
        "--log_dir", type=str, help="Path to log directory", required=True
    )
    parser.add_argument(
        "--swe_bench_tasks",
        type=str,
        help="Path to dataset file or HF datasets name",
        required=True,
    )
    parser.add_argument(
        "--output_dir", type=str, help="Path to output directory", required=True
    )
    args = parser.parse_args()
    generate_report(**vars(args))