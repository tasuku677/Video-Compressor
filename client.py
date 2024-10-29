import socket
import os
from pathlib import Path
import json
import subprocess
from utils import helper

dpath = 'client_temp'
if not os.path.exists(dpath):
    os.makedirs(dpath)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server_address = input('Error: Enter server address: ')
server_address = '127.0.0.1'
server_port = 9001
print('Connecting to {} port {}'.format(server_address, server_port))

try:
    sock.connect((server_address, server_port))
except Exception as e:
    print('Error: ' + str(e))
    exit(1)

try:
    #Send the request and the video
    # filepath = input('Type in a file to upload: ')
    # filepath = os.path.join(dpath,'movie.mp4')
    filepath = os.path.join(dpath,'music.mp4')
    extention = helper.get_extention(filepath)
    file_size = helper.get_filesize(filepath)
    arg_json = helper.choose_command(extention)
    header = helper.protocol_header(len(json.dumps(arg_json)), len(extention), file_size)
    sock.send(header)
    helper.send_data(sock, json.dumps(arg_json), extention, filepath)

    # Receive the response
    json_size, media_type_size, payload_size = helper.receive_header(sock)
    filepath = os.path.join(dpath, 'output.mp4')
    helper.receive_data(sock, json_size, media_type_size, payload_size, filepath)

finally:
    print('closing socket')
    sock.close()