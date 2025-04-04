FROM th4tkh13m/vulnbench-base:3.9


# Dependencies
# Ensure system is updated and has basic utilities
RUN apt-get update && apt-get install -y apt-utils software-properties-common
RUN apt-get install -y build-essential libcurl4-gnutls-dev libxml2-dev libssl-dev

RUN git clone https://github.com/red-hat-storage/ocs-ci.git /app
WORKDIR /app
RUN git checkout 29c57497850150833cbd5f514b3c40289b6f4676

# Install dependencies
RUN rm -rf /app/src/ocp-network-split && pip install -r requirements-dev.txt



RUN pip install pytest-cov

# Test command: pytest --ignore=tests -c pytest_unittests.ini --cov=ocs_ci


WORKDIR /vulnbench
COPY swebench_docker swebench_docker
COPY --chmod=0755  dockers/entrypoint.sh .

ENTRYPOINT [ "./entrypoint.sh" ]