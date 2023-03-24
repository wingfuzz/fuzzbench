from logger import logger
from process import popen
from config import *
from utils import check_image_exist 
import multiprocessing
from typing import List

def build_base_image(rebuild:str) -> int:
    """ 构建一个基础镜像，后续镜像皆依赖于此
        rebuild (str): 是否重新构建镜像
    Returns:
        int: 成功返回0 失败返回1
    """
    logger.info("build base image start.")
    docker_file_path =  os.path.join(ROOT_DIR_PATH, "docker")
    docker_file = os.path.join(docker_file_path, "Dockerfile")
    if rebuild == "OFF" and check_image_exist(BASE_IMAGE_NAME):
        return 0
    code, _ = popen(f"docker build --file {docker_file} --tag {BASE_IMAGE_NAME} {docker_file_path}")
    if code == 0 :
        logger.info("build base image success.")
    else:
        logger.error("build base image failed.")
    return code


def build_fuzzer_image(fuzzer:str, rebuild:str) -> int:
    """ 构建一个 fuzzer 镜像
    Args:
        fuzzer (str): 模糊测试器的名字
        rebuild (str): 是否重新构建镜像
    Returns:
        int: 成功返回0 失败返回1
    """
    logger.info(f"build fuzzer {fuzzer} image start.")
    fuzzer_image_name = os.path.join(DOCKER_IMAGE_BASE_TAG, fuzzer)
    if rebuild == "OFF" and check_image_exist(fuzzer_image_name):
            return 0
    docker_file_path =  os.path.join(ROOT_DIR_PATH, "fuzzers", fuzzer)
    docker_file = os.path.join(docker_file_path, "Dockerfile")
    code, _ = popen(f"docker build -t {fuzzer_image_name} --file {docker_file} {docker_file_path}")
    if code == 0 :
        logger.info(f"build fuzzer {fuzzer} image success.")
    else:
        logger.error(f"build fuzzer {fuzzer} image failed.")
    return code


def build_fuzz_target_image(fuzzer:str, target_project:str, rebuild:str) -> int:
    """ 构建被测项目的镜像
    Args:
        fuzzer (str): 模糊测试器的名字
        target_project (str): 被测项目的名字
        rebuild (str): 是否重新构建镜像
    Returns:
        int: 成功返回0 失败返回1
    """
    image_name = os.path.join(DOCKER_IMAGE_BASE_TAG, f"{fuzzer}_{target_project}")
    logger.info(f"build fuzz target image {image_name} start.")
    if rebuild == "OFF" and check_image_exist(image_name):
            return 0
    docker_file_path =  os.path.join(ROOT_DIR_PATH, "benchmarks", target_project)
    docker_file = os.path.join(docker_file_path, "Dockerfile")
    fuzzer_image_name = os.path.join(DOCKER_IMAGE_BASE_TAG, fuzzer)
    code, _ = popen(f"docker build -t {image_name} --file {docker_file} \
                    --build-arg parent_image={fuzzer_image_name} \
                    {docker_file_path}")
    if code == 0 :
        logger.info(f"build fuzz target image {image_name} success.")
    else:
        logger.error(f"build fuzz target image {image_name} failed.")
    return code


def build_fuzz_images(fuzzers:List[str], fuzz_targets:List[str], rebuild:str) -> int:
    """ 构建 所有 fuzz 镜像

    Args:
        fuzzers (List[str]): 模糊测试器的列表
        fuzz_targets (List[str]): 被测项目的列表
        rebuild (str): 是否重新构建镜像

    Returns:
        int: 成功返回0 失败返回1
    """
    target_args = [(fuzzer, target) for fuzzer in fuzzers for target in fuzz_targets]
    print("build:", target_args)
    if build_base_image(rebuild):
        return 1
    
    print("build fuzzers")
    for fuzzer in fuzzers:
        if build_fuzzer_image(fuzzer, rebuild):
            return 1
        
    print("build projects")
    for target in fuzz_targets:
        if build_fuzz_target_image(fuzzer, target, rebuild):
            return 1
