#!/usr/bin/env bash
# Re-record hero demo: runs offline suite and captures output for GIF assembly.
set -euo pipefail
cd "$(dirname "$0")/.."
python scripts/verify_all.py --offline
echo "suite done -> results/suite.json"
echo "Next: record 10-15s terminal with peek/ShareX/QuickTime, export assets/demo.gif (<5MB)."
echo "Optimize: ffmpeg -i demo.mp4 -vf fps=12,scale=800:-1 assets/demo.gif && gifsicle -O3 --colors 128 assets/demo.gif -o assets/demo.gif"
