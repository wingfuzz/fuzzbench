# Copyright 2020 Google LLC
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

ENV FUZZ_PROJECT=libpng-1.2.56

RUN apt-get update && \
    apt-get install -y \
    make \
    autoconf \
    automake \
    libtool \
    wget \
    zlib1g-dev

RUN wget \
    https://downloads.sourceforge.net/project/libpng/libpng12/older-releases/1.2.56/libpng-1.2.56.tar.gz

RUN wget -qO $OUT/fuzz-target.dict \
    https://raw.githubusercontent.com/google/fuzzing/master/dictionaries/png.dict
ADD seeds /opt/seeds
COPY target.cc $SRC/
COPY png_mutator.h $SRC/

COPY build.sh $SRC/
COPY run_build.sh $SRC/
COPY benchmark.yaml /
COPY run_fuzz.sh /

RUN chmod +x /run_fuzz.sh && chmod +x $SRC/run_build.sh && $SRC/run_build.sh 
COPY run_monitor.sh /
RUN chmod +x /run_monitor.sh
