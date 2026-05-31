# Zeek → Splunk Pipeline (with Python Analysis)

```mermaid
flowchart TD

    subgraph CAPTURE["Packet Capture Layer"]
        PCAP["PCAP Input<br/>• college_dns_noise.pcap<br/>• offline analysis"]
    end

    subgraph ZEEK_LAYER["Zeek Processing Layer"]
        ZEEK_NODE["Zeek 8.0.5<br/>• zeek -C -r *.pcap<br/>• generates TSV logs"]
        LOGS["Zeek Logs Directory<br/>logs_college_dns_noise/<br/>• dns.log<br/>• conn.log<br/>• weird.log"]
        ZEEK_NODE --> LOGS
    end

    %% Python Analysis Path
    subgraph PY["Python Analysis Layer"]
        PY_SCRIPT["dns_analysis.py<br/>• pandas DataFrame<br/>• timestamp parsing<br/>• top domains"]
        DF["Pandas DataFrame<br/>• df.head()<br/>• df.describe()"]
        PNG["Matplotlib Output<br/>dns_top_domains.png"]
        PY_SCRIPT --> DF --> PNG
    end

    %% Splunk Ingestion Path
    subgraph SPLUNK_INGEST["Splunk Ingestion Layer"]
        MON["Splunk Monitor Input<br/>monitor:///logs_college_dns_noise<br/>• watches directory<br/>• re-ingests on restart"]
    end

    subgraph PARSING["TA‑Zeek Parsing Layer"]
        TA["Splunk TA‑Zeek<br/>• sourcetype mapping<br/>• field extraction<br/>• props/transforms"]
    end

    subgraph INDEXING["Index & Search Layer"]
        INDEX["Splunk Index: zeek_lab<br/>• parsed events<br/>• searchable fields"]
        SEARCH["Dashboards & SPL<br/>• DNS analytics<br/>• conn-state analysis<br/>• exfil detection"]
    end

    %% Main Flow
    PCAP -->|zeek -C -r| ZEEK_NODE
    LOGS -->|monitor input| MON
    MON -->|raw events| TA
    TA -->|parsed events| INDEX
    INDEX -->|SPL queries| SEARCH

    %% Python Branch
    LOGS -->|offline analysis| PY_SCRIPT
