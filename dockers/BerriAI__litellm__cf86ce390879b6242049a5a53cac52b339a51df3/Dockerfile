FROM th4tkh13m/vulnbench-base:3.11
RUN git clone https://github.com/BerriAI/litellm.git /app
WORKDIR /app


RUN apt-get update && \
    apt-get install --no-install-recommends -y curl

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"



# Configure Poetry to not create virtual environments
# RUN poetry config virtualenvs.create false

# Install dependencies with poetry
RUN poetry install --with dev --extras proxy
# RUN poetry add --dev coverage

# Add poetry's virtualenv to PATH if needed (optional depending on run_test.py)

# Checkout the specific commit
RUN git -c advice.detachedHead=false checkout cf86ce390879b6242049a5a53cac52b339a51df3

# Rerun poetry install to ensure all dependencies are installed
RUN poetry install --with dev --extras proxy

WORKDIR /vulnbench
COPY swebench_docker swebench_docker
COPY --chmod=0755  dockers/entrypoint.sh .

ENTRYPOINT [ "./entrypoint.sh" ]

