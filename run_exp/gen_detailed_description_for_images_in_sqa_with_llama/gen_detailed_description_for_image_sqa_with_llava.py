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
model_size = "13b"

# ! specify the evaluation split
eval_split = "minitest"  # [minitest, test, minitest_first_40, scienceqa_chameleon_gpt4_test_failure_cases]

model_vqa_llavabench = [
    "python", "-m", "llava.eval.model_vqa",
    "--model-path", "liuhaotian/llava-v1.5-{}".format(model_size),
    "--question-file", "/home/guanglin.zhou/code/LLaVA/run_exp/gen_detailed_description_for_images_in_sqa_with_llama/sqa_{}_questions_in_vqa_format.jsonl".format(eval_split),
    "--image-folder", "/l/users/guanglin.zhou/llava/playground/data/eval/scienceqa/images",
    "--answers-file", "{}/llava-v1.5-{}_gen_detailed_description_for_image_sqa_{}.jsonl".format(output_dir, model_size, eval_split),
    "--temperature", "0",
    "--conv-mode", "vicuna_v1"
]
subprocess.run(model_vqa_llavabench)

post_setup(output_dir)
