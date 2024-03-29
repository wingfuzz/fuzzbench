#!/bin/bash -eu
# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
################################################################################


./configure
make -j$(nproc) clean
make -j$(nproc) libz.a

# Do not make check as there are tests that fail when compiled with MSAN.
# make -j$(nproc) check

b=$(basename -s .cc $SRC/zlib_uncompress_fuzzer.cc)
$CXX $CXXFLAGS -std=c++11 -I. /work/src/zlib_uncompress_fuzzer.cc -o $OUT/fuzz-target $LIB_FUZZING_ENGINE ./libz.a
echo "CXXFLAGS $CXXFLAGS"

zip $OUT/seed_corpus.zip *.*
rm -rf /out/seeds

unzip /out/seed_corpus.zip -d /out/seeds
find /out/seeds/ -size +999k -exec rm {} \;