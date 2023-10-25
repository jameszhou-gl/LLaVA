import subprocess
import os
import sys
import json
import shutil
from datetime import datetime


def pre_setup():
    # Get the current time in the required format
    current_time = datetime.now().strftime('%Y-%m-%d-%H_%M_%S')
    # Define the raw output directory
    output_dir = f"/home/guanglin.zhou/code/LLaVA/run_exp/exp_results/{current_time}"
    # Create the directory
    os.makedirs(output_dir)

    # Get the current script's file path
    current_file_path = os.path.abspath(__file__)
    # Define the destination path in the output directory
    destination_file_path = os.path.join(
        output_dir, os.path.basename(current_file_path))
    # Copy the current script file to the output directory
    shutil.copy(current_file_path, destination_file_path)
    return output_dir


def post_setup(output_dir):
    # Define the current directory where the output file resides (change this if different)
    current_dir = os.getcwd()

    # Construct the full paths
    src_path = os.path.join(current_dir, output_file)
    dst_path = os.path.join(output_dir, output_file)
    # Check if the source file exists and move it; otherwise, assert an error
    if os.path.exists(src_path):
        shutil.move(src_path, dst_path)
    else:
        assert False, f"Source file {src_path} does not exist."


# Capture the output file name from the command-line arguments
output_file = sys.argv[1]
# Capture the optional second argument if it exists
continue_path = None
if len(sys.argv) > 2:
    continue_path = sys.argv[2]
    output_dir = continue_path
else:
    output_dir = pre_setup()

# ! specify the model size
model_size = "7b"

model_vqa_llavabench = [
    "python", "-m", "llava.eval.model_vqa",
    "--model-path", "liuhaotian/llava-v1.5-{}".format(model_size),
    "--question-file", "/l/users/guanglin.zhou/llava/playground/data/eval/llava-bench-in-the-wild/questions.jsonl",
    "--image-folder", "/l/users/guanglin.zhou/llava/playground/data/eval/llava-bench-in-the-wild/images",
    "--answers-file", "{}/llava-v1.5-{}.jsonl".format(output_dir, model_size),
    "--temperature", "0",
    "--conv-mode", "vicuna_v1"
]
subprocess.run(model_vqa_llavabench)


review_path = "{}/reviews".format(output_dir)
os.makedirs(review_path, exist_ok=True)

eval_gpt_review_bench = [
    "python", "-m", "llava.eval.eval_gpt_review_bench",
    "--question-file", "/l/users/guanglin.zhou/llava/playground/data/eval/llava-bench-in-the-wild/questions.jsonl",
    "--context", "/l/users/guanglin.zhou/llava/playground/data/eval/llava-bench-in-the-wild/context.jsonl"
    "--rule", "llava/eval/table/rule.json",
    "--answer-list", "/l/users/guanglin.zhou/llava/playground/data/eval/llava-bench-in-the-wild/answers_gpt4.jsonl", "{}/llava-v1.5-{}.jsonl".format(output_dir, model_size),
    "--output", "{}/llava-v1.5-{}.jsonl".format(review_path, model_size)
]
subprocess.run(eval_gpt_review_bench)

post_setup(output_dir)
