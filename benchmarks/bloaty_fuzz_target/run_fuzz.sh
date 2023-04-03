
unzip /out/fuzz_target_seed_corpus.zip -d /out/seeds  
cd /out
output=/tmp/fuzzbench/$FUZZER_NAME/$FUZZ_PROJECT/output
mkdir -p $output

if [ "$FUZZER_NAME" == "libfuzzer" ]; then
    export ASAN_OPTIONS=abort_on_error=1:symbolize=0:handle_abort=1:handle_sigill=1:detect_container_overflow=0
fi

PYTHONPATH=$WORK/fuzzbench python3 -u -c "from fuzzers.$FUZZER_NAME import fuzzer; fuzzer.fuzz('/out/seeds', '$output', './fuzz_target')"