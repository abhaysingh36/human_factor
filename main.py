import time
from sensors.imu import IMU
from sensors.gps import GPS
from motor_control.motors import Motors
from navigation.ekf import EKF
from navigation.pid import PID
from navigation.rth import RTH

imu = IMU()
gps = GPS()
motors = Motors([18, 19, 20, 21])
ekf = EKF()
pid_pitch = PID(1.0, 0.1, 0.05)
pid_roll = PID(1.0, 0.1, 0.05)
pid_alt = PID(1.5, 0.2, 0.1)

home_position = None

try:
    while True:
        imu_data = imu.get_data()
        gps_data = gps.get_position()

        if home_position is None and gps_data:
            home_position = gps_data
            rth = RTH(home_position)

        ekf.predict(imu_data, 0.02)
        if gps_data:
            ekf.update(gps_data)

        target_pitch, target_roll, target_alt = 0, 0, 2
        pitch_correction = pid_pitch.compute(target_pitch, ekf.state[1], 0.02)
        roll_correction = pid_roll.compute(target_roll, ekf.state[0], 0.02)
        altitude_correction = pid_alt.compute(target_alt, ekf.state[2], 0.02)

        motor_speeds = [
            50 + roll_correction - pitch_correction + altitude_correction,
            50 - roll_correction - pitch_correction + altitude_correction,
            50 + roll_correction + pitch_correction + altitude_correction,
            50 - roll_correction + pitch_correction + altitude_correction,
        ]
        motors.set_speeds(motor_speeds)

        time.sleep(0.02)

except KeyboardInterrupt:
    motors.cleanup()
