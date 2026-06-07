## 📘 Project Overview

This project demonstrates a complete, end‑to‑end workflow for analyzing DNS traffic using Zeek.  
It is designed as a clean, reproducible lab environment suitable for interviews, training, and portfolio demonstrations.

The workflow includes:

- **A DNS‑focused PCAP**  
  A curated capture containing realistic DNS noise and query patterns.

- **Automated Zeek log generation**  
  A pipeline that processes the PCAP and produces structured Zeek logs  
  (`dns.log`, `conn.log`, `weird.log`, etc.).

- **Custom analysis and formatting scripts**  
  Tools for converting Zeek logs to JSON, cleaning output, generating terminal summaries,  
  and producing visualizations such as `dns_top_domains.png`.

- **Splunk ingestion and dashboards**  
  A Splunk monitor input ingests Zeek logs, the TA‑Zeek add‑on parses fields,  
  and dashboards provide DNS analytics and search workflows.

- **A reproducible environment**  
  Optional Dockerfile, reset scripts, and a status‑check script ensure the lab can be reset  
  and rerun consistently.

- **A Jupyter Notebook analysis workflow**  
  A guided notebook (`dns_analysis_demo.ipynb`) that loads `dns.json`, explores DNS behavior,  
  filters events, and visualizes top domains.

The goal of this project is to show how to take **raw packet data → generate Zeek logs → parse them → analyze DNS behavior** using a combination of automation, scripting, Splunk ingestion, and interactive notebook analysis.

---
## Project Structure

```
zeek_lab/
│
│   # Pipeline (PCAP → Zeek → Analysis)
├── process_pcaps.sh                 # Main pipeline script: runs Zeek on PCAPs and prepares logs
│
│   # Scripts (analysis + automation helpers)
├── scripts/                         # All analysis and automation scripts
│   ├── dns_analysis.py              # Parses Zeek DNS logs and generates charts
│   ├── dns_to_json.py               # Converts Zeek DNS logs to JSON (for pandas)
│   ├── reset_lab.py                 # Wipes logs + PNGs (safe: does NOT touch notebooks)
│   ├── demo_status_check.py         # Checks Splunk, Jupyter, and project readiness
│   ├── pretty.sh                    # Formats JSON/Zeek logs for readability
│   └── pretty_all.sh                # Batch formatting helper for all logs
│
│   # Integrations (future API-driven modules)
├── integrations/
│   └── splunk/
│       ├── splunk_client.py         # Planned Splunk REST API client
│       ├── hec_sender.py            # Planned HEC event sender
│       └── README.md                # Notes for future Splunk integration
│
│   # Logs (ignored in Git)
├── logs_college_dns_noise/          # Zeek output logs generated from PCAPs (ignored via .gitignore)
│
│   # Notebooks (your demo lives here)
├── notebooks/
│   └── dns_analysis_demo.ipynb      # Your Jupyter demo notebook (KEEP this!)
│
│   # Data (optional, if you want dns.json in repo)
├── data/
│   └── dns.json                     # JSON output from dns_to_json.py (safe to commit)
│
│   # Documentation
├── flowchart.md                     # Pipeline flowchart (Mermaid)
├── zeek_cluster.md                  # Notes on Zeek cluster deployment
├── README.md                        # Main documentation
│
│   # Helpers / Misc
├── Dockerfile                       # Optional container build for Zeek environment
├── .gitignore                       # Git ignore rules
│
└── (NO .git directory in repo)      # .git/ stays local, NEVER committed
```
