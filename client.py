import socket
import os
from pathlib import Path
import json
import subprocess


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
    filepath = 'movie.mp4'
    with open(filepath, 'rb') as f:
        f.seek (0, os.SEEK_END)
        file_size  = f.tell()
        f.seek(0)

        if file_size > pow(2, 32):
            raise Exception('File size exceeds 4TB limit')
        
        file_name = os.path.basename(filepath)
        file_name_size = file_name.encode('utf-8')
        media_type_size = ('mp4').encode('utf-8')

        header = protocol_header(0, len('mp4'), file_size)
        sock.send(header)

        if not file_name.endswith('.mp4'):
            raise Exception('File is not an mp4')

        while True:
            data = f.read(1024)
            if not data:
                break
            print('Sending...')
            sock.send(data)

finally:
    print('closing socket')
    sock.close()