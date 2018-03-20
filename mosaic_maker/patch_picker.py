import cv2
from config import SET_DESCRIPTION_CSV_FILE_NAME, \
    MAX_ACCEPTED_MIN_HISTOGRAM_DISTANCE, PATCH_SIZE, \
    USE_SOBEL_DESCRIPTOR, USE_HISTOGRAM_DESCRIPTOR, HISTOGRAM_VECTOR_LENGTH
import numpy as np

from mosaic_maker.patch import Patch


class PatchPicker:
    def __init__(self, set_name, set_path):
        self.set_name = set_name
        self.set_path = set_path

        self.patches = self._load_patches()

    def _load_patches(self):
        (patches_dict, sobel_patches_dict) = self._load_patches_images()
        descriptions_dict = self._load_csv()

        patches_list = []

        for patch_name in descriptions_dict.keys():
            patches_list.append(Patch(patch_name,
                                      patches_dict[patch_name], sobel_patches_dict[patch_name],
                                      descriptions_dict[patch_name]))

        return np.array(patches_list)

    def _load_patches_images(self):
        patches_path = self.set_path / 'images'
        sobel_patches_path = self.set_path / 'sobel-images'

        patches_dict = {}
        sobel_patches_dict = {}

        for patch_path in patches_path.iterdir():
            patch_name = patch_path.name

            if patch_name.startswith('.'):
                continue

            patches_dict[patch_name] = cv2.imread(patch_path.as_posix())
            sobel_patches_dict[patch_name] = cv2.imread((sobel_patches_path / patch_name).as_posix(), cv2.IMREAD_GRAYSCALE)

        return patches_dict, sobel_patches_dict

    def _load_csv(self):
        descriptions_dict = {}

        csv_path = self.set_path / SET_DESCRIPTION_CSV_FILE_NAME

        with open(csv_path) as csv_file:
            for row in csv_file:
                first_comma = row.find(',')
                file_name = row[:first_comma]
                features_string = row[first_comma + 1:]
                features = np.fromstring(features_string, sep=',', dtype=np.float32)
                descriptions_dict[file_name] = features

            csv_file.close()

        return descriptions_dict

    def pick_patch_for(self, target_patch):
        sobel_vector_length = PATCH_SIZE ** 2

        sobel_distances = np.array([], np.float32)
        histogram_distances = np.array([], np.float32)

        for patch in self.patches:
            if USE_SOBEL_DESCRIPTOR:
                patch_sobel_vector = patch.features[:sobel_vector_length]
                target_patch_sobel_vector = target_patch.features[:sobel_vector_length]

                diff = (target_patch_sobel_vector - patch_sobel_vector) ** 2
                distance = np.sum(diff)

                sobel_distances = np.append(sobel_distances, distance)

            if USE_HISTOGRAM_DESCRIPTOR:
                patch_histogram_vector = patch.features[-HISTOGRAM_VECTOR_LENGTH:]
                target_patch_histogram_vector = target_patch.features[-HISTOGRAM_VECTOR_LENGTH:]

                distance = cv2.compareHist(target_patch_histogram_vector, patch_histogram_vector, cv2.HISTCMP_CHISQR_ALT)
                histogram_distances = np.append(histogram_distances, distance)

        if not USE_SOBEL_DESCRIPTOR:
            best_patch_index = np.argmin(histogram_distances)
        elif not USE_HISTOGRAM_DESCRIPTOR:
            best_patch_index = np.argmin(sobel_distances)
        else:
            cv2.normalize(sobel_distances, sobel_distances)
            cv2.normalize(histogram_distances, histogram_distances)

            sobel_distances_diff = sobel_distances - min(sobel_distances)
            histogram_distances_diff = histogram_distances - min(histogram_distances)

            best_matched_indices = np.where(histogram_distances_diff < MAX_ACCEPTED_MIN_HISTOGRAM_DISTANCE)[0]
            chosen_patches_values = sobel_distances_diff[best_matched_indices]
            best_patch_index = best_matched_indices[np.argmin(chosen_patches_values)]

            print(len(best_matched_indices))

        return self.patches[best_patch_index]
