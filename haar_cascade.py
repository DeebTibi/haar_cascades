from helpers.integral_image import compute_integral_image
from helpers.haar_shapes import *
HAAR_SIZE = (1, 2)
MAX_VAL = 0
MIN_X, MIN_Y, MAX_X, MAX_Y = (-1, -1, -1, -1)


#   Entry Function
def main(img_location, block_size, haar_filter_scale, threshold):
    img = Image.open(img_location).convert("L")
    w, h = img.size
    if block_size > min(w, h):
        raise Exception(
            "block size is bigger than image, try lowering block size.")
    haar_size = (HAAR_SIZE[0], HAAR_SIZE[1])
    int_img = compute_integral_image(img)
    for x_0 in range(w):
        for y_0 in range(h):
            window = (x_0, y_0, x_0 + block_size - 1, y_0 + block_size - 1)
            if window[2] >= w or window[3] >= h:
                continue
            if not test_1(int_img, (w, h), x_0, y_0, haar_size, haar_filter_scale, window, threshold):
                continue
            if not test_2(int_img, (w, h), x_0, y_0, haar_size, haar_filter_scale, window, threshold):
                continue
            if not test_3(int_img, (w, h), x_0, y_0, haar_size, haar_filter_scale, window, threshold):
                continue
            print(f"Found face at point: ({x_0}, {y_0})")
    print("No face was found")
    return False


def test_1(int_img, img_size, x_0, y_0, size, haar_filter_scale, window, threshold):
    """Executes the first haar test using the first collection pass of haar filters"""
    global MAX_VAL
    for x in range(x_0, window[2] + 1):
        for y in range(y_0, window[3] + 1):
            for haar_scale in haar_filter_scale:
                haar_val_1 = category_01_haar_01(
                    int_img, img_size, x, y, (size[0] * haar_scale, size[1] * haar_scale), window)
                haar_val_2 = category_01_haar_02(
                    int_img, img_size, x, y, (size[1] * haar_scale, size[0] * haar_scale), window)
            if not max(haar_val_2, haar_val_1) <= MAX_VAL:
                # print(f"{x}, {y}: {MAX_VAL}")
                MAX_VAL = max(haar_val_2, haar_val_1)
            if haar_val_1 >= threshold or haar_val_2 >= threshold:
                return True
    return False


def test_2(int_img, img_size, x_0, y_0, size, haar_filter_scale, window, threshold):
    """Executes the second haar test using the second collection pass of haar filters"""
    global MIN_X, MIN_Y, MAX_X, MAX_Y
    for x in range(x_0, window[2] + 1):
        for y in range(y_0, window[3] + 1):
            for haar_scale in haar_filter_scale:
                haar_val_1 = category_02_haar_01(
                    int_img, img_size, x, y, (size[0] * haar_scale, size[1] * haar_scale), window)
                haar_val_2 = category_02_haar_02(
                    int_img, img_size, x, y, (size[1] * haar_scale, size[0] * haar_scale), window)
            print(haar_val_2)
            if haar_val_1 >= threshold or haar_val_2 >= threshold:
                MIN_X = x if MIN_X == -1 or x < MIN_X else MIN_X
                MIN_Y = y if MIN_Y == -1 or y < MIN_Y else MIN_Y
                MAX_X = x if MAX_X == -1 or x > MAX_X else MAX_X
                MAX_Y = x if MAX_Y == -1 or y > MAX_Y else MAX_Y
                return True
    return False


def test_3(int_img, img_size, x_0, y_0, size, haar_scale_size, window, threshold):
    """Executes the third haar test using the last collection pass of haar filters"""
    a = min(size[0], size[1])
    for x in range(x_0, window[2] + 1):
        for y in range(y_0, window[3] + 1):
            for haar_scale in haar_scale_size:
                haar_val = category_03_haar_01(
                    int_img, img_size, x, y, (a * haar_scale, a * haar_scale), window)
            if haar_val >= threshold:
                return True
    return False


