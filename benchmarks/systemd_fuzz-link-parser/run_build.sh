cd /systemd

if [ "$FUZZER_NAME" == "libfuzzer" ]; then
    mv /systemd/meson.build /systemd/old-meson.build 
    mv $SRC/meson.build /systemd/
fi

if [ "$FUZZER_NAME" == "afl" ]; then
    export FUZZING_ENGINE=/libAFL.a
fi

PYTHONPATH=$WORK/fuzzbench python3 -u -c "from fuzzers import utils; utils.initialize_env(); from fuzzers.$FUZZER_NAME import fuzzer; fuzzer.build()"

cd /out 
rm -rf ./seeds
unzip fuzz-link-parser_seed_corpus.zip -d ./seeds
find /out/seeds/ -size +999k -exec rm {} \;