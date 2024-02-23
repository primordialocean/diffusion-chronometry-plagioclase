class PhysicalConstants:
    def __init__(self):
        self.R_CONST = 8.31 # J/mol
        self.KELVIN = 273.15 # K as C

class Units:
    def __init__(self):
        self.UM = 1e-6 # um as m
        self.SECOND = 1 # day as second
        self.DAY = 60 * 60 * 24 # day as second
        self.YEAR = 60 * 60 * 24 * 365.25 # year as second
        self.TIME_UNITS = {
            "s": 1,
            "d": 60 * 60 * 24,
            "y": 60 * 60 * 24 * 365.25
            }