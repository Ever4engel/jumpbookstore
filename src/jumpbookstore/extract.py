import os
import zipfile
import io
import json
from tqdm import tqdm
from PIL import Image

from . import image_solver
from . import cipher


def extract_from_jar(src_jarfile, dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    zf = zipfile.ZipFile(src_jarfile)
    with zf.open('configuration_pack.json') as f:
        with io.TextIOWrapper(f, encoding='utf-8_sig') as g:
            configuration_pack = json.loads(g.read())

    c = '0.dat'
    bs = 128
    hs = 1024
    ct = configuration_pack['ct']
    st = configuration_pack['st']
    et = configuration_pack['et']
    key1 = (ct + st + c).encode()
    key2 = (ct + c + et).encode()
    key3 = (c + st + et).encode()

    configuration = configuration_pack['configuration']
    contents = configuration['contents']

    for content in tqdm(contents, total=len(contents)):
        index = str(content['index']).zfill(5)

        filename = content['file']
        fileinfo = configuration_pack[filename]

        basename = os.path.basename(filename)
        basename_wo_extension, _ = os.path.splitext(basename)

        dat_filename = f'{filename}/{c}'
        dat_filename_wo_ext, _ = os.path.splitext(dat_filename)
        dst_filename = f'{dest_dir}/{index}_{basename_wo_extension}.jpg'

        with zf.open(dat_filename) as f:
            decrypted = cipher.decrypt_dat(f.read(), key1, key2, key3, hs, bs)

        shuffled_image = Image.open(io.BytesIO(decrypted))

        # see drawPage_ in viewer_image_1.2.5_2018-10-05.js
        width = shuffled_image.width
        height = shuffled_image.height
        pageinfo = fileinfo['FileLinkInfo']['PageLinkInfoList'][0]['Page']
        dummy_height = pageinfo['DummyHeight']
        dummy_width = pageinfo['DummyWidth']

        orig_size = (width - dummy_width, height - dummy_height)
        original_image = Image.new('RGB', orig_size)

        pattern = image_solver.calculate_pattern(dat_filename_wo_ext)
        moves = image_solver.calculate_moves(width, height, 64, 64, pattern)

        for move in moves:
            (srcX, srcY, destX, destY, width, height) = move

            src_rect = (destX, destY, destX + width, destY + height)
            crop = shuffled_image.crop(src_rect)

            dst_pos = (srcX, srcY)
            original_image.paste(crop, dst_pos)

        original_image.save(dst_filename)
    zf.close()
