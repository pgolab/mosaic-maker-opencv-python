import cv2
from config import PROJECT_ROOT, IMAGES_SET, PATCH_SIZE, DESCRIPTION_CSV_FILE_NAME
from mosaic_maker.basic_processing.image_processor import ImageProcessor


def index_images(set_name, patch_size):
    source_path = PROJECT_ROOT / f'assets/source-images/{set_name}'
    target_path = PROJECT_ROOT / f'assets/indexed-sources/{set_name}'
    images_target_path = target_path / 'images'
    sobel_images_target_path = target_path / 'sobel-images'
    description_target_path = target_path / DESCRIPTION_CSV_FILE_NAME

    images_target_path.mkdir(parents=True, exist_ok=True)
    sobel_images_target_path.mkdir(parents=True, exist_ok=True)
    description_file = open(description_target_path, 'w')

    print('PROCESSING FILES:')

    for image_path in source_path.iterdir():
        image_name = image_path.name

        if image_name.startswith('.'):
            continue

        print(f'\r  > {image_name}', end='')

        image = cv2.imread(image_path.as_posix())

        if image is None:
            print('    ERROR: image corrupted')
            continue

        processed_image = ImageProcessor(image_name, image, patch_size).processed_image
        cv2.imwrite(f'{images_target_path.as_posix()}/{image_name}', processed_image.image)
        cv2.imwrite(f'{sobel_images_target_path.as_posix()}/{image_name}', processed_image.sobel_image)
        description_file.write(f'{str(processed_image)}\n')

    description_file.close()

    print('  DONE')


if __name__ == "__main__":
    index_images(IMAGES_SET, PATCH_SIZE)


