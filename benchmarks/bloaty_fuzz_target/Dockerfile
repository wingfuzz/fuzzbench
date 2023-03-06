
ARG parent_image
FROM $parent_image

RUN git clone https://github.com/google/bloaty.git $SRC/bloaty


COPY build.sh $SRC/
COPY run_build.sh $SRC/
