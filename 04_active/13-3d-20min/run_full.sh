#!/usr/bin/env bash
# Render the 20-minute 3D version in two halves at once (36,000 frames at 30 fps), then join them.
set -e
cd "$(dirname "$0")"
python3 render3d_full.py video 0 18000 &
python3 render3d_full.py video 18000 36000 &
wait
cd ../../out
printf "file 'part_00000.mp4'\nfile 'part_18000.mp4'\n" > parts.txt
ffmpeg -y -v error -f concat -safe 0 -i parts.txt -c copy README_nine_stages_3d_full_light.mp4
echo "wrote out/README_nine_stages_3d_full_light.mp4"
