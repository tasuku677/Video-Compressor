import socket
import os
from pathlib import Path
import json

from ffmpeg import commands
from utils import helper

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = '0.0.0.0'
server_port = 9001

dpath = 'server_temp'
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
        json_size, media_type_size, payload_size = helper.receive_header(connection)
        stream_rate = 1024

        if payload_size > 4 * 1024 * 1024 * 1024:  # 4TB in bytes
            print('Payload size exceeds 4TB limit. Connection will be closed.')
            raise Exception('Payload size exceeds 4TB limit')

        print('Received header from client. Byte lengths: Json length {}, Media type size {}, Data size {}'.format(json_size, media_type_size, payload_size))

        # Recieve the payload
        file_name = os.path.join(dpath, 'input.mp4')
        helper.receive_data(connection, payload_size, file_name)

        # Run the ffmpeg command
        commands.ffmpeg_run(file_name, os.path.join(dpath, 'output.mp4'))

        #return the output file
        filepath = os.path.join(dpath,'output.mp4')
        file_size = helper.get_filesize(filepath)
        if file_size > pow(2, 32):
            raise Exception('File size exceeds 4TB limit')
        helper.send_header(connection, filepath, file_size)
        helper.send_data(connection, filepath)


    except Exception as e:
        print('Error: ' +  str(e))
    finally:
        print('Closing connection')
        connection.close()

