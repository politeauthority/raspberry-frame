FROM debian:jessie
RUN apt-get update --fix-missing
RUN apt-get install -y --no-install-recommends \
    git \
    python-pip \
    python \
    emacs

RUN mkdir /data/ && \
    cd /opt/ && \
    pip install -r /opt/raspberry-frame/requirements.txt && \
    git config --global alias.co checkout && \
    git config --global alias.br branch && \
    git config --global alias.ci commit && \
    git config --global alias.st status && \
    git config --global alias.unstage 'reset HEAD --'

ENV PA_BASE_LOGGING_DIR='/data/logs'
ENV PA_BUILD="dev"
ENV PA_APP_DATA_PATH="/data/"
ENV TZ=America/Denver

VOLUME /opt/raspberry-frame/
VOLUME /data/

EXPOSE 80
