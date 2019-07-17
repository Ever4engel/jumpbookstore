import time
import math
import requests
from tqdm import tqdm


def get_time():
    return int(time.time() * 1000)


def download_with_progress_bar(url, filename):
    f = open(filename, 'wb')
    r = requests.get(url, stream=True)

    total_length = int(r.headers.get('content-length'))
    block_size = 1024
    for chunk in tqdm(
        r.iter_content(chunk_size=block_size),
        total=math.ceil(total_length/block_size),
        unit='KB',
        unit_scale=True
    ):
        if chunk:
            f.write(chunk)
            f.flush()

    r.close()
    f.close()
