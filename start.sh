#!/bin/bash

# Start lightweight Flask web server to bind $PORT (needed for Render)
python3 web_alive.py &

# Run your existing bot script (whatever you used in run.sh)
bash run.sh
