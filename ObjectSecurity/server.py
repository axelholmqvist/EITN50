import socket
import time
import threading
import pickle
import random
import string
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from Crypto.Cipher import AES

"""
Sources:

https://stackoverflow.com/questions/57286946/python-diffie-hellman-exchange-cryptography-library-shared-key-not-the-same
https://cryptography.io/en/latest/hazmat/primitives/asymmetric/dh/
"""

""" Server socket values """
UDP_IP = "127.0.0.1"
UDP_PORT = 5004
BUFFER_SIZE = 64
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def ecdh_handshake(client_ip, client_port):
    """
    Function that manages the handshake performed with the ECDH algorithm.

    Returns the derived key (shared secret)
    """
    print("Initializing handshake...")
    time.sleep(1)

    server_private_key = ec.generate_private_key(ec.SECP384R1, default_backend())
    server_public_key = server_private_key.public_key()
    encoded_server_public_key = server_public_key.public_bytes(Encoding.X962, PublicFormat.CompressedPoint)

    sock.sendto(encoded_server_public_key, (client_ip, client_port))
    time.sleep(1)

    client_public_key, _ = sock.recvfrom(BUFFER_SIZE)
    print(f"Received from client: {client_public_key}")

    shared_key = server_private_key.exchange(ec.ECDH(), ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP384R1(), client_public_key))
    print(f"\n{shared_key}")

    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)

    print(f"\n{derived_key}")

    return derived_key

def aes_decrypt(encrypted_message, key, iv):
    """
    Function that decrypts the messages received from the client. 

    Returns the decrypted and decoded message.
    """
    decryption_suite = AES.new(key, AES.MODE_CFB, iv)
    decrypted_message = decryption_suite.decrypt(base64.b64decode(encrypted_message))
    return decrypted_message.decode()

def start_server():
    """
    Starts the server and the session. The server listens for messages from the client.
    The session consist of the handshake and receiving messages. 
    """
    print("Starting server...")
    time.sleep(1)
    print("Server is up and running!")

    while True:
        message, address = sock.recvfrom(BUFFER_SIZE)
        client_ip = address[0]
        client_port = address[1]
        print(f"\n[{client_ip}:{client_port}]: {message}")
        derived_key = ecdh_handshake(client_ip, client_port)
        iv, _ = sock.recvfrom(BUFFER_SIZE)
        encrypted_message, _ = sock.recvfrom(BUFFER_SIZE)
        decrypted_message = aes_decrypt(encrypted_message, derived_key, iv)

        print(f"\n{decrypted_message}")

start_server()
