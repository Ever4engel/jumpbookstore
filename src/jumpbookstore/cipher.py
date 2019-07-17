import base64
import hashlib
from Crypto.Cipher import ARC4


# a1b is defined in bookshelf_1.2.5_2018-10-05.js
CONST_a1b = bytearray([143, 9, 67, 216, 136, 253, 221, 64,
                       152, 250, 226, 76, 9, 7, 7, 163])


def decrypt_license(bid, u1, encrypted_license):
    # see a0l in bookshelf_1.2.5_2018-10-05.js
    h = bid.encode()
    if u1:
        h += u1.encode()
    h += CONST_a1b

    # see dea0qData_ in bookshelf_1.2.5_2018-10-05.js
    data = base64.b64decode(encrypted_license)
    salt = data[8:16]
    body = data[16:]

    key = hashlib.md5(h + salt).digest()
    cipher = ARC4.new(key)
    decrypted_license = cipher.decrypt(body).decode('utf-8')
    return decrypted_license


def decrypt_dat(base64data, key1, key2, key3, hs, bs):
    blob = base64.b64decode(base64data)
    prepared = prepare(key3, blob)
    decrypted = decrypt(key2, bs, prepared)
    finished = finish(key1, hs, decrypted)
    return finished


def gen_rc4_table(key):
    s = bytearray(range(256))
    j = 0
    for i in range(256):
        j = (j + s[i] + key[i % len(key)]) & 0xff
        s[i], s[j] = s[j], s[i]
    return s


def prepare(key, data):
    s = gen_rc4_table(key)
    return bytearray([b ^ s[i & 0xff] for i, b in enumerate(data)])


def decrypt(key, bsize, data):
    s = []
    for i in range(0, len(data), bsize):
        s.append(data[i])

    cipher = ARC4.new(key)
    c = list(cipher.decrypt(bytearray(s)))

    for i in range(0, len(data), bsize):
        data[i] = c.pop(0)

    return data


def finish(key, hsize, data):
    hsize = min([hsize, len(data)])

    cipher = ARC4.new(key)
    for i, x in enumerate(cipher.decrypt(data[:hsize])):
        data[i] = x

    return data
