# rikma
aes-256 (GCM) encryptor/decryptor on python🐍

<p align="center">
  <img src="https://user-images.githubusercontent.com/78678868/156518487-10021ef5-02a6-4f20-9fc1-64761bc3dcb1.gif" width=70% height=70%>
</p>

Usage
----

```
         \                     
 .___  ` |   , , _ , _     ___ 
 /   \ | |  /  |' `|' `.  /   `
 |   ' | |-<   |   |   | |    |
 /     / /  \_ /   '   / `.__/|
 
 
usage: rikma.py [-h, --help]
                [--encrypt] [--decrypt]
                [--type <file/folder>] [--path <object>]
                [--password <pass>] [--gen-password <len>]
                [--dnp-gen-password] [--dnw-gen-password]
                [--no-colors]
                [--version]

encrypt/decrypt files with aes-256 encryption

options:
  -h, --help            show this help message and exit
  --encrypt             run in encrypt mode
  --decrypt             run in decrypt mode
  --type <file/folder>  type of object to encrypt/decrypt
  --path <object>       path to object for encryption/decryption
  --password <pass>     password for encryption/decryption
  --gen-password <len>  generate password with <len> length
  --dnp-gen-password    dont print generated password
  --dnw-gen-password    dont write generated password to file
  --no-colors           dont init colorama
  --version             display version and quit
```

* Run in default mode
```
$ python rikma.py
```
* Run in default mode without colors
```
$ python rikma.py --no-colors
```
* Encrypt folder with generated password 8 chars length
```
$ python rikma.py --encrypt --type folder --path .\folder --gen-password 8
```
* Decrypt file with specified password
```
$ python rikma.py --decrypt --type file --path .\folder\file.txt.enc --password pass
```
* Dont print generated password
```
$ python rikma.py --gen-password 256 --dnp-gen-password
```
* Dont write to file generated password
```
$ python rikma.py --gen-password 256 --dnw-gen-password
```
* Display version
```
$ python rikma.py --version
```
* Get help
```
$ python rikma.py --help
```
