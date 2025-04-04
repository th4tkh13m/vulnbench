FROM th4tkh13m/vulnbench-base:3.9

RUN git clone https://github.com/PyCQA/bandit.git /app
WORKDIR /app
RUN git -c advice.detachedHead=false checkout b983c276759233e68ef236ed6f34e07e038327f5

RUN pip install -r requirements.txt -r test-requirements.txt
RUN pip install .[yaml,toml,baseline,sarif]

ENV PYTHON="coverage run --source bandit --parallel-mode"

RUN coverage erase

WORKDIR /vulnbench
COPY swebench_docker swebench_docker
COPY --chmod=0755  dockers/entrypoint.sh .

ENTRYPOINT [ "./entrypoint.sh" ]