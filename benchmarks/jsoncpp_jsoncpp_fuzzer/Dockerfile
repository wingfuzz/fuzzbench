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

ARG parent_image
FROM $parent_image
ENV FUZZ_PROJECT=jsoncpp_jsoncpp_fuzzer

RUN apt-get update && apt-get install -y build-essential make curl wget


# Install latest cmake.
# RUN wget https://github.com/Kitware/CMake/releases/download/v3.14.5/cmake-3.14.5-Linux-x86_64.sh && \
#     chmod +x cmake-3.14.5-Linux-x86_64.sh && \
#     ./cmake-3.14.5-Linux-x86_64.sh --skip-license --prefix="/usr/local"

RUN git clone --depth 1 https://github.com/open-source-parsers/jsoncpp
#WORKDIR jsoncpp

COPY build.sh $SRC/
COPY run_build.sh $SRC/
COPY benchmark.yaml /
COPY run_fuzz.sh /

RUN chmod +x /run_fuzz.sh && chmod +x $SRC/run_build.sh && $SRC/run_build.sh
COPY run_monitor.sh /
RUN chmod +x /run_monitor.sh


