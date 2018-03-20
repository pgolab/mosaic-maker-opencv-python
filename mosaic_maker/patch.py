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
                cielab_grid_part = cv2.cvtColor(self.image[y0:y1,x0:x1], cv2.COLOR_BGR2Lab)

                histogram = cv2.calcHist([cielab_grid_part],
                                         [0, 1, 2],
                                         None,
                                         HISTOGRAM_BUCKETS,
                                         [0, 255, 0, 255, 0, 255])
                cv2.normalize(histogram, histogram)
                features = np.append(features, histogram.flatten())

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

