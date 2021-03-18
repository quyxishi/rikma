import os
import pyAesCrypt
import random

bufferSize = 512 * 1024
result = 0


def encrypt(path):
    global result
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            if name != "desktop.ini" and ".enc" not in name:
                print("\nEncrypting: ", name)
                print("Path: ", os.path.join(path, name))
                pyAesCrypt.encryptFile(os.path.join(path, name),
                                       os.path.join(path, name + ".enc"),
                                       key,
                                       bufferSize)
                print("Encrypted name: ", name + ".enc")
                print("Encrypted path: ", os.path.join(path, name + ".enc"))
                print("Key: ", key)
                os.remove(os.path.join(path, name))
                result += 1
        else:
            if os.path.join(path, name) != "C:\Windows" and "desktop.ini" not in os.path.join(path, name):
                encrypt(os.path.join(path, name))


def decrypt(path):
    global result
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            if ".enc" in name:
                print("\nDecrypting ", name)
                print("Path: ", os.path.join(path, name))
                pyAesCrypt.decryptFile(os.path.join(path, name),
                                       os.path.join(path, name.replace(".enc", "")),
                                       key,
                                       bufferSize)
                print("Decrypted name: ", name.replace(".enc", ""))
                print("Decrypted path: ", os.path.join(path, name.replace(".enc", "")))
                print("Key: ", key)
                os.remove(os.path.join(path, name))
                result += 1
        else:
            if os.path.join(path, name) != "C:\Windows" and "desktop.ini" not in os.path.join(path, name):
                decrypt(os.path.join(path, name))


print(""" 
                  .=-.-.,--.-.,-.         ___    ,---.      
      .-.,.---.  /==/_ /==/- |\  \ .-._ .'=.'\ .--.'  \     
     /==/  `   \|==|, ||==|_ `/_ //==/ \|==|  |\==\-/\ \    
    |==|-, .=., |==|  ||==| ,   / |==|,|  / - |/==/-|_\ |   
    |==|   '='  /==|- ||==|-  .|  |==|  \/  , |\==\,   - \  
    |==|- ,   .'|==| ,||==| _ , \ |==|- ,   _ |/==/ -   ,|  
    |==|_  . ,'.|==|- |/==/  '\  ||==| _ /\   /==/-  /\ - \ 
    /==/  /\ ,  )==/. /\==\ /\=\.'/==/  / / , |==\ _.\=\.-' 
    `--`-`--`--'`--`-`  `--`      `--`./  `--` `--`         
""")
pickq = input("{~} Menu:\n1) Encrypt\n2) Decrypt\n> ")
if pickq == "1":
    pathq = input("Path, example C:\\Users\\Admin\\Desktop:\n> ")
    passq = input("Key, leave empty if you want to generate key:\n> ")

    if passq == " " or passq == "":
        lengthq = input("Length of generated key (4-256):\n> ")

        if 4 <= int(lengthq) <= 257:
            lengthq = lengthq
        else:
            lengthq = "4"


        def random_string_generator(str_size, allowed_chars):
            return ''.join(random.choice(allowed_chars) for _ in range(str_size))


        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&-/?@\^_|~0123456789"
        size = int(lengthq)
        key = random_string_generator(size, chars)
    else:
        key = passq

    try:
        encrypt(pathq)
        print("\nTotal encrypted files: " + str(result))
    except Exception as ex:
        print(ex)
elif pickq == "2":
    pathq = input("Path, example C:\\Users\\Admin\\Desktop:\n> ")
    passq = input("Key:\n> ")

    if passq != "" or passq != "":
        print(passq)
        key = passq
    else:
        print("Enter valid key:\n> ")

    try:
        decrypt(pathq)
        print("\nTotal decrypted files: " + str(result))
    except Exception as ex:
        print(ex)
