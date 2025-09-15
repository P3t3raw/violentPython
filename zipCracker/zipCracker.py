import zipfile
import argparse
from threading import Thread

def extract_file(zfile,password):
    try:
        zfile.extractall(pwd=password.encode('utf-8'))
        print(f"[+]Found password: {password}")
    except:
        pass

def main():
    parser=argparse.ArgumentParser(description="zip file password cracker")
    parser.add_argument("-f", "--file", dest="zname", required=True, help="specify zip file")
    parser.add_argument("-d","--dictionary",dest="dname",required=True,help="specify dictionary file")

    args=parser.parse_args()

    zname=args.zname
    dname=args.dname

    try:
        zfile = zipfile.ZipFile(zname)
    except FileNotFoundError:
        print(f"[-] Zip file not found: {zname}")
        return
    
    try:
        with open(dname,"r", encoding="utf-8", errors="ignore") as passfile:
            for line in passfile:
                password=line.strip()
                t=Thread(target=extract_file,args=(zfile, password))
                t.start()
    except FileNotFoundError:
        print(f"[-] Dictionary file not found: {dname}")


if __name__=="__main__":
    main()