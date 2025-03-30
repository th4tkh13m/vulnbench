FROM vulnbench-base:3.9

# Clone youtube-dl to /app
RUN git clone https://github.com/ytdl-org/youtube-dl.git  /app
WORKDIR /app
RUN git -c advice.detachedHead=false checkout 420d53387cff54ea1fccca061438d59bdb50a39c



# Install dependencies
RUN pip install pynose coverage

# Keep this list in sync with the `offlinetest` target in Makefile
ENV DOWNLOAD_TESTS="age_restriction|download|iqiyi_sdk_interpreter|socks|subtitles|write_annotations|youtube_lists|youtube_signature"
ENV test_set="-I test_($DOWNLOAD_TESTS)\.py"
ENV multiprocess_args="--processes=4 --process-timeout=540"

#["nosetests test --verbose $test_set $multiprocess_args"]
# CMD ["nosetests", "test", "--verbose", "$test_set", "$multiprocess_args"]
# We gonna run tests in the next step, so we don't need to run them here
# Sleep for 10 minutes to keep the container running
# ENTRYPOINT ["python3", "/app/run_test.py"]

WORKDIR /vulnbench
COPY swebench_docker swebench_docker
COPY --chmod=0755  dockers/entrypoint.sh .

ENTRYPOINT [ "./entrypoint.sh" ]
