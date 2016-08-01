def get_pixels_from_argument(num, reference):
    if type(num) != int:
        num = int(num) if not num.endswith("%") else reference*int(num[:-1])//100
    return num

def calc_window_coords(w, screen, monitors):
    w["x"] = get_pixels_from_argument(w["x"], monitors[screen].width)
    w["x"] += monitors[screen].x
    w["y"] = get_pixels_from_argument(w["y"], monitors[screen].height)
    w["y"] += monitors[screen].y
    w["width"] = get_pixels_from_argument(w["width"], monitors[screen].width)
    w["height"] = get_pixels_from_argument(w["height"], monitors[screen].height)
    
    return w
