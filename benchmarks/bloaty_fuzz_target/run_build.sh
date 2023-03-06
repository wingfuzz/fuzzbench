cd $WORK
PYTHONPATH=./fuzzbench python3 -u -c "from fuzzers import utils; utils.initialize_env(); from fuzzers.$FUZZER_NAME import fuzzer; fuzzer.build()"