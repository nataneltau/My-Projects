import socket
from Crypto.Cipher import AES

KEY = b'Choose smart key'
IV = b'Secure yout data'

def send_message(ip: str, port: int):
    """Send an *encrypted* message to the given ip + port.

    Julia expects the message to be encrypted, so re-implement this function accordingly.

    Notes:
    1. The encryption is based on AES.
    2. Julia and Winston already have a common shared key, just define it on your own.
    3. Mind the padding! AES works in blocks of 16 bytes.
    """
    # TODO: RE-IMPLEMENT THIS FUNCTION
    #raise NotImplementedError()
    #create AES object
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    
    #pad and encrypt our message, we can assume no message is longer than 15 bytes
    message = b'I love you'
    padded_msg = message.ljust(16)
    #print(list(padded_msg))
    ency_pad_msg = cipher.encrypt(padded_msg)
    
    #create connection and send the encrypted message
    connection = socket.socket()
    try:
        connection.connect((ip, port))
        connection.send(ency_pad_msg)
    finally:
        connection.close()


def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    send_message('127.0.0.1', 1984)


if __name__ == '__main__':
    main()
