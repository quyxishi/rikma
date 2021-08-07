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

def encrypt(path):
    global result
    for name in os.listdir(path):
        try:
            if os.path.isfile(os.path.join(path, name)):
                if '.aes' not in name:
                    print('\nEncrypting:         ', name)
                    print('Path:               ', os.path.join(path, name))
                    print('Size:               ', getSize(os.path.join(path, name)))
                    pyAesCrypt.encryptFile(os.path.join(path, name),
                                           os.path.join(path, name + '.aes'),
                                           key,
                                           bufferSize)
                    print('Encrypted name:     ', name + '.aes')
                    print('Encrypted path:     ', os.path.join(path, name + '.aes'))
                    print('Encrypted size:     ', getSize(os.path.join(path, name + '.aes')))
                    print('Key:                 "'+key+'"')
                    os.remove(os.path.join(path, name))
                    result += 1
            elif '-a' in str(sys.argv) or '--all' in str(sys.argv):
                encrypt(os.path.join(path, name))
        except Exception as ex:
            print(ex)
            pass


def decrypt(path):
    global result
    for name in os.listdir(path):
        try:
            if os.path.isfile(os.path.join(path, name)):
                if '.aes' in name:
                    print('\nDecrypting          ', name)
                    print('Path:               ', os.path.join(path, name))
                    print('Size:               ', getSize(os.path.join(path, name)))
                    pyAesCrypt.decryptFile(os.path.join(path, name),
                                           os.path.join(path, name.replace('.aes', '')),
                                           key,
                                           bufferSize)
                    print('Decrypted name:     ', name.replace('.aes', ''))
                    print('Decrypted path:     ', os.path.join(path, name.replace('.aes', '')))
                    print('Decrypted size:     ', getSize(os.path.join(path, name.replace('.aes', ''))))
                    print('Key:                 "'+key+'"')
                    os.remove(os.path.join(path, name))
                    result += 1
            elif '-a' in str(sys.argv) or '--all' in str(sys.argv):
                decrypt(os.path.join(path, name))
        except Exception as ex:
            print(ex)
            pass

if __name__ == '__main__':
    if '-e' in str(sys.argv) or '-d' in str(sys.argv) or '--encrypt' in str(sys.argv) or '--decrypt' in str(sys.argv):
        try:
            print(rikmaLogo)
            if '-e' in str(sys.argv) or '--encrypt' in str(sys.argv):
                pathq = input('Path, example C:\\Users\\Admin\\Desktop, ./Desktop :\n> ')

                if not os.path.exists(pathq):
                    while not os.path.exists(pathq):
                        pathq = input('Incorrect path, example C:\\Users\\Admin\\Desktop, ./Desktop :\n> ')
                        time.sleep(0.05)

                passq = input('Key, leave empty if you want to generate key:\n> ')

                if passq == ' ' or passq == '':
                    lengthq = input('Length of generated key (4-256):\n> ')

                    if 4 <= int(lengthq) <= 257:
                        lengthq = lengthq
                    else:
                        lengthq = '4'


                    def random_string_generator(str_size, allowed_chars):
                        return ''.join(random.choice(allowed_chars) for _ in range(str_size))


                    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&-/?@\^_|~0123456789'
                    size = int(lengthq)
                    key = random_string_generator(size, chars)
                else:
                    key = passq

                starttime = time.time()
                encrypt(pathq)
                totaltime = time.time() - starttime
                print('\nTotal encrypted files: ' + str(result))
                print('Estimated time: ' + str(totaltime))
            elif '-d' in str(sys.argv) or '--decrypt' in str(sys.argv):
                pathq = input('Path, example C:\\Users\\Admin\\Desktop, ./Desktop :\n> ')

                if not os.path.exists(pathq):
                    while not os.path.exists(pathq):
                        pathq = input('Incorrect path, example C:\\Users\\Admin\\Desktop, ./Desktop :\n> ')
                        time.sleep(0.05)

                passq = input('Key:\n> ')

                if passq != '' and passq != ' ' and len(passq) >= 0:
                    key = passq
                else:
                    while passq == '' or passq == ' ' or len(passq) <= 0:
                        passq = input('Enter valid key:\n> ')
                        time.sleep(0.05)
                    key = passq

                starttime = time.time()
                decrypt(pathq)
                totaltime = time.time() - starttime
                print('\nTotal decrypted files: ' + str(result))
                print('Estimated time: ' + str(totaltime))
        except KeyboardInterrupt:
            print('\nKeyboardInterrupt')
            quit()
    else:
        if '-h' in str(sys.argv) or '--help' in str(sys.argv):
            print('''
Usage: rikma.py [-h, --help] [-a, --all-folders]
                [-e, --encrypt] [-d, --decrypt]

Optional arguments:
    -h, --help          Show this message
    -e, --encrypt       Run in encrypt mode
    -d, --decrypt       Run in decrypt mode
    -a, --all           Encrypt/decrypt all files in folders in your path''')
        else:
            print('Invalid usage, run "rikma.py --help" for details')
