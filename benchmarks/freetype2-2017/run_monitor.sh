#!/bin/sh
while :
do
    sleep 600
    PYTHONPATH=$WORK/fuzzbench python3 -u -c "import asyncio; from fuzzers.coverage import monitor; asyncio.run(monitor.run('/out/fuzz-target'))" &
done


#watch --interval 60 --precise --color PYTHONPATH=$WORK/fuzzbench python3 -u -c "import asyncio; from fuzzers.coverage import monitor; try: asyncio.run(monitor.run('/out/fuzz_target')) except Exception as e: print('\033[91m{}\033[0m'.format(e))"
