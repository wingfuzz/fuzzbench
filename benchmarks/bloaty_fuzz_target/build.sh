#!/bin/bash

cd $WORK
cmake -G Ninja -DBUILD_TESTING=false $SRC/bloaty

# 如果当前编译器是clang 则在尾部添加 /usr/lib/llvm-12/lib/clang/12.0.0/lib/linux/libclang_rt.builtins-x86_64.a
# if [ "$FUZZER_NAME" = "libfuzzer" ]; then
#   export CXXFLAGS="$CXXFLAGS /usr/lib/llvm-12/lib/clang/12.0.0/lib/linux/libclang_rt.builtins-x86_64.a"
# fi

ninja -j$(nproc) -v
cp fuzz_target $OUT
zip -j $OUT/fuzz_target_seed_corpus.zip $SRC/bloaty/tests/testdata/fuzz_corpus/*
