from string import ascii_letters, printable, digits

def charset():
    ignore = ascii_letters + digits
    accept = printable[63:]
    payload = "_GET"
    for c in payload:
        for i in xrange(256):
            for j in xrange(256):
                if chr(i^j) == c and chr(i) not in ignore and chr(j) not in ignore \
                        and chr(i) in accept and chr(j) in accept:
                    print '%s = %s ^ %s' % (c, chr(i), chr(j))
