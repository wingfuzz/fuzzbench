
ARG parent_image
ARG FUZZER
FROM $parent_image
COPY fuzzers.tar.gz $SRC/

RUN git clone https://github.com/google/bloaty.git

WORKDIR bloaty
ENV FUZZER $FUZZER
COPY build.sh $SRC/
