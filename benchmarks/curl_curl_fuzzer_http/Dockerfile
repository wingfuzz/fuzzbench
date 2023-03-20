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

ENV FUZZ_PROJECT=curl_curl_fuzzer_http

ENV GIT_HTTP_LOW_SPEED_LIMIT=1000
ENV GIT_HTTP_LOW_SPEED_TIME=3600
ENV GIT_HTTP_MAX_REQUESTS=100
ENV GIT_HTTP_BUFFER_SIZE=1M

# Curl will be checked out to the commit hash specified in benchmark.yaml.
RUN git clone https://github.com/curl/curl-fuzzer /src/curl_fuzzer
RUN git -C /src/curl_fuzzer checkout dd486c1e5910e722e43c451d4de928ac80f5967d
RUN git clone --depth 1 https://github.com/curl/curl.git /src/curl

# Use curl-fuzzer's scripts to get latest dependencies.
RUN /src/curl_fuzzer/scripts/ossfuzzdeps.sh

COPY build.sh $SRC/
COPY run_build.sh $SRC/
COPY benchmark.yaml /
COPY run_fuzz.sh /

RUN chmod +x /run_fuzz.sh && chmod +x $SRC/run_build.sh && $SRC/run_build.sh 
COPY run_monitor.sh /
RUN chmod +x /run_monitor.sh
