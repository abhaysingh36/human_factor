class RTH:
    def __init__(self, home_position):
        self.home_position = home_position

    def compute_target(self, current_position):
        return {
            "lat": self.home_position["lat"] - current_position["lat"],
            "lon": self.home_position["lon"] - current_position["lon"],
            "alt": self.home_position["alt"]
        }
