FROM th4tkh13m/vulnbench-base:3.9

# Clone faircloth-lab/phyluce to /app
RUN git clone https://github.com/simpeg/simpeg.git /app
WORKDIR /app
RUN git -c advice.detachedHead=false checkout 985593fd655dd4a58443e7be9a938dab6b978a6f

# Install conda
RUN mkdir -p ~/miniconda3
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
RUN bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
RUN rm ~/miniconda3/miniconda.sh

# Add conda to PATH
ENV PATH="/root/miniconda3/bin:${PATH}"
# Create conda environment
RUN conda env create -f environment.yml -y
# Activate the conda environment
RUN echo "source activate simpeg-dev" > ~/.bashrc
RUN /bin/bash -c "source ~/.bashrc"

# Using conda in path
ENV PATH="/root/miniconda3/envs/simpeg-dev/bin:${PATH}"

# Install dependencies
RUN pip install .
RUN pip install pytest-xdist pytest-cov coverage pytest-timeout




WORKDIR /vulnbench
COPY swebench_docker swebench_docker
COPY --chmod=0755  dockers/entrypoint.sh .

ENTRYPOINT [ "./entrypoint.sh" ]