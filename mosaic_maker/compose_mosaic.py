import cv2
from imutils import resize
from config import PROJECT_ROOT, TARGET_IMAGE, IMAGES_SET, PATCH_SIZE
from mosaic_maker.mosaic.mosaic_image import MosaicImage
from mosaic_maker.mosaic.patch_picker import PatchPicker


def compose_mosaic(image_path, set_name, patch_size, output_path):
    patches_path = PROJECT_ROOT / 'assets/indexed-sources/{}'.format(set_name)
    patch_picker = PatchPicker(set_name, patches_path)

    target_image = cv2.imread(image_path)

    mosaic_image = MosaicImage(target_image, patch_size, patch_picker)

    mosaic = mosaic_image.compose_mosaic()

    cv2.imshow('mosaic', resize(mosaic, width=400))

    cv2.imshow('final target', target_image)
    cv2.imshow('final mosaic', mosaic)

    cv2.imwrite(output_path, mosaic)

if __name__ == "__main__":
    compose_mosaic('{}/assets/{}'.format(PROJECT_ROOT.as_posix(), TARGET_IMAGE), IMAGES_SET, PATCH_SIZE,
                   '{}/assets/{}'.format(PROJECT_ROOT.as_posix(), 'output.jpg'))
    cv2.waitKey()


