FROM th4tkh13m/vulnbench-base:3.12

RUN git clone https://github.com/microsoft/botbuilder-python.git /app
WORKDIR /app
RUN git -c advice.detachedHead=false checkout bd5662abb1297ebd457ace2918c26e5d611271e9



RUN pip install -e ./libraries/botbuilder-schema
RUN pip install -e ./libraries/botframework-connector
RUN pip install -e ./libraries/botframework-streaming
RUN pip install -e ./libraries/botbuilder-core
RUN pip install -e ./libraries/botbuilder-ai
RUN pip install -e ./libraries/botbuilder-applicationinsights
RUN pip install -e ./libraries/botbuilder-dialogs
RUN pip install -e ./libraries/botbuilder-azure
RUN pip install -e ./libraries/botbuilder-integration-applicationinsights-aiohttp
RUN pip install -e ./libraries/botbuilder-adapters-slack
RUN pip install -e ./libraries/botbuilder-integration-aiohttp
RUN pip install -e ./libraries/botbuilder-testing

RUN pip install -r ./libraries/botframework-connector/tests/requirements.txt
RUN pip install -r ./libraries/botbuilder-core/tests/requirements.txt
RUN pip install -r ./libraries/botbuilder-ai/tests/requirements.txt

RUN pip install coverage

WORKDIR /vulnbench
COPY swebench_docker swebench_docker
COPY --chmod=0755  dockers/entrypoint.sh .

ENTRYPOINT [ "./entrypoint.sh" ]