FROM th4tkh13m/vulnbench-base:3.11

RUN git clone https://github.com/linkml/linkml.git /app
WORKDIR /app
RUN git -c advice.detachedHead=false checkout 3ae9ee399590a03b6840a610e02ff4c944b23b1c

RUN apt-get update && \
    apt-get install --no-install-recommends -y curl

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"




# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add poetry to PATH (note the leading /)
# ENV PATH="/root/.local/bin:${PATH}"

# Install dependencies with poetry
RUN poetry install --all-extras
RUN pip install coverage
# Add poetry's virtualenv to PATH if needed (optional depending on run_test.py)
# ENV PATH="/root/.local/share/pypoetry/venv/bin:${PATH}"



WORKDIR /vulnbench
COPY swebench_docker swebench_docker
COPY --chmod=0755  dockers/entrypoint.sh .

ENTRYPOINT [ "./entrypoint.sh" ]