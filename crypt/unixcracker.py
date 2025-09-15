from passlib.hash import des_crypt

def testPass(cryptPass):
    #Old Unix crypt() used first two chars as salt
    salt = cryptPass[0:2]

    with open('dictionary.txt','r', encoding='utf-8') as dictFile:
        for word in dictFile:
            word = word.strip('\n')
            cryptWord = des_crypt.hash(word, salt=salt)

            if cryptWord == cryptPass:
                print(f"[+] Found Password: {word}\n")
                return
    print("[-] Password Not Found.\n")        

def main():
    with open('passwords.txt','r', encoding='utf-8') as passFile:
        for line in passFile:
            if ":" in line:
                user = line.split(':')[0]
                cryptPass = line.split(':')[1].strip()
                print(f"[*] Cracking Password For : {user}")
                testPass(cryptPass)

if __name__ == "__main__":
    main()