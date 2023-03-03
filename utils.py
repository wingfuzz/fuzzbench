

from process import popen
from config import *

def check_image_exist(image_name:str, rebuild:str) -> bool:
    """ 检查基础镜像是否存在， 是否重新构建
        需要重建镜像时直接返回 Fasle
    Returns:
        bool: 镜像存在则为真， 镜像不存在则为假
    """
    print(rebuild)
    if rebuild == "ON":
        return False
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



