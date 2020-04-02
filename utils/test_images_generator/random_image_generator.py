import cv2
import numpy as np

from utils.test_images_generator.generator_config import AVAILABLE_SHAPES_DICT
from utils.test_images_generator.generator_utils import generate_random_color, generate_random_image_points


def generate_random_image(width, height):
    # ---------------------------------------------------------------------------------------
    # ToDo generate white image
    # https://numpy.org/doc/1.18/reference/generated/numpy.full.html

    # generated_image = np.zeros((height, width, 3), dtype=np.uint8)
    # ---------------------------------------------------------------------------------------
    generated_image = np.full((height, width, 3), (255, 255, 255), dtype=np.uint8)

    # ---------------------------------------------------------------------------------------
    # ToDo choose random number of shapes from AVAILABLE_SHAPES_DICT
    # https://numpy.org/doc/1.18/reference/random/generated/numpy.random.randint.html
    # https://numpy.org/doc/1.18/reference/random/generated/numpy.random.choice.html

    # chosen_shapes = []
    # ---------------------------------------------------------------------------------------
    shapes_count = np.random.randint(5, 10)
    chosen_shapes = np.random.choice(list(AVAILABLE_SHAPES_DICT.values()), shapes_count)

    for shape in chosen_shapes:
        if shape == AVAILABLE_SHAPES_DICT['LINE']:
            _draw_random_line(generated_image)
        elif shape == AVAILABLE_SHAPES_DICT['TRIANGLE']:
            _draw_random_triangle(generated_image)
        elif shape == AVAILABLE_SHAPES_DICT['RECTANGLE']:
            _draw_random_rectangle(generated_image)
        elif shape == AVAILABLE_SHAPES_DICT['CIRCLE']:
            _draw_random_circle(generated_image)

    return generated_image


def _draw_random_line(generated_image):
    # ---------------------------------------------------------------------------------------
    # ToDo draw random line (use _generate_random_image_points and _generate_random_color)
    # https://docs.opencv.org/master/dc/da5/tutorial_py_drawing_functions.html
    # return
    # ---------------------------------------------------------------------------------------
    line_points = generate_random_image_points(generated_image, 2)
    cv2.line(generated_image, line_points[0], line_points[1], generate_random_color(), 2)


def _draw_random_triangle(generated_image):
    # ---------------------------------------------------------------------------------------
    # ToDo draw random triangle (use _generate_random_image_points and _generate_random_color)
    # https://docs.opencv.org/3.1.0/dc/da5/tutorial_py_drawing_functions.html
    # https://docs.opencv.org/master/d6/d6e/group__imgproc__draw.html#ga3069baf93b51565e386c8e591f8418e6
    # format for triangle: reshape((-1, 1, 2)
    # https://numpy.org/doc/1.18/reference/generated/numpy.reshape.html
    # return
    # ---------------------------------------------------------------------------------------
    triangle_points = generate_random_image_points(generated_image, 3)
    reshaped_triangle_points = np.array(triangle_points).reshape((-1, 1, 2))
    cv2.fillConvexPoly(generated_image, reshaped_triangle_points, generate_random_color())


def _draw_random_rectangle(generated_image):
    # ---------------------------------------------------------------------------------------
    # ToDo draw random line (use _generate_random_image_points and _generate_random_color)
    # https://docs.opencv.org/master/dc/da5/tutorial_py_drawing_functions.html
    # return
    # ---------------------------------------------------------------------------------------
    rectangle_points = generate_random_image_points(generated_image, 2)
    cv2.rectangle(generated_image, rectangle_points[0], rectangle_points[1], generate_random_color(), -1)


def _draw_random_circle(generated_image):
    # ---------------------------------------------------------------------------------------
    # ToDo draw random line (use _generate_random_image_points and _generate_random_color)
    # https://docs.opencv.org/master/dc/da5/tutorial_py_drawing_functions.html
    # return
    # ---------------------------------------------------------------------------------------
    center = generate_random_image_points(generated_image, 1)
    max_radius = min(generated_image.shape[0], generated_image.shape[1]) / 2
    radius = np.random.randint(0, max_radius)
    cv2.circle(generated_image, center[0], radius, generate_random_color(), -1)
