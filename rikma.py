import os
import pyAesCrypt
import random
import sys
import humanize
import time

bufferSize = 512 * 1024
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
                if name != 'desktop.ini' and '.aes' not in name:
                    print('\nEncrypting: ', name)
                    print('Path: ', os.path.join(path, name))
                    print('Size: ', getSize(os.path.join(path, name)))
                    pyAesCrypt.encryptFile(os.path.join(path, name),
                                           os.path.join(path, name + '.aes'),
                                           key,
                                           bufferSize)
                    print('Encrypted name: ', name + '.aes')
                    print('Encrypted path: ', os.path.join(path, name + '.aes'))
                    print('Encrypted size: ', getSize(os.path.join(path, name + '.aes')))
                    print('Key: ', key)
                    os.remove(os.path.join(path, name))
                    result += 1
            else:
                if 'desktop.ini' not in os.path.join(path, name):
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
                    print('\nDecrypting ', name)
                    print('Path: ', os.path.join(path, name))
                    print('Size: ', getSize(os.path.join(path, name)))
                    pyAesCrypt.decryptFile(os.path.join(path, name),
                                           os.path.join(path, name.replace('.aes', '')),
                                           key,
                                           bufferSize)
                    print('Decrypted name: ', name.replace('.aes', ''))
                    print('Decrypted path: ', os.path.join(path, name.replace('.aes', '')))
                    print('Decrypted size: ', getSize(os.path.join(path, name.replace('.aes', ''))))
                    print('Key: ', key)
                    os.remove(os.path.join(path, name))
                    result += 1
            else:
                if 'desktop.ini' not in os.path.join(path, name):
                    decrypt(os.path.join(path, name))
        except Exception as ex:
            print(ex)
            pass

if __name__ == '__main__':
    if '-e' in str(sys.argv) or '-d' in str(sys.argv) or '--encrypt' in str(sys.argv) or '--decrypt' in str(sys.argv):
        print(rikmaLogo)
        if '-e' in str(sys.argv) or '--encrypt' in str(sys.argv):
            pathq = input('Path, example C:\\Users\\Admin\\Desktop:\n> ')
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
            pathq = input('Path, example C:\\Users\\Admin\\Desktop:\n> ')
            passq = input('Key:\n> ')

            if passq != '' or passq != '':
                print(passq)
                key = passq
            else:
                print('Enter valid key:\n> ')

            starttime = time.time()
            decrypt(pathq)
            totaltime = time.time() - starttime
            print('\nTotal decrypted files: ' + str(result))
            print('Estimated time: ' + str(totaltime))
    else:
        print('''
Usage: rikma.py [-e, --encrypt] [-d, --decrypt]''')
