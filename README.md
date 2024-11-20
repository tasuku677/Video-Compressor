# Video-Compressor

This project demonstrates a client-server model for video and audio processing. The server utilizes **FFmpeg** to process media files sent by the client, and returns the processed output.

## Features

- **Server for Media Processing**:
  - Accepts media files from clients.
  - Processes files using FFmpeg based on specified commands.
  - Returns the processed files to the client.
- **Client for Media Transfer**:
  - Sends media files and processing instructions to the server.
  - Receives the processed media output.
- **FFmpeg Integration**:
  - Handles various media processing tasks such as compression, resizing, format conversion, and more.

# Commands

| Command | Description                                       | Example JSON                                |
|---------|---------------------------------------------------|--------------------------------------------|
| 1       | Compress video with adjustable quality (crf).     | `{"command": 1, "crf": 23}`                |
| 2       | Resize video to a specific aspect ratio.          | `{"command": 2, "ratio_choice": "1"}`      |
| 3       | Change video resolution to a predefined standard. | `{"command": 3, "resolution_choice": "2"}` |
| 4       | Extract audio from video and save as MP3.         | `{"command": 4}`                           |
| 5       | Convert video to GIF format.                      | `{"command": 5}`                           |
| 6      

## File Overview

### `server.py`
The server-side script that:
1. Listens for incoming client connections.
2. Receives media files and instructions.
3. Processes the files using FFmpeg.
4. Sends back the processed output.

### `client.py`
The client-side script that:
1. Connects to the server.
2. Sends media files and processing commands.
3. Receives the processed output.


## Prerequisites

- **Python 3.7+**
- **FFmpeg** installed and accessible from the command line.

### Installing FFmpeg

- **Linux**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Windows**: Download from [FFmpeg official website](https://ffmpeg.org/download.html).

## Usage

### Running the Server

1. Start the server by running `server.py`:
    ```bash
    python server.py
    ```
2. The server will listen on:
   - Address: `0.0.0.0`
   - Port: `9001`
3. Media files will be stored temporarily in the `server_temp` directory.

### Running the Client

1. Start the client by running `client.py`:
    ```bash
    python client.py
    ```
2. The client will connect to:
   - Address: `127.0.0.1`
   - Port: `9001`
3. Media files must be placed in the `client_temp` directory before sending them to the server.

### Communication Protocol

1. **Header**:  
   - Contains metadata about the file and command, such as JSON size, media type size, and payload size.
2. **Payload**:  
   - Includes the media file and the command details in JSON format.
3. **Response**:  
   - The server sends back the processed media file using a similar protocol.
