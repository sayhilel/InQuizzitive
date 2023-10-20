from flask import Flask, render_template, Response
from src.headTracker import head_tracking_game  # Assuming headTracker.py is in the src directory

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    frames = head_tracking_game()
    for frame in frames:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
