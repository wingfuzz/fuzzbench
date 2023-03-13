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
ENV FUZZ_PROJECT=freetype2-2017
#RUN git clone git://git.sv.nongnu.org/freetype/freetype2.git
RUN git clone https://github.com/Mojang/freetype2.git
RUN git clone https://github.com/unicode-org/text-rendering-tests.git TRT
RUN wget https://github.com/libarchive/libarchive/releases/download/v3.4.3/libarchive-3.4.3.tar.xz

COPY build.sh $SRC/
COPY run_build.sh $SRC/
COPY benchmark.yaml /
COPY run_fuzz.sh /

RUN chmod +x /run_fuzz.sh && chmod +x $SRC/run_build.sh && $SRC/run_build.sh
COPY run_monitor.sh /
RUN chmod +x /run_monitor.sh
#CMD /run_fuzz.sh