#!/bin/bash

cd $WORK
cmake -G Ninja -DBUILD_TESTING=false $SRC/bloaty
ninja clean
ninja -j$(nproc) -v
cp fuzz_target $OUT
mkdir -p $OUT/seeds/
cp $SRC/bloaty/tests/testdata/fuzz_corpus/* $OUT/seeds/
