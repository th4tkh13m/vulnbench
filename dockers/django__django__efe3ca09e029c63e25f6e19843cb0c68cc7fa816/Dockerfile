FROM th4tkh13m:vulnbench-base:3.12

# Clone django to /app
RUN git clone https://github.com/django/django.git /app
WORKDIR /app
RUN git checkout efe3ca09e029c63e25f6e19843cb0c68cc7fa816

# Install dependencies
RUN apt-get update && apt-get install -y apt-utils software-properties-common
RUN apt-get install -y libmemcached-dev zlib1g-dev

# Install dependencies
RUN cd tests && pip install -e .. && pip install -r requirements/py3.txt


WORKDIR /vulnbench
COPY swebench_docker swebench_docker
COPY --chmod=0755  dockers/entrypoint.sh .


ENTRYPOINT [ "./entrypoint.sh" ]
