import requests
import mimetypes


ALLOWED_IMAGES_TYPES = ['image/jpeg', 'image/png']
MIME_TYPES_TO_EXTENSIONS_DICT = {
    'image/jpeg': 'jpg',
    'image/png': 'png'
}


def get_images_urls(query, results_count=10, offset=0, results_size='medium'):
    search_request = _build_search_request(query, results_count, offset, results_size)

    if search_request.status_code == 200:
        request_content = search_request.json()

        if request_content['status'] == 'success':
            return list(_filter_and_map_to_urls(request_content['data']['result']['items']))
        else:
            print(request_content)
            return []
    else:
        print(search_request.status_code)
        print(search_request.text)
        return []


def _build_search_request(query, results_count=10, offset=0, results_size='medium'):
    params = {
        'q': ' '.join(query),
        'count': results_count,
        'offset': offset,
        'size': results_size,
        'imagetype': 'photo'
    }
    headers = {
        'User-Agent': 'MosaicApp/0.0 lab project for OpenCV classes'
    }
    return requests.get('https://api.qwant.com/api/search/images', params=params, headers=headers)


def _filter_and_map_to_urls(items):
    return map(lambda url_and_image_type: (url_and_image_type[0], MIME_TYPES_TO_EXTENSIONS_DICT[url_and_image_type[1]]),
               filter(lambda url_and_image_type: url_and_image_type[1] in ALLOWED_IMAGES_TYPES,
                      map(lambda url: (url, mimetypes.guess_type(url)[0]),
                          map(lambda item: item['media'], items))
                      )
               )
