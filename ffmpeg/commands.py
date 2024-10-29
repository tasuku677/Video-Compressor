import subprocess
import os
import json

ratio_hash = {
    '1': '1280:720',
    '2': '800:600',
    '3': '1000:1000'
}
resolution_hash = {
    '1': '1920:1080',
    '2': '1280:720',
    '3': '854:480',
    '4': '640:360'
}

def ffmpeg_run(input_file_path, output_file_path):
    command = input('Choose the command to run:\n'
                    ' 1. Compress the file\n'
                    ' 2. Change the ratio of the file\n'
                    ' 3. Change the resolution of the file\n'
                    ' 4. Convert the video to audio\n'
                    ' 5. Make a gif from the video\n'
                    ' 6. Exit\n')

    if command == '1':
        crf = 51
        subprocess.run(f"ffmpeg -i {input_file_path} -vcodec libx264 -crf {crf} -preset medium {output_file_path}".split())
    elif command == '2':
        ratio_choice = input('Choose the desired ratio:\n'
                     ' 1. 16:9\n'
                     ' 2. 4:3\n'
                     ' 3. 1:1\n')
        ratio = ratio_hash[ratio_choice]
        width, height = map(int, ratio.split(':'))
        subprocess.run([
            "ffmpeg", "-i", input_file_path, 
            "-vf", f"scale=w={width}:h={height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2", 
            output_file_path
        ])
    elif command == '3':
        resolution_choice = input('Choice the desired ratio: \
                    1. 1920 : 1080 \
                    2. 1280 : 720 \
                    3. 854 : 480 \
                    4. 640 : 360' )
        ratio= resolution_hash[resolution_choice]
        subprocess.run(f"ffmpeg -i {input_file_path} -vf scale={ratio} {output_file_path}".split())
    elif command == '4':
        command_json = {
            "ffmpeg": "ffmpeg",
            "options": ["-i", "-vn"],
            "input": "input.mp4",
            "output": "output.mp3"
        }
        input_file_name, input_file_extension = os.path.splitext(input_file_path)
        output_file_path = input_file_name + '.mp3'
        subprocess.run(f"ffmpeg -i {input_file_path} -vn -acodec libmp3lame {output_file_path}".split())
    elif command == '5':
        command_json = {
            "ffmpeg": "ffmpeg",
            "options": "-i",
            "input": "input.mp4",
            "output": "output.gif"
        }
        subprocess.run("ffmpeg -i input.mp4 output.gif".split())
    elif command == '6':
        exit(0)
    else:
        print('Invalid command')
        exit(1)