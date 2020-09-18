import socket
import time
import threading
import pickle
import random
import string
import base64
from Crypto.Cipher import AES

LOCAL_IP = "127.0.0.1"
LOCAL_PORT = 20002

BUFFER_SIZE = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!disconnect"

UDP_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UDP_client_socket.connect((LOCAL_IP, LOCAL_PORT))

def generate_DH_values(P, G, x):
    b = random.randint(9999, 99999)
    y = int(pow(G, b, P))
    return b, y

def generate_DH_secret(x, b, P):
    secret = int(pow(x, b, P))
    return secret

def handshake():
    # Diffie Hellman secret
    print(f"\n[SERVER] {UDP_client_socket.recv(2048).decode(FORMAT)}")
    P = int(UDP_client_socket.recv(2048).decode(FORMAT))
    G = int(UDP_client_socket.recv(2048).decode(FORMAT))
    x = int(UDP_client_socket.recv(2048).decode(FORMAT))
    print(f"\n[SERVER] P: {P}, G: {G}, x: {x}")
    b, y = generate_DH_values(P, G, x)
    UDP_client_socket.send(f"{y}".encode(FORMAT))
    secret = generate_DH_secret(x, b, P)
    print(f"\nSecret: {secret}")

    # AES Encryption Key and IV
    key = str(secret).zfill(32)
    print(f"\nKey: {key}")

    iv = UDP_client_socket.recv(2048).decode(FORMAT)
    print(f"\nIV: {iv}")

    return key, iv

def encrypt(message, key, iv):
    encryption_suite = AES.new(key, AES.MODE_CFB, iv)
    encrypted_message = encryption_suite.encrypt(message)
    encoded_encrypted_message = base64.b64encode(encrypted_message)
    return encoded_encrypted_message

def decrypt(encrypted_message, key, iv):
    decryption_suite = AES.new(key, AES.MODE_CFB, iv)
    decrypted_message = decryption_suite.decrypt(base64.b64decode(encrypted_message))
    return decrypted_message

def send(message):
    UDP_client_socket.send(encrypt(message, key, iv))

key, iv = handshake()

while True:
    input_message = input('\nSend message: ')
    send(input_message)
    if input_message == DISCONNECT_MESSAGE:
        break