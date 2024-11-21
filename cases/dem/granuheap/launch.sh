#!/bin/bash

CURRENT_PATH=$(pwd)
SHELL_FILE='ti64.sh'
PRM_FILE='granuheap_ti64.prm'

for dir in "$CURRENT_PATH"/*; do
    if [[ -d "$dir" ]]; then
        if [[ -f "$dir/$PRM_FILE" && "$dir" != "$CURRENT_PATH" ]]; then
            cd "$dir" || continue
            case_name=$(basename "$dir")
            sbatch -J "$case_name" "$SHELL_FILE"
        fi
    fi
done
