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

def ffmpeg_run(input_filepath, dpath, arg_json = []):
    output_filepath = os.path.join(dpath, 'output.mp4')
    arg_json = json.loads(arg_json)
    command = arg_json['command']
    if command == 1:
        crf = arg_json['crf']
        subprocess.run(f"ffmpeg -i {input_filepath} -vcodec libx264 -crf {crf} -preset medium {output_filepath}".split())
    elif command == 2:
        ratio_choice = arg_json['ratio_choice']
        ratio = ratio_hash[ratio_choice]
        width, height = map(int, ratio.split(':'))
        subprocess.run([
            "ffmpeg", "-i", input_filepath, 
            "-vf", f"scale=w={width}:h={height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2", 
            output_filepath
        ])
    elif command == 3:
        resolution_choice = arg_json['resolution_choice']
        ratio= resolution_hash[resolution_choice]
        width, height = map(int, ratio.split(':'))
        subprocess.run([
            "ffmpeg", "-i", input_filepath, 
            "-vf", f"scale=w={width}:h={height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2", 
            output_filepath
        ])
    elif command == 4:
        output_filepath = 'server_temp/output.mp3'
        subprocess.run(f"ffmpeg -i {input_filepath} -vn -acodec libmp3lame {output_filepath}".split())
    elif command == 5:
        output_filepath = 'server_temp/output.gif'
        subprocess.run(f"ffmpeg -i {input_filepath} {output_filepath}".split())
    elif command == 6:
        exit(0)
    else:
        print('Invalid command')
        exit(1)
    return output_filepath