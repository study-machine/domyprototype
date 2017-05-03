# -*- coding: utf-8 -*-
# @Time    : 17/3/7 下午2:15
# @Author  : wxy
# @File    : utils.py
import os
import shutil
import zipfile

from domyprototype.settings import MEDIA_ROOT


def unzip_file(full_filename, username, id):
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    # 原型文件保存在media/prototype/用户名/id/下面
    save_path = os.path.join(MEDIA_ROOT, 'prototype', username, str(id))

    if zipfile.is_zipfile(full_filename) == False:
        return False, '检测到不是zip文件'
    try:
        # 解压缩
        z = zipfile.ZipFile(full_filename, 'r')
        # 如果将文件放在一个文件夹中，namelist()的第一个是文件夹名
        folder_name = z.namelist()[0]
        z.extractall(save_path)
        z.close()
    except:
        try:
            unzip_extract_gbk(full_filename, save_path)
        except:
            return False, '解压gbk也失败'
    # 删除zip包
    os.remove(full_filename)

    # 要保存到数据库中的index路径
    try:
        index_path = os.path.join('prototype', username, str(id), folder_name, 'index.html')
    except:
        index_path = os.path.join('prototype', username, str(id), folder_name.decode('gbk'), 'index.html')

    return True, index_path


def unzip_extract_gbk(full_filename, save_path):
    z = zipfile.ZipFile(full_filename, 'r')
    for name in z.namelist():
        utf8name = name.decode('gbk')
        print "Extracting " + utf8name
        pathname = os.path.dirname(utf8name)
        full_pathname = os.path.join(MEDIA_ROOT, save_path, pathname)
        full_utf8name = os.path.join(MEDIA_ROOT, save_path, utf8name)
        if not os.path.exists(full_pathname) and full_pathname != "":
            os.makedirs(full_pathname)
        data = z.read(name)
        if not os.path.exists(full_utf8name):
            fo = open(full_utf8name, 'w')
            fo.write(data)
            fo.close
    z.close()
    return


def remove_prototype_dir(username, str_id):
    path = os.path.join(MEDIA_ROOT, 'prototype', username, str_id)
    if os.path.exists(path):
        shutil.rmtree(path)
    return os.path.exists(path)


