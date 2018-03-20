import cv2
import numpy as np

from config import PATCH_SIZE,\
    USE_HISTOGRAM_DESCRIPTOR, USE_SOBEL_DESCRIPTOR, \
    HISTOGRAM_BUCKETS, HISTOGRAM_GRID_SHAPE


class Patch:
    def __init__(self, name, image, sobel_image, features=None):
        self.name = name
        self.image = image
        self.sobel_image = sobel_image

        if features is None:
            self.features = self._calculate_features()
        else:
            self.features = features

    def _calculate_features(self):
        features = np.array([], dtype=np.float32)

        if USE_SOBEL_DESCRIPTOR:
            flatten_image = np.float32(self.sobel_image).flatten()
            cv2.normalize(flatten_image, flatten_image)
            features = np.append(features, flatten_image)

        if USE_HISTOGRAM_DESCRIPTOR:
            histogram_grid = self._get_grid_division()

            for (x0, y0, x1, y1) in histogram_grid:
                # ToDo convert image color space to one with uniform values
                # https://docs.opencv.org/2.4/modules/imgproc/doc/miscellaneous_transformations.html#cvtcolor

                # ToDo calculate 3d histogram of converted image
                # https://docs.opencv.org/3.1.0/d1/db7/tutorial_py_histogram_begins.html
                # https://docs.opencv.org/3.1.0/dd/d0d/tutorial_py_2d_histogram.html

                # ToDo normalize histogram
                # https://docs.opencv.org/2.4/modules/core/doc/operations_on_arrays.html?highlight=normalize#cv2.normalize

                features = np.append(features, [])

        return features

    @staticmethod
    def _get_grid_division():
        grid = []

        x_step = int(PATCH_SIZE / HISTOGRAM_GRID_SHAPE[0])
        y_step = int(PATCH_SIZE / HISTOGRAM_GRID_SHAPE[1])
        for y in range(0, PATCH_SIZE, y_step):
            for x in range(0, PATCH_SIZE, x_step):
                grid.append((x, y, x + x_step, y + y_step))

        return grid

    def __str__(self):
        return '{},{}'.format(self.name, ','.join(str(value) for value in self.features))

