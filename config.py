import functools
import operator
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
IMAGES_SET = 'test'
TARGET_IMAGE = 'test-target.jpg'

PATCH_SIZE = 32

SOBEL_BLUR_KERNEL_SHAPE = (3, 3)
EDGES_LOWER_THRESHOLD = 120

HISTOGRAM_GRID_SHAPE = (4, 4)
HISTOGRAM_BUCKETS = (8, 8, 8)
HISTOGRAM_VECTOR_LENGTH = functools.reduce(operator.mul, HISTOGRAM_GRID_SHAPE, 1) \
                          * functools.reduce(operator.mul, HISTOGRAM_BUCKETS, 1)

ACCEPTED_HISTOGRAM_DISTANCE_MARGIN = 0.05

USE_SOBEL_DESCRIPTOR = True
USE_HISTOGRAM_DESCRIPTOR = False

DESCRIPTION_CSV_FILE_NAME = 'set-description.csv'

assert PATCH_SIZE % HISTOGRAM_GRID_SHAPE[0] == 0 and PATCH_SIZE % HISTOGRAM_GRID_SHAPE[1] == 0,\
    'HISTOGRAM_GRID_SHAPE dimensions have to be divisors of the PATCH_SIZE'
