# rikma
XChaCha20-Poly1305 & AES-256 (GCM) encryptor/decryptor on python🐍

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
                [--xchachapoly] [--aes]
                [--encrypt] [--decrypt]
                [--type <file/folder>] [--path <object>] [--path-file <object>]
                [--password <pass>] [--show-password] [--gen-password <len>]
                [--dnp-gen-password] [--dnw-gen-password]
                [--fast-mode]
                [--random-names]
                [--no-colors]
                [--version]

encrypt/decrypt files with xchacha20-poly1305 or aes-256 gcm cipher

options:
  -h, --help            show this help message and exit
  --xchachapoly         use xchacha20-poly1305 cipher
  --aes                 use aes-256 gcm cipher
  --encrypt             run in encrypt mode
  --decrypt             run in decrypt mode
  --type <file/folder>  type of object to encrypt/decrypt
  --path <object>       path to object for encryption/decryption
  --path-file <object>  load paths from file for encryption/decryption
  --password <pass>     password for encryption/decryption
  --show-password       dont ask for password validation, show password
  --gen-password <len>  generate password with <len> length
  --dnp-gen-password    dont print generated password
  --dnw-gen-password    dont write generated password to file
  --fast-mode           lower cpu/memory cost factor, insecure
  --random-names        rename file names to random string
  --no-colors           dont init colorama
  --version             display version and quit
```

* Run in default mode
```
$ python rikma.py
```
* Use XChaCha20-Poly1305 cipher
```
$ python rikma.py --xchachapoly
```
* Use AES-256 GCM cipher
```
$ python rikma.py --aes
```
* Run in default mode without colors
```
$ python rikma.py --no-colors
```
* Encrypt folder with generated password 8 chars length
```
$ python rikma.py --xchachapoly --encrypt --type folder --path .\folder --gen-password 8
```
* Decrypt file with specified password
```
$ python rikma.py --xchachapoly --decrypt --type file --path .\folder\file.txt.enc --password pass
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
