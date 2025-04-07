# VULNBENCH

## Running the prompting dataset
```sh
python -m inference.create_text_dataset --dataset_name_or_path <dataset_name_or_path> --prompt_style <prompt_style> --output_dir <output_dir> --file_source <file_source> 

# Example
python -m  inference.create_text_dataset --dataset_name_or_path tmp/youtube_dl_vuln_dataset --output_dir tmp/datasets --splits test

```

## Running the inference script
```sh
python -m inference.run_api --dataset_name_or_path <dataset_name_or_path> --model_name_or_path <model_name_or_path> --output_dir <output_dir> --model_args <model_args>
# Example
OPENAI_API_BASE="http://localhost:8000/v1" OPENAI_API_KEY="EMPTY" python -m inference.run_api --dataset_name_or_path ./tmp/.__tmp__youtube_dl_vuln_dataset__style-3__fs-vulnerable --model_name_or_path /project/phan/codellama/Qwen2.5-Coder-32B-Instruct --output_dir ./tmp/ 
```
```sh
python -m run_evaluation --predictions_path ./tmp/Qwen2.5-Coder-32B-Instruct__.__tmp__youtube_dl_vuln_dataset__style-3__fs-vulnerable__test.jsonl --log_dir ./tmp/log-qwen32b --swe_bench_tasks ./tmp/youtube_dl_vuln_dataset/ --num_processes 6 --namespace th4tkh13m
```