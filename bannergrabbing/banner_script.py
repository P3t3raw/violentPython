import socket
import os
import sys

def retBanner(ip,port):
    try:
        # socket.setdefaulttimeout(5)
        s1= socket.socket()
        s1.connect((ip,port))
        banner = s1.recv(1024).decode().strip()
        return banner
    except Exception as e:
        print(f"[-] Error: {e}")
        return

def checkVulns(banner):
    f = open("vuln_banners.txt",'r')
    for line in f.readlines():
        if line.strip('\n') in banner:
            print("[+] Server is vulnerable: "+banner.strip('\n'))
    # if 'FreeFloat Ftp Server (Version 1.00)' in banner:
    #     print ('[+] FreeFloat FTP Server is vulnerable.')
    # elif '3Com 3CDaemon FTP Server Version 2.0' in banner:
    #     print ('[+] 3CDaemon FTP Server is vulnerable.')
    # elif 'Ability Server 2.34' in banner:
    #     print ('[+] Ability FTP Server is vulnerable.')
    # elif 'Sami FTP Server 2.0.2' in banner:
    #     print ('[+] Sami FTP Server is vulnerable.')
    # else:
    #     print ('[-] FTP Server is not vulnerable.')
    # return

def main():
    ip1 = "127.0.0.1"
    port = 8084
    banner1=retBanner(ip1,port)

    if banner1:
        print(f"[+] {ip1} : {banner1}")
        checkVulns(banner1)

if __name__ == '__main__':
    main()