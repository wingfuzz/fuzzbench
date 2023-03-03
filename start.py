from logger import logger
from process import popen
from config import *
from utils import check_base_image_exist 
import argparse

def build_base_image() -> int:
    """ 构建一个基础镜像，后续镜像皆依赖于此
    Returns:
        int: 成功返回0 失败返回1
    """
    logger.info("build base image start.")
    docker_file_path =  os.path.join(ROOT_DIR_PATH, "docker")
    docker_file = os.path.join(docker_file_path, "Dockerfile")
    code, _ = popen(f"docker build --file {docker_file} --tag {BASE_IMAGE_NAME} {docker_file_path}")
    if code == 0 :
        logger.info("build base image success.")
    else:
        logger.error("build base image failed.")
    return code


def build_fuzzer_image(fuzzer:str) -> int:
    """ 构建一个 fuzzer 镜像
    Args:
        fuzzer (str): 模糊测试器的名字
    Returns:
        int: 成功返回0 失败返回1
    """
    logger.info(f"build fuzzer {fuzzer} image start.")
    fuzzer_image_name = os.path.join(DOCKER_IMAGE_BASE_TAG, fuzzer)
    docker_file_path =  os.path.join(ROOT_DIR_PATH, "fuzzers", fuzzer)
    docker_file = os.path.join(docker_file_path, "Dockerfile")
    code, _ = popen(f"docker build -t {fuzzer_image_name} --file {docker_file} {docker_file_path}")
    if code == 0 :
        logger.info(f"build fuzzer {fuzzer} image success.")
    else:
        logger.error(f"build fuzzer {fuzzer} image failed.")
    return code


def build_fuzz_target_image(fuzzer:str, target_project:str) -> int:
    """ 构建被测项目的镜像
    Args:
        fuzzer (str): 模糊测试器的名字
        target_project (str): 被测项目的名字
    Returns:
        int: 成功返回0 失败返回1
    """
    if (build_fuzzer_image(fuzzer)):
        exit(1)

    image_name = os.path.join(DOCKER_IMAGE_BASE_TAG, f"{fuzzer}_{target_project}")
    logger.info(f"build fuzz target image {image_name} start.")
    docker_file_path =  os.path.join(ROOT_DIR_PATH, "benchmarks", target_project)
    docker_file = os.path.join(docker_file_path, "Dockerfile")
    fuzzer_image_name = os.path.join(DOCKER_IMAGE_BASE_TAG, fuzzer)
    code, _ = popen(f"docker build -t {image_name} --file {docker_file} \
                    --build-arg parent_image={fuzzer_image_name} \
                    --build-arg FUZZER={fuzzer} {docker_file_path}")
    if code == 0 :
        logger.info(f"build fuzz target image {image_name} success.")
    else:
        logger.error(f"build fuzz target image {image_name} failed.")
    return code


def build_images(fuzzers:list[str], fuzz_targets:list[str]) -> int:
    """构建所有镜像
    Args:
        fuzzers (list[str]): 模糊测试器的列表
        fuzz_targets (list[str]): 被测项目的列表

    Returns:
        int: 成功返回0 失败返回1
    """
    if not check_base_image_exist():
        if (build_base_image()):
            logger.error("Build base image failed.")
            exit(1)

    for fuzzer in fuzzers:
        for target in fuzz_targets:
            if build_fuzz_target_image(fuzzer, target):
                return 1
    return 0


def main():
    logger.info("start.")
    parser = argparse.ArgumentParser(description='Open source fuzzbench')
    parser.add_argument("-f", "--fuzzers", nargs='+', type=str, default=[], help="fuzzers list")
    parser.add_argument("-t", "--fuzz_targets", nargs='+', type=str, default=[], help="fuzz target project names")
    args, other_args = parser.parse_known_args()
    if len(args.fuzzers) == 0:
        logger.info("Please input fuzzer")
        parser.print_help()
        return 1
    
    if len(args.fuzz_targets) == 0:
        logger.info("Please input fuzz target projects")
        parser.print_help()
        return 1
    
    

if __name__ == "__main__":
    main()
