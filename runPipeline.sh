#!/bin/bash

# This should be run from the root directory of the project
# Run Node.js script to create files
node src/pipelineGetData.js today

# Capture filenames in a variable (modify this based on how your Node.js script logs filenames)
file_name=$(cat data/filename.txt)

# Run Python script with filenames as arguments
python src/pipeline_analyze.py $file_name
