import pytest
import socket
import threading
import time
import os
from honey_core import AdvancedHoneyEngine

@pytest.fixture(scope="module")
def honey_service():
    engine = AdvancedHoneyEngine(port=9998)
    proc = threading.Thread(target=engine.start, daemon=True)
    proc.start()
    time.sleep(1) # Ensure socket is bound
    return engine

def test_banner_emulation(honey_service):
    """Verify that the honeypot correctly baits attackers with a fake banner."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 9998))
        banner = s.recv(1024)
        assert b"OpenSSH_7.4p1" in banner

def test_automated_blacklisting(honey_service):
    """Ensure the IP is recorded after an interaction."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 9998))
    
    time.sleep(2) # Account for the random jitter
    assert os.path.exists("data/blacklist.txt")
    with open("data/blacklist.txt", "r") as f:
        assert "127.0.0.1" in f.read()