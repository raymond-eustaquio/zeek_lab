FROM ubuntu:22.04

# System + Zeek dependencies
RUN apt update && \
    apt install -y \
        zeek \
        curl \
        git \
        python3 \
        python3-pip \
        jq \
        less \
        vim && \
    apt clean

# Python dependencies for dns_analysis.py
RUN pip3 install pandas matplotlib

WORKDIR /zeek

COPY . /zeek

CMD ["/bin/bash"]
