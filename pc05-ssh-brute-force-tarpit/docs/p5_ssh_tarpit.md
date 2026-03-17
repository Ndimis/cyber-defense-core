# Concept Explainer: SSH Brute-Force Tarpit (The Active Decoy)

### 🧠 The Core Concept
A **Tarpit** (also known as a "Sticky Honeypot") is a proactive defense mechanism designed to manipulate the TCP/IP protocol to exhaust an attacker's resources. Unlike a firewall that drops packets (telling the attacker "you are blocked"), a Tarpit accepts the connection but refuses to let go.

The **Active Decoy** strategy works by exploiting the timeout logic of automated brute-force tools:
1.  **Handshake Hook:** The Tarpit completes the TCP three-way handshake, creating an established connection in the attacker's process table.
2.  **Protocol Stalling:** Once the connection is open, the Tarpit drips the mandatory "SSH-2.0" banner at a rate of one character every few seconds.
3.  **Thread Starvation:** By keeping the socket open, we force the attacker's bot to occupy one of its limited execution threads. If we trap 1,000 bots, we effectively take 1,000 threads out of the attacker's global pool.



### 🛠️ Technical Details & Lessons Learned
1.  **Manipulating the TCP Window:** Advanced Tarpits can set the TCP Window size to 0. This tells the attacker's machine, "I am too busy to receive data; wait for me," causing the attacking script to pause without closing the connection.
2.  **Asynchronous Resource Management:** In our implementation, we use `threading`. However, for high-density defense (trapping 10,000+ IPs), **Asynchronous I/O (`asyncio`)** is preferred to prevent our own server from running out of memory while managing "stuck" connections.
3.  **The "Slow-Drip" Banner:** Standard SSH clients expect a banner string immediately. By sending `S...S...H...-...2...0`, we stay just active enough to reset the "Keep-Alive" timers in the attacker's kernel, preventing a natural timeout.
4.  **Logging as Intel:** While the attacker is trapped, we can log the "fingerprint" of their connection (TCP options, sequence numbers), which can be used to identify the specific botnet software they are running.

### 📝 Key Takeaway
> **Defense is about shifting the economics of the attack.** A firewall block costs the attacker 0.1 seconds. A Tarpit costs them 30 minutes of CPU time and a network socket. By increasing the "cost of entry," we make our network an unattractive and unprofitable target.

### 🚀 How to Run

1. **Install Dependencies**:
   This project uses standard Python libraries:
   ```bash
   pip install -r requirements.txt