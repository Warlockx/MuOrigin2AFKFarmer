import win32api
import win32con
import win32gui
import time


class WinApi:
    def __init__(self, window_name, scaled_resolution):
        self.window_name = window_name
        self.handle = self.get_handle()
        self.scaled_resolution = scaled_resolution
        self.real_resolution = self.get_real_resolution()

    def get_real_resolution(self):
        rect = win32gui.GetWindowRect(self.handle)
        w = rect[2] - rect[0]
        h = rect[3] - rect[1]
        return h, w

    def get_handle(self):
        parent = win32gui.FindWindow(None, self.window_name)
        return win32gui.FindWindowEx(parent, None, None, 'ScreenBoardClassWindow')

    def mouse_click_drag(self, start_coord, end_coord):
        current_cord = start_coord
        win32api.PostMessage(self.handle, win32con.WM_LBUTTONDOWN, 1, self.make_l_param(start_coord))
        while current_cord != end_coord:
            current_cord[0] += max(-1, min(end_coord[0] - current_cord[0], 1))
            current_cord[1] += max(-1, min(end_coord[1] - current_cord[1], 1))
            win32api.PostMessage(self.handle, win32con.WM_MOUSEMOVE, 1, self.make_l_param(current_cord))
            time.sleep(.0005)
        win32api.PostMessage(self.handle, win32con.WM_LBUTTONUP, 0, self.make_l_param(end_coord))

    def make_l_param(self, coord):
        # we do this to scale to the resolution of the running program
        _h = self.scaled_resolution[0] / self.real_resolution[0]
        _w = self.scaled_resolution[1] / self.real_resolution[1]
        coord = (int(coord[0] / _h), int(coord[1] / _w))
        print('clicked at {}'.format(coord))
        return (coord[1] << 16) | coord[0]

    def mouse_click(self, cords, shape=(10, 10)):
        w, h = shape
        cords = (int(cords[0] + w / 2),
                 int(cords[1] + h / 2))

        win32api.PostMessage(self.handle, win32con.WM_LBUTTONDOWN, 1, self.make_l_param(cords))
        win32api.PostMessage(self.handle, win32con.WM_LBUTTONUP, 0, self.make_l_param(cords))
