import cv2
import numpy as np

from config import PROJECT_ROOT, PATCH_SIZE

from utils.test_images_generator.generator_config import AVAILABLE_COLORS_DICT
from utils.test_images_generator.random_image_generator import generate_random_image


def generate_patches_set(set_name, patch_size, count, target_width, target_height):
    images_path = PROJECT_ROOT / f'assets/source-images/{set_name}'
    images_path.mkdir(parents=True, exist_ok=True)

    colors = list(AVAILABLE_COLORS_DICT.values())
    colors.append((255, 255, 255))
    full_color_images = list(map(lambda color: np.full((patch_size, patch_size, 3), color, dtype=np.uint8), colors))

    generated_patches = 0

    for color_image in full_color_images:
        cv2.imwrite(f'{images_path.as_posix()}/{generated_patches:04d}.jpg', color_image)
        generated_patches += 1

    while generated_patches < count:
        generated_image = generate_random_image(target_width, target_height)

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
                    cv2.imwrite(f'{images_path.as_posix()}/{generated_patches:04d}.jpg', patch)
                    generated_patches += 1

                    print(f'\rGENERATED {generated_patches:04d} OF {count} PATCHES', end='')


def generate_target_image(image_name, width, height):
    generated_image = generate_random_image(width, height)

    image_path = PROJECT_ROOT / f'assets/{image_name}'

    cv2.imwrite(image_path.as_posix(), generated_image)
    cv2.imshow('generated image', generated_image)


if __name__ == "__main__":
    generate_patches_set('test', PATCH_SIZE, 300, 900, 500)
    generate_target_image('test-target.jpg', 900, 500)
    cv2.waitKey(0)

