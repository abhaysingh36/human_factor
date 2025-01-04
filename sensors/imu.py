from smbus import SMBus

class IMU:
    def __init__(self, address=0x68):
        self.bus = SMBus(1)
        self.address = address
        self.bus.write_byte_data(self.address, 0x6B, 0)  # Wake up MPU6050

    def read_raw_data(self, addr):
        high = self.bus.read_byte_data(self.address, addr)
        low = self.bus.read_byte_data(self.address, addr + 1)
        value = (high << 8) | low
        return value - 65536 if value > 32768 else value

    def get_data(self):
        acc_x = self.read_raw_data(0x3B) / 16384.0
        acc_y = self.read_raw_data(0x3D) / 16384.0
        acc_z = self.read_raw_data(0x3F) / 16384.0
        gyro_x = self.read_raw_data(0x43) / 131.0
        gyro_y = self.read_raw_data(0x45) / 131.0
        gyro_z = self.read_raw_data(0x47) / 131.0
        return {"acc": [acc_x, acc_y, acc_z], "gyro": [gyro_x, gyro_y, gyro_z]}
