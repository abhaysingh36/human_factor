import numpy as np

class EKF:
    def __init__(self):
        self.state = np.zeros(6)  # [x, y, z, vx, vy, vz]
        self.covariance = np.eye(6) * 0.1

    def predict(self, imu_data, dt):
        acc = imu_data["acc"]
        F = np.eye(6)
        F[0, 3], F[1, 4], F[2, 5] = dt, dt, dt
        Q = np.eye(6) * 0.01
        self.state = F @ self.state + np.concatenate((np.zeros(3), acc * dt))
        self.covariance = F @ self.covariance @ F.T + Q

    def update(self, gps_data):
        H = np.eye(6)[:3, :]
        R = np.eye(3) * 5
        z = np.array([gps_data["lat"], gps_data["lon"], gps_data["alt"]])
        y = z - H @ self.state
        S = H @ self.covariance @ H.T + R
        K = self.covariance @ H.T @ np.linalg.inv(S)
        self.state = self.state + K @ y
        self.covariance = (np.eye(6) - K @ H) @ self.covariance
