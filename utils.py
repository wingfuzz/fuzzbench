

from process import popen
from config import *

def check_base_image_exist() -> bool:
    """ 检查基础镜像是否存在

    Returns:
        bool: 存在则为真， 不存在则为假
    """
    code, ret = popen('docker images --format "{{.Repository}}"')
    if code:
        return False
    out_lines = ret.split("\n")
    for line in out_lines:
        if line == BASE_IMAGE_NAME:
            return True
        else:
            pass 
    return False



