import cv2
import numpy as np

from utils.test_images_generator.generator_config import AVAILABLE_SHAPES_DICT
from utils.test_images_generator.generator_utils import generate_random_color, generate_random_image_points


def generate_random_image(width, height):
    generated_image = np.full((height, width, 3), (255, 255, 255), dtype=np.uint8)

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
    line_points = generate_random_image_points(generated_image, 2)
    cv2.line(generated_image, line_points[0], line_points[1], generate_random_color(), 2)


def _draw_random_triangle(generated_image):
    triangle_points = generate_random_image_points(generated_image, 3)
    reshaped_triangle_points = np.array(triangle_points).reshape((-1, 1, 2))
    cv2.fillConvexPoly(generated_image, reshaped_triangle_points, generate_random_color())


def _draw_random_rectangle(generated_image):
    rectangle_points = generate_random_image_points(generated_image, 2)
    cv2.rectangle(generated_image, rectangle_points[0], rectangle_points[1], generate_random_color(), -1)


def _draw_random_circle(generated_image):
    center = generate_random_image_points(generated_image, 1)
    max_radius = min(generated_image.shape[0], generated_image.shape[1]) / 2
    radius = np.random.randint(0, max_radius)
    cv2.circle(generated_image, center[0], radius, generate_random_color(), -1)
