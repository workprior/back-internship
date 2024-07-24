from OpenSSL import crypto

key = crypto.PKey()
key.generate_key(crypto.TYPE_RSA, 2048)

private_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, key)
with open("jwt-private.pem", "wb") as f:
    f.write(private_key)

public_key = crypto.dump_publickey(crypto.FILETYPE_PEM, key)
with open("jwt-public.pem", "wb") as f:
    f.write(public_key)
