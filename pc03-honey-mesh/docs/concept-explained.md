# 🧠 Concept Explainer: Distributed Honey-Mesh

### 📌 The Concept: Horizontal Deception
In a real network, an attacker doesn't just look for one port; they perform **Horizontal Scanning** to find any weak point. A single honeypot is like a single mouse trap. A **Honey-Mesh** is a coordinated sensor network that covers the entire "Attack Surface".

### 🏗️ Architecture: Master-Agent Design
The Honey-Mesh operates using a centralized controller that manages multiple independent **HoneyNodes**:
1.  **Threaded Isolation**: Each service (FTP, Telnet, HTTP) runs in its own thread. If an attacker crashes the FTP node, the HTTP node remains active.
2.  **Service Emulation (Banners)**: Each node provides unique "Banners" that mimic real-world software versions. This forces the attacker to reveal their specific toolkit (e.g., if they try an Apache exploit on Port 80 vs. a Telnet brute-force on Port 23).
3.  **Intelligence Aggregation**: All nodes report to a single forensics file. This allows a security analyst to see a "Unified Attack Path"—for example, seeing that the same IP scanned Port 21, then 23, then 80 in sequence.

### 🛡️ Real-World Impact: Reconnaissance Thwarting
By populating unused ports with deceptive listeners, we achieve:
* **Early Warning**: We detect the "Scanning" phase of the Kill Chain before the actual "Exploitation" begins.
* **Attacker Profiling**: By observing which ports are hit first, we can determine if the attacker is a bot (scanning all ports) or a human (targeting specific business services).

### 🎓 Professional Takeaway
This project demonstrates expertise in **Concurrent Programming (Threading)** and **Security Orchestration**. It proves you can build high-performance, multi-threaded systems that provide wide-spectrum visibility across a network infrastructure.