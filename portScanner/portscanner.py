import argparse
import socket
from threading import Thread, Semaphore

screenLock=Semaphore(value=1)

def connScan(tgtHost, tgtPort):
    try:
        connSkt=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connSkt.connect((tgtHost,tgtPort))
        connSkt.send(b'ViolentPython \r\n') #must send bytes in python 3
        results = connSkt.recv(100)

        with screenLock:
            print(f"[+] {tgtPort}/tcp open")
            print(f"[+]{results.decode(errors='ignore')}")

    except Exception:
        with screenLock:
            print(f"[-] {tgtPort}/tcp closed")

    finally:
        connSkt.close()

def portScan(tgtHost, tgtPorts):
    try:
        tgtIP= socket.gethostbyname(tgtHost)
    except socket.gaierror:
        print(f"[-]Cannot resolve '{tgtHost}':Unknown host")
        return
    
    try:
        tgtName=socket.gethostbyaddr(tgtIP)
        print(f"\n[+] Scan Results for: {tgtName[0]}")
    except socket.herror:
        print(f"\n[+]Scan Results for: {tgtIP}")

    socket.setdefaulttimeout(1)    
    for tgtPort in tgtPorts:
        t=Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()

def main():
    parser=argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("-H", dest="tgtHost", type=str, help="Specify target host")
    parser.add_argument("-p",dest="tgtPort",type=str, help="Specify target port(s), separated by comma")

    args=parser.parse_args()

    if not args.tgtHost or not args.tgtPort:
        parser.print_usage()
        exit(0)

    tgtHost = args.tgtHost
    tgtPorts = [p.strip() for p in args.tgtPort.split(",")]        
    portScan(tgtHost, tgtPorts)

if __name__=="__main__":
    main()