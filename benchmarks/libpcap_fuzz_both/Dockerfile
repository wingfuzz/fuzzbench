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

ENV FUZZ_PROJECT=libpcap_fuzz_both

RUN apt-get update && apt-get install -y make cmake flex bison
RUN git clone https://github.com/the-tcpdump-group/libpcap.git libpcap

# For corpus as wireshark.
RUN git clone https://github.com/the-tcpdump-group/tcpdump.git tcpdump && \
    git -C tcpdump checkout 032e4923e5202ea4d5a6d1cead83ed1927135874


COPY build.sh $SRC/


COPY run_build.sh $SRC/
COPY benchmark.yaml /
COPY run_fuzz.sh /

RUN chmod +x /run_fuzz.sh && chmod +x $SRC/run_build.sh && $SRC/run_build.sh 
COPY run_monitor.sh /
RUN chmod +x /run_monitor.sh

