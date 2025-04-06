FROM th4tkh13m/vulnbench-base:3.12

RUN git clone https://github.com/RedHatInsights/insights-core.git /app
WORKDIR /app
RUN git -c advice.detachedHead=false checkout 57df3dad1a48cad3c4cfd35487cf64c135aca9bf

RUN pip install -e .[develop]


RUN pip install coverage

WORKDIR /vulnbench
COPY swebench_docker swebench_docker
COPY --chmod=0755  dockers/entrypoint.sh .

ENTRYPOINT [ "./entrypoint.sh" ]