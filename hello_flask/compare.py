import bcrypt
pw = "testing4"
salted = bcrypt.hashpw(bytes(pw, 'utf-8'), bcrypt.gensalt(12))
print(salted)
print(bcrypt.checkpw(bytes(pw, 'utf-8'), salted))
print(b'$2b$12$MdrtqZn1KrFoCIN3QLnFcOmc4ZgoAsUJ3HyfzgniLlEPRXC2L1Qvq' == salted)


