#!/bin/bash

json_file="data/df_attributes.json"
newest_created_time=$(jq -r '.notion_df_test.newest_created_time' $json_file)

echo newest_created_time: $newest_created_time

# # Run Python script with filenames as arguments
# python src/pipeline_analyze.py \
#     notion_time_tracking_parsed_today_2023-12-27_1523.json \
#     notion_df_test
