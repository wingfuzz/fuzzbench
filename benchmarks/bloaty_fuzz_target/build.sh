
cd $WORK
tar -xzvf fuzzers.tar.gz
PYTHONPATH=$SRC python3 -u -c "from fuzzers import utils; utils.initialize_env(); from fuzzers.$FUZZER import fuzzer; fuzzer.build()"
cmake -G Ninja -DBUILD_TESTING=false $SRC/bloaty
ninja -j$(nproc)
cp fuzz_target $OUT
zip -j $OUT/fuzz_target_seed_corpus.zip $SRC/bloaty/tests/testdata/fuzz_corpus/*
