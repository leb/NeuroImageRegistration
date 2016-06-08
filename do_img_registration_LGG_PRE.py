# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 15:02:02 2016

@author: dahoiv
"""

import os
import sqlite3
import ConvertDataToDB
import image_registration


def find_images():
    """ Find images for registration """
    conn = sqlite3.connect(image_registration.DB_PATH)
    conn.text_factory = str
    cursor = conn.execute('''SELECT pid from Patient where diagnose = ?''', ('LGG',))
    ids = []
    for row in cursor:
        cursor2 = conn.execute('''SELECT id from Images where pid = ? AND diag_pre_post = ?''', (row[0], "pre"))
        for _id in cursor2:
            ids.append(_id[0])
        cursor2.close()

    cursor.close()
    conn.close()
    print(ids)
    return ids

# pylint: disable= invalid-name
if __name__ == "__main__":
    os.nice(19)
    image_registration.setup("LGG_PRE/")
    if not os.path.exists(image_registration.TEMP_FOLDER_PATH):
        os.makedirs(image_registration.TEMP_FOLDER_PATH)

    image_registration.prepare_template(image_registration.TEMPLATE_VOLUME,
                                        image_registration.TEMPLATE_MASK)

    pre_images = find_images()

    data_transforms = image_registration.get_transforms(pre_images, image_registration.SYN)

    ConvertDataToDB.save_transform_to_database(data_transforms)