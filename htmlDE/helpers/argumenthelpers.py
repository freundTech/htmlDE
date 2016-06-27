def get_pixels_from_argument(num, reference):
    num = int(num) if not num.endswith("%") else reference*int(num[:-1])//100
    return num
