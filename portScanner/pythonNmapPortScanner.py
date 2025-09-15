import argparse
import nmap

def nmap_scan(host, ports):
    nm = nmap.PortScanner()
    print(f"[+] Scanning {host} on ports {ports}...")

    nm.scan(hosts=host, ports=ports, arguments="-sV")  # -sV grabs service info

    for target in nm.all_hosts():
        print(f"\n[+] Scan Results for {target} ({nm[target].hostname()})")
        print(f"    State: {nm[target].state()}")

        for proto in nm[target].all_protocols():
            print(f"    Protocol: {proto}")
            ports = nm[target][proto].keys()
            for port in sorted(ports):
                state = nm[target][proto][port]['state']
                name = nm[target][proto][port].get('name', 'unknown')
                product = nm[target][proto][port].get('product', '')
                version = nm[target][proto][port].get('version', '')
                extrainfo = nm[target][proto][port].get('extrainfo', '')

                print(f"      Port {port:>5} : {state:<7} {name} {product} {version} {extrainfo}")

def main():
    parser = argparse.ArgumentParser(description="Port Scanner using python-nmap")
    parser.add_argument("-H", dest="targetHost", required=True, help="Target host or IP")
    parser.add_argument("-p", dest="targetPorts", required=True, help="Target ports (e.g. 22,80,443 or 1-100)")

    args = parser.parse_args()
    nmap_scan(args.targetHost, args.targetPorts)

if __name__ == "__main__":
    main()
