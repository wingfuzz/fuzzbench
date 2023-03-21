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

ARG parent_image
FROM $parent_image

ENV FUZZ_PROJECT=zlib_zlib_uncompress_fuzzer

RUN apt-get update && apt-get install -y make autoconf automake libtool clang-12 llvm-12 lld-12 libc++-12-dev libc++abi-12-dev
RUN git clone --depth 1 -b develop https://github.com/madler/zlib.git
WORKDIR zlib
COPY build.sh $SRC/
COPY zlib_uncompress_fuzzer.cc $SRC/

COPY run_build.sh $SRC/
COPY benchmark.yaml /
COPY run_fuzz.sh /

RUN chmod +x /run_fuzz.sh && chmod +x $SRC/run_build.sh 
#RUN $SRC/run_build.sh 
COPY run_monitor.sh /
RUN chmod +x /run_monitor.sh
