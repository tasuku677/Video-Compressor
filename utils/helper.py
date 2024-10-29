import os

def protocol_header(json_size, media_type_size, payload_size):
    return json_size.to_bytes(2, byteorder='big') + media_type_size.to_bytes(1, byteorder='big') + payload_size.to_bytes(5, byteorder='big')

def get_filesize(filepath): 
    with open(filepath, 'rb') as f:
        f.seek (0, os.SEEK_END)
        file_size  = f.tell()
        f.seek(0)
    if file_size > pow(2, 32):
        raise Exception('File size exceeds 4TB limit')
    return file_size


def send_header(sock, filepath, file_size):
    file_name = os.path.basename(filepath)
    file_name_size = file_name.encode('utf-8')
    media_type_size = ('mp4').encode('utf-8')
    if not file_name.endswith('.mp4'):
        raise Exception('File is not an mp4')
    header = protocol_header(0, len('mp4'), file_size)
    sock.send(header)

def send_data(sock, filepath):
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

def receive_data(sock, payload_size, file_name):
    stream_rate = 1024
    body = b''
    while payload_size > 0:
        body += sock.recv(stream_rate if payload_size > stream_rate else payload_size)
        payload_size -= stream_rate
        print('Receiving...')
    with open(file_name, 'wb+') as f:
        f.write(body)
        print('File saved')
