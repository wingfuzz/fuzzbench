

from process import popen
from config import *
import csv 
from typing import List

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
    popen(f"tar -zcvf {ROOT_DIR_PATH}/docker/fuzzbench.tar.gz .")


def unzip_work_dir_code():
    """ 解压缩项目代码
    """
    popen(f"tar -zxvf /work/fuzzbench.tar.gz /work")


def writeCsv(filename: str, data: List[List[str]]) -> None:
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, doublequote=True)
        writer.writerow(DOCKER_CONTAINER_CSV_HEADER)
        for i in data:
            writer.writerow(i)
       

def readCsv(filename: str) -> List[List[str]]:
    res:List[List[str]] = []
    with open(filename, 'r', newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, doublequote=True)
        header = reader.__next__()
        if header != DOCKER_CONTAINER_CSV_HEADER:
            raise ValueError("csv header is {} error. require {}".format(header, DOCKER_CONTAINER_CSV_HEADER))
        for row in reader:
            res.append(row)
    return res 