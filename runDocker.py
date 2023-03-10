from logger import logger
from process import popen, timeout_popen
from config import * 
from buildImages import build_fuzz_images, build_coverage_images
from utils import check_image_exist, writeCsv
import time 


def run_docker(fuzzers:list[str], fuzz_targets:list[str], rebuild:str, cpus:float, memory:str, stop_timeout:int) -> None:
    """ 运行 docker 构建镜像，运行镜像

    Args:
        fuzzers (list[str]): 模糊测试器的列表
        fuzz_targets (list[str]): 被测项目的列表
        rebuild (str): 是否重新构建镜像
        cpus (float): 容器所需的cpu数目
        memory (str): 容器所需的内存
        stop_timeout (int): 容器运行的时间, 单位 秒

    Returns:
        None : 中间步骤出错则退出 
    """

    if not os.path.exists(SHARED_DIR):
        os.mkdir(SHARED_DIR)

    run_images = {}
    for fuzzer in fuzzers:
        for target in fuzz_targets:
            container_name = f"{fuzzer}_{target}"
            image_name = os.path.join(DOCKER_IMAGE_BASE_TAG, container_name)
            run_images[container_name] = image_name

    build_fuzz_images(fuzzers, fuzz_targets, rebuild)
    #build_coverage_images(fuzz_targets, rebuild)

    for c in run_images.keys():
        container_name = c 
        image_name = run_images[c]
        if "coverage" in container_name:
            pass 
        else:
            code, _ = popen(f"docker run -d --rm --name {container_name} --cpus {cpus} --memory {memory} --volume {SHARED_DIR}:{SHARED_DIR} {image_name} /bin/sh /run_fuzz.sh")
            if code != 0:
                exit(code)



    for t in fuzz_targets:
        image_name = os.path.join(DOCKER_IMAGE_BASE_TAG, f"coverage_{t}")
        code, _ = popen(f"docker run -d --rm --name coverage_{t} --cpus 1 --memory 1G --volume {SHARED_DIR}:{SHARED_DIR} --volume /root/opensourcefuzzbench:/work/fuzzbench {image_name} /bin/sh /run_monitor.sh")
        if code != 0:
            exit(code)
        

