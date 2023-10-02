import socket
import ssl
import threading
import numpy as np
from termcolor import colored
from time import sleep
from threading import Thread
import ast
# Initialize socket
exit()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = '0.0.0.0'
port = 12345

server_socket.bind((host, port))
server_socket.listen(24)

# Wrap socket with SSL
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem') #If viewing on GitHub: you must create your own keys.
def client_thread(conn,id,addr):
    id = f'{id:x}'
    conn.send(id.encode('utf-8'))
    while True:
        try:
            message = conn.recv()
            if not message:
                clients.remove(client)
                ids.remove(id)
                conn.close()
                print(f"{colored('(-)','light_red')} {addr}")
                for client in clients:
                    try:
                        if client != conn:
                            client.sendall("del".encode('utf-8'))
                            sleep(0.01)
                            client.sendall(id.encode('utf-8'))
                    except:
                        clients.remove(client)
                break
            if(message.decode('utf-8') == 'user' or message.decode('utf-8') == 'name'):
                conn.sendall(id.encode('utf-8'))
            elif(message == b"STARTGAME"):
                other_player = conn.recv().decode('utf-8')
                other_dest = clids[other_player]
                other_dest.sendall(b"STARTGAME")
                sleep(0.01)
                other_dest.sendall(id.encode('utf-8'))
                sleep(0.01)
                other_dest.sendall(f"PLAIN: {id} wants to play RPS! Type n to decline, or anything else to accept.".encode('utf-8'))
                other_id = other_dest.recv()
                y_or_n = other_dest.recv()
                conn.sendall(b"GAMEDATA")
                sleep(0.01)
                conn.sendall(other_id)
                sleep(0.01)
                conn.sendall(y_or_n)
                while True:
                    #other_dest.sendall(b"GAMEDATA")
                    #sleep(0.01)
                    other_dest.sendall("PLAIN: Other user is deciding. Please wait.".encode('utf-8'))
                    msg2 = conn.recv()
                    #other_dest.sendall(b'GAMEDATA')
                    #sleep(0.01)
                    other_dest.sendall(msg2)
                    other_response = other_dest.recv()
                    conn.sendall(b"GAMEDATA")
                    sleep(0.01)
                    conn.sendall(other_response)

            elif (message.decode('utf-8') == 'list' or message.decode('utf-8') == 'l'):
                conn.sendall((f"There are currently {len(ids)} users online: {', '.join(ids)}").encode('utf-8'))
            elif (message == b"KEY"):
                to = conn.recv().decode('utf-8')
                if to not in ids:
                    continue
                k = conn.recv()
                recp = clids[to]
                recp.sendall(b"KEY")
                sleep(0.01)
                recp.sendall(id.encode('utf-8')) 
                sleep(0.1)
                recp.sendall(k)
                print(f"{id} {colored('-->', 'light_green')} {to} {colored('(ECDH-256)', 'light_magenta')}")
            elif (message == b"KEYBACK"):
                home = conn.recv().decode('utf-8')
                if home not in ids:
                    continue
                sa = conn.recv()
                ky = conn.recv()
                iv = conn.recv()
                dest = clids[home]
                dest.sendall(b"KEYBACK")
                sleep(0.01)
                dest.sendall(id.encode('utf-8'))
                sleep(0.01)
                dest.sendall(sa)
                sleep(0.01)
                dest.sendall(ky)
                sleep(0.01)
                dest.sendall(iv)
                print(f"{id} {colored('-->', 'light_green')} {home} {colored('(ECDH)', 'light_magenta')} (PublicKey: {ky.decode('utf-8')})")
            elif (message == b"MAIL"):
                t = conn.recv().decode('utf-8')
                if t not in ids:
                    continue
                mes = conn.recv()
                rec = clids[t]
                rec.sendall(b"MAIL")
                sleep(0.01)
                rec.sendall(id.encode('utf-8')) 
                sleep(0.01)
                rec.sendall(mes)
                print(f"{id} {colored('-->', 'light_green')} {t} {colored('[...]', 'red')}")
            else:
                print(f"{id}: [...] {colored('(Fernet)', 'light_magenta')}")

            # Broadcast message to all connected clients
                for client in clients:
                    try:
                        if client != conn:
                            client.sendall(b"MESSAGE")
                            sleep(0.01)
                            client.sendall(id.encode('utf-8'))
                            sleep(0.01)
                            client.sendall(message)
                            
                    except:
                        clients.remove(client)
        except Exception as e:
            clients.remove(conn)
            ids.remove(f'{id}')
            conn.close()
            print(f"{colored('(-)','light_red')} {addr}")
            for client in clients:
                try:
                    if client != conn:
                        client.sendall("del".encode('utf-8'))
                        sleep(0.01)
                        client.sendall(id.encode('utf-8'))
                except:
                    clients.remove(client)            
            break

clients = []
ids = []
clids = {}
while True:
    try:
        client_socket, addr = server_socket.accept()
        conn = context.wrap_socket(client_socket, server_side=True)
    except ssl.SSLError as e:
        print(f"SSL error: {e}")
        continue
    except Exception as e:
        print(f"error: {e}")
        continue
    username = np.random.randint(0x10000,0xFFFFF)
    print(f"{colored('(+)','light_green')} {addr} (Username: {username:x})")
    clients.append(conn)
    clids[f'{username:x}'] = conn
    ids.append(f'{username:x}')
    threading.Thread(target=client_thread, args=(conn,username,addr)).start()
