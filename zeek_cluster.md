# Zeek Cluster Architecture

This document describes the modern Zeek cluster layout including Manager, Proxy, Workers, and NIC capture methods (AF_PACKET, PF_RING, DPDK, XDP).

## ASCII Diagram (Original)

```text
<your ASCII diagram here>
```

## Mermaid Diagram (Rendered on GitHub)

```mermaid
flowchart TD
    Manager["Manager<br/>• config distribution<br/>• log aggregation<br/>• cluster control"]

    Proxy["Proxy<br/>• event routing<br/>• state synchronization<br/>• load balancing"]

    Worker1["Worker 1<br/>zeek -i eth0<br/>AF_PACKET"]
    Worker2["Worker 2<br/>zeek -i eth1<br/>PF_RING"]
    WorkerN["Worker N<br/>zeek -i ethX<br/>AF_PACKET"]

    NIC1["NIC / Capture<br/>• AF_PACKET<br/>• PF_RING<br/>• libpcap"]
    NIC2["NIC / Capture<br/>• PF_RING<br/>• DPDK<br/>• libpcap"]
    NICN["NIC / Capture<br/>• AF_PACKET<br/>• XDP<br/>• PF_RING ZC"]

    Manager -->|Broker Messaging| Proxy
    Proxy -->|Broker Messaging| Worker1
    Proxy -->|Broker Messaging| Worker2
    Proxy -->|Broker Messaging| WorkerN

    Worker1 --> NIC1
    Worker2 --> NIC2
    WorkerN --> NICN
```
