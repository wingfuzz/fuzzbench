

from process import popen
from config import *

def check_image_exist(image_name:str) -> bool:
    """ 检查基础镜像是否存在， 是否重新构建
        需要重建镜像时直接返回 Fasle
    Returns:
        bool: 镜像存在则为真， 镜像不存在则为假
    """
    code, ret = popen('docker images --format "{{.Repository}}"')
    if code:
        return False
    out_lines = ret.split("\n")
    for line in out_lines:
        if line == image_name:
            return True
        else:
            pass 
    return False


def compression_work_dir_code():
    """ 打包项目代码
    """
    popen(f"tar -zcvf {ROOT_DIR_PATH}/docker/fuzzbench.tar.gz {ROOT_DIR_PATH}")


def unzip_work_dir_code():
    """ 解压缩项目代码
    """
    popen(f"tar -zxvf /work/fuzzbench.tar.gz /work")



