cd /systemd
PYTHONPATH=$WORK/fuzzbench python3 -u -c "from fuzzers import utils; utils.initialize_env(); from fuzzers.$FUZZER_NAME import fuzzer; fuzzer.build()"
cd /out 
rm -rf ./seeds
unzip fuzz-link-parser_seed_corpus.zip -d ./seeds