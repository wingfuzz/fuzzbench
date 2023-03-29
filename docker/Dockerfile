# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive \
    ASAN_OPTIONS="abort_on_error=1:symbolize=0:handle_abort=1:handle_sigill=1" \
    UBSAN_OPTIONS="abort_on_error=1:print_stacktrace=1:report_error_type=1:symbolize=0" \
    WORK=/work \
    SRC=$WORK/src \
    OUT=/out \
    ROOT_DIR=/src

RUN mv /etc/apt/sources.list /etc/apt/sources.list-back && echo \
    "deb http://mirrors.dev.shuimuyulin.com/ubuntu/ focal main restricted universe multiverse\n\
    deb http://mirrors.dev.shuimuyulin.com/ubuntu/ focal-security main restricted universe multiverse\n\
    deb http://mirrors.dev.shuimuyulin.com/ubuntu/ focal-updates main restricted universe multiverse\n\
    deb http://mirrors.dev.shuimuyulin.com/ubuntu/ focal-proposed main restricted universe multiverse\n\
    #deb http://mirrors.dev.shuimuyulin.com/ubuntu/ focal-backports main restricted universe multiverse\n\
    " > /etc/apt/sources.list && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    python3 python3-pip \
    gcc g++ clang llvm lld libc++-dev libc++abi-dev \
    cmake make git \
    ninja-build \
    autoconf \
    automake \
    libtool \
    build-essential \
    rsync \
    wget \
    curl \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    virtualenv \
    libbz2-dev \
    liblzma-dev \
    libsqlite3-dev \
    libz-dev \
    zip \
    unzip \
    vim \
    ragel \
    pkg-config && \
    pip config set global.index-url http://mirrors.dev.shuimuyulin.com/pypi/web/simple && \
    pip config set install.trusted-host mirrors.dev.shuimuyulin.com && \
    pip3 install --upgrade pip && \
    apt-get clean && \
    mkdir -p $WORK && \
    mkdir -p $SRC && \
    mkdir -p $OUT && \
    mkdir -p /work/fuzzbench

COPY fuzzbench.tar.gz /work
RUN tar -zxvf /work/fuzzbench.tar.gz -C /work/fuzzbench

