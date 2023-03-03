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

FROM gcr.io/oss-fuzz-base/base-builder@sha256:c18f9615c9824b61ce982e0bac4b157b2eff5b9240cc6310a4815a826bb804e3
RUN apt-get update && apt-get install -y make cmake flex bison
RUN git clone --depth 1 https://github.com/the-tcpdump-group/libpcap.git libpcap
# for corpus as wireshark
RUN git clone --depth=1 https://github.com/the-tcpdump-group/tcpdump.git tcpdump
WORKDIR $SRC
COPY build.sh $SRC/
COPY patch.diff $SRC/
