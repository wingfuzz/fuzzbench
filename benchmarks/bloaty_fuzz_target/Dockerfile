
ARG parent_image
ARG FUZZER
FROM $parent_image

RUN git clone https://github.com/google/bloaty.git

WORKDIR bloaty
COPY build.sh $SRC/
