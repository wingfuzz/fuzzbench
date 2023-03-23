#!/bin/sh
while :
do
    sleep 600
    PYTHONPATH=$WORK/fuzzbench python3 -u -c "import asyncio; from fuzzers.coverage import monitor; asyncio.run(monitor.run('/out/fuzz-link-parser'))" &
done