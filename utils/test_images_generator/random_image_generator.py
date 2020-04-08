import cv2
import numpy as np

from utils.test_images_generator.generator_config import AVAILABLE_SHAPES_DICT
from utils.test_images_generator.generator_utils import generate_random_color, generate_random_image_points


def generate_random_image(width, height):
    # ToDo generate white image
    # https://numpy.org/doc/1.18/reference/generated/numpy.full.html
    generated_image = np.zeros((height, width, 3), dtype=np.uint8)

    # ToDo choose random number of shapes from AVAILABLE_SHAPES_DICT
    # https://numpy.org/doc/1.18/reference/random/generated/numpy.random.randint.html
    # https://numpy.org/doc/1.18/reference/random/generated/numpy.random.choice.html
    chosen_shapes = []

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
    # ToDo draw random line (use _generate_random_image_points and _generate_random_color)
    # https://docs.opencv.org/master/dc/da5/tutorial_py_drawing_functions.html
    return


def _draw_random_triangle(generated_image):
    # ToDo draw random triangle (use _generate_random_image_points and _generate_random_color)
    # https://docs.opencv.org/3.1.0/dc/da5/tutorial_py_drawing_functions.html
    # https://docs.opencv.org/master/d6/d6e/group__imgproc__draw.html#ga3069baf93b51565e386c8e591f8418e6
    # format for triangle: reshape((-1, 1, 2)
    # https://numpy.org/doc/1.18/reference/generated/numpy.reshape.html
    return


def _draw_random_rectangle(generated_image):
    # ToDo draw random line (use _generate_random_image_points and _generate_random_color)
    # https://docs.opencv.org/master/dc/da5/tutorial_py_drawing_functions.html
    return


def _draw_random_circle(generated_image):
    # ToDo draw random line (use _generate_random_image_points and _generate_random_color)
    # https://docs.opencv.org/master/dc/da5/tutorial_py_drawing_functions.html
    return
