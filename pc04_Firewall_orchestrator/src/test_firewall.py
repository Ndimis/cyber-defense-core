import pytest
from firewall_engine import manage_firewall, WHITELIST

def test_whitelist_protection():
    """Ensure the orchestrator refuses to block whitelisted IPs."""
    target = WHITELIST[0]
    result = manage_firewall(target, simulate=True)
    assert "Action Denied" in result

def test_invalid_ip_validation():
    """Ensure the engine rejects malformed IP strings."""
    bad_ip = "999.999.999.999"
    result = manage_firewall(bad_ip)
    assert "Error" in result

def test_simulation_string():
    """Verify the command structure is generated correctly in simulation."""
    target = "10.0.0.50"
    result = manage_firewall(target, action="block", simulate=True)
    assert "iptables -A INPUT -s 10.0.0.50 -j DROP" in result

def test_unblock_logic():
    """Verify the command changes from Append (-A) to Delete (-D) for unblocking."""
    target = "10.0.0.50"
    result = manage_firewall(target, action="unblock", simulate=True)
    assert "-D" in result