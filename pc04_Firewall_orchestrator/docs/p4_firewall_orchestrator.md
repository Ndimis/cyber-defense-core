# Concept Explainer: Automated IP Shunning & Firewall Orchestrator

### 🧠 The Core Concept
The **Firewall Orchestrator** is an active defense tool that bridges the gap between detection and response. In modern security environments, manually blocking an IP address is too slow to stop automated attacks. 

This project uses **API-driven security management** to:
1.  **Ingest Alerts:** Receive a "Malicious IP" signal (from your Scanner or Honeypot).
2.  **Validate:** Ensure the IP isn't on a **Whitelist** (like your own Admin IP) to prevent self-denial of service.
3.  **Execute:** Use system commands to programmatically drop all traffic from that source.



### 🛠️ Lessons Learned
1.  **Fail-Safe Mechanisms:** Automation can be dangerous. We implement a strict whitelist check to ensure critical infrastructure or legitimate user IPs are never accidentally shunned.
2.  **Input Sanitization:** Since we are passing IP addresses to system commands, we use the `ipaddress` library to validate that the input is a real IP, preventing command injection attacks.
3.  **Simulation vs. Production:** We built a toggle to "print" the command instead of executing it, allowing for safe debugging in a development environment.

### 📝 Key Takeaway
> **Defense is a race against time.** By automating the "Shun" command, we reduce the "Mean Time to Remediate" (MTTR) from minutes to milliseconds, effectively neutralizing automated botnets before they can perform a multi-stage exploit.

### 🚀 How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt