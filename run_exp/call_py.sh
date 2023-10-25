#!/bin/bash
#SBATCH --job-name=exp
#SBATCH --output=output.%A.txt           # Standard output and error log
#SBATCH --nodes=1                                     # Run all processes on a single node
#SBATCH --ntasks=1                                    # Run on a single CPU
#SBATCH --mem=40G                                 # Total RAM to be used
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=64                     # Number of CPU cores
#SBATCH -p long                                          # Use the gpu partition
source ~/anaconda3/etc/profile.d/conda.sh
conda activate llava

# Get the current time in the required format and store it in start_time
start_time=$(date "+%Y-%m-%d %H:%M:%S")
echo "Start time: $start_time"

# Check if the Python file name is provided
if [ -z "$1" ]; then
  echo "Please provide the Python file name as an argument."
  exit 1
fi

# Get the Python file name from the argument
python_file="$1"

# Execute the Python file and pass the output file name as an argument
python "$python_file" "output.${SLURM_JOB_ID}.txt"

# Get the current time in the required format and store it in end_time
end_time=$(date "+%Y-%m-%d %H:%M:%S")

echo "End time: $end_time"
echo "Execution complete."