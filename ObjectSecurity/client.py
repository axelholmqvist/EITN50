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
    print("\nHandshake started...")

    client_private_key = ec.generate_private_key(ec.SECP384R1, default_backend())
    client_public_key = client_private_key.public_key()
    encoded_client_public_key = client_public_key.public_bytes(Encoding.X962, PublicFormat.CompressedPoint)

    print("Public key received from server")
    server_public_key, _ = sock.recvfrom(BUFFER_SIZE)
    #print(server_public_key)

    print("Public key sent to server")
    sock.sendto(encoded_client_public_key, (UDP_IP, UDP_PORT))
    time.sleep(1)

    print("Calculating shared key...")
    shared_key = client_private_key.exchange(ec.ECDH(), ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP384R1(), server_public_key))
    #print(shared_key)

    print("Generating derived key...")
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)
    
    print("Handshake is finished!")
    #print(derived_key)

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

def aes_decrypt(encrypted_message, key, iv):
    """
    Function that decrypts the messages received. 
    Returns the decrypted and decoded message.
    """
    decryption_suite = AES.new(key, AES.MODE_CFB, iv)
    decrypted_message = decryption_suite.decrypt(base64.b64decode(encrypted_message))
    return decrypted_message.decode()

def send(message, derived_key, client_ip, client_port):
    """
    Function for encrypting and sending a message (+ the iv).
    """
    iv, encrypted_message = aes_encrypt(message, derived_key)
    sock.sendto(iv, (client_ip, client_port))
    sock.sendto(encrypted_message, (client_ip, client_port))

def receive(derived_key):
    """
    Function for receiving and decrypting an encrypted message (+ the iv).
    Returns the decrypted message.
    """
    iv, _ = sock.recvfrom(BUFFER_SIZE)
    encrypted_message, _ = sock.recvfrom(BUFFER_SIZE)
    decrypted_message = aes_decrypt(encrypted_message, derived_key, iv)
    return decrypted_message

def start_session():
    """
    Starts a new session with sending a 'Hello' to the server. 
    Each session starts with a handshake. After the handshake is complete,
    encrypted messages are sent to the server.
    """
    hello_message = b"Hello"

    sock.sendto(hello_message, (UDP_IP, UDP_PORT))
    print(f"\nSent to server: {hello_message.decode()}")
    derived_key = ecdh_handshake()

    send(input("\nUsername: "), derived_key, UDP_IP, UDP_PORT)
    send(input("Password: "), derived_key, UDP_IP, UDP_PORT)
    authentication_status = receive(derived_key)

    print(f"\n[SERVER]: {authentication_status}")
    if authentication_status == 'Successful authentication':
        send(input("\nSafe message to server: "), derived_key, UDP_IP, UDP_PORT)
        print("\n")

start_session()