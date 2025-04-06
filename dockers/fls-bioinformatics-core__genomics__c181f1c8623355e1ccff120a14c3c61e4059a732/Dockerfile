FROM th4tkh13m/vulnbench-base:3.9

RUN git clone https://github.com/fls-bioinformatics-core/genomics.git /app
WORKDIR /app
RUN git -c advice.detachedHead=false checkout c181f1c8623355e1ccff120a14c3c61e4059a732

# Install uv
RUN pip install -e .
RUN pip install coverage nose

WORKDIR /vulnbench
COPY swebench_docker swebench_docker
COPY --chmod=0755  dockers/entrypoint.sh .

ENTRYPOINT [ "./entrypoint.sh" ]
