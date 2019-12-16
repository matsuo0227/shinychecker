import os
import shutil
from pathlib import Path

dir_update = 'update/'
dir_images = '../app/assets/images/'

update_files = Path(dir_update).glob(u'**/*.jpg')

for f in update_files:
    src = str(f)
    dist = src.replace(dir_update, dir_images)
    print('move to "{}"'.format(dist))
    shutil.move(src, dist)