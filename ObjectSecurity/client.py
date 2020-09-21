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


""" Client socket values """
UDP_IP = "127.0.0.1"
UDP_PORT = 5004
BUFFER_SIZE = 64
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def ecdh_handshake():
    """
    Function that manages the handshake performed with the ECDH algorithm.

    Returns the derived key (shared secret)
    """
    client_private_key = ec.generate_private_key(ec.SECP384R1, default_backend())
    client_public_key = client_private_key.public_key()
    encoded_client_public_key = client_public_key.public_bytes(Encoding.X962, PublicFormat.CompressedPoint)

    #Receives public key from server
    server_public_key, _ = sock.recvfrom(BUFFER_SIZE)
    print(f"Received from server: {server_public_key}")

    #Sends public key to server
    sock.sendto(encoded_client_public_key, (UDP_IP, UDP_PORT))
    time.sleep(1)

    shared_key = client_private_key.exchange(ec.ECDH(), ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP384R1(), server_public_key))
    print(f"\n{shared_key}")

    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)

    print(f"\n{derived_key}")

    return derived_key

def aes_encrypt(message, key):
    """
    Function responsible for encrypting the messages using AES.

    Returns the initialization vector and encrypted message.
    """
    iv = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))
    encoded_iv = iv.encode('utf-8')

    encryption_suite = AES.new(key, AES.MODE_CFB, iv)
    encrypted_message = encryption_suite.encrypt(message)
    encoded_encrypted_message = base64.b64encode(encrypted_message)
    
    return encoded_iv, encoded_encrypted_message

def start_session():
    """
    Starts a new session. Each session starts with a handshake. After the handshake is complete,
    encrypted messages are sent to the server.
    """
    sock.sendto(b"Hello", (UDP_IP, UDP_PORT))
    print("\nSent to server: b'Hello'")
    derived_key = ecdh_handshake()
    iv, encrypted_message = aes_encrypt(input("Write message to server: "), derived_key)
    sock.sendto(iv, (UDP_IP, UDP_PORT))
    sock.sendto(encrypted_message, (UDP_IP, UDP_PORT))

start_session()