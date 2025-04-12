FROM th4tkh13m/vulnbench-base:3.10

RUN git clone https://github.com/transferwise/pipelinewise.git /app
WORKDIR /app
RUN git -c advice.detachedHead=false checkout 3d8e7bc6214a6876ec3871ca4b4aca6bbe27ba17

RUN apt-get -qq update \
    && apt-get -qqy --no-install-recommends install \
        apt-utils \
        alien \
        gnupg \
        libaio1 \
        mbuffer \
        wget \
        tzdata \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -U --no-cache-dir pip

# Add Mongodb ppa
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add - \
    && echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.4 multiverse" | tee /etc/apt/sources.list.d/mongodb.list \
    && apt-get -qq update \
    && apt-get -qqy --no-install-recommends install \
        mongodb-database-tools \
    && rm -rf /var/lib/apt/lists/*

RUN make pipelinewise all_connectors -e pw_acceptlicenses=y

# Activate the virtualenv at source /app/.virtualenvs/pipelinewise/bin/activate
# RUN . /app/.virtualenvs/pipelinewise/bin/activate
ENV PIPELINEWISE_HOME=/app

RUN . /app/.virtualenvs/pipelinewise/bin/activate && coverage erase
ENV PATH="/app/.virtualenvs/pipelinewise/bin:${PATH}"

WORKDIR /vulnbench
COPY swebench_docker swebench_docker
COPY --chmod=0755  dockers/entrypoint.sh .

ENTRYPOINT ["./entrypoint.sh"]

