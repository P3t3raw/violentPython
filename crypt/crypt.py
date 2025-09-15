from passlib.hash import des_crypt

words = ["password","secret","kali"]

for w in words:
    salt = w[:2]
    hash_val=des_crypt.hash(w,salt=salt)
    print(hash_val)