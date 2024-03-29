
ARG DOCKER_IMAGE_PREFIX=""

FROM ${DOCKER_IMAGE_PREFIX}base-image

ENV FUZZER_NAME="coverage"

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        python3-dev \
        python3-setuptools \
        automake \
        cmake \
        git \
        flex \
        bison \
        # for QEMU mode
        ninja-build \
        gcc-$(gcc --version|head -n1|sed 's/\..*//'|sed 's/.* //')-plugin-dev \
        libstdc++-$(gcc --version|head -n1|sed 's/\..*//'|sed 's/.* //')-dev \
        clang-12 llvm-12 lld-12 libc++-12-dev libc++abi-12-dev &&\
    apt-get clean
        
# Download afl++.
RUN git clone -b dev https://github.com/AFLplusplus/AFLplusplus /afl && \
    cd /afl && \
    git checkout 6f4b5ae0832774389b12c5a8cd3fb95821b438e5 || \
    true

# Build without Python support as we don't need it.
# Set AFL_NO_X86 to skip flaky tests.
RUN cd /afl && \
    unset CFLAGS CXXFLAGS && \
    export CC=clang-12 AFL_NO_X86=1 LLVM_CONFIG=llvm-config-12 && \
    PYTHON_INCLUDE=/ make -j && \
    make install && \
    cp utils/aflpp_driver/libAFLDriver.a / 

ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/out"
#ENV AFL_MAP_SIZE=2621440
ENV PATH="$PATH:/out"
ENV AFL_SKIP_CPUFREQ=1
ENV AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES=1
ENV AFL_TESTCACHE_SIZE=2
ENV AFL_CC_COMPILER="LTO"
ENV BUILD_MODES="lto"

ENV AFL_MAP_SIZE="1024000"