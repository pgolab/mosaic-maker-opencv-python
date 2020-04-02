import numpy as np
from utils.test_images_generator.generator_config import AVAILABLE_COLORS_DICT


def generate_random_color():
    selected_color = np.random.choice(list(AVAILABLE_COLORS_DICT.keys()))
    return AVAILABLE_COLORS_DICT[selected_color]
    # ------------------------------------------------------------------------------------
    # ToDo choose random color from AVAILABLE_COLORS_DICT
    # https://numpy.org/doc/1.18/reference/random/generated/numpy.random.choice.html
    # return (0, 0, 0)


def generate_random_image_points(image, count):
    widths = np.random.randint(0, image.shape[1], size=count)
    heights = np.random.randint(0, image.shape[0], size=count)
    return list(zip(widths, heights))

