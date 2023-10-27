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
export CUDA_VISIBLE_DEVICES=1,2,3
python "$python_file"

# Get the current time in the required format and store it in end_time
end_time=$(date "+%Y-%m-%d %H:%M:%S")

echo "End time: $end_time"
echo "Execution complete."