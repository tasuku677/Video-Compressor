import socket
import os
from pathlib import Path
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = '0.0.0.0'
server_port = 9001

dpath = 'temp'
if not os.path.exists(dpath):
    os.makedirs(dpath)

print('Starting up on {} port {}'.format(server_address, server_port))  

sock.bind((server_address, server_port))
sock.listen(1)

while True:
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        #Recieve the header
        header = connection.recv(8)
        json_size = int.from_bytes(header[0:2], byteorder='big')
        media_type_size = int.from_bytes(header[2:3], byteorder='big')
        payload_size = int.from_bytes(header[3:], byteorder='big')
        stream_rate = 1024

        if payload_size > 4 * 1024 * 1024 * 1024:  # 4TB in bytes
            print('Payload size exceeds 4TB limit. Connection will be closed.')
            raise Exception('Payload size exceeds 4TB limit')

        print('Received header from client. Byte lengths: Json length {}, Media type size {}, Data size {}'.format(json_size, media_type_size, payload_size))

        # Recieve the payload
        body = b''
        while payload_size > 0:
            body += connection.recv(stream_rate if payload_size > stream_rate else payload_size)
            payload_size -= stream_rate
        with open(os.path.join(dpath,'OUTPUT_FILE'), 'wb+') as f:
            f.write(body)
        print('File saved')

        

    except Exception as e:
        print('Error: ' +  str(e))
    finally:
        print('Closing connection')
        connection.close()

