#!/bin/sh
echo "Get Value older than 90"
find /log -type f -mtime 90 -name "*.log" -exec rm -f {} \;
aws s3 cp ./ s3://patchofs3 --recurive
find . -maxdepth 1