import pytest
import socket
import threading
import time
from tarpit_engine import start_tarpit

def test_tarpit_delay():
    """
    Verify that the tarpit actually introduces a delay.
    """
    # Start tarpit in a background thread on a unique port
    port = 2225
    t = threading.Thread(target=start_tarpit, args=('127.0.0.1', port, 0.5), daemon=True)
    t.start()
    time.sleep(1) # Give the server time to bind

    start_time = time.time()
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', port))
    
    # We expect 5 characters. At 0.5s delay each, this should take ~2.5s
    received_data = b""
    for _ in range(5):
        char = client.recv(1)
        if not char: break
        received_data += char
    
    end_time = time.time()
    duration = end_time - start_time
    
    client.close()
    
    assert len(received_data) == 5
    assert duration >= 2.0  # Mathematically: 5 chars * 0.5s = 2.5s