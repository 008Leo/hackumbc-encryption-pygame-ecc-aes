import socket
import ssl
import threading
import os
import sys
import getpass
from termcolor import colored
from time import sleep
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import subprocess
if os.name == 'nt':
    from colorama import init
    init()
import bcrypt
from threading import Thread
key = ""
if not os.path.exists("hash.hash") and os.path.exists('key.key'):
    dk = getpass.getpass('Create password to encrypt key.key:')
    dk = str(dk)
    with open('key.key', 'r') as f:
        plain = f.read()
    salt = (dk.encode('utf-8')[:16] + b'\0' * 16)[:16]
    kfc = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
)
    
    c = Cipher(algorithms.AES(kfc.derive(dk.encode())), modes.CTR(salt))
    ee = c.encryptor()
    ed = (ee.update(plain.encode('utf-8')) + ee.finalize())
    with open ('hash.hash', 'wb') as f1:
        f1.write(bcrypt.hashpw(dk.encode('utf-8'),bcrypt.gensalt())) 
    with open ('key.key','wb') as f2:
        f2.write(ed) 
    del dk,salt,kfc,f,c,ee,ed

hhash = b''
with open('hash.hash', 'rb') as r1:
    hhash = r1.read()
dckey = getpass.getpass('Enter password to decrypt key.key:')
dckey = str(dckey)
check = bcrypt.checkpw(dckey.encode('utf-8'), hhash)
if(check == False):
    print("Password incorrect")
    exit()
CURVE = ec.SECP256R1()
ECC_PRIVATE_KEY = ec.generate_private_key(CURVE)
ECC_PUBLIC_KEY = ECC_PRIVATE_KEY.public_key()
GENOME = (dckey.encode('utf-8')[:16] + b'\0' * 16)[:16]
a = 0
def derive_key(password: str):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=GENOME,
        iterations=100000
    )    
    return kdf.derive(password.encode())
def DHKEYGEN(password,gen):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=gen,
        iterations=100000
    )
    return(kdf.derive(password))
def decrypt_from_file(file,pa):
    key = derive_key(pa)
    with open(file, 'rb') as file:
        data = file.read()
    ct = data
    c = Cipher(algorithms.AES(key), modes.CTR(GENOME))
    d = c.decryptor()
    return (d.update(ct) + d.finalize()).decode()
LOCK = Fernet(decrypt_from_file('key.key',dckey).encode('utf-8'))
del dckey, GENOME, derive_key, decrypt_from_file
VAULT = Fernet(Fernet.generate_key())
def AES_file_encrypt(name,k,iv):
    c = Cipher(algorithms.AES(k), modes.CTR(iv))
    e = c.encryptor()
    a = b''
    with open(name,'rb') as f:
        a = f.read()
    return (e.update(a)+e.finalize())
def AES_byte_encrypt(b,k,iv):
    c = Cipher(algorithms.AES(k), modes.CTR(iv))
    ct = c.encryptor()
    if type(b) is bytes:
        return(ct.update(b) + ct.finalize())
    if type(b) is str:
        return(ct.update(b.encode('utf-8'))+ct.finalize())
def AES_byte_decrypt(cd,k,iv,t):
    c = Cipher(algorithms.AES(k), modes.CTR(iv))
    d = c.decryptor()
    if t == "bytes":
        return (d.update(cd) + d.finalize())
    elif t == "str":
        return (d.update(cd) + d.finalize()).decode()
keys = {}
ret = ""
downloads = {}
ivs = {}
result = ""
def send_message(sock):
    while True:
        message = input()
        if(message.startswith("offlinegame")):
            gm = message.split()[1]
            if(gm == "cf"):
                os.system('start cmd /K "python conflip.py"')
            elif(gm == "numguess"):
                os.system('start cmd /K "python number_guesser.py')
            elif(gm == "blackjack"):
                os.system('start cmd /K "python blackjack.py')
            elif(gm == "fighter"):
                os.system('start cmd /K "python main.py')
        elif(message == 'q'):
            secure_sock.close()
            sys.exit()
        elif(message == 'list' or message == 'user' or message == 'name'):
            sock.sendall(message.encode('utf-8'))
        elif(message.startswith('msg ') or message.startswith("w ") or message.startswith("send ") or message.startswith("r ")):
            to = message.split()[1]
            if message.startswith('r '):
                to = ret
                message = f'A {message}'
            k = b""
            iv = b''
            if(to):
                if to not in keys:
                    sock.sendall(b"KEY")
                    sleep(0.01)
                    sock.sendall(to.encode('utf-8'))
                    sleep(0.01)
                    sock.sendall(ECC_PUBLIC_KEY.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo))
                    while to not in keys:
                        sleep(0.25)
                if (message.split()[2] == "game"):
                    if (message.split()[3] == "rps"):
                        other_usr_id = message.split()[1]
                        print(f"Sent {message.split()[1]} a game request.")
                        sock.sendall(b"STARTGAME")
                        sleep(0.01)
                        sock.sendall(to.encode('utf-8'))
                        while result == "":
                            sleep(0.25)
                        if result == "n":
                            continue
                        result = ""
                        proc = subprocess.Popen(
                            ['python3', 'RockPaperScissors.py'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            text=True  # Makes stdin and stdout text-based streams
                        )
                        sent = 0
                        while True:
                            # Read a line of output from the other script
                            if (sent == 0):
                                output_line = proc.stdout.readline().strip()
                                input_data = input(output_line)
                                proc.stdin.write(input_data + "\n")
                                sent = 1
                                proc.stdin.flush()
                            output_line = proc.stdout.readline().strip()
                            if not output_line and proc.poll() is not None:
                                break
                            if output_line:
                                if (output_line.startswith("RESULT:")):
                                    print(output_line)
                                    o_l = proc.stdout.readline().strip()
                                    sock.sendall(AES_byte_encrypt(output_line),VAULT.decrypt(keys[other_usr_id],ttl=None),VAULT.decrypt(ivs[other_usr_id]))
                                    sent = 0
                                    ask = input("Would you like to play again? y/n")
                                    if (ask == "y"):
                                        print("Asking other user. Please wait...")
                                        sock.sendall(AES_byte_encrypt("Would you like to play again? y/n",VAULT.decrypt(keys[other_usr_id]),VAULT.decrypt(ivs[other_usr_id])))
                                        while result == "":
                                            sleep(0.25)
                                        if result == "n":
                                            proc.terminate()
                                            break
                                        result = ""
                                        sock.sendall(AES_byte_encrypt(output_line),VAULT.decrypt(keys[other_usr_id],VAULT.decrypt(ivs[other_usr_id])))
                                    else:
                                        proc.terminate()
                                        break
                                else:
                                    print("Other user is deciding. Please wait...")
                                    sock.sendall(AES_byte_encrypt(output_line),VAULT.decrypt(keys[other_usr_id],VAULT.decrypt(ivs[other_usr_id])))
                                    while result == "":
                                        sleep(0.25)
                                    proc.stdin.write(result + "\n")
                                    proc.stdin.flush()
                                    result = ""

                                    

                else:    
                    sleep(0.05)
                    sock.sendall(b"MAIL")
                    sleep(0.01)
                    sock.sendall(to.encode('utf-8'))
                    sleep(0.01)
                    sock.sendall(LOCK.encrypt(AES_byte_encrypt(' '.join(message.split()[2:]), VAULT.decrypt(keys[to]), VAULT.decrypt(ivs[to]))))
                    del k,iv
        else: 
            sock.sendall(LOCK.encrypt(message.encode('utf-8')))

host = '(REDACTED)'
context = ssl.create_default_context()
context.load_verify_locations('cert.pem')
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_sock = context.wrap_socket(client_socket, server_hostname=host)
secure_sock.connect((host, 12345))
threading.Thread(target=send_message, args=(secure_sock,)).start()
print(colored("Connected","light_green"))
result = ""
nam = secure_sock.recv().decode('utf-8')
print(f"Username: {colored(nam,'light_green')}")
while True:
    data = secure_sock.recv()
    if data == b"KEYBACK":
        tto = secure_sock.recv().decode('utf-8')
        kdf_salt = secure_sock.recv()
        ecc_key = secure_sock.recv()
        aes_iv = secure_sock.recv()
        slat = LOCK.decrypt(kdf_salt,ttl=None)
        keys[tto] = VAULT.encrypt(DHKEYGEN(ECC_PRIVATE_KEY.exchange(ec.ECDH(), serialization.load_pem_public_key(ecc_key)),slat))
        ivs[tto] = VAULT.encrypt(LOCK.decrypt(aes_iv,ttl=None))
    elif data == b"MESSAGE":
        suser = secure_sock.recv().decode('utf-8')
        rata = secure_sock.recv()
        print(f"{suser}: {LOCK.decrypt(rata,ttl=None).decode('utf-8')}")
        del rata
    elif data == b"KEY":
        fr = secure_sock.recv().decode('utf-8')
        init = LOCK.encrypt(os.urandom(16))
        aaaa = secure_sock.recv()
        aaac = serialization.load_pem_public_key(aaaa)
        keys[fr] = VAULT.encrypt(DHKEYGEN(ECC_PRIVATE_KEY.exchange(ec.ECDH(), aaac),LOCK.decrypt(init)))
        iv = LOCK.encrypt(os.urandom(16))
        ivs[fr] = VAULT.encrypt(LOCK.decrypt(iv))
        PUBLICKEY = ECC_PUBLIC_KEY.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)
        secure_sock.sendall(b"KEYBACK")
        sleep(0.01)
        secure_sock.sendall(fr.encode('utf-8'))
        sleep(0.03)
        secure_sock.sendall(init)
        sleep(0.03)
        secure_sock.sendall(PUBLICKEY)
        sleep(0.03)
        secure_sock.sendall(iv)
    elif data == b"STARTGAME":
        other_usr = secure_sock.recv().decode('utf-8')
        while True:
            decrypted = ""
            a = secure_sock.recv().decode('utf-8')
            if(a.startswith("PLAIN: ")):
                decrypted = ' '.join(a.split()[1:])
            else:
                decrypted = AES_byte_decrypt(a,VAULT.decrypt(keys[other_usr],ttl=None), VAULT.decrypt(ivs[other_usr],ttl=None),'str')
            print(decrypted)
            inpp = input()
            if(a.startswith("PLAIN:")) and (inpp == "y" or inpp == "n"):
                secure_sock.sendall(id.encode('utf-8'))
                sleep(0.01)
                secure_sock.sendall(inpp.encode('utf-8'))
            else:
                secure_sock.sendall(AES_byte_encrypt(inpp),VAULT.decrypt(keys[other_usr],ttl=None),VAULT.decrypt(ivs[other_usr],ttl=None))
    elif data == b"GAMEDATA":
        decrypted = ""
        usrs_id = secure_sock.recv().decode('utf-8')
        from_usr = secure_sock.recv()
        if (from_usr.decode('utf-8') == "y" or from_usr.decode('utf-8') == "n"):
            result = from_usr.decode('utf-8')
        decrypted = AES_byte_decrypt(from_usr,VAULT.decrypt(keys[usrs_id],ttl=None),VAULT.decrypt(ivs[usrs_id],ttl=None),'str')
        if decrypted == 'QUIT':
            result = "QUIT"
        else:
            result = decrypted
        print(decrypted
    elif data == b"MAIL":
        frm = secure_sock.recv().decode('utf-8')
        mail = secure_sock.recv()
        print(f"{colored('-->', 'light_green')} {colored(frm,'magenta')}: {AES_byte_decrypt(LOCK.decrypt(mail, ttl=None), VAULT.decrypt(keys[frm],ttl=None), VAULT.decrypt(ivs[frm],ttl=None), 'str')}")
        ret = frm
        del mail
    elif data == b'DEL':
        ff = secure_sock.recv().decode('utf-8')
        if ff in keys:
            del keys[ff]
    elif data:
        print(data)
    else:
        print(colored("Disconnected from server","light_red"))
        exit()
