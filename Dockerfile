FROM debian:jessie-backports

# install needed debian packages & clean up
RUN	apt-get update -y && \
    apt-get install -y --no-install-recommends curl tar ca-certificates unzip && \
    apt-get install -y python-pip python-dev python-lxml && \
    apt-get install -y python-mysqldb python-m2crypto && \
    apt-get clean autoclean && \
    apt-get autoremove --yes && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

ADD ./requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN adduser --disabled-password --quiet apprunner
USER apprunner
RUN mkdir -p /home/apprunner/running
ADD ./realip /home/apprunner/running/realip
WORKDIR /home/apprunner/running

EXPOSE 8080
CMD ["python", "-m", "realip", "gunicorn"]
