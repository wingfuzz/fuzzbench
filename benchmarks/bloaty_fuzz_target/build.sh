
cd $WORK
cmake -G Ninja -DBUILD_TESTING=false $SRC/bloaty
ninja -j$(nproc) -v
cp fuzz_target $OUT
zip -j $OUT/fuzz_target_seed_corpus.zip $SRC/bloaty/tests/testdata/fuzz_corpus/*
