from flask import Flask, render_template, request, send_file
from flask_cors import CORS
import subprocess
import os
import string
import random
from flask import jsonify
import time

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for all routes

@app.route('/')
def index():
    # Return the index page ../index.html (outside of the tools/compressor folder)
    return render_template('index.html')

def generate_random_filename():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

@app.route('/delete-file', methods=['POST'])
def delete_file():
    data = request.get_json()
    filename = data.get('filename')

    if filename:
        output_path = f'output/{filename}.mp4'
        try:
            os.remove(output_path)
            print(f"File '{output_path}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting file '{output_path}': {e}")

        return jsonify({'message': 'File deleted successfully'}), 200
    else:
        return jsonify({'error': 'Filename not provided'}), 400

@app.route('/compress', methods=['POST'])
def compress():
    video_file = request.files['video']
    target_size = int(request.form['target_size'])

    # Use the original filename (without extension) for output file
    original_filename = video_file.filename.rsplit('.', 1)[0]
    random_filename = generate_random_filename()
    video_path = f'uploads/{random_filename}.mp4'
    video_file.save(video_path)

    # Get video information
    video_info = get_video_info(video_path)
    print_video_info(video_info)

    # Calculate bitrate using FFmpeg
    output_path = f'output/{original_filename}.mp4'
    calculated_bitrate = calculate_bitrate(video_path, target_size)
    subprocess.run(['ffmpeg', '-i', video_path, '-b:v', f'{calculated_bitrate}k', output_path])

    # Delete original and compressed files
    os.remove(video_path)

    # Return the compressed video file for download
    return send_file(output_path, as_attachment=True, download_name=f'{original_filename}.mp4')

def get_video_info(video_path):
    result = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,duration,bit_rate', '-of', 'default=noprint_wrappers=1:nokey=1', video_path], stdout=subprocess.PIPE, text=True)
    
    width, height, duration, bit_rate = map(float, result.stdout.strip().split())
    
    return {
        'width': int(width),
        'height': int(height),
        'duration': duration,
        'bit_rate': bit_rate
    }

def print_video_info(video_info):
    print(f"Video Name: {request.files['video'].filename}")
    print(f"Original File Size: {request.files['video'].content_length} bytes")
    print(f"Duration: {video_info['duration']} seconds")
    print(f"Original Bitrate: {video_info['bit_rate']} bps")

def calculate_bitrate(video_path, target_size):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_path], stdout=subprocess.PIPE)
    duration = float(result.stdout)

    # Calculate bitrate to achieve target size
    bitrate = int((target_size * 8 * 1024) / duration)  # Convert target_size to kilobits (1 byte = 8 bits)
    return bitrate

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    # Use the following command to run the app with Gunicorn
    # gunicorn -w 4 -b 0.0.0.0:$PORT main:app
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))
