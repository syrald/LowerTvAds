FROM python:3.6

RUN apt-get update -y && \
    apt-get install libsndfile1-dev -y

RUN pip install librosa

ENTRYPOINT ["/bin/bash"]