import os
import pyAesCrypt
import random
import sys
import humanize
import time

bufferSize = 128 * 1024
result = 0

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

def getSize(file):
    st = os.stat(file).st_size
    return humanize.naturalsize(st)

def randomStr(str_size):
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&-/?@\^_|~0123456789') for _ in range(str_size))

def encrypt(path, key):
    global result
    for name in os.listdir(path):
        try:
            if os.path.isfile(os.path.join(path, name)):
                if '.aes' not in name:
                    if not '-f' in str(sys.argv) and not '--folders' in str(sys.argv):
                        print('\nEncrypting:         ', name)
                        print('Path:               ', os.path.join(path, name))
                        print('Size:               ', getSize(os.path.join(path, name)))
                    key = randomStr(int(lengthq)) if '-g' in str(sys.argv) or '--gen-each' in str(sys.argv) else key
                    pyAesCrypt.encryptFile(os.path.join(path, name),
                                        os.path.join(path, name + '.aes'),
                                        key,
                                        bufferSize)
                    if not '-f' in str(sys.argv) and not '--folders' in str(sys.argv):
                        print('Encrypted name:     ', name + '.aes')
                        print('Encrypted path:     ', os.path.join(path, name + '.aes'))
                        print('Encrypted size:     ', getSize(os.path.join(path, name + '.aes')))
                        print('Key:                 "'+key+'"')
                    os.remove(os.path.join(path, name))
                    result += 1
            elif '-a' in str(sys.argv) or '--all' in str(sys.argv):
                xd = print('Encrypting          ', os.path.join(path, name)) if '-f' in str(sys.argv) or '--folders' in str(sys.argv) else ''
                encrypt(os.path.join(path, name), key)
        except Exception as ex:
            print(ex)
            pass


def decrypt(path, key):
    global result
    for name in os.listdir(path):
        try:
            if os.path.isfile(os.path.join(path, name)):
                if '.aes' in name:
                    if not '-f' in str(sys.argv) and not '--folders' in str(sys.argv):
                        print('\nDecrypting          ', name)
                        print('Path:               ', os.path.join(path, name))
                        print('Size:               ', getSize(os.path.join(path, name)))
                    pyAesCrypt.decryptFile(os.path.join(path, name),
                                           os.path.join(path, name.replace('.aes', '')),
                                           key,
                                           bufferSize)
                    if not '-f' in str(sys.argv) and not '--folders' in str(sys.argv):
                        print('Decrypted name:     ', name.replace('.aes', ''))
                        print('Decrypted path:     ', os.path.join(path, name.replace('.aes', '')))
                        print('Decrypted size:     ', getSize(os.path.join(path, name.replace('.aes', ''))))
                        print('Key:                 "'+key+'"')
                    os.remove(os.path.join(path, name))
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
                pathq = input('Path, example C:\\Users\\Admin\\Desktop, .\Desktop :\n> ')

                if not os.path.exists(pathq):
                    while not os.path.exists(pathq):
                        pathq = input('Incorrect path, example C:\\Users\\Admin\\Desktop, .\Desktop :\n> ')
                        time.sleep(0.05)
                
                if not '-g' in str(sys.argv) and not '--gen-each' in str(sys.argv):
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
                else:
                    lengthq = input('Length of generated keys (4-256):\n> ')

                    if 4 <= int(lengthq) <= 257:
                        lengthq = lengthq
                    else:
                        lengthq = '4'

                print('\nEncrypting in '+pathq)
                starttime = time.time()
                encrypt(pathq, key)
                totaltime = time.time() - starttime
                print('\nTotal encrypted files: ' + str(result))
                print('Elapsed time: ' + str(totaltime))
            elif '-d' in str(sys.argv) or '--decrypt' in str(sys.argv):
                pathq = input('Path, example C:\\Users\\Admin\\Desktop, .\Desktop :\n> ')

                if not os.path.exists(pathq):
                    while not os.path.exists(pathq):
                        pathq = input('Incorrect path, example C:\\Users\\Admin\\Desktop, .\Desktop :\n> ')
                        time.sleep(0.05)

                passq = input('Key:\n> ')

                if passq != '' and passq != ' ' and len(passq) >= 0:
                    key = passq
                else:
                    while passq == '' or passq == ' ' or len(passq) <= 0:
                        passq = input('Enter valid key:\n> ')
                        time.sleep(0.05)
                    key = passq

                print('\nDecrypting in '+pathq)
                starttime = time.time()
                decrypt(pathq, key)
                totaltime = time.time() - starttime
                print('\nTotal decrypted files: ' + str(result))
                print('Elapsed time: ' + str(totaltime))
        except KeyboardInterrupt:
            print('\nKeyboardInterrupt')
            quit()
    else:
        if '-h' in str(sys.argv) or '--help' in str(sys.argv):
            print('''
Usage: rikma.py [-h, --help] [-a, --all-folders] [-g, --gen-each] [-f, --folders]
                [-e, --encrypt] [-d, --decrypt]

Optional arguments:
    -h, --help          Show this message
    -e, --encrypt       Run in encrypt mode
    -d, --decrypt       Run in decrypt mode
    -a, --all           Encrypt/decrypt all files in subfolders in your path
    -g, --gen-each      Generate new key for each file in encrypt mode
    -f, --folders       Show folders only''')
        else:
            print('Invalid usage, run "rikma.py --help" for details')
