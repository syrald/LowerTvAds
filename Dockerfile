FROM python:3.6
MAINTAINER Vianney Bacoup <vianney.bacoup@gmail.com>

RUN apt-get update -y && \
    apt-get upgrade	&& \
    apt-get install -y --no-install-recommends \
        libsndfile1 \
        libperlio-gzip-perl
        
RUN pip install librosa && \
    pip install pandas && \
    pip install keras && \
    pip install --user --upgrade tensorflow

ENTRYPOINT ["/home/LowerTvAds/entrypoint.sh"]
