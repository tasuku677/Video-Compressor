import socket
import os
from pathlib import Path
import json
import subprocess
from utils import helper

header = {
    "header_size": 8,
    "media_type_size": "mp4",
    'payload_size': 100
}

media_type_size = ["mp4", "mp3", "json", "avi"]

command_json = {
    "ffmpeg": "ffmpeg",
    "options": "-i",
    "input": "input.mp4",
    "output": "output.mp3"
}
# subprocess.run(['ffmpeg', '-i', 'input.mp4', 'output.mp3'])

dpath = 'client_temp'
if not os.path.exists(dpath):
    os.makedirs(dpath)

def protocol_header(json_size, media_type_size, payload_size):
    return json_size.to_bytes(2, byteorder='big') + media_type_size.to_bytes(1, byteorder='big') + payload_size.to_bytes(5, byteorder='big')

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
    # filepath = input('Type in a file to upload: ')
    filepath = os.path.join(dpath,'movie.mp4')
    file_size = helper.get_filesize(filepath)
    helper.send_header(sock, filepath, file_size)
    helper.send_data(sock, filepath)

    # Receive the response
    json_size, media_type_size, payload_size = helper.receive_header(sock)
    helper.receive_data(sock, payload_size, "client_temp/output.mp4")

finally:
    print('closing socket')
    sock.close()