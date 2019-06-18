FROM python:3

# don't place it into $GOPATH/bin because Drone mounts $GOPATH as volume
RUN pip install bottle
RUN pip install requests
RUN pip install gunicorn
RUN pip install gevent

COPY webhook.py /
CMD [ "python" ,  "webhook.py" ]
# COPY golangci-lint /usr/bin/
# RUN apt-get update
# RUN apt-get install -y python3 python3-pip
# RUN pip3 install requests
# RUN pip3 install python-gitlab
# COPY scripts/gitlab /usr/bin/gitlab
# COPY golangci.yml /.golangci.yml
# CMD ["golangci-lint"]
