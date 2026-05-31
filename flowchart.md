# Zeek → Splunk Pipeline (with Python Analysis)

```mermaid
flowchart TD

%% ============================
%% LEFT SIDE: PIPELINE (YELLOW)
%% ============================

classDef yellow fill:#fff3b0,stroke:#e0b000,stroke-width:2px,color:#000;

subgraph CAPTURE["Packet Capture Layer"]
    PCAP["PCAP Input<br/>• college_dns_noise.pcap<br/>• offline analysis"]
end
class CAPTURE yellow

subgraph ZEEK["Zeek Processing Layer"]
    ZEEK_PROC["Zeek 8.0.5<br/>• zeek -C -r *.pcap<br/>• generates TSV logs"]
    LOGS["Zeek Logs Directory<br/>logs_college_dns_noise/<br/>• dns.log<br/>• conn.log<br/>• weird.log"]
    ZEEK_PROC --> LOGS
end
class ZEEK yellow

subgraph PY["Python Analysis Layer"]
    JSON["dns.json<br/>• converted from dns.log"]
    PY_SCRIPT["dns_analysis.py<br/>• pandas DataFrame<br/>• filtering<br/>• top domains"]
    PNG["dns_top_domains.png<br/>• matplotlib output"]
    TERM["Terminal Output<br/>• Top DNS Queries<br/>• printed to console"]
    JSON --> PY_SCRIPT --> PNG
    PY_SCRIPT --> TERM
end
class PY yellow

subgraph SPLUNK_INGEST["Splunk Ingestion Layer"]
    MON["Splunk Monitor Input<br/>monitor:///logs_college_dns_noise"]
end
class SPLUNK_INGEST yellow

subgraph PARSING["TA‑Zeek Parsing Layer"]
    TA["Splunk TA‑Zeek<br/>• sourcetype mapping<br/>• field extraction"]
end
class PARSING yellow

subgraph INDEXING["Index & Search Layer"]
    INDEX["Splunk Index: zeek_lab<br/>• parsed events"]
    SEARCH["Dashboards & SPL<br/>• DNS analytics<br/>• conn-state analysis"]
end
class INDEXING yellow

%% Main Flow
PCAP -->|zeek -C -r| ZEEK_PROC
LOGS -->|monitor input| MON
MON -->|raw events| TA
TA -->|parsed events| INDEX
INDEX -->|SPL queries| SEARCH
LOGS -->|offline analysis| JSON

%% ============================
%% RIGHT SIDE: DEMO SEQUENCE (BLUE)
%% ============================

classDef blue fill:#d7eaff,stroke:#005bbb,stroke-width:2px,color:#000;

subgraph DEMO["Demo Sequence (Runbook)"]
    RESET["reset_lab.py<br/>• wipes logs + PNGs"]
    PIPE["process_pcaps.sh<br/>• regenerates Zeek logs"]
    STATUS["demo_status_check.py<br/>• validates Splunk<br/>• validates Jupyter<br/>• checks dns.json<br/>• checks notebook"]
    NB["dns_analysis_demo.ipynb<br/>• Jupyter walkthrough"]
    SPL["Splunk UI<br/>• dashboards<br/>• field extraction"]
end
class DEMO blue

%% Demo Flow
RESET --> PIPE --> STATUS --> NB
STATUS --> SPL
