# Zeek → Splunk Pipeline (with Python Analysis)

```mermaid
flowchart TD

    subgraph CAPTURE["Packet Capture Layer"]
        PCAP["PCAP Input\n• college_dns_noise.pcap\n• offline analysis"]
    end

    subgraph ZEEK_LAYER["Zeek Processing Layer"]
        ZEEK_NODE["Zeek 8.0.5\n• zeek -C -r *.pcap\n• generates TSV logs"]
        LOGS["Zeek Logs Directory\nlogs_college_dns_noise/\n• dns.log\n• conn.log\n• weird.log"]
        ZEEK_NODE --> LOGS
    end

    %% Python Analysis Path
    subgraph PY["Python Analysis Layer"]
        PY_SCRIPT["dns_analysis.py\n• pandas DataFrame\n• timestamp parsing\n• top domains"]
        DF["Pandas DataFrame\n• df.head()\n• df.describe()"]
        PNG["Matplotlib Output\ndns_top_domains.png"]
        PY_SCRIPT --> DF --> PNG
    end

    %% Splunk Ingestion Path
    subgraph SPLUNK_INGEST["Splunk Ingestion Layer"]
        MON["Splunk Monitor Input\nmonitor:///logs_college_dns_noise\n• watches directory\n• re-ingests on restart"]
    end

    subgraph PARSING["TA‑Zeek Parsing Layer"]
        TA["Splunk TA‑Zeek\n• sourcetype mapping\n• field extraction\n• props/transforms"]
    end

    subgraph INDEXING["Index & Search Layer"]
        INDEX["Splunk Index: zeek_lab\n• parsed events\n• searchable fields"]
        SEARCH["Dashboards & SPL\n• DNS analytics\n• conn-state analysis\n• exfil detection"]
    end

    %% Main Flow
    PCAP -->|zeek -C -r| ZEEK_NODE
    LOGS -->|monitor input| MON
    MON -->|raw events| TA
    TA -->|parsed events| INDEX
    INDEX -->|SPL queries| SEARCH

    %% Python Branch
    LOGS -->|offline analysis| PY_SCRIPT
