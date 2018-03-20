from pathlib import Path
import requests
import shutil
from time import sleep

from config import PROJECT_ROOT
from utils.images_loader.qwant_images_search import get_images_urls


DATA_PAGE_SIZE = 50


def load_images(set_name, queries, count):
    images_path = PROJECT_ROOT / Path('assets/source-images/{}'.format(set_name))
    images_set = set()

    print('GETTING IMAGES URLS')

    query_index = 0;
    while query_index < len(queries):
        query = queries[query_index]
        print('  > PROCESSING: {}'.format(query))
        try:
            query_images = _collect_urls_for(query, count)
            print('    {} RESULTS FOUND'.format(len(query_images)))

            images_set.update(query_images)

            if len(query_images) >= 0:
                query_index += 1
            else:
                sleep(60)
        except:
            sleep(60)
            print('    ERROR OCCURED')

        sleep(5)

    print('{} UNIQUE IMAGES FOUND'.format(len(images_set)))

    print('GETTING IMAGES URLS')

    _load_and_save_query_result_images(images_path, images_set)


def _collect_urls_for(query, count):
    current_offset = 0
    loaded_urls = []

    while current_offset < count:
        new_urls = get_images_urls(query, min(DATA_PAGE_SIZE, count), current_offset)
        loaded_urls += new_urls

        if len(new_urls) == 0:
            break

        current_offset += DATA_PAGE_SIZE

    return loaded_urls


def _load_and_save_query_result_images(path, images):
    path.mkdir(parents=True, exist_ok=True)

    print('LOADING_IMAGES')

    failed_requests = []

    for (index, (url, image_extension)) in enumerate(images):
        print('  > LOADING IMAGE {:3d}/{}'.format(index + 1, len(images)))

        image_name = '{:03d}.{}'.format(index, image_extension)

        try:
            load_and_save_image(url, path / image_name)
            print('    DONE')
        except:
            failed_requests.append((image_name, url))

    if len(failed_requests) > 0:
        print('  {} REQUESTS HAVE FAILED:'.format(len(failed_requests)))
        print(failed_requests)


def load_and_save_image(url, image_path):
    image_request = requests.get(url, stream=True, timeout=60)
    if image_request.status_code == 200:
        with open(image_path, 'wb') as image_file:
            image_request.raw.decode_content = True
            shutil.copyfileobj(image_request.raw, image_file)


if __name__ == "__main__":
    load_images('underwater', [['coral', 'reef'], ['coral', 'reef', '2'], ['coral', 'reef', '3'],
                               ['underwater'], ['underwater', 'seaweed'], ['underwater', 'fish'],
                               ['underwater', 'life'], ['underwater', 'coral'],
                               ['coral', 'fish'], ['underwater', 'shrimp']], 500)
