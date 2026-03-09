### `src/firewall_engine.py`

import argparse
import subprocess
import ipaddress
import sys

# Pre-defined Whitelist to prevent accidental lockout
WHITELIST = ["127.0.0.1", "192.168.1.1", "8.8.8.8"]

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def manage_firewall(ip, action="block", simulate=True):
    """
    Simulates or executes a firewall block command using iptables logic.
    """
    if not is_valid_ip(ip):
        return f"Error: {ip} is not a valid IP address."

    if ip in WHITELIST:
        return f"Action Denied: {ip} is on the whitelist."

    # Construct the command (Linux iptables style)
    # -A INPUT: Append to input chain
    # -s: Source IP
    # -j DROP: Jump to DROP (block)
    cmd = ["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"]
    
    if action == "unblock":
        cmd[2] = "-D" # Change Append to Delete

    if simulate:
        return f"[SIMULATION] Executing: {' '.join(cmd)}"
    
    try:
        # In a real environment, this would execute the command
        # subprocess.run(cmd, check=True)
        return f"Successfully {action}ed {ip}"
    except Exception as e:
        return f"Failed to modify firewall: {str(e)}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Firewall Orchestrator")
    parser.add_argument("--block", help="IP address to block")
    parser.add_argument("--simulate", action="store_true", help="Run without executing system commands")
    
    args = parser.parse_args()
    
    if args.block:
        result = manage_firewall(args.block, simulate=args.simulate)
        print(result)
    else:
        parser.print_help()