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

# Project directory inside container
WORKDIR /zeek_lab

# Only copy code, not data or PCAPs
COPY scripts/ /zeek_lab/scripts/
COPY integrations/ /zeek_lab/integrations/
COPY process_pcaps.sh /zeek_lab/

CMD ["/bin/bash"]
