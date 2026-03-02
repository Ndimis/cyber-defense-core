import socket
import threading
import logging
import sys
import os
import time

# UTF-8 Fix for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

# Centralized Forensics Logging
if not os.path.exists("logs"): os.makedirs("logs")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[logging.FileHandler("logs/mesh_intelligence.log", encoding='utf-8'), logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("HoneyMesh")

class HoneyNode(threading.Thread):
    """A standalone deception node mimicking a specific service."""
    def __init__(self, port, service_name, banner):
        super().__init__()
        self.port = port
        self.service_name = service_name
        self.banner = banner
        self.running = True

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind(("0.0.0.0", self.port))
            server.listen(5)
            logger.info(f"📡 Node Online: {self.service_name} on Port {self.port}")
            
            while self.running:
                client, addr = server.accept()
                attacker_ip = addr[0]
                logger.warning(f"🚨 INTRUSION: {attacker_ip} hit {self.service_name} (Port {self.port})")
                
                # Send the specific service bait
                client.send(self.banner.encode('utf-8'))
                client.close()
        except Exception as e:
            if self.running:
                logger.error(f"❌ Node {self.port} Failure: {e}")
        finally:
            server.close()

class MeshController:
    """Manages multiple HoneyNodes and aggregates security intelligence."""
    def __init__(self, service_configs):
        self.nodes = []
        for config in service_configs:
            node = HoneyNode(config['port'], config['name'], config['banner'])
            self.nodes.append(node)

    def deploy(self):
        logger.info("🛡️ Deploying Distributed Honey-Mesh...")
        for node in self.nodes:
            node.start()

    def shutdown(self):
        logger.info("🛑 Shutting down Mesh...")
        for node in self.nodes:
            node.running = False
            # Dummy connection to break the accept() block
            try:
                socket.socket().connect(("127.0.0.1", node.port))
            except: pass

if __name__ == "__main__":
    # Define our deceptive surface area
    services = [
        {"port": 21, "name": "FTP-Service", "banner": "220 (vsFTPd 3.0.3)\n"},
        {"port": 23, "name": "Telnet-Srv", "banner": "Welcome to Linux 4.4.0-generic\nlogin: "},
        {"port": 80, "name": "HTTP-Server", "banner": "HTTP/1.1 200 OK\nServer: Apache/2.4.18\n\n"}
    ]
    
    mesh = MeshController(services)
    mesh.deploy()