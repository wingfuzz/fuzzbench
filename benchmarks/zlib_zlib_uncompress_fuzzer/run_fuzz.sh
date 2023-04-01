#!/bin/bash
cd /out
output=/tmp/fuzzbench/$FUZZER_NAME/$FUZZ_PROJECT/output
rm -rf output
mkdir -p $output
find /out/seeds/ -size +999k -exec rm {} \;
PYTHONPATH=$WORK/fuzzbench python3 -u -c "from fuzzers.$FUZZER_NAME import fuzzer; fuzzer.fuzz('/out/seeds', '$output', '/out/fuzz-target')"