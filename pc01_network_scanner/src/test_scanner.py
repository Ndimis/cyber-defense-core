import pytest
from scanner import scan_network

def test_localhost_scan_structure():
    """
    Test that the scanner returns a list and contains 
    expected keys like 'host' and 'status'.
    """
    # Scanning localhost is safe and doesn't require network access
    results = scan_network('127.0.0.1')
    
    assert isinstance(results, list)
    if len(results) > 0:
        assert "host" in results[0]
        assert "status" in results[0]

def test_invalid_ip():
    """
    Ensure the scanner raises ValueError for non-IP strings.
    """
    with pytest.raises(ValueError):
        scan_network('999.999.999.999')