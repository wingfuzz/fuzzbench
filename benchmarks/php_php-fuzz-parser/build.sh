#!/bin/bash -eu
# Copyright 2019 Google Inc.
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

make clean distclean || echo "no need to clean"

# build oniguruma and link statically
pushd oniguruma
make clean distclean || echo "no need to clean"
autoreconf -vfi
./configure
make -j$(nproc)
popd
export ONIG_CFLAGS="-I$PWD/oniguruma/src"
export ONIG_LIBS="$PWD/oniguruma/src/.libs/libonig.a"

if [ ! -f $ONIG_LIBS ]; then
    echo "ONIG LIBS not exists"
    exit 1
fi

# PHP's zend_function union is incompatible with the object-size sanitizer
export CFLAGS="$CFLAGS -fno-sanitize=object-size"
export CXXFLAGS="$CXXFLAGS -fno-sanitize=object-size"
export LIBS="$LIBS $ONIG_LIBS"

# build project
./buildconf
./configure \
    --disable-all \
    --enable-option-checking=fatal \
    --enable-fuzzer \
    --enable-exif \
    --enable-mbstring \
    --without-pcre-jit \
    --disable-phpdbg \
    --disable-cgi \
    --with-pic
make -j$(nproc)

# Generate initial corpus for parser fuzzer
sapi/cli/php sapi/fuzzer/generate_parser_corpus.php
cp sapi/fuzzer/dict/parser $OUT/php-fuzz-parser.dict

cp sapi/fuzzer/php-fuzz-parser $OUT/
mkdir -p $OUT/seeds
cp -r sapi/fuzzer/corpus/parser/* $OUT/seeds
