#!/bin/bash
#SBATCH --job-name=exp
#SBATCH --output=output.%A.txt           # Standard output and error log
#SBATCH --nodes=1                                     # Run all processes on a single node
#SBATCH --ntasks=1                                    # Run on a single CPU
#SBATCH --mem=80G                                 # Total RAM to be used
#SBATCH --gres=gpu:2
#SBATCH --cpus-per-task=64                     # Number of CPU cores
#SBATCH -p long                                          # Use the gpu partition
source ~/anaconda3/etc/profile.d/conda.sh
conda activate llava

python -m llava.eval.model_vqa_science \
    --model-path liuhaotian/llava-v1.5-13b \
    --question-file /l/users/guanglin.zhou/llava/playground/data/eval/scienceqa/llava_minitest_CQM-A.json \
    --image-folder /l/users/guanglin.zhou/llava/playground/data/eval/scienceqa/images/test \
    --answers-file /l/users/guanglin.zhou/llava/playground/data/eval/scienceqa/answers/llava-v1.5-13b.jsonl \
    --single-pred-prompt \
    --temperature 0 \
    --conv-mode vicuna_v1

python llava/eval/eval_science_qa.py \
    --base-dir /l/users/guanglin.zhou/llava/playground/data/eval/scienceqa \
    --result-file /l/users/guanglin.zhou/llava/playground/data/eval/scienceqa/answers/llava-v1.5-13b.jsonl \
    --output-file /l/users/guanglin.zhou/llava/playground/data/eval/scienceqa/answers/llava-v1.5-13b_output.jsonl \
    --output-result /l/users/guanglin.zhou/llava/playground/data/eval/scienceqa/answers/llava-v1.5-13b_result.json
