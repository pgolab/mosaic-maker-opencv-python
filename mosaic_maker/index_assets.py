import cv2
from config import PROJECT_ROOT, IMAGES_SET, PATCH_SIZE, SET_DESCRIPTION_CSV_FILE_NAME
from mosaic_maker.image_processor import ImageProcessor


def index_images(set_name, patch_size):
    set_source_path = PROJECT_ROOT / 'assets/source-images/{}'.format(set_name)
    set_target_path = PROJECT_ROOT / 'assets/indexed-sources/{}'.format(set_name)
    set_images_target_path = set_target_path / 'images'
    set_sobel_images_target_path = set_target_path / 'sobel-images'
    set_description_target_path = set_target_path / SET_DESCRIPTION_CSV_FILE_NAME

    set_images_target_path.mkdir(parents=True, exist_ok=True)
    set_sobel_images_target_path.mkdir(parents=True, exist_ok=True)
    set_description_file = open(set_description_target_path, 'w')

    print('PROCESSING FILES:')

    for image_path in set_source_path.iterdir():
        image_name = image_path.name

        if image_name.startswith('.'):
            continue

        print('  > {}'.format(image_name))

        image = cv2.imread(image_path.as_posix())

        if image is None:
            print('    ERROR: image corrupted')
            continue

        processed_image = ImageProcessor(image_name, image, patch_size).processed_image
        cv2.imwrite('{}/{}'.format(set_images_target_path.as_posix(), image_name), processed_image.image)
        cv2.imwrite('{}/{}'.format(set_sobel_images_target_path.as_posix(), image_name), processed_image.sobel_image)
        set_description_file.write('{}\n'.format(str(processed_image)))

    set_description_file.close()

    print('  DONE')


if __name__ == "__main__":
    index_images(IMAGES_SET, PATCH_SIZE)


