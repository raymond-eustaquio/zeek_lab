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

zeek_lab/
├── pcaps/           # Sample PCAPs used for analysis
├── logs/            # Zeek logs generated from the PCAPs
├── scripts/         # Custom tools (pretty-printer, helpers, etc.)
├── Dockerfile       # Reproducible Zeek environment
└── README.md        # Project documentation
