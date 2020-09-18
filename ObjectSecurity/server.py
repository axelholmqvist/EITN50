import socket
import time
import threading
import pickle
import random
import string
import base64
from Crypto.Cipher import AES

'''
https://pythontic.com/modules/socket/udp-client-server-example?fbclid=IwAR2fbrVyX4wloO4sbGrWv5CzNJX1tZk6ydcTEapxvbLhX2ejh3sPJVsaZEA
https://www.youtube.com/watch?v=3QiPPX-KeSc
https://blog.ruanbekker.com/blog/2018/04/30/encryption-and-decryption-with-the-pycrypto-module-using-the-aes-cipher-in-python/
'''

LOCAL_IP = "127.0.0.1"
LOCAL_PORT = 20002

BUFFER_SIZE = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!disconnect"

UDP_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UDP_server_socket.bind((LOCAL_IP, LOCAL_PORT))

def generate_DH_values():
    P = 23
    G = 9
    a = 4
    x = int(pow(G, a, P))
    return P, G, a, x

def generate_DH_secret(y, a, P):
    secret = int(pow(y, a, P))
    return secret

def handshake(UDP_client_socket, address):
    # Diffie Hellman secret
    P, G, a, x = generate_DH_values()
    UDP_client_socket.send("Initializing handshake...".encode(FORMAT))
    time.sleep(1)
    UDP_client_socket.send(f"{P}".encode(FORMAT))
    time.sleep(0.5)
    UDP_client_socket.send(f"{G}".encode(FORMAT))
    time.sleep(0.5)
    UDP_client_socket.send(f"{x}".encode(FORMAT))
    y = int(UDP_client_socket.recv(2048).decode(FORMAT))
    print(f"\n[{address[0]}:{address[1]}] y: {y}")
    secret = generate_DH_secret(y, a, P)
    print(f"\nSecret: {secret}")
    
    # AES Encryption Key and IV
    key = str(secret).zfill(32)
    print(f"\nKey: {key}")

    iv = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))
    print(f"\nIV: {iv}")

    UDP_client_socket.send(f"{iv}".encode(FORMAT))

    return key, iv

def decrypt(encrypted_message, key, iv):
    decryption_suite = AES.new(key, AES.MODE_CFB, iv)
    decrypted_message = decryption_suite.decrypt(base64.b64decode(encrypted_message))
    return decrypted_message.decode(FORMAT)

def client_handler(UDP_client_socket, address):
    print(f"\n[NEW CONNECTION] {address[0]}:{address[1]} has connected.")

    key, iv = handshake(UDP_client_socket, address)

    connected = True
    while connected:
        message = UDP_client_socket.recv(BUFFER_SIZE)
        decrypted_message = decrypt(message, key, iv)

        if decrypted_message == DISCONNECT_MESSAGE:
            connected = False

        print(f"\n[{address[0]}:{address[1]}] {decrypted_message}")

    UDP_client_socket.close()

def start():
    time.sleep(1)
    UDP_server_socket.listen(BUFFER_SIZE)
    print(f"[RUNNING] Server is up and running on {LOCAL_IP}: {LOCAL_PORT}")
    while True:
        UDP_client_socket, address = UDP_server_socket.accept()
        thread = threading.Thread(target=client_handler, args=(UDP_client_socket, address))
        thread.start()
        print(f"[CONNECTIONS] {threading.active_count() - 1} active connection(s)")

print('\n[STARTING] Server is starting...')
start()







'''
[ ] work on the principle of object security,
[ ] provide integrity, confidentiality, and replay protection,
[X] use UDP as the way to exchange data between the two parties (sending and receiving
party),
[ ] work on the principle of forward security,
[ ] should have at least two distinct parts; handshake and (protected) data exchange,
[ ] actually work when we test it. The data packets should by small as one can expect
for small IoT devices, say max 64 bytes,

Examples of useful cryptography libraries are
• PyCrypto or cryptography when you program in python.
'''