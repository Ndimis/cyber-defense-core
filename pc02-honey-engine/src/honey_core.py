import socket
import logging
import os
import random
import time
import sys

# 1. ENCODING FIX: Ensure the terminal handles UTF-8 for emojis (Windows fix)
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

# 2. LOGGING CONFIGURATION
if not os.path.exists("data"): 
    os.makedirs("data")

# Create a specialized logger that supports UTF-8
logger = logging.getLogger("HoneyEngine")
logger.setLevel(logging.INFO)

# Define the format for our forensics
formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')

# File Handler: Saves forensic data to disk in UTF-8
file_handler = logging.FileHandler("data/honeypot_forensics.log", encoding='utf-8')
file_handler.setFormatter(formatter)

# Stream Handler: Displays alerts to the console
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

class AdvancedHoneyEngine:
    def __init__(self, port=2222):
        self.port = port
        self.blacklist_path = "data/blacklist.txt"
        # PITFALL: Mimic an old, vulnerable SSH banner to bait scanners
        self.banner = b"SSH-2.0-OpenSSH_7.4p1 Debian-10+deb9u7\r\n"

    def start(self):
        """Initializes the deceptive listener."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server.bind(("0.0.0.0", self.port))
            server.listen(10)
            logger.info(f"🛡️ Advanced HoneyEngine deployed on port {self.port}...")
            
            while True:
                client, addr = server.accept()
                attacker_ip = addr[0]
                
                # PITFALL 1: Timing Jitter (Thwarting automated timing attacks)
                time.sleep(random.uniform(0.5, 2.0))
                
                # PITFALL 2: Service Emulation (The Bait)
                client.send(self.banner)
                
                # PITFALL 3: Payload Capture (Collecting Intelligence)
                try:
                    # Capture the first 1024 bytes of the attacker's intent
                    payload = client.recv(1024).decode('utf-8', errors='ignore').strip()
                    if payload:
                        logger.warning(f"🚨 INTRUSION FROM {attacker_ip} | PAYLOAD: {payload}")
                    else:
                        logger.warning(f"🚨 CONNECTION FROM {attacker_ip} (Scanned only)")
                except Exception as e:
                    logger.error(f"Failed to capture payload: {e}")

                # AUTOMATED RESPONSE: Blacklist the IP
                self._update_blacklist(attacker_ip)
                client.close()
                
        except KeyboardInterrupt:
            logger.info("🛑 Shutting down Deception Engine...")
        except Exception as e:
            logger.critical(f"💥 System Failure: {e}")
        finally:
            server.close()

    def _update_blacklist(self, ip):
        """Automated Remediation: Adds unique IPs to a blacklist file."""
        # Ensure the IP isn't already listed
        existing_ips = set()
        if os.path.exists(self.blacklist_path):
            with open(self.blacklist_path, "r", encoding='utf-8') as f:
                existing_ips = {line.strip() for line in f}

        if ip not in existing_ips:
            with open(self.blacklist_path, "a", encoding='utf-8') as f:
                f.write(f"{ip}\n")
            logger.info(f"🚫 IP {ip} successfully added to the automated blacklist.")

if __name__ == "__main__":
    honey = AdvancedHoneyEngine()
    honey.start()