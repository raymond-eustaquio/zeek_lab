# Zeek DNS Analysis Lab

This project demonstrates a complete workflow for analyzing DNS traffic using Zeek.  
It includes:

- A DNS‑focused PCAP
- Generated Zeek logs
- Custom log‑formatting scripts
- A reproducible Docker environment
- A clean analysis workflow suitable for interviews or training

The goal is to show how to take raw packet data → generate Zeek logs → parse them → analyze DNS behavior.

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
│   ├── reset_lab.py                 # Wipes logs, PNGs, and resets environment
│   ├── pretty.sh                    # Formats JSON/Zeek logs for readability
│   └── pretty_all.sh                # Batch formatting helper for all logs
│
│   # Integrations (future API-driven modules)
├── integrations/                    # External system integrations
│   └── splunk/                      # Future Splunk REST + HEC integration
│       ├── splunk_client.py         # Planned Splunk REST API client
│       ├── hec_sender.py            # Planned HEC event sender
│       └── README.md                # Notes for future Splunk integration
│
│   # Logs (ignored in Git)
├── logs_college_dns_noise/          # Zeek output logs generated from PCAPs
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
└── .git                             # Git repository metadata
```

