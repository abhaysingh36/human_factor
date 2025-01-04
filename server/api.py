from flask import Flask, jsonify, Response, request
import threading
import time
import cv2
import json

class API:
    def __init__(self, imu, gps, ekf, yolo):
        self.app = Flask(__name__)
        self.imu = imu
        self.gps = gps
        self.ekf = ekf
        self.yolo = yolo
        self.camera = cv2.VideoCapture(0)
        self.latest_frame = None
        self.start_routes()

    def start_routes(self):
        @self.app.route('/data', methods=['GET'])
        def get_data():
            gps_data = self.gps.get_position()
            imu_data = self.imu.get_data()
            velocity = self.ekf.state[3:6].tolist()
            return jsonify({
                "gps": gps_data,
                "imu": imu_data,
                "velocity": velocity
            })

        @self.app.route('/video_feed', methods=['GET'])
        def video_feed():
            return Response(self.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def generate_frames(self):
        while True:
            success, frame = self.camera.read()
            if not success:
                break
            detections, processed_frame = self.yolo.detect(frame)
            self.latest_frame = processed_frame  # Keep latest frame for processing
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    def run(self, host='0.0.0.0', port=5000):
        self.app.run(host=host, port=port, debug=False, use_reloader=False)
