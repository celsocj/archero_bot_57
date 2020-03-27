import time
from adb_connector import *
import json


class GameScreenConnector:
    def __init__(self, width, height):
        self.debug = True
        self.width = width
        self.height = height
        # This should be in format rgba
        self.coords_path = "datas/static_coords.json"
        static_write = ""  # "
        self.static_coords = {
            "in_game": {"coordinates": [[53 / 1080, 45 / 2220], [53 / 1080, 65 / 2220], [53 / 1080, 85 / 2220], [76 / 1080, 45 / 2220], [76 / 1080, 65 / 2220], [76 / 1080, 85 / 2220]],
                        "values": [[255, 255, 255, 255], [255, 255, 255, 255], [255, 255, 255, 255], [255, 255, 255, 255], [255, 255, 255, 255], [255, 255, 255, 255]]},
            "repeat_endgame_question": {"coordinates": [[200 / 1080, 900 / 2220], [200 / 1080, 1200 / 2220], [900 / 1080, 900 / 2220], [900 / 1080, 1200 / 2220]],
                                        "values": [[219, 217, 207, 255], [219, 217, 207, 255], [219, 217, 207, 255], [219, 217, 207, 255]]},
            "endgame": {"coordinates": [[170 / 1080, 1230 / 2220], [890 / 1080, 1230 / 2220], [800 / 1080, 780 / 2220]],
                        "values": [[48, 98, 199, 255], [48, 98, 199, 255], [48, 98, 199, 255]]},
            "angel_heal": {"coordinates": [[50 / 1080, 367 / 2220], [1020 / 1080, 367 / 2220]],
                           "values": [[0, 118, 255, 255], [0, 118, 255, 255]]},
            "least_5_energy": {"coordinates": [[370 / 1080, 60 / 2220]],
                               "values": [[53, 199, 41, 255]]},
            "leveled_up": {"coordinates": [[70 / 1080, 530 / 2220], [1020 / 1080, 530 / 2220], [1430 / 1080, 80 / 2220], [1430 / 1080, 338 / 2220], [1430 / 1080, 410 / 2220], [1430 / 1080, 670 / 2220], [1430 / 1080, 740 / 2220], [1430 / 1080, 998 / 2220]],
                           "values": [[255, 181, 0, 255], [255, 181, 0, 255], [101, 200, 2, 255], [101, 200, 2, 255], [101, 200, 2, 255], [101, 200, 2, 255], [101, 200, 2, 255], [101, 200, 2, 255]]},
            "fortune_wheel": {"coordinates": [[70 / 1080, 370 / 2220], [1020 / 1080, 370 / 2220]],
                              "values": [[255, 181, 0, 255], [255, 181, 0, 255]]},
            "devil_question": {"coordinates": [[70 / 1080, 370 / 2220], [1020 / 1080, 370 / 2220]],
                               "values": [[243, 38, 81, 255], [243, 38, 81, 255]]},
            "ad_ask": {"coordinates": [[70 / 1080, 370 / 2220], [1020 / 1080, 370 / 2220], [460 / 1080, 1647 / 2220], [480 / 1080, 1647 / 2220]],
                       "values": [[255, 181, 0, 255], [255, 181, 0, 255], [255, 255, 255, 255], [255, 255, 255, 255]]},
            "mistery_vendor": {"coordinates": [[70 / 1080, 370 / 2220], [1020 / 1080, 370 / 2220], [57 / 1080, 2126 / 2220], [89 / 1080, 2126 / 2220], [57 / 1080, 2161 / 2220], [89 / 1080, 2161 / 2220]],
                               "values": [[255, 181, 0, 255], [255, 181, 0, 255], [255, 255, 255, 255], [255, 255, 255, 255], [255, 255, 255, 255], [255, 255, 255, 255]]},
            "equip_question_ask": {"coordinates": [[170 / 1080, 1230 / 2220], [890 / 1080, 1230 / 2220], [800 / 1080, 780 / 2220]],
                                   "values": [[48, 98, 199, 255], [48, 98, 199, 255], [48, 98, 199, 255]]}
        }
        self._saveStaticCoords()
        # """
        self.static_coords = {}
        self._loadStaticCoords()
        self.yellow_experience = [255, 170, 16, 255]
        # Line coordinates: x1,y1,x2,y2
        self.lineHorExpBarCoordinates = [160 / 1080, 180 / 2220, 930 / 1080, 180 / 2220]
        self.lineHorUpCoordinates = [180 / 1080, 2 / 2220, 890 / 1080, 2 / 2220]

    def _loadStaticCoords(self):
        with open(self.coords_path, 'r') as json_file:
            self.static_coords = json.load(json_file)

    def _saveStaticCoords(self):
        with open(self.coords_path, 'w') as json_file:
            json.dump(self.static_coords, json_file)

    def pixel_equals(self, px_readed, px_expected, around=5):
        # checking only RGB from RGBA
        return px_expected[0] - around <= px_readed[0] <= px_expected[0] + around \
               and px_expected[1] - around <= px_readed[1] <= px_expected[1] + around \
               and px_expected[2] - around <= px_readed[2] <= px_expected[2] + around

    def getFrameAttr(self, frame, attributes):
        attr_data = []
        for attr in attributes:
            x = int(attr[0] * self.width)
            y = int(attr[1] * self.height)
            attr_data.append(frame[int(y * self.width + x)])
        return attr_data

    def _check_screen_points_equal(self, frame, points_list, points_value):
        """
        Gets 2 lists of x,y coordinates where to get values and list of values to comapre.
        Returns true if current frame have those values
        :param points_list: a list of x,y coordinates (absolute, not normalized)
        :param points_value: a list (same size of points_list) with values for equals check (values are 4d)
        :return:
        """
        if len(points_list) != len(points_value):
            print("Wrong size between points and values!")
            return False
        if self.debug: print("-----------------------------------")
        if self.debug: print("|   Smartphone   |     Values     |")
        attr_data = self.getFrameAttr(frame, points_list)
        equal = True
        for i in range(len(attr_data)):
            if self.debug: print("| %4d %4d %4d | %4d %4d %4d |" % (attr_data[i][0], attr_data[i][1], attr_data[i][2], points_value[i][0], points_value[i][1], points_value[i][2]))
            if not self.pixel_equals(attr_data[i], points_value[i], around=2):
                equal = False
        if self.debug: print("|-->         %s" % ("  equal           <--|" if equal else "not equal         <--|"))
        if self.debug: print("-----------------------------------")
        return equal

    def checkFrame(self, coords_name: str, frame=None):
        """
        Given a coordinates name it checkes if the Frame has those pixels.
        If no Frame given , it will take a screenshot.
        :return:
        """
        if coords_name not in self.static_coords.keys():
            print("No coordinates called %s is saved in memory! Returning false." % coords_name)
            return False
        if self.debug: print("Checking %s" % (coords_name))
        if frame is None:
            frame = self.getFrame()
        is_equal = self._check_screen_points_equal(frame, self.static_coords[coords_name]["coordinates"], self.static_coords[coords_name]["values"])
        return is_equal

    def getFrame(self):
        return adb_screen_getpixels()

    def getFrameStateComplete(self, frame=None) -> dict:
        """
        Computes a complete check on given frame (takes a screen if none passed.
        Returns a dictionary with all known states with boolean value assigned.
        :return:
        """
        result = {}
        if frame is None:
            frame = self.getFrame()
        for k, v in self.static_coords.items():
            if self.debug: print("Checking %s" % (k))
            result[k] = self._check_screen_points_equal(frame, v["coordinates"], v["values"])
        return result

    def getFrameState(self, frame=None) -> str:
        """
        Computes a complete check on given frame (takes a screen if none passed.
        Returns a string with the name of current state, or unknown if no state found.
        :return:
        """
        state = "unknown"
        if frame is None:
            frame = self.getFrame()
        for k, v in self.static_coords.items():
            if self.debug: print("Checking %s" % (k))
            if self._check_screen_points_equal(frame, v["coordinates"], v["values"]):
                state = k
                break
        return state

    def _getHorLine(self, hor_line, frame):
        """
        Returns a horizontal line (list of colors) given hor_line [x1, y1, x2, y2] coordinates. If no frame given, it takes a screen.
        :param hor_line:
        :param frame:
        :return:
        """
        x1, y1, x2, y2 = hor_line[0] * self.width, hor_line[1] * self.height, hor_line[2] * self.width, hor_line[3] * self.height
        if frame is None:
            frame = self.getFrame()
        start = int(y1 * self.width + x1)
        size = int(x2 - x1)
        line = frame[start:start + size]
        return line

    def getLineExpBar(self, frame=None):
        """
        Returns the colors of Experience bar as a line. If no frame given, it takes a screen.
        :param frame:
        :return:
        """
        line = self._getHorLine(self.lineHorExpBarCoordinates, frame)
        masked_yellow = []
        for px in line:
            if self.pixel_equals(px, self.yellow_experience, 3):
                masked_yellow.append(px)
            else:
                masked_yellow.append([0, 0, 0, 0])
        return masked_yellow

    def getLineUpper(self, frame=None):
        """
        Returns the colors of Experience bar as a line. If no frame given, it takes a screen.
        :param frame:
        :return:
        """
        return self._getHorLine(self.lineHorUpCoordinates, frame)

    def _checkBarHasChanged(self, old_line_hor_bar, current_exp_bar, around=0):
        if len(old_line_hor_bar) != len(current_exp_bar):
            min_len = min(len(old_line_hor_bar), len(current_exp_bar))
            old_line_hor_bar = old_line_hor_bar[:min_len]
            current_exp_bar = current_exp_bar[:min_len]
        changed = False
        for i in range(len(old_line_hor_bar)):
            if not self.pixel_equals(old_line_hor_bar[i], current_exp_bar[i], around=around):
                changed = True
                break
        return changed

    def checkExpBarHasChanged(self, old_line_hor_bar, frame=None):
        """
        Checks if old experience bar line is different that this one. If no frame given, it takes a screen.
        :param old_line_hor_bar:
        :param frame:
        :return:
        """
        if self.debug: print("Checking LineExpBar has changed")
        new_line = self.getLineExpBar(frame)
        return self._checkBarHasChanged(old_line_hor_bar, new_line, around=2)

    def checkUpperLineHasChanged(self, old_line, frame=None):
        """
        Checks if old upper line is different that this one. If no frame given, it takes a screen.
        :param old_line:
        :param frame:
        :return:
        """
        if self.debug: print("Checking LineUpper has changed")
        new_line = self.getLineUpper(frame)
        return self._checkBarHasChanged(old_line, new_line, around=0)
