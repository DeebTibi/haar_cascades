from PIL import Image

def pixels_in_single_dim_rectangle(image:Image.Image, x_0, y_0, rect_size, show = False):
    """ gathers all pixels in an image within a single dimensional
     rectangle of specified size from an offset """
    w, h = image.size
    rect_x, rect_y = rect_size
    pix_matrix = image.load()
    pixels_in_rect = []
    if y_0 > h or x_0 > w:
        return []
    pixel_remain = rect_x
    k = 0
    while k < pixel_remain:
        if x_0 + k > w-1:
            break
        for i in range(y_0, h):
            if i - y_0 + 1 > rect_y:
                break
            pixels_in_rect.append(pix_matrix[x_0 + k,i] / 255)
            if show:
                pix_matrix[x_0 + k, i] = 0
        k += 1
    return pixels_in_rect


def detect_vertical_edge(image, threshold):
    w, h = image.size
    rect_dim = (6,3)
    for x in range(w):
        for y in range(h):
            black_rect = pixels_in_single_dim_rectangle(image, x, y, rect_dim)
            white_rect = pixels_in_single_dim_rectangle(image, x, y + rect_dim[1], rect_dim)
            if not black_rect or not white_rect \
                    or len(black_rect) != len(white_rect):
                continue
            res = (sum(black_rect)/len(black_rect)) - (sum(white_rect)/len(white_rect))
            print(res)
