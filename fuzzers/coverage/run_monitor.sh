PYTHONPATH=$WORK/fuzzbench python3 -u -c "import asyncio; from fuzzers.coverage import monitor; asyncio.run(monitor.main())"

