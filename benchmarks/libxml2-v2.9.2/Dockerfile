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

FROM gcr.io/oss-fuzz-base/base-builder@sha256:fee307a212b2f77f208b209e2335e4a5e640f55dbe6dbe76a3e50475f9160eca

RUN mv /etc/apt/sources.list /etc/apt/sources.list-back && echo \
    "deb http://dev.mirrors.shuimuyulin.com/ubuntu/ xenial main restricted universe multiverse\n\
    deb http://dev.mirrors.shuimuyulin.com/ubuntu/ xenial-security main restricted universe multiverse\n\
    deb http://dev.mirrors.shuimuyulin.com/ubuntu/ xenial-updates main restricted universe multiverse\n\
    deb http://dev.mirrors.shuimuyulin.com/ubuntu/ xenial-proposed main restricted universe multiverse\n\
    #deb http://dev.mirrors.shuimuyulin.com/ubuntu/ xenial-backports main restricted universe multiverse\n\
    " > /etc/apt/sources.list

RUN apt-get update && \
    apt-get install -y \
    make \
    wget \
    autoconf \
    automake \
    libtool \
    libglib2.0-dev \
    build-essential \
    zlib1g-dev \
    liblzma-dev

ENV ALL_PROXY="http://192.168.221.1:10809"

RUN git clone https://gitlab.gnome.org/GNOME/libxml2.git

RUN wget -qO $OUT/fuzz-target.dict \
    https://raw.githubusercontent.com/google/AFL/debe27037b9444bbf090a0ffbd5d24889bb887ae/dictionaries/xml.dict
COPY target.cc build.sh $SRC/
