# Concept Explainer: Automated Reconnaissance

### 🔍 Overview

Before a defender can protect a network, they must know what is on it. This project automates the **Reconnaissance** phase by programmatically mapping a target's attack surface.

### 🏗️ Phases of the Project

1. **Target Identification:** Defining the IP range or host to be scanned.
2. **Port Discovery:** Probing for open TCP/UDP ports to see which services are "listening."
3. **Service Version Detection:** Using Nmap's `-sV` flag to determine exactly which software version is running (e.g., Apache 2.4.41).
4. **Data Structuring:** Converting raw tool output into a clean JSON/Dictionary format for further analysis or automation.

**Note:** You must also have the Nmap binaries installed on your Windows machine for the Python library to work.

### 🛡️ Defensive Perspective (The "Blue Team" View)

By running this script daily, a security engineer can:

- **Detect Shadow IT:** Find unauthorized servers added to the network.
- **Vulnerability Mapping:** If a new vulnerability (CVE) is announced for "OpenSSH 8.2," we can instantly query our scan results to see which hosts are at risk.

### 🎓 Lessons Learned

- **Network Noise:** Standard scans are "loud" and easily blocked by firewalls. I learned that slowing down the scan timing (`-T3` vs `-T5`) helps evade simple rate-limiting.
- **Permission Errors:** Running Nmap via Python on Windows often requires "Run as Administrator" because raw socket manipulation is a protected system action.
- **Parsing Complexity:** Raw Nmap output is messy. I learned how to use the `python-nmap` wrapper to extract only the critical data points (Host, Port, State, Service).

### :blue_book: Example Output

Host : 127.0.0.1 :

--> : {'port': 135, 'service': 'msrpc', 'state': 'open'}

--> : {'port': 137, 'service': 'netbios-ns', 'state': 'filtered'}

--> : {'port': 445, 'service': 'microsoft-ds', 'state': 'open'}

--> : {'port': 903, 'service': 'vmware-auth', 'state': 'open'}

--> : {'port': 913, 'service': 'vmware-auth', 'state': 'open'}
