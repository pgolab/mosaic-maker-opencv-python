import numpy as np
import cv2
from imutils import resize

import threading

from mosaic_maker.basic_processing.image_processor import ImageProcessor

from mosaic_maker.patch.patch import Patch


class MosaicImage:
    def __init__(self, image, patch_size, patch_picker):
        self.original_image = image
        self.patch_size = patch_size
        self.patch_picker = patch_picker

        self.target_image = self._crop_image_to_patch_size(image.copy(), patch_size)
        self.target_sobel_image = ImageProcessor.calculate_sobel_magnitude_image(self.target_image)

        self.processing_image = False

    @staticmethod
    def _crop_image_to_patch_size(image, patch_size):
        # ToDo crop image so it is divisible by patch_size
        return image

    def compose_mosaic(self):
        print('BUILDING MOSAIC')

        target_image = self.target_image
        target_sobel_image = self.target_sobel_image

        mosaic = np.zeros(target_image.shape, np.uint8)
        sobel_mosaic = np.zeros(target_sobel_image.shape, np.uint8)

        (height, width) = target_image.shape[:2]

        target_image_copy = target_image.copy()
        target_sobel_image_copy = target_sobel_image.copy()

        self.processing_image = True
        threading.Thread(target=lambda: self._compose_mosaic_for(width, height, mosaic, sobel_mosaic, target_image_copy, target_sobel_image_copy)).start()
        self._progress_display_loop(mosaic, sobel_mosaic, target_image_copy, target_sobel_image_copy)

        return mosaic

    def _compose_mosaic_for(self, width, height, mosaic, sobel_mosaic, target_image_copy, target_sobel_image_copy):
        for y in range(0, height, self.patch_size):
            for x in range(0, width, self.patch_size):
                self._select_patch_for(x, y, mosaic, sobel_mosaic, target_image_copy, target_sobel_image_copy)

        self.processing_image = False

    def _select_patch_for(self, x, y, mosaic, sobel_mosaic, target_image_copy, target_sobel_image_copy):
        # ToDo create patch for current position

        # ToDo select patch from patch picker

        # ToDo update mosaic and draw current window representation on images copies

        return

    def _progress_display_loop(self, mosaic, sobel_mosaic, target_image_copy, target_sobel_image_copy):
        while self.processing_image:
            cv2.imshow('current target window', resize(target_image_copy, width=400))
            cv2.imshow('current sobel target window', resize(target_sobel_image_copy, width=400))
            cv2.imshow('mosaic', resize(mosaic, width=400))
            cv2.imshow('sobel mosaic', resize(sobel_mosaic, width=400))
            cv2.waitKey(10)
