FROM ubuntu:22.04

RUN apt update && \
    apt install -y zeek curl git python3 && \
    apt clean

WORKDIR /zeek

COPY . /zeek

CMD ["/bin/bash"]
