import cv2
import numpy as np
from pathlib import Path

from config import PROJECT_ROOT, PATCH_SIZE


AVAILABLE_SHAPES_DICT = {
    'LINE': 'LINE',
    'TRIANGLE': 'TRIANGLE',
    'RECTANGLE': 'RECTANGLE',
    'CIRCLE': 'CIRCLE',
}

AVAILABLE_COLORS_DICT = {
    'RED': (0, 0, 255),
    'GREEN': (0, 255, 0),
    'BLUE': (255, 0, 0),
    'YELLOW': (0, 255, 255),
    'PURPLE': (255, 0, 255),
    'CYAN': (255, 255, 0)
}


def generate_patches_set(set_name, patch_size, count, target_width, target_height):
    images_path = PROJECT_ROOT / Path('assets/source-images/{}'.format(set_name))
    images_path.mkdir(parents=True, exist_ok=True)

    colors = list(AVAILABLE_COLORS_DICT.values())
    colors.append((255, 255, 255))
    full_color_images = list(map(lambda color: np.full((patch_size, patch_size, 3), color, dtype=np.uint8), colors))

    generated_patches = 0

    for color_image in full_color_images:
        cv2.imwrite('{}/{:04d}.jpg'.format(images_path.as_posix(), generated_patches), color_image)
        generated_patches += 1

    while generated_patches < count:
        generated_image = _generate_random_image(target_width, target_height)
        cv2.imshow('generated image', generated_image)
        cv2.waitKey(1)

        for y in range(0, target_height - patch_size, patch_size):
            for x in range(0, target_width - patch_size, patch_size):
                if generated_patches >= count:
                    continue

                patch = generated_image[y:y + patch_size, x:x + patch_size]

                is_patch_interesting = True

                for color_image in full_color_images:
                    if np.array_equal(patch, color_image):
                        is_patch_interesting = False

                if is_patch_interesting:
                    cv2.imwrite('{}/{:04d}.jpg'.format(images_path.as_posix(), generated_patches), patch)
                    generated_patches += 1

                    print('GENERATED {:04d} OF {} PATCHES'.format(generated_patches, count))

    cv2.waitKey(0)


def generate_target_image(image_name, width, height):
    generated_image = _generate_random_image(width, height)

    image_path = PROJECT_ROOT / Path('assets/{}'.format(image_name))

    cv2.imwrite(image_path.as_posix(), generated_image)

    cv2.imshow('generated image', generated_image)
    cv2.waitKey(0)


def _generate_random_image(width, height):
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
    line_points = _generate_random_image_points(generated_image, 2)
    cv2.line(generated_image, line_points[0], line_points[1], _get_random_color(), 2)


def _draw_random_triangle(generated_image):
    triangle_points = _generate_random_image_points(generated_image, 3)
    reshaped_triangle_points = np.array(triangle_points).reshape((-1, 1, 2))
    cv2.fillConvexPoly(generated_image, reshaped_triangle_points, _get_random_color())


def _draw_random_rectangle(generated_image):
    rectangle_points = _generate_random_image_points(generated_image, 2)
    cv2.rectangle(generated_image, rectangle_points[0], rectangle_points[1], _get_random_color(), -1)


def _draw_random_circle(generated_image):
    center = _generate_random_image_points(generated_image, 1)
    max_radius = min(generated_image.shape[0], generated_image.shape[1]) / 2
    radius = np.random.randint(0, max_radius)
    cv2.circle(generated_image, center[0], radius, _get_random_color(), -1)


def _generate_random_image_points(image, count):
    widths = np.random.randint(0, image.shape[1], size=count)
    heights = np.random.randint(0, image.shape[0], size=count)
    return list(zip(widths, heights))


def _get_random_color():
    selected_color = np.random.choice(list(AVAILABLE_COLORS_DICT.keys()))
    return AVAILABLE_COLORS_DICT[selected_color]


if __name__ == "__main__":
    generate_patches_set('test', PATCH_SIZE, 300, 900, 500)
    generate_target_image('test-target.jpg', 900, 500)
