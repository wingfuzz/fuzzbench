#!/bin/sh
while :
do
    sleep 60
    PYTHONPATH=$WORK/fuzzbench python3 -u -c "import asyncio; from fuzzers.coverage import monitor; asyncio.run(monitor.run('./output/crashes', './output/queue', '/out/fuzz-target'))" &
done

