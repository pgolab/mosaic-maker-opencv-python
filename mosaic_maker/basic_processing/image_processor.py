import cv2
from math import floor

from config import SOBEL_BLUR_KERNEL_SHAPE, EDGES_LOWER_THRESHOLD
from mosaic_maker.patch.patch import Patch


class ImageProcessor:
    def __init__(self, image_name, source_image, patch_size):
        self.image_name = image_name
        self.source_image = source_image

        self.cropped_image = self._crop_to_square(source_image)
        self.sobel_magnitude_image = self.calculate_sobel_magnitude_image(self.cropped_image)

        rescaled_image = cv2.resize(self.cropped_image, (patch_size, patch_size))
        rescaled_sobel_magnitude_image = cv2.resize(self.sobel_magnitude_image, (patch_size, patch_size))

        self.processed_image = Patch(image_name, rescaled_image, rescaled_sobel_magnitude_image)

    @staticmethod
    def _crop_to_square(image):
        # ToDo return image cropped to center square
        # https://docs.scipy.org/doc/numpy-dev/user/quickstart.html
        return image.copy()

    @staticmethod
    def calculate_sobel_magnitude_image(image):
        # ToDo convert image to grayscale and blur the result
        # https://docs.opencv.org/master/df/d9d/tutorial_py_colorspaces.html
        # https://docs.opencv.org/master/d4/d13/tutorial_py_filtering.html

        # ToDo calculate gradients
        # https://docs.opencv.org/master/d5/d0f/tutorial_py_gradients.html

        # ToDo combine gradients into one
        # https://docs.opencv.org/4.2.0/d2/de8/group__core__array.html#ga3460e9c9f37b563ab9dd550c4d8c4e7d
        # https://docs.opencv.org/4.2.0/d2/de8/group__core__array.html#gafafb2513349db3bcff51f54ee5592a19

        # ToDo threshold edges to get most important ones
        # https://docs.opencv.org/master/d7/d4d/tutorial_py_thresholding.html

        return image.copy()
