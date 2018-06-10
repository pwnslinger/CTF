from Crypto.Util.number import *


def enc(msg):
    enc = [msg[i:i+2] + str(int(msg[i]) ^ int(msg[min(i+1, len(msg)-1)])) for i in range(0, len(msg), 2)]
    return ''.join(enc)


def dec(enc):
    dec = ''.join(enc[i:i+2] for i in range(0, len(enc), 3))
    if len(enc)%8 == 0:
        return dec
    else:
        return dec[:-1]


if __name__ == '__main__':

    with open('FLAG.enc', 'rb') as fp:
        buf = fp.read()
    fp.close()

    buf = bin(bytes_to_long(buf))[2:]

    for i in xrange(1000):
        buf = dec(buf)
        flag = long_to_bytes(int(buf,2))
        if 'ASIS' in flag:
            print '#%d -> %s' % (i+1, str(flag))
            break

