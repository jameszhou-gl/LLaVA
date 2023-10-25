#!/bin/bash

# Target directory
TARGET_DIR="/l/users/guanglin.zhou/llava/playground/data/eval/llava-bench-in-the-wild"

# Create the target directory if it doesn't exist
mkdir -p $TARGET_DIR

# Run Python script to download dataset
python3 - <<END
from datasets import load_dataset
dataset = load_dataset('liuhaotian/llava-bench-in-the-wild')
dataset.save_to_disk('$TARGET_DIR')
END
