import pytest
import socket
import time
from mesh_core import MeshController

@pytest.fixture(scope="module")
def mesh_system():
    configs = [
        {"port": 5001, "name": "Test1", "banner": "B1"},
        {"port": 5002, "name": "Test2", "banner": "B2"}
    ]
    mesh = MeshController(configs)
    mesh.deploy()
    time.sleep(1) # Wait for threads to bind
    yield mesh
    mesh.shutdown()

def test_multi_port_availability(mesh_system):
    """Ensure both honey-ports are responding correctly."""
    for port in [5001, 5002]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            assert s.connect_ex(("127.0.0.1", port)) == 0

def test_service_specific_banners(mesh_system):
    """Verify each node sends its unique bait."""
    # Check Node 1
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 5001))
        assert s.recv(1024).decode() == "B1"
    
    # Check Node 2
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 5002))
        assert s.recv(1024).decode() == "B2"