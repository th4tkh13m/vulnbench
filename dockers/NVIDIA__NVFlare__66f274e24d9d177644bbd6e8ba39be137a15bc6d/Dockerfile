FROM th4tkh13m/vulnbench-base:3.12

RUN git clone https://github.com/NVIDIA/NVFlare.git /app
WORKDIR /app
RUN git -c advice.detachedHead=false checkout 66f274e24d9d177644bbd6e8ba39be137a15bc6d

RUN pip install -e .[dev]


RUN pip install coverage


WORKDIR /vulnbench
COPY swebench_docker swebench_docker
COPY --chmod=0755  dockers/entrypoint.sh .
ENTRYPOINT [ "./entrypoint.sh" ]
