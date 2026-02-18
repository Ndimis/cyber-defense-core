import nmap
import ipaddress

def scan_network(target_ip):
    
    # Validate IP format before starting Nmap
    try:
        ipaddress.ip_address(target_ip)
    except ValueError:
        raise ValueError(f"Invalid IP address: {target_ip}")
    # Initialize the Nmap PortScanner
    nm = nmap.PortScanner()
    
    # Perform a simple scan on common ports
    # Arguments: -sV (Service Version detection), -T4 (Timing template for speed)
    nm.scan(target_ip, '22-2000', arguments='-sV')
    
    scan_results = []
    for host in nm.all_hosts():
        host_info = {
            "host": host,
            "status": nm[host].state(),
            "protocols": []
        }
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()
            for port in ports:
                state = nm[host][proto][port]['state']
                service = nm[host][proto][port]['name']
                host_info["protocols"].append({
                    "port": port,
                    "service": service,
                    "state": state
                })
        scan_results.append(host_info)
    return scan_results

if __name__ == "__main__":
    # Test on your local machine or gateway
    results = scan_network('127.0.0.1')
    for elt in results:
        print(f"Host : {elt['host']} : ")
        for proto in elt['protocols']:
            print(f"--> : {proto}")