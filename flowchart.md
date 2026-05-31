# Zeek → Splunk Pipeline (with Python Analysis)

```mermaid
flowchart TD

    %% ============================
    %% PCAP → Zeek → Logs Pipeline
    %% ============================

    PCAP["PCAP Input<br/>• college_dns_noise.pcap<br/>• offline analysis"]
    ZEEK["Zeek Processing<br/>• zeek -C -r *.pcap<br/>• generates TSV logs"]
    LOGS["Zeek Logs Directory<br/>logs_college_dns_noise/<br/>• dns.log<br/>• conn.log<br/>• weird.log"]

    %% ============================
    %% Reset + Pipeline Scripts
    %% ============================

    RESET["reset_lab.py<br/>• wipes logs<br/>• removes PNGs<br/>• safe reset"]
    PIPE["process_pcaps.sh<br/>• runs Zeek<br/>• regenerates logs"]

    %% ============================
    %% Demo Status Check
    %% ============================

    DEMO["demo_status_check.py<br/>• checks Splunk status<br/>• checks Jupyter<br/>• verifies dns.json<br/>• verifies notebook<br/>• verifies logs + PCAP"]

    %% ============================
    %% Analysis Paths
    %% ============================

    JSON["dns.json<br/>• converted from dns.log<br/>• used by pandas"]
    NB["dns_analysis_demo.ipynb<br/>• Jupyter analysis<br/>• filtering<br/>• charts"]
    SPLUNK["Splunk Ingestion<br/>• monitor input<br/>• TA-Zeek parsing<br/>• dashboards"]

    %% ============================
    %% Edges
    %% ============================

    PCAP --> ZEEK --> LOGS
    RESET --> PIPE --> LOGS

    LOGS --> JSON
    LOGS --> SPLUNK

    PIPE --> DEMO
    DEMO --> NB
    DEMO --> SPLUNK
