import argparse
import os
import pyminizip

def create_protected_zip(input_file,output_zip,password,compression_level):
    if not os.path.exists(input_file):
        print(f"[-]File not found: {input_file}")
        return
    
    try:
        pyminizip.compress(input_file,None,output_zip,password,compression_level)
        print(f"[+]Created password-protected zip: {output_zip}")
        print(f"[+]Password:{password}")
    except Exception as e:
        print(f"[-] Error creating zip: {e}")
def main():
    parser=argparse.ArgumentParser(description="Create a password-protected zip file")
    parser.add_argument("-f","--file", dest="file", required=True, help="file to compress into zip")
    parser.add_argument("-o","--output", dest="output", required=True,help="output zip file name")
    parser.add_argument("-p","--password", dest="password", required=True, help="password for the zip file")
    parser.add_argument("-l","--level", dest="level", type=int, default=5,help="compression level (1=fastest,9=best)")

    args=parser.parse_args()
    create_protected_zip(args.file, args.output,args.password,args.level)


if __name__=="__main__":
    main()