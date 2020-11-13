FROM python:3.7-slim

LABEL base_image="python:3.7-slim"
LABEL about.home="https://github.com/Clinical-Genomics/vogue"
LABEL about.license="MIT License (MIT)"

# Update apt-get and then cleanup
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# Run commands as non-root user
RUN useradd --create-home --shell /bin/bash worker
RUN chown worker:worker -R /home/worker
USER worker

# Copy Vogue to /tmp to make it available to install
WORKDIR /home/worker/vogue
COPY . /home/worker/vogue
RUN pip install --no-cache-dir -r /home/worker/vogue/requirements.txt -e .

ENTRYPOINT ["vogue"]
CMD ["--help"]