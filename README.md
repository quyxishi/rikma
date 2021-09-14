# rikma
aes-256 encryptor/decryptor on python🐍

<p align="center">
  <img src="https://user-images.githubusercontent.com/78678868/130137480-46a72bd3-d7ee-413d-942b-b03a8931ba87.png" width=70% height=70%>
</p>

Usage
----

```
                  .=-.-.,--.-.,-.         ___    ,---.      
      .-.,.---.  /==/_ /==/- |\  \ .-._ .'=.'\ .--.'  \     
     /==/  `   \|==|, ||==|_ `/_ //==/ \|==|  |\==\-/\ \    
    |==|-, .=., |==|  ||==| ,   / |==|,|  / - |/==/-|_\ |   
    |==|   '='  /==|- ||==|-  .|  |==|  \/  , |\==\,   - \  
    |==|- ,   .'|==| ,||==| _ , \ |==|- ,   _ |/==/ -   ,|  
    |==|_  . ,'.|==|- |/==/  '\  ||==| _ /\   /==/-  /\ - \ 
    /==/  /\ ,  )==/. /\==\ /\=\.'/==/  / / , |==\ _.\=\.-' 
    `--`-`--`--'`--`-`  `--`      `--`./  `--` `--`         

Usage: rikma.py [-h, --help] [-a, --all-folders] [-f, --folders]
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
    -l, --log-file <file>           Create rikma log file
```

* Encrypt
```
$ python rikma.py --encrypt
```
* Decrypt
```
$ python rikma.py --decrypt
```
* Encrypt/Decrypt only one file
```
$ python rikma.py --encrypt
$ python rikma.py --decrypt --one-file
```
* Encrypt/decrypt all subfolders in your path
```
$ python rikma.py --encrypt --all
$ python rikma.py --decrypt --all
```
* Encrypt with generated 3 keys with 8 chars length
```
$ python rikma.py --encrypt --gen-keys 3 8
```
* Encrypt and create log file
```
$ python rikma.py --encrypt --log-file log.txt
```
* Get help
```
$ python rikma.py --help
```
