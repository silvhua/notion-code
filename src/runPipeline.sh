#!/bin/bash

# This should be run from the root directory of the project
json_file="data/df_attributes.json"
newest_created_time=$(jq -r '.notion_df_test.newest_created_time' $json_file)

echo newest_created_time: $newest_created_time

# Run Node.js script to create files
node src/pipelineGetData.js $newest_created_time notion_df_test

# Capture filenames in a variable (modify this based on how your Node.js script logs filenames)
file_name=$(data/filename.txt)

# Run Python script with filenames as arguments
python src/pipeline_analyze.py $file_name notion_df_test
