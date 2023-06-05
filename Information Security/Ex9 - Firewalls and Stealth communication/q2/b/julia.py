import socket
from Crypto.Cipher import AES

KEY = b'Choose smart key'
IV = b'Secure yout data'

def receive_message(port: int) -> str:
    """Receive *encrypted* messages on the given TCP port.

    As Winston sends encrypted messages, re-implement this function so to
    be able to decrypt the messages.

    Notes:
    1. The encryption is based on AES.
    2. Julia and Winston already have a common shared key, just define it on your own.
    3. Mind the padding! AES works in blocks of 16 bytes.
    """
    # TODO: RE-IMPLEMENT THIS FUNCTION
    #raise NotImplementedError()
    #create AES object
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    
    #listen to a connection
    listener = socket.socket()
    try:
        listener.bind(('', port))
        listener.listen(1)
        connection, address = listener.accept()
        try:
            #read the message
            dec_pad_msg = connection.recv(1024)
            #decrypt the message
            dec_pad_msg = cipher.decrypt(dec_pad_msg).decode('latin-1')
            #remove the padding from the message
            dec_msg = dec_pad_msg.rstrip()
            
            return dec_msg #return the message
        finally:
            connection.close()
    finally:
        listener.close()


def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    message = receive_message(1984)
    print('received: %s' % message)


if __name__ == '__main__':
    main()
