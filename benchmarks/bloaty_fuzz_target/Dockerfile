
ARG parent_image
FROM $parent_image
ENV FUZZ_PROJECT=bloaty_fuzz_target
RUN git clone https://github.com/google/bloaty.git $SRC/bloaty

COPY build.sh $SRC/
COPY run_build.sh $SRC/
COPY benchmark.yaml /
COPY run_fuzz.sh /

RUN chmod +x /run_fuzz.sh && chmod +x $SRC/run_build.sh && $SRC/run_build.sh 
COPY run_monitor.sh /
RUN chmod +x /run_monitor.sh
#CMD /run_fuzz.sh
