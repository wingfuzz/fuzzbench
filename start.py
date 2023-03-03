from logger import logger
from process import popen
from config import *


def build_base_image() -> int:
    """ 构建一个基础镜像，后续镜像皆依赖于此
    Returns:
        int: 成功返回0 失败返回1
    """
    logger.info("build base image start.")
    base_image_name = os.path.join(DOCKER_IMAGE_BASE_TAG, "base-image")
    docker_file_path =  os.path.join(ROOT_DIR_PATH, "docker")
    docker_file = os.path.join(docker_file_path, "Dockerfile")
    code, _ = popen(f"docker build --file {docker_file} --tag {base_image_name} {docker_file_path}")
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


def main():
    logger.info("start.")
    if (build_base_image()):
        exit(1)

    build_fuzz_target_image("afl", "bloaty_fuzz_target")






if __name__ == "__main__":
    main()
