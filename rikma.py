from Crypto.Random import get_random_bytes
from string import ascii_letters, digits
from Crypto.Protocol.KDF import scrypt
from humanize import naturalsize
from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Cipher import AES
from time import sleep, time, strftime, gmtime
from pwinput import pwinput
from random import choice
import argparse
import sys
import os

__name__ = 'rikma'
__version__ = '1.1.6'

spacescount = len(os.path.basename(sys.argv[0])) + 8
spaces = ' ' * spacescount

parser = argparse.ArgumentParser(description='encrypt/decrypt files with xchacha20-poly1305 or aes-256 gcm cipher', usage=f'{os.path.basename(sys.argv[0])} [-h, --help]\n{spaces}[--xchachapoly] [--aes]\n{spaces}[--encrypt] [--decrypt]\n{spaces}[--type <file/folder>] [--path <object>] [--path-file <object>]\n{spaces}[--password <pass>] [--show-password] [--gen-password <len>]\n{spaces}[--dnp-gen-password] [--dnw-gen-password]\n{spaces}[--fast-mode]\n{spaces}[--random-names]\n{spaces}[--no-colors]\n{spaces}[--version]')
parser.add_argument('--xchachapoly', dest='xchachapoly', action='store_true', help='use xchacha20-poly1305 cipher')
parser.add_argument('--aes', dest='aes', action='store_true', help='use aes-256 gcm cipher')
parser.add_argument('--encrypt', dest='encrypt', action='store_true', help='run in encrypt mode')
parser.add_argument('--decrypt', dest='decrypt', action='store_true', help='run in decrypt mode')
parser.add_argument('--type', metavar='<file/folder>', dest='type', type=str, nargs=1, help='type of object to encrypt/decrypt')
parser.add_argument('--path', metavar='<object>', dest='path', type=str, nargs=1, help='path to object for encryption/decryption')
parser.add_argument('--path-file', metavar='<object>', dest='pathsfromfile', type=str, nargs=1, help='load paths from file for encryption/decryption')
parser.add_argument('--password', metavar='<pass>', dest='passw', type=str, nargs=1, help='password for encryption/decryption')
parser.add_argument('--show-password', dest='showpassword', action='store_true', help='dont ask for password validation, show password')
parser.add_argument('--gen-password', metavar='<len>', dest='genpass', type=int, nargs=1, help='generate password with <len> length')
parser.add_argument('--dnp-gen-password', dest='dnpgenpass', action='store_true', help='dont print generated password')
parser.add_argument('--dnw-gen-password', dest='dnwgenpass', action='store_true', help='dont write generated password to file')
parser.add_argument('--log-file', dest='logfile', action='store_true', help='write stdout & stderr to generated file too, no colors')
parser.add_argument('--fast-mode', dest='fastmode', action='store_true', help='lower cpu/memory cost factor, insecure')
parser.add_argument('--random-names', dest='randomnames', action='store_true', help='rename file names to random string')
parser.add_argument('--no-colors', dest='nocolors', action='store_true', help='dont init colorama')
parser.add_argument('--no-pause', dest='nopause', action='store_true', help='dont pause once program has finished')
parser.add_argument('--version', dest='ver', action='store_true', help='display version and quit')
args = parser.parse_args()


def getrandomstr(size: int = 10) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(size))

if args.logfile:
    class Writers(object):
        def __init__(self, *writers):
            self.writers = writers

        def write(self, string):
            for w in self.writers:
                w.write(string)

        def flush(self):
            for w in self.writers:
                w.flush()

    logfile = open(strftime('rikma-%mm%dd%Yy-%Hh%Mm%SsUTC.log', gmtime(time())), 'w')
    sys.stdout = Writers(sys.__stdout__, logfile)
    sys.stderr = Writers(sys.__stdout__, logfile)

if args.ver:
    print(__version__)
    sys.exit(0)

if args.type is not None:
    if ('file' not in args.type and 'folder' not in args.type) or ('file' in args.type and 'folder' in args.type):
        print('[x] Argument "--type" must be equal "file" or "folder"')
        sys.exit(1)

if args.path is not None:
    if args.pathsfromfile is not None:
        print('[x] Both arguments used "--path" & "--path-file"')
        sys.exit(1)

    if args.type is None:
        print('[x] Didnt specify type of file, use argument "--type"')
        sys.exit(1)

    if not os.path.exists(args.path[0]):
        print('[x] "--path": Path is not exists')
        sys.exit(1)

    if 'file' in args.type[0] and not os.path.isfile(args.path[0]):
        print('[x] "--path": Path is not a file')
        sys.exit(1)

    elif 'folder' in args.type[0] and not os.path.isdir(args.path[0]):
        print('[x] "--path": Path is not a directory')
        sys.exit(1)

if args.pathsfromfile is not None:
    if args.type is None:
        print('[x] Didnt specify type of file, use argument "--type"')
        sys.exit(1)

    if not os.path.exists(args.pathsfromfile[0]):
        print('[x] "--path-file": Path is not exists')
        sys.exit(1)
    
    if not os.path.isfile(args.pathsfromfile[0]):
        print('[x] "--path-file": Path is not a file')
        sys.exit(1)
    
    with open(args.pathsfromfile[0], 'r', encoding='utf-8') as f:
        paths = f.readlines()
    
    args.path = []
    pathslist = []

    for path in paths:
        strippedpath = path.strip()

        if not os.path.exists(strippedpath):
            print(f'[!] Path "{strippedpath}" is not exists, skipping')
            continue

        if 'file' in args.type[0] and not os.path.isfile(strippedpath):
            print(f'[!] Path "{strippedpath}" is not a file, skipping')
            continue
        
        if 'folder' in args.type[0] and not os.path.isdir(strippedpath):
            print(f'[!] Path "{strippedpath}" is not a folder, skipping')
            continue

        pathslist.append(strippedpath)

    print(f'[i] Loaded {len(pathslist)} paths from file')

    if len(pathslist) == 0:
        sys.exit(1)
    
    args.path.append(pathslist)

if args.passw is not None:
    if args.genpass is not None:
        print("[x] Password already specified")
        sys.exit(1)

    if len(args.passw[0]) <= 1:
        print('\n[x] Password length must be more than one')
        sys.exit(1)

if args.genpass is not None:
    geneask = int(args.genpass[0])

    if geneask <= 1:
        print('\n[x] Generated password length must be more than one')
        sys.exit(1)

    args.passw = []
    args.passw.append(getrandomstr(geneask))

    if not args.dnpgenpass:
        print(f'\n[i] Generated password: "{args.passw[0]}"')
        sleep(.5)

    if not args.dnwgenpass:
        filename = 'genpassword-{0}.txt'.format(geneask)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(args.passw[0])

        print(f'[!] Saved password in "{filename}"')
        sleep(.5)


def printlogo(colormods: any) -> None:
    print(f"""{colormods.bbrb}
         \\                     
 .___  ` |   , , _ , _     ___ 
 /   \\ | |  /  |' `|' `.  /   `
 |   ' | |-<   |   |   | |    |
 /     / /  \\_ /   '   / `.__/|
{colormods.rs}""")


def overwritefile(file: str) -> None:
    with open(file, 'ba+') as fl:
        length = fl.tell()

    with open(file, 'br+') as fl:
        fl.seek(0)
        fl.write(os.urandom(length))

    os.remove(file)


def getfilesize(file: str) -> str:
    return naturalsize(os.stat(file).st_size, binary=True)


def randomnamefile(file: str) -> str:
    newfilename = getrandomstr()

    currentfiledir = os.path.dirname(file)
    currentfile = os.path.basename(file).split('.')
    currentfileext = '.' + '.'.join(currentfile[1:]) if len(currentfile) > 1 else ''

    newfilepath = os.path.join(currentfiledir, newfilename + currentfileext)

    return newfilepath


def aesencrypt(file: str, password: str, buffersize: int = 128 * 1024, n: int = 17, randomnames: bool = False) -> bool:
    global unkwfiles
    global totalfiles

    if '.enc' in file:
        return False

    if os.stat(file).st_size == 0:
        return False

    newfile = randomnamefile(os.path.abspath(file)) if randomnames else file

    try:
        filein = open(file, 'rb')
        fileout = open(newfile + '.enc', 'wb')
    except OSError:
        return False

    unkwfiles += 1
    print(f'{getfilesize(file)} {cmods.bbrb}:{cmods.rs} {os.path.abspath(file)}' if newfile == file else f'{getfilesize(file)} {cmods.bbrb}:{cmods.rs} {os.path.abspath(file)}  {cmods.bbrb}->{cmods.rs}  {newfile}')

    try:
        salt = get_random_bytes(32)
        key = scrypt(password, salt, key_len=32, N=2**n, r=8, p=1)
        fileout.write(salt)

        cipher = AES.new(key, AES.MODE_GCM)
        fileout.write(cipher.nonce)

        data = filein.read(buffersize)

        while len(data) != 0:
            encdata = cipher.encrypt(data)
            fileout.write(encdata)

            data = filein.read(buffersize)

        tag = cipher.digest()
        fileout.write(tag)

        filein.close()
        fileout.close()

        totalfiles += 1

        overwritefile(file)

        return True
    except Exception as e:
        try:
            filein.close()
            fileout.close()

            os.remove(newfile + '.enc')
        except NotImplementedError:
            pass
        except OSError:
            pass

        print(f"{__errn} Can't encrypt: {e}")

        return False


def aesdecrypt(file: str, password: str, buffersize: int = 128 * 1024, n: int = 17, randomnames: bool = False) -> bool:
    global unkwfiles
    global totalfiles

    if '.enc' not in file:
        return False
    
    if os.stat(file).st_size == 0:
        return False

    newfile = randomnamefile(os.path.abspath(file)) if randomnames else file
    formatedfileout = os.path.join(os.path.dirname(newfile), os.path.basename(newfile).replace('.enc', ''))

    try:
        filein = open(file, 'rb')
        fileout = open(formatedfileout, 'wb')
    except OSError:
        return False

    unkwfiles += 1
    print(f'{getfilesize(file)} {cmods.bbrb}:{cmods.rs} {os.path.abspath(file)}' if newfile == file else f'{getfilesize(file)} {cmods.bbrb}:{cmods.rs} {os.path.abspath(file)}  {cmods.bbrb}->{cmods.rs}  {newfile}')

    try:
        salt = filein.read(32)
        key = scrypt(password, salt, key_len=32, N=2**n, r=8, p=1)
        nonce = filein.read(16)

        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

        encdatasize = os.path.getsize(file) - 64

        for _ in range(int(encdatasize / buffersize)):
            data = filein.read(buffersize)
            decdata = cipher.decrypt(data)
            fileout.write(decdata)

        data = filein.read(int(encdatasize % buffersize))
        decdata = cipher.decrypt(data)
        fileout.write(decdata)

        tag = filein.read(16)
        cipher.verify(tag)

        filein.close()
        fileout.close()

        totalfiles += 1

        os.remove(file)

        return True
    except Exception as e:
        try:
            filein.close()
            fileout.close()

            os.remove(formatedfileout)
        except NotImplementedError:
            pass
        except OSError:
            pass

        if e.__class__ == ValueError:
            print(f'{__errn} Incorrect password or encrypted in fast mode: {e}')
        else:
            print(f"{__errn} Can't decrypt: {e}")

        return False


def xchachapolyencrypt(file: str, password: str, buffersize: int = 128 * 1024, n: int = 17, randomnames: bool = False) -> bool:
    global unkwfiles
    global totalfiles

    if '.enc' in file:
        return False

    if os.stat(file).st_size == 0:
        return False

    newfile = randomnamefile(os.path.abspath(file)) if randomnames else file

    try:
        filein = open(file, 'rb')
        fileout = open(newfile + '.enc', 'wb')
    except OSError:
        return False

    unkwfiles += 1
    print(f'{getfilesize(file)} {cmods.bbrb}:{cmods.rs} {os.path.abspath(file)}' if newfile == file else f'{getfilesize(file)} {cmods.bbrb}:{cmods.rs} {os.path.abspath(file)}  {cmods.bbrb}->{cmods.rs}  {newfile}')

    try:
        salt = get_random_bytes(32)
        key = scrypt(password, salt, key_len=32, N=2**n, r=8, p=1)
        fileout.write(salt)

        nonce = get_random_bytes(24)
        fileout.write(nonce)
        aad = get_random_bytes(32)
        fileout.write(aad)

        cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
        cipher.update(aad)

        data = filein.read(buffersize)

        while len(data) != 0:
            encdata = cipher.encrypt(data)
            fileout.write(encdata)

            data = filein.read(buffersize)
        
        tag = cipher.digest()
        fileout.write(tag)

        filein.close()
        fileout.close()

        totalfiles += 1

        overwritefile(file)

        return True
    except Exception as e:
        try:
            filein.close()
            fileout.close()

            os.remove(newfile + '.enc')
        except NotImplementedError:
            pass
        except OSError:
            pass

        print(f"{__errn} Can't encrypt: {e}")

        return False


def xchachapolydecrypt(file: str, password: str, buffersize: int = 128 * 1024, n: int = 17, randomnames: bool = False) -> bool:
    global unkwfiles
    global totalfiles

    if '.enc' not in file:
        return False
    
    if os.stat(file).st_size == 0:
        return False

    newfile = randomnamefile(os.path.abspath(file)) if randomnames else file
    formatedfileout = os.path.join(os.path.dirname(newfile), os.path.basename(newfile).replace('.enc', ''))

    try:
        filein = open(file, 'rb')
        fileout = open(formatedfileout, 'wb')
    except OSError:
        return False

    unkwfiles += 1
    print(f'{getfilesize(file)} {cmods.bbrb}:{cmods.rs} {os.path.abspath(file)}' if newfile == file else f'{getfilesize(file)} {cmods.bbrb}:{cmods.rs} {os.path.abspath(file)}  {cmods.bbrb}->{cmods.rs}  {newfile}')

    try:
        salt = filein.read(32)
        key = scrypt(password, salt, key_len=32, N=2**n, r=8, p=1)

        nonce = filein.read(24)
        aad = filein.read(32)

        cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
        cipher.update(aad)

        encdatasize = os.path.getsize(file) - 104

        for _ in range(int(encdatasize / buffersize)):
            data = filein.read(buffersize)
            decdata = cipher.decrypt(data)
            fileout.write(decdata)
        
        data = filein.read(int(encdatasize % buffersize))
        decdata = cipher.decrypt(data)
        fileout.write(decdata)
        
        tag = filein.read(16)
        cipher.verify(tag)

        filein.close()
        fileout.close()

        totalfiles += 1

        os.remove(file)

        return True
    except Exception as e:
        try:
            filein.close()
            fileout.close()

            os.remove(formatedfileout)
        except NotImplementedError:
            pass
        except OSError:
            pass

        if e.__class__ == ValueError:
            print(f'{__errn} Incorrect password or encrypted in fast mode: {e}')
        else:
            print(f"{__errn} Can't decrypt: {e}")

        return False


def workwithdirs(folder: str, password: str, encryptordecrypt: bool, xchachapolyoraes: bool, n: int = 17, randomnames: bool = False) -> bool:
    global unkwfiles
    global totalfiles

    globaldirstatus = True

    for root, dirs, files in os.walk(folder):
        for file in files:
            fwpath = os.path.join(root, file)

            if xchachapolyoraes:
                if encryptordecrypt:
                    status = xchachapolyencrypt(fwpath, password, n=n, randomnames=randomnames)
                else:
                    status = xchachapolydecrypt(fwpath, password, n=n, randomnames=randomnames)
            else:
                if encryptordecrypt:
                    status = aesencrypt(fwpath, password, n=n, randomnames=randomnames)
                else:
                    status = aesdecrypt(fwpath, password, n=n, randomnames=randomnames)
            
            globaldirstatus = False if not status else globaldirstatus

    if unkwfiles == 0:
        print(f'{__warn} Files not found in this directory')

    return globaldirstatus


def askopen(title: str, filetypes: tuple, folder: bool = False) -> str:
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)

    if folder:
        a = filedialog.askdirectory(title=title, mustexist=True)
    else:
        a = filedialog.askopenfilename(title=title, filetypes=filetypes)

    root.destroy()

    return a


if __name__ == 'rikma':
    if not args.nocolors and not args.logfile:
        import colorama

        colorama.init(autoreset=True)

        class cmods:
            rs = '\x1b[0m'
            bold = '\x1b[1m'
            bbrb = '\x1b[1m\x1b[34;1m'
            bbrr = '\x1b[1m\x1b[31;1m'
            bbry = '\x1b[1m\x1b[33;1m'
    else:
        class cmods:
            rs = ''
            bold = ''
            bbrb = ''
            bbrr = ''
            bbry = ''

    __info = f'{cmods.bbrb}[i]{cmods.rs}'
    __warn = f'{cmods.bbry}[!]{cmods.rs}'
    __errn = f'{cmods.bbrr}[x]{cmods.rs}'

    printlogo(cmods)

    try:
        if not args.xchachapoly and not args.aes:
            print(f'\n{__info} Choose cipher:\n{cmods.bbrb}(1){cmods.rs} XChaCha20-Poly1305\n{cmods.bbrb}(2){cmods.rs} AES-256 GCM\n > ', end='')
            cipherask = input().strip()

            if ('1' not in cipherask and '2' not in cipherask) or ('1' in cipherask and '2' in cipherask):
                sys.exit(1)
        else:
            cipherask = '1' if args.xchachapoly else '2'

        if not args.encrypt and not args.decrypt:
            print(f'\n{__info} Choose mode:\n{cmods.bbrb}(1){cmods.rs} Encrypt\n{cmods.bbrb}(2){cmods.rs} Decrypt\n > ', end='')
            modeask = input().strip()

            if ('1' not in modeask and '2' not in modeask) or ('1' in modeask and '2' in modeask):
                sys.exit(1)
        else:
            modeask = '1' if args.encrypt else '2'

        if args.type is None:
            print(f'\n\n{__info} Choose what to encrypt/decrypt:\n{cmods.bbrb}(1){cmods.rs} File\n{cmods.bbrb}(2){cmods.rs} Folder\n > ', end='')
            typeask = input().strip()

            if ('1' not in typeask and '2' not in typeask) or ('1' in typeask and '2' in typeask):
                sys.exit(1)
        else:
            typeask = '1' if 'file' in args.type[0] else '2'

        if args.path is None:
            if sys.platform != 'win32':
                print(f'\n\n{__info} Enter path to object for encryption/decryption:\n > ', end='')
                pathask = input().strip()

                if not os.path.exists(pathask):
                    print(f'\n{__errn} Path is not exists')
                    sys.exit(1)
                if '1' in typeask and not os.path.isfile(pathask):
                    print(f'\n{__errn} Path is not a file')
                    sys.exit(1)
                elif '2' in typeask and not os.path.isdir(pathask):
                    print(f'\n{__errn} Path is not a directory')
                    sys.exit(1)
            else:
                print(f'\n\n{__info} Enter path to object for encryption/decryption:\n > ', end='')

                pathask = askopen('Select file', (('All files', '*.*'), ('All files', ''))) if '1' in typeask else askopen('Select folder', (('All files', '*.*'), ('All files', '')), True)

                if pathask == '':
                    pathask = None

                print(pathask if pathask is not None else f'{cmods.bbrr}None{cmods.rs}')

                if pathask is None:
                    print(f'\n{__errn} Canceled by user')
                    sys.exit(1)

                if not os.path.exists(pathask):
                    print(f'\n{__warn} Path is not exists')
                    sys.exit(1)

        else:
            pathask = args.path[0]

        if args.passw is None:
            print(f'\n\n{__info} Enter password for encryption/decryption:\n{__warn} Spaces at start & end will be removed\n{__warn} Leave field empty, if you want to generate password\n > ', end='')
            passask = pwinput('').strip() if not args.showpassword else input().strip()

            if len(passask) <= 1 and passask != '':
                print(f'\n{__errn} Password length must be more than one')
                sys.exit(1)

            if passask == '':
                print(f'\n\n{__info} Enter length of generated password:\n > ', end='')
                geneask = input().strip()

                try:
                    int(geneask)
                except ValueError:
                    print(f'\n{__errn} Length must be integer')
                    sys.exit(1)

                if int(geneask) <= 1:
                    print(f'\n{__errn} Password length must be more than one')
                    sys.exit(1)

                passask = getrandomstr(int(geneask))

                if not args.dnpgenpass:
                    print(f'\n{__info} Generated password: "{passask}"')
                    sleep(.5)

                if not args.dnwgenpass:
                    filename = 'genpassword-{0}.txt'.format(int(geneask))

                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(passask)

                    print(f'{__warn} Saved password in "{filename}"')
                    sleep(.5)
            elif not args.showpassword and '2' not in modeask:
                print(f'\n\n{__info} Repeat password:\n > ', end='')
                repeatpassask = pwinput('').strip()

                if repeatpassask != passask:
                    print(f'\n{__errn} Password didnt match')
                    sys.exit(1)
        else:
            passask = args.passw[0]

        unkwfiles = 0
        totalfiles = 0

        start = time()
        print()

        if type(pathask) is not list:
            if '1' in modeask:
                if '1' in typeask:
                    globalstatus = xchachapolyencrypt(pathask, passask, n=17 if not args.fastmode else 14, randomnames=args.randomnames) if '1' in cipherask else aesencrypt(pathask, passask, n=17 if not args.fastmode else 14, randomnames=args.randomnames)
                else:
                    globalstatus = workwithdirs(pathask, passask, encryptordecrypt=True, xchachapolyoraes='1' in cipherask, n=17 if not args.fastmode else 14, randomnames=args.randomnames)
            else:
                if '1' in typeask:
                    globalstatus = xchachapolydecrypt(pathask, passask, n=17 if not args.fastmode else 14, randomnames=args.randomnames) if '1' in cipherask else aesdecrypt(pathask, passask, n=17 if not args.fastmode else 14, randomnames=args.randomnames)
                else:
                    globalstatus = workwithdirs(pathask, passask, encryptordecrypt=False, xchachapolyoraes='1' in cipherask, n=17 if not args.fastmode else 14, randomnames=args.randomnames)
        else:
            globalstatus = True

            if '1' in modeask:
                if '1' in typeask:
                    for path in pathask:
                        status = xchachapolyencrypt(path, passask, n=17 if not args.fastmode else 14, randomnames=args.randomnames) if '1' in cipherask else aesencrypt(pathask, passask, n=17 if not args.fastmode else 14, randomnames=args.randomnames)
                        globalstatus = False if not status else globalstatus
                else:
                    for path in pathask:
                        status = workwithdirs(path, passask, encryptordecrypt=True, xchachapolyoraes='1' in cipherask, n=17 if not args.fastmode else 14, randomnames=args.randomnames)
                        globalstatus = False if not status else globalstatus
            else:
                if '1' in typeask:
                    for path in pathask:
                        status = xchachapolydecrypt(path, passask, n=17 if not args.fastmode else 14, randomnames=args.randomnames) if '1' in cipherask else aesdecrypt(pathask, passask, n=17 if not args.fastmode else 14, randomnames=args.randomnames)
                        globalstatus = False if not status else globalstatus
                else:
                    for path in pathask:
                        status = workwithdirs(path, passask, encryptordecrypt=False, xchachapolyoraes='1' in cipherask, n=17 if not args.fastmode else 14, randomnames=args.randomnames)
                        globalstatus = False if not status else globalstatus
        
        # TODO: .

        end = time() - start
        print()

        if globalstatus or (unkwfiles - totalfiles) == 0:
            if '1' in modeask:
                print(f'{__info} Successfully encrypted {totalfiles} file(s)\t{end}')
            else:
                print(f'{__info} Successfully decrypted {totalfiles} file(s)\t{end}')
        else:
            if '1' in modeask:
                print(f'{__info} There were errors during encryption, successfully encrypted {totalfiles} file(s)\t{end}')
            else:
                print(f'{__info} There were errors during decryption, successfully decrypted {totalfiles} file(s)\t{end}')
        
        if args.logfile:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            logfile.close()

        if not args.nopause:
            print()
            os.system('pause')
    except KeyboardInterrupt:
        print(f'\n\n{__errn} KeyboardInterrupt')
        sys.exit(2)
