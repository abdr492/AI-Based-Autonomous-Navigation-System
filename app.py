from flask import Flask, request, jsonify, send_from_directory
import os
import logging

# Disable Flask default logging for cleaner terminal output alongside Pygame
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__, static_folder='.', static_url_path='')

# Global telemetry state
telemetry_data = {
    "sys_status": "WAITING FOR ENGINE...",
    "status_color": "var(--accent-red)",
    "speed": 0.0,
    "distance": 200,
    "fps": 0,
    "ping": 0,
    "logs": ["[Flask] Server Initialized. Awaiting Pygame engine connection..."],
    "tracker_coords": "X:0 Y:0",
    "obj_count": 0
}

@app.route('/')
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'index.html')

@app.route('/update_telemetry', methods=['POST'])
def update_telemetry():
    global telemetry_data
    try:
        data = request.json
        if data:
            telemetry_data.update(data)
            return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/get_telemetry', methods=['GET'])
def get_telemetry():
    return jsonify(telemetry_data)

if __name__ == '__main__':
    print("[FLASK] Starting Telemetry Dashboard on http://127.0.0.1:5000/")
    app.run(port=5000, debug=False, threaded=True)
