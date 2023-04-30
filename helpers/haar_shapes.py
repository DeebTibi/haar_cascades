import numpy as np
from PIL import Image


def rectangle_sum(int_img, img_size, x_0, y_0, size: tuple):
    """ Efficiently compute the sum of pixels in rectangle
        at point x_0, y_0 of a specified size using an integral image."""
    rect_w, rect_h = size
    w, h = img_size
    p1 = (x_0, y_0)
    p2 = (x_0 + rect_w - 1, y_0)
    p3 = (x_0 + rect_w - 1, y_0 + rect_h - 1)
    p4 = (x_0, y_0 + rect_h - 1)
    for p in [p1, p2, p3, p4]:
        if p[0] >= w or p[1] >= h:
            return -1
    # rectangle is at the origin
    if p1[1] == 0 and p1[0] == 0:
        return int_img[p3[0]][p3[1]]

    # rectangle is adjacent to upper border special case.
    if p1[1] == 0:
        return int_img[p3[0]][p3[1]] - int_img[p4[0] - 1][p4[1]]

    # rectangle is adjacent to left border special case.
    if p1[0] == 0:
        return int_img[p3[0]][p3[1]] - int_img[p2[0]][p2[1] - 1]

    return int_img[p3[0]][p3[1]] - int_img[p4[0] - 1][p4[1]] - int_img[p2[0]][p2[1] - 1] + int_img[p1[0] - 1][p1[1] - 1]


def category_01_haar_01(int_img, img_size,  x_0, y_0, size, window):
    """ Calculate haar value from haar filter (i)(a) within a specified window.
    reference in the following image: https://rb.gy/fnlus1"""
    w, h = size
    min_x, min_y, max_x, max_y = window
    if x_0 < min_x or y_0 < min_y or x_0 + 2*(w-1) > max_x or y_0 + h - 1 > max_y:
        return -1
    white = rectangle_sum(int_img, img_size, x_0, y_0, size)
    black = rectangle_sum(int_img, img_size, x_0 + w - 1, y_0, size)
    if white == -1 or black == -1:
        return -1
    return round(abs(white - black)/(2*w*h*255), 2)


def category_01_haar_02(int_img, img_size, x_0, y_0, size, window):
    """ Calculate haar value from haar filter (i)(b) within a specified window.
    reference in the following image: https://rb.gy/fnlus1"""
    w, h = size
    min_x, min_y, max_x, max_y = window
    if x_0 < min_x or y_0 < min_y or x_0 + w - 1 > max_x or y_0 + 2*(h - 1) > max_y:
        return -1
    white = rectangle_sum(int_img, img_size, x_0, y_0, size)
    black = rectangle_sum(int_img, img_size, x_0, y_0 + h - 1, size)
    if white == -1 or black == -1:
        return -1
    return round(abs(white - black)/(2*w*h*255), 2)


def category_02_haar_01(int_img, img_size, x_0, y_0, size, window):
    """ Calculate haar value from haar filter (ii)(a) within a specified window.
    reference in the following image: https://rb.gy/fnlus1"""
    w, h = size
    min_x, min_y, max_x, max_y = window
    if x_0 < min_x or y_0 < min_y or x_0 + 3*(w-1) > max_x or y_0 + h - 1 > max_y:
        return -1
    white_1 = rectangle_sum(int_img, img_size, x_0, y_0, size)
    black = rectangle_sum(int_img, img_size, x_0 + w - 1, y_0, size)
    white_2 = rectangle_sum(int_img, img_size, x_0 + 2*w - 2, y_0, size)
    if white_1 == -1 or white_2 == -1 or black == -1:
        return -1
    return round(abs(white_1 + white_2 - black)/(3*w*h*255), 2)


def category_02_haar_02(int_img, img_size, x_0, y_0, size, window):
    """ Calculate haar value from haar filter (ii)(c) within a specified window.
    reference in the following image: https://rb.gy/fnlus1"""
    w, h = size
    min_x, min_y, max_x, max_y = window
    if x_0 < min_x or y_0 < min_y or x_0 + w - 1 > max_x or y_0 + 3*(h - 1) > max_y:
        return -1
    white_1 = rectangle_sum(int_img, img_size, x_0, y_0, size)
    black = rectangle_sum(int_img, img_size, x_0, y_0 + h - 1, size)
    white_2 = rectangle_sum(int_img, img_size, x_0, y_0 + 2*h - 2, size)
    if white_1 == -1 or white_2 == -1 or black == -1:
        return -1
    return round(abs(white_1 + white_2 - black)/(3*w*h*255), 2)


def category_03_haar_01(int_img, img_size, x_0, y_0, size, window):
    """ Calculate haar value from haar a cube haar filter within a specified window """
    w, h = size
    if w != h:
        raise Exception(
            "Category 3 haar 1 filter must be supplied with a square (w==h)")
    min_x, min_y, max_x, max_y = window
    if x_0 < min_x or y_0 < min_y or x_0 + 2*(w - 1) > max_x or y_0 + 2*(h - 1) > max_y:
        return -1
    white_1 = rectangle_sum(int_img, img_size, x_0, y_0, size)
    black_1 = rectangle_sum(int_img, img_size, x_0, y_0 + h - 1, size)
    white_2 = rectangle_sum(int_img, img_size, x_0 + w - 1, y_0 + h - 1, size)
    black_2 = rectangle_sum(int_img, img_size, x_0 + w - 1, y_0, size)
    if white_1 == -1 or white_2 == -1 or black_1 == -1 or black_2 == -1:
        return -1
    return round(abs(white_1 + white_2 - black_1 - black_2)/(4*w*h*255), 2)
