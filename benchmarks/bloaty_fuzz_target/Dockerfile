
ARG parent_image
ARG FUZZER
FROM $parent_image
COPY fuzzers.tar.gz $SRC/
ENV ALL_PROXY="http://192.168.221.1:10809"

RUN git clone https://github.com/google/bloaty.git

WORKDIR bloaty
ENV FUZZER $FUZZER
COPY build.sh $SRC/
