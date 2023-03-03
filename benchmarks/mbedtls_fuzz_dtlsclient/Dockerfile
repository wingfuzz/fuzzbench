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

FROM gcr.io/oss-fuzz-base/base-builder@sha256:fee307a212b2f77f208b209e2335e4a5e640f55dbe6dbe76a3e50475f9160eca
RUN apt-get update && apt-get install -y make cmake
RUN git clone --recursive --depth 1 https://github.com/ARMmbed/mbedtls.git mbedtls
RUN git clone --depth 1 https://github.com/google/boringssl.git boringssl
RUN git clone --depth 1 https://github.com/openssl/openssl.git openssl
RUN git clone https://github.com/ARMmbed/mbed-crypto mbedtls/crypto
WORKDIR mbedtls
COPY build.sh $SRC/