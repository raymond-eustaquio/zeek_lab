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
  ├── integrations/
  │     └── splunk/
  │           ├── splunk_client.py      # REST API client (stub)
  │           ├── hec_sender.py         # HEC event sender (stub)
  │           └── README.md             # Notes + future roadmap
  ├── scripts/
  │     ├── dns_analysis.py
  │     ├── reset_lab.py
  │     └── process_pcaps.sh
  ├── .gitignore
  ├── README.md
  └── project_structure.md
```

