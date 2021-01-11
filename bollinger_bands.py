import numpy as np
import math
class Bollinger_Bands(object):

    def __init__(self,data):
        self.array_data = np.array(data)
        self.Bperiods = 49
        self.middle_band = []
        self.standard_deviation = []
        self.upper_band = []
        self.lower_band = []
        self.calc_middle_band()
        self.calc_standard_deviation()
        self.upper_lower_bands()

    def calc_middle_band(self):
        y = 0
        array_Middleband = []
        data = self.array_data
        for x in range(0, self.array_data.size - self.Bperiods):
            sum = 0
            for j in range(0, self.Bperiods + 1):  # upto 20 periods value
                z = self.array_data[y]
                sum = sum + z
                y = y + 1
            sum = sum / 50
            array_Middleband.append(sum)
            y = y - (self.Bperiods)
        self.middle_band = array_Middleband

    def calc_standard_deviation(self):
        stndrd_deviation = []
        y = 0
        z = 0
        # taking periods for counting SD equal Bperiods
        for x in range(0, self.array_data.size - self.Bperiods):
            sum = 0
            for j in range(0, self.Bperiods + 1):  # up to 20 periods value
                z = self.middle_band[x]
                sum = sum + ((z - self.array_data[y]) * (z - self.array_data[y]))
                y = y + 1
            sum = sum / 49
            sum = math.sqrt(sum)
            stndrd_deviation.append(sum)
            y = y - (self.Bperiods)
        self.standard_deviation = stndrd_deviation

    def upper_lower_bands(self):
        upper_band = []
        lower_band = []
        for x in range(0, len(self.standard_deviation)):
            upper_band.append(self.middle_band[x] + (self.standard_deviation[x]))
            lower_band.append(self.middle_band[x] - (self.standard_deviation[x]))
        self.lower_band = lower_band
        self.upper_band = upper_band
