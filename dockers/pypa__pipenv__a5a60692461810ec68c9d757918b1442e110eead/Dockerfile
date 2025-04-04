FROM th4tkh13m/vulnbench-base:3.9

RUN git clone https://github.com/pypa/pipenv.git /app
WORKDIR /app
RUN git checkout a5a60692461810ec68c9d757918b1442e110eead

# Install dependencies
# Install pipenv
RUN pip install --user pipenv

# Add pipenv to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Use pipenv to install dependencies
RUN pipenv install --dev

WORKDIR /vulnbench
COPY swebench_docker swebench_docker
COPY --chmod=0755  dockers/entrypoint.sh .


# Test command: pipenv run pytest
ENTRYPOINT ["./entrypoint.sh"]