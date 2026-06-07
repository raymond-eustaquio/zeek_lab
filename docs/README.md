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

flowchart TD

    %% -------------------------
    %% INPUTS
    %% -------------------------
    A[PCAP Files<br>*.pcap]:::pcap

    %% -------------------------
    %% ZEEK PROCESSING
    %% -------------------------
    A --> B[Run Zeek<br>-C -r file.pcap]:::zeek
    B --> C[Zeek Logs<br>dns.log, conn.log, weird.log]:::logs

    %% -------------------------
    %% JSON CONVERSION
    %% -------------------------
    C --> D[Convert to JSON<br>dns_to_json.py]:::json
    D --> E[data/generated/dns.json]:::data

    %% -------------------------
    %% JUPYTER ANALYSIS
    %% -------------------------
    E --> F[Load into Jupyter<br>dns_analysis_demo.ipynb]:::jupyter
    F --> G[Charts, Insights, Detection]:::analysis

    %% -------------------------
    %% SPLUNK INGESTION
    %% -------------------------
    C --> H[Splunk Monitor Input<br>TA‑Zeek Field Extraction]:::splunk
    H --> I[Splunk Dashboards<br>DNS Analytics]:::dashboards

    %% -------------------------
    %% INTERACTIVE DEMO
    %% -------------------------
    G -. triggers .-> J[Interactive Demo<br>Press Enter to Advance]:::demo
    J --> K[Step‑by‑Step Walkthrough]:::demo

    %% -------------------------
    %% DARK MODE STYLES
    %% -------------------------
    classDef pcap fill:#1e3a8a,stroke:#60a5fa,stroke-width:1px,color:#e5e7eb;
    classDef zeek fill:#7c2d12,stroke:#fb923c,stroke-width:1px,color:#fef3c7;
    classDef logs fill:#78350f,stroke:#fbbf24,stroke-width:1px,color:#fef9c3;
    classDef json fill:#064e3b,stroke:#34d399,stroke-width:1px,color:#d1fae5;
    classDef data fill:#065f46,stroke:#10b981,stroke-width:1px,color:#ecfdf5;
    classDef jupyter fill:#831843,stroke:#f472b6,stroke-width:1px,color:#fce7f3;
    classDef analysis fill:#4c1d95,stroke:#c084fc,stroke-width:1px,color:#ede9fe;
    classDef splunk fill:#1f2937,stroke:#9ca3af,stroke-width:1px,color:#f3f4f6;
    classDef dashboards fill:#111827,stroke:#6b7280,stroke-width:1px,color:#e5e7eb;
    classDef demo fill:#0c4a6e,stroke:#38bdf8,stroke-width:1px,color:#e0f2fe;
