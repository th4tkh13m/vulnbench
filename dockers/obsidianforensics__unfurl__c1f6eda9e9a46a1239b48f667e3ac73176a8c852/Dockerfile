FROM th4tkh13m/vulnbench-base:3.11

RUN git clone https://github.com/obsidianforensics/unfurl.git /app
WORKDIR /app
RUN git -c advice.detachedHead=false checkout c1f6eda9e9a46a1239b48f667e3ac73176a8c852

RUN pip install -r requirements-all.txt
RUN pip install coverage
RUN pip install -e .


WORKDIR /vulnbench
COPY swebench_docker swebench_docker
COPY --chmod=0755  dockers/entrypoint.sh .

ENTRYPOINT [ "./entrypoint.sh" ]
