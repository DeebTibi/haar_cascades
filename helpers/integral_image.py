from PIL import Image

# not the most efficient but should get the job done for small or medium-sized images.
def compute_integral_image(img:Image.Image):
    # Convert PIL image to grayscale and get image size
    img_gray = img.convert('L')
    width, height = img_gray.size
    # Initialize integral image with zeros
    integral = Image.new("L", (width, height), 0)
    integral_img = [[0 for _ in range(height)] for _ in range(width)]

    # Compute the first row and column of the integral image
    row_sum = 0
    for x in range(width):
        row_sum += img_gray.getpixel((x, 0))
        integral_img[x][0] = row_sum

    col_sum = 0
    for y in range(height):
        col_sum += img_gray.getpixel((0, y))
        integral_img[0][y] = col_sum

    # Compute the rest of the integral image
    for x in range(1, width):
        for y in range(1, height):
            pixel_value = img_gray.getpixel((x, y))
            integral_img[x][y] = pixel_value + integral_img[x - 1][y] + \
                integral_img[x][y - 1] - integral_img[x - 1][y - 1]

    return integral_img

def matrixBlockSum(mat, K: int):

    h, w = len(mat), len(mat[0])
    integral_image = [[0 for y in range(w)] for x in range(h)]

    # building integral image to speed up block sum computation
    for y in range(0, h):
        summation = 0

        for x in range(0, w):
            summation += mat[y][x]
            integral_image[y][x] = summation

            if y > 0:
                integral_image[y][x] += integral_image[y - 1][x]

    # compute block sum by looking-up integral image
    output_image = [[0 for y in range(w)] for x in range(h)]

    for y in range(h):
        for x in range(w):

            min_row, max_row = max(0, y - K), min(h - 1, y + K)
            min_col, max_col = max(0, x - K), min(w - 1, x + K)

            output_image[y][x] = integral_image[max_row][max_col]

            if min_row > 0:
                output_image[y][x] -= integral_image[min_row - 1][max_col]

            if min_col > 0:
                output_image[y][x] -= integral_image[max_row][min_col - 1]

            if min_col > 0 and min_row > 0:
                output_image[y][x] += integral_image[min_row - 1][min_col - 1]

    return output_image

