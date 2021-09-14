import os
import pyAesCrypt
import random
import sys
import humanize
import time

keysPos = int
keys = int
keysLen = int

logPos = int
logFile = ''

bufferSize = 128 * 1024
result = 0
keysList = []

rikmaLogo = '''
                  .=-.-.,--.-.,-.         ___    ,---.      
      .-.,.---.  /==/_ /==/- |\  \ .-._ .'=.'\ .--.'  \     
     /==/  `   \|==|, ||==|_ `/_ //==/ \|==|  |\==\-/\ \    
    |==|-, .=., |==|  ||==| ,   / |==|,|  / - |/==/-|_\ |   
    |==|   '='  /==|- ||==|-  .|  |==|  \/  , |\==\,   - \  
    |==|- ,   .'|==| ,||==| _ , \ |==|- ,   _ |/==/ -   ,|  
    |==|_  . ,'.|==|- |/==/  '\  ||==| _ /\   /==/-  /\ - \ 
    /==/  /\ ,  )==/. /\==\ /\=\.'/==/  / / , |==\ _.\=\.-' 
    `--`-`--`--'`--`-`  `--`      `--`./  `--` `--`         
'''

def exitOnException():
    xd = logFile.close() if isinstance(logFile, type) and logFile != '' else ''
    quit(0)

if '-g' in str(sys.argv) or '--gen-keys' in str(sys.argv):
    if '-e' in str(sys.argv) or '--encrypt' in str(sys.argv):
        try:
            for i in range(0, len(sys.argv)):
                keysPos = i if '-g' in sys.argv[i] or '--gen-keys' in sys.argv[i] else keysPos
            
            if int(sys.argv[keysPos+1]):
                keys = int(sys.argv[keysPos+1])
            if int(sys.argv[keysPos+2]):
                keyLen = int(sys.argv[keysPos+2])
        except Exception as ex:
            if 'index out of range' in str(ex):
                print(f'Error: the {sys.argv[keysPos]} argument requires 2 variables: <keys>, <length>')
            elif 'invalid literal for int()' in str(ex):
                print(f'Error: variables for {sys.argv[keysPos]} argument, must be integer')
            else:
                print(f'Unknown error: {str(ex)}')
            exitOnException()

if '-l' in str(sys.argv) or '--log-file' in str(sys.argv):
    try:
        for i in range(0, len(sys.argv)):
            logPos = i if '-l' in sys.argv[i] or '--log-file' in sys.argv[i] else logPos

        if sys.argv[logPos+1]:
            logFile = sys.argv[logPos+1]
    except Exception as ex:
        if 'index out of range' in str(ex):
            print(f'Error: the {sys.argv[logPos]} argument requires 1 variable: <file>')
        else:
            print(f'Unknown error: {str(ex)}')
        exitOnException()

def getSize(file):
    st = os.stat(file).st_size
    return humanize.naturalsize(st)

def randomStr(strSize):
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&-/?@\^~0123456789') for _ in range(strSize))

def genKeys(keys, keyLen):
    if len(keysList) == 0:
        if 4 <= keyLen <= 256:
            pass
        else:
            if keyLen <= 4:
                print('Key/s length must be at least 4 characters')
            elif keyLen >= 256:
                print('Key/s length must be no more than 256 characters')
            keyLen = 8
            print('Using 8 characters key/s length\n')

        for _ in range(keys):
            keysList.append(randomStr(keyLen))

        print(f'Generated {str(len(keysList))} key/s:')
        for i in range(len(keysList)):
            print(f'  "{keysList[i]}"')
        print('')

def secureDelete(path):
    try:
        with open(path, "ba+") as f:
            length = f.tell()
            f.close()
        with open(path, "br+") as f:
            f.seek(0)
            f.write(os.urandom(length))
            f.close()
        os.remove(path)
    except Exception as ex:
        print(ex)

def encrypt(path, key):
    global result
    if '-o' in str(sys.argv) or '--one-file':
        try:
            name = os.path.basename(path)
            path = path.replace(name, '')
            size = getSize(os.path.join(path, name))
            print('\nEncrypting:         ', name)
            print('Path:               ', os.path.join(path, name))
            print('Size:               ', size)

            key = random.choice(keysList) if '-g' in str(sys.argv) or '--gen-keys' in str(sys.argv) else key
            pyAesCrypt.encryptFile(os.path.join(path, name),
                                os.path.join(path, name + '.aes'),
                                key,
                                bufferSize)
            encSize = getSize(os.path.join(path, name + '.aes'))

            print('Encrypted name:     ', name + '.aes')
            print('Encrypted path:     ', os.path.join(path, name + '.aes'))
            print('Encrypted size:     ', encSize)
            print('Key:                 "'+key+'"')
            if logFile != '':
                logFile.write(f'''
Encrypting:         {name}
Path:               {os.path.join(path, name)}
Size:               {size}
Encrypted name:     {name + '.aes'}
Encrypted path:     {os.path.join(path, name + '.aes')}
Encrypted size:     {encSize}
Key:                "{key}"
''')
            print('Rewriting old file ...')
            secureDelete(os.path.join(path, name))
            result += 1
            return
        except Exception as ex:
            print(ex)
            return

    for name in os.listdir(path):
        try:
            if os.path.isfile(os.path.join(path, name)):
                if '.aes' not in name:
                    size = getSize(os.path.join(path, name))
                    if not '-f' in str(sys.argv) and not '--folders' in str(sys.argv):
                        print('\nEncrypting:         ', name)
                        print('Path:               ', os.path.join(path, name))
                        print('Size:               ', size)
                    key = random.choice(keysList) if '-g' in str(sys.argv) or '--gen-keys' in str(sys.argv) else key
                    pyAesCrypt.encryptFile(os.path.join(path, name),
                                        os.path.join(path, name + '.aes'),
                                        key,
                                        bufferSize)
                    encSize = getSize(os.path.join(path, name + '.aes'))
                    if not '-f' in str(sys.argv) and not '--folders' in str(sys.argv):
                        print('Encrypted name:     ', name + '.aes')
                        print('Encrypted path:     ', os.path.join(path, name + '.aes'))
                        print('Encrypted size:     ', encSize)
                        print('Key:                 "'+key+'"')
                    if logFile != '':
                        logFile.write(f'''
Encrypting:         {name}
Path:               {os.path.join(path, name)}
Size:               {size}
Encrypted name:     {name + '.aes'}
Encrypted path:     {os.path.join(path, name + '.aes')}
Encrypted size:     {encSize}
Key:                "{key}"
''')
                    print('Rewriting old file ...')
                    secureDelete(os.path.join(path, name))
                    result += 1
            elif '-a' in str(sys.argv) or '--all' in str(sys.argv):
                xd = print('Encrypting          ', os.path.join(path, name)) if '-f' in str(sys.argv) or '--folders' in str(sys.argv) else ''
                encrypt(os.path.join(path, name), key)
        except Exception as ex:
            print(ex)
            pass


def decrypt(path, key):
    global result
    if '-o' in str(sys.argv) or '--one-file':
        try:
            name = os.path.basename(path)
            path = path.replace(name, '')
            size = getSize(os.path.join(path, name))
            print('\nDecrypting:         ', name)
            print('Path:               ', os.path.join(path, name))
            print('Size:               ', size)

            pyAesCrypt.decryptFile(os.path.join(path, name),
                                           os.path.join(path, name.replace('.aes', '')),
                                           key,
                                           bufferSize)
            decSize = getSize(os.path.join(path, name.replace('.aes', '')))

            print('Decrypted name:     ', name + '.aes')
            print('Decrypted path:     ', os.path.join(path, name + '.aes'))
            print('Decrypted size:     ', decSize)
            print('Key:                 "'+key+'"')
            if logFile != '':
                logFile.write(f'''
Decrypting:         {name}
Path:               {os.path.join(path, name)}
Size:               {size}
Decrypted name:     {name.replace('.aes', '')}
Decrypted path:     {os.path.join(path, name.replace('.aes', ''))}
Decrypted size:     {decSize}
Key:                "{key}"
''')
            print('Rewriting old file ...')
            secureDelete(os.path.join(path, name))
            result += 1
            return
        except Exception as ex:
            print(ex)
            return

    for name in os.listdir(path):
        try:
            if os.path.isfile(os.path.join(path, name)):
                if '.aes' in name:
                    size = getSize(os.path.join(path, name))
                    if not '-f' in str(sys.argv) and not '--folders' in str(sys.argv):
                        print('\nDecrypting          ', name)
                        print('Path:               ', os.path.join(path, name))
                        print('Size:               ', getSize(os.path.join(path, name)))
                    pyAesCrypt.decryptFile(os.path.join(path, name),
                                           os.path.join(path, name.replace('.aes', '')),
                                           key,
                                           bufferSize)
                    decSize = getSize(os.path.join(path, name.replace('.aes', '')))
                    if not '-f' in str(sys.argv) and not '--folders' in str(sys.argv):
                        print('Decrypted name:     ', name.replace('.aes', ''))
                        print('Decrypted path:     ', os.path.join(path, name.replace('.aes', '')))
                        print('Decrypted size:     ', decSize)
                        print('Key:                 "'+key+'"')
                    if logFile != '':
                        logFile.write(f'''
Decrypting:         {name}
Path:               {os.path.join(path, name)}
Size:               {size}
Decrypted name:     {name.replace('.aes', '')}
Decrypted path:     {os.path.join(path, name.replace('.aes', ''))}
Decrypted size:     {decSize}
Key:                "{key}"
''')                
                    print('Rewriting old file ...')
                    secureDelete(os.path.join(path, name))
                    result += 1
            elif '-a' in str(sys.argv) or '--all' in str(sys.argv):
                xd = print('Decrypting          ', os.path.join(path, name)) if '-f' in str(sys.argv) or '--folders' in str(sys.argv) else ''
                decrypt(os.path.join(path, name), key)
        except Exception as ex:
            print(ex)
            pass

if __name__ == '__main__':
    if '-e' in str(sys.argv) or '-d' in str(sys.argv) or '--encrypt' in str(sys.argv) or '--decrypt' in str(sys.argv):
        try:
            print(rikmaLogo)
            if '-e' in str(sys.argv) or '--encrypt' in str(sys.argv):
                if '-g' in str(sys.argv) or '--gen-keys' in str(sys.argv):
                    key = ''
                    genKeys(keys, keyLen)

                pathq = input('Path, example C:\\Users\\Admin\\Desktop, .\Desktop :\n> ') if '-o' not in str(sys.argv) and '--one-file' not in str(sys.argv) else input('Path to file, example C:\\Users\\Admin\\Desktop\\file.txt, .\\Desktop\\file.txt :\n> ')

                if '-o' not in str(sys.argv) and '--one-file' not in str(sys.argv):
                    if not os.path.exists(pathq):
                        while not os.path.exists(pathq):
                            pathq = input('Incorrect path, example C:\\Users\\Admin\\Desktop, .\Desktop :\n> ')
                            time.sleep(0.05)
                else:
                    if not os.path.isfile(pathq):
                        while True:
                            pathq = input('Incorrect file path, example C:\\Users\\Admin\\Desktop\\file.txt, .\\Desktop\\file.txt :\n> ')
                            
                            if os.path.exists(pathq) and os.path.isfile(pathq):
                                break
                            
                            time.sleep(0.05)
                
                if not '-g' in str(sys.argv) and not '--gen-keys' in str(sys.argv):
                    passq = input('Key, leave empty if you want to generate key:\n> ')

                    if passq == ' ' or passq == '':
                        lengthq = input('Length of generated key (4-256):\n> ')

                        if 4 <= int(lengthq) <= 257:
                            lengthq = lengthq
                        else:
                            lengthq = '4'

                        size = int(lengthq)
                        key = randomStr(size)
                    else:
                        key = passq
                
                if logFile != '':
                    print(f'\nCreated log file {logFile}')
                    logFile = open(logFile, 'w')
                    logFile.write(rikmaLogo)
                    logFile.write('\n{~} '+time.strftime('%a, %d %b %Y %H:%M:%S', time.gmtime(time.time()))+'\n')
                xd = print('\nEncrypting in '+pathq) if '-o' not in str(sys.argv) and '--one-file' not in str(sys.argv) else print('\nEncrypting '+pathq)
                starttime = time.time()
                encrypt(pathq, key)
                totaltime = time.time() - starttime
                print('\nTotal encrypted files: ' + str(result))
                print('Elapsed time: ' + str(totaltime))
                if logFile != '':
                    logFile.write(f'\nTotal encrypted files: {str(result)}\nElapsed time: {str(totaltime)}\n')
                    logFile.close()
            elif '-d' in str(sys.argv) or '--decrypt' in str(sys.argv):
                pathq = input('Path, example C:\\Users\\Admin\\Desktop, .\Desktop :\n> ') if '-o' not in str(sys.argv) and '--one-file' not in str(sys.argv) else input('Path to file, example C:\\Users\\Admin\\Desktop\\file.txt, .\\Desktop\\file.txt :\n> ')

                if '-o' not in str(sys.argv) and '--one-file' not in str(sys.argv):
                    if not os.path.exists(pathq):
                        while not os.path.exists(pathq):
                            pathq = input('Incorrect path, example C:\\Users\\Admin\\Desktop, .\Desktop :\n> ')
                            time.sleep(0.05)
                else:
                    if not os.path.isfile(pathq):
                        while True:
                            pathq = input('Incorrect file path, example C:\\Users\\Admin\\Desktop\\file.txt, .\\Desktop\\file.txt :\n> ')
                            
                            if os.path.exists(pathq) and os.path.isfile(pathq):
                                break
                            
                            time.sleep(0.05)

                passq = input('Key:\n> ')

                if passq != '' and passq != ' ' and len(passq) >= 0:
                    key = passq
                else:
                    while passq == '' or passq == ' ' or len(passq) <= 0:
                        passq = input('Enter valid key:\n> ')
                        time.sleep(0.05)
                    key = passq

                if logFile != '':
                    print(f'\nCreated log file {logFile}')
                    logFile = open(logFile, 'w')
                    logFile.write(rikmaLogo)
                    logFile.write('\n{~} '+time.strftime('%a, %d %b %Y %H:%M:%S', time.gmtime(time.time()))+'\n')
                print('\nDecrypting in '+pathq) if '-o' not in str(sys.argv) and '--one-file' not in str(sys.argv) else print('\nDecrypting '+pathq)
                starttime = time.time()
                decrypt(pathq, key)
                totaltime = time.time() - starttime
                print('\nTotal decrypted files: ' + str(result))
                print('Elapsed time: ' + str(totaltime))
                if logFile != '':
                    logFile.write(f'\nTotal decrypted files: {str(result)}\nElapsed time: {str(totaltime)}\n')
                    logFile.close()
        except KeyboardInterrupt:
            print('\nKeyboardInterrupt')
            exitOnException()
    else:
        if '-h' in str(sys.argv) or '--help' in str(sys.argv):
            print(rikmaLogo)
            print('''Usage: rikma.py [-h, --help] [-a, --all-folders] [-f, --folders]
                [-g, --gen-keys <keys> <length>] [-l, --log-file <file>] [-o, --one-file]
                [-e, --encrypt] [-d, --decrypt]

Required arguments:
    -e, --encrypt                   Run in encrypt mode
    -d, --decrypt                   Run in decrypt mode

Optional arguments:
    -h, --help                      Show this message
    -a, --all                       Encrypt/decrypt all files in subfolders
    -o, --one-file                  Encrypt/decrypt only one file
    -g, --gen-keys <keys> <length>  Generate <keys> key/s with length <length> chars for encrypt mode
    -f, --folders                   Show folders only
    -l, --log-file <file>           Create rikma log file''')
        else:
            print('Invalid usage, run "rikma.py --help" for details')
