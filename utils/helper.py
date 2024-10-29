import os
import json
def protocol_header(json_size, media_type_size, payload_size):
    return json_size.to_bytes(2, byteorder='big') + media_type_size.to_bytes(1, byteorder='big') + payload_size.to_bytes(5, byteorder='big')

def get_extention(file_path):
    return file_path.split('.')[-1]

def choose_command(extention):
    command = input('Choose the command to run:\n'
                    ' 1. Compress the file\n'
                    ' 2. Change the ratio of the file\n'
                    ' 3. Change the resolution of the file\n'
                    ' 4. Convert the video to audio\n'
                    ' 5. Make a gif from the video\n'
                    ' 6. Exit\n')
    if command == '1':
        crf = input('Choose the CRF value (0-51): \n')
        return {
            'command': 1,
            'crf': crf,
            'extention': extention
        }
    elif command == '2':
        ratio_choice = input('Choose the desired ratio:\n'
                     ' 1. 16:9\n'
                     ' 2. 4:3\n'
                     ' 3. 1:1\n')
        return {
            'command': 2,
            'ratio_choice': ratio_choice,
            'extention': extention
        }
    elif command == '3':
        resolution_choice = input('Choose the desired resolution:\n'
                      ' 1. 1920:1080\n'
                      ' 2. 1280:720\n'
                      ' 3. 854:480\n'
                      ' 4. 640:360\n')
        return {
            'command': 3,
            'resolution_choice': resolution_choice,
            'extention': extention
        }
    elif command == '4':
        return {
            'command': 4,
            'extention': extention
        }
    elif command == '5':
        return {
            'command': 5,
            'extention': extention
        }   
    else:
        return {
            'command': -1
        }
    
def get_filesize(filepath): 
    with open(filepath, 'rb') as f:
        f.seek (0, os.SEEK_END)
        file_size  = f.tell()
        f.seek(0)
    if file_size > pow(2, 32):
        raise Exception('File size exceeds 4TB limit')
    return file_size


def send_data(sock,  arg_json, extention, filepath):
    sock.send(arg_json.encode())
    sock.send(extention.encode())
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            sock.send(data)
            print('Sending...')
    print('Sent: data')

def receive_header(sock):
    header = sock.recv(8)
    json_size = int.from_bytes(header[0:2], byteorder='big')
    media_type_size = int.from_bytes(header[2:3], byteorder='big')
    payload_size = int.from_bytes(header[3:], byteorder='big')
    return [json_size, media_type_size, payload_size]

def receive_data(sock, json_size, media_type_size, payload_size, file_name):
    args_json = sock.recv(json_size).decode()
    media_type = sock.recv(media_type_size).decode()
    stream_rate = 1024
    body = b''
    while payload_size > 0:
        body += sock.recv(stream_rate if payload_size > stream_rate else payload_size)
        payload_size -= stream_rate
        print('Receiving...')
    file_name = file_name.split('.')[0] + '.' + media_type
    with open(file_name, 'wb+') as f:
        f.write(body)
        print('File saved')
    return args_json
