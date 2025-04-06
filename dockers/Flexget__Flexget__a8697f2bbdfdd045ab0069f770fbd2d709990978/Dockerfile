FROM th4tkh13m/vulnbench-base:3.9

RUN git clone https://github.com/Flexget/Flexget.git /app
WORKDIR /app
RUN git -c advice.detachedHead=false checkout a8697f2bbdfdd045ab0069f770fbd2d709990978

# Install uv
RUN pip install uv

# Setup uv environment
RUN uv venv .venv

# Setup .venv in PATH
ENV PATH="/app/.venv/bin:${PATH}"

# Install base package with all plugin test dependencies
RUN uv pip install . --group plugin-test --group dev
RUN uv pip install coverage


WORKDIR /vulnbench
COPY swebench_docker swebench_docker
COPY --chmod=0755  dockers/entrypoint.sh .

RUN pip install coverage

ENTRYPOINT [ "./entrypoint.sh" ]