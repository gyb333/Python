import shutil
import os

def rm_path(p):
    if os.path.exists(p):       # 判断文件夹是否存在
        shutil.rmtree(p)        # 删除文件夹

def mk_Path(path):
    if not os.path.exists(path):
        os.makedirs(path)