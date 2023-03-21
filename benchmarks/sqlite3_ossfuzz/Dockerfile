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

ENV FUZZ_PROJECT=sqlite3_ossfuzz

RUN apt-get update && apt-get install -y make autoconf automake libtool curl tcl zlib1g-dev

RUN mkdir $SRC/sqlite3 && \
    cd $SRC/sqlite3 && \
    curl 'https://sqlite.org/src/tarball/sqlite.tar.gz?r=c78cbf2e86850cc6' -o sqlite3.tar.gz && \
        tar xzf sqlite3.tar.gz --strip-components 1

RUN find $SRC/sqlite3 -name "*.test" | xargs zip $SRC/ossfuzz_seed_corpus.zip

WORKDIR sqlite3
COPY build.sh *.dict $SRC/

COPY run_build.sh $SRC/
COPY benchmark.yaml /
COPY run_fuzz.sh /

RUN chmod +x /run_fuzz.sh && chmod +x $SRC/run_build.sh && $SRC/run_build.sh 
COPY run_monitor.sh /
RUN chmod +x /run_monitor.sh