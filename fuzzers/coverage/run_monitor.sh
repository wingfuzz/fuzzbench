cd /out
output=/tmp/fuzzbench/$FUZZER_NAME/$FUZZ_PROJECT/output
mkdir -p $output
PYTHONPATH=$WORK/fuzzbench python3 -u -c "import asyncio; from fuzzers.coverage import monitor; asyncio.run(monitor.main())"