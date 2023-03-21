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

ARG parent_image
FROM $parent_image

ENV FUZZ_PROJECT=systemd_fuzz-link-parser

RUN apt-get update &&\
    apt-get install -y gperf m4 gettext python3-pip \
        libcap-dev libmount-dev libkmod-dev \
        pkg-config wget zstd patchelf && \
    pip3 install meson ninja jinja2


RUN git clone \
        --depth 1 \
        --branch v252 \
        https://github.com/systemd/systemd && \
    cp /systemd/tools/oss-fuzz.sh $SRC/build.sh && \
    # Move shared libraries and tweak rpath for all $ARCHITECTURE.
    sed -i '119d;126d' $SRC/build.sh


# COPY build.sh $SRC/

COPY run_build.sh $SRC/
COPY benchmark.yaml /
COPY run_fuzz.sh /
COPY run_monitor.sh /

RUN chmod +x /run_fuzz.sh && chmod +x $SRC/run_build.sh 
RUN $SRC/run_build.sh 
RUN chmod +x /run_monitor.sh