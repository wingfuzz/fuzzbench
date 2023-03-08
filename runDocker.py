from logger import logger
from process import popen, timeout_popen
from config import * 
from buildImages import build_fuzz_target_image, build_fuzzer_image, build_base_image
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

    if build_base_image(rebuild):
        return 1
    
    if not os.path.exists(SHARED_DIR):
        os.mkdir(SHARED_DIR)

    container_list = []
    for fuzzer in fuzzers:
        if (build_fuzzer_image(fuzzer, rebuild)):
            exit(1)
        for target in fuzz_targets:
            if build_fuzz_target_image(fuzzer, target, rebuild):
                exit(1)
            container_name = f"{fuzzer}_{target}"
            image_name = os.path.join(DOCKER_IMAGE_BASE_TAG, container_name)
            if check_image_exist(image_name):
                code, out = popen(f"docker run -d --rm --name {container_name} --cpus {cpus} --memory {memory} --volume {SHARED_DIR}:{SHARED_DIR} {image_name}")
                if code != 0:
                    exit(code)
                container_list.append([container_name, str(time.time()), str(stop_timeout)])
                
            else:
                logger.error(f"Can not find {image_name} image.")
                exit(1)
    writeCsv(DOCKER_CONTAINER_CSV, container_list)