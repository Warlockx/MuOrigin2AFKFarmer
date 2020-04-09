import win32gui
import win32ui
import win32con
import cv2


def resize(img, scaled_resolution):
    a = scaled_resolution[0] / img.shape[0]
    b = scaled_resolution[1] / img.shape[1]

    return cv2.resize(img, None, fx=a, fy=b, interpolation=cv2.INTER_CUBIC)


def get_rect(rect):
    return [(rect[2]-rect[0]), (rect[3]-rect[1])]


def get_image(handle, save):
    rect = get_rect(win32gui.GetWindowRect(handle))
    window_dc = win32gui.GetWindowDC(handle)
    dc_obj = win32ui.CreateDCFromHandle(window_dc)
    compatible_dc = dc_obj.CreateCompatibleDC()
    data_bitmap = win32ui.CreateBitmap()
    data_bitmap.CreateCompatibleBitmap(dc_obj, rect[0], rect[1])
    compatible_dc.SelectObject(data_bitmap)
    compatible_dc.BitBlt((0, 0), (rect[0], rect[1]), dc_obj, (0, 0), win32con.SRCCOPY)
    if save:
        data_bitmap.SaveBitmapFile(compatible_dc, 'ss.jpg')
    b = data_bitmap.GetBitmapBits(True)
    dc_obj.DeleteDC()
    compatible_dc.DeleteDC()
    win32gui.ReleaseDC(handle, window_dc)
    win32gui.DeleteObject(data_bitmap.GetHandle())
    return [b, rect]
