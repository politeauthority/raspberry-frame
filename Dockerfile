FROM debian:jessie
RUN apt-get update --fix-missing
RUN apt-get install -y --no-install-recommends \
    git \
    python-pip \
    python \
    libmysqlclient-dev \
    python-mysqldb \
    mysql-client \
    emacs

RUN mkdir /data/ && \
    cd /opt/ && \
    git clone https://github.com/politeauthority/raspberry-frame.git && \
    git config --global alias.co checkout && \
    git config --global alias.br branch && \
    git config --global alias.ci commit && \
    git config --global alias.st status && \
    git config --global alias.unstage 'reset HEAD --' && \
    echo 'alias dblocal="mysql -h${RF_MYSQL_HOST} -u${RF_MYSQL_USER} -p${RF_MYSQL_PASS} ${RF_MYSQL_NAME}"' >> /root/.bashrc

ENV RASPBERRY_FRAME_BASE_LOGGING_DIR='/data/logs'
ENV RASPBERRY_FRAME_BUILD="dev"
ENV RF_MYSQL_USER="root"
ENV RF_MYSQL_HOST="mysql"
ENV RF_MYSQL_PASS="password"
ENV RF_MYSQL_NAME="raspberry_frame"
ENV RF_MYSQL_PORT="3306"
ENV RASPBERRY_FRAME_APP_DATA_PATH="/data/"
ENV INSTAGRAM_CLIENT_ID="None"
ENV INSTAGRAM_CLIENT_SECRET="None"
ENV INSTAGRAM_TOKEN="None"
ENV TZ=America/Denver

VOLUME /opt/raspberry-frame/
VOLUME /data/

EXPOSE 80
