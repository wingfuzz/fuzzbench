#!/bin/bash -eu
# Copyright 2018 Google Inc.
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

cd /libpcap
# build project
rm -rf build
mkdir -p build
cd build
cmake .. -DDISABLE_DBUS=1 -DDISABLE_RDMA=1 -DBUILD_WITH_LIBNL=OFF -DDISABLE_LINUX_USBMON=ON -DDISABLE_BLUETOOTH=ON -DDISABLE_NETMAP=ON -DDISABLE_DPDK=ON
make -j $(nproc)

# build fuzz targets
$CC $CFLAGS -I.. -c ../testprogs/fuzz/fuzz_both.c -o fuzz_both.o
$CXX $CXXFLAGS fuzz_both.o -o $OUT/fuzz_both libpcap.a $LIB_FUZZING_ENGINE

# export other associated stuff
cd ..
cp testprogs/fuzz/fuzz_*.options $OUT/
# builds corpus
cd /tcpdump/
zip -r fuzz_pcap_seed_corpus.zip tests/
cp fuzz_pcap_seed_corpus.zip $OUT/
cd /libpcap/testprogs/BPF
mkdir -p corpus
ls *.txt | while read i; do tail -1 $i > corpus/$i; done
cp -r corpus/ $OUT/
# zip -r fuzz_filter_seed_corpus.zip corpus/
# cp fuzz_filter_seed_corpus.zip $OUT/
