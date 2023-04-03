from logger import logger
from process import popen, timeout_popen
from config import * 
from buildImages import build_fuzz_images
from utils import check_image_exist, writeCsv
import time 
from typing import List 


def run_docker_build(fuzzers:List[str], fuzz_targets:List[str], rebuild:str) -> None:
    
    if not os.path.exists(SHARED_DIR):
        os.mkdir(SHARED_DIR)

    run_images = {}
    for fuzzer in fuzzers:
        for target in fuzz_targets:
            container_name = f"{fuzzer}_{target}"
            image_name = os.path.join(DOCKER_IMAGE_BASE_TAG, container_name)
            run_images[container_name] = image_name
    
    build_fuzz_images(fuzzers, fuzz_targets, rebuild)


def run_docker_fuzz(fuzzers:List[str], fuzz_targets:List[str], cpus:float, memory:str) -> None:
    if not os.path.exists(SHARED_DIR):
        os.mkdir(SHARED_DIR)

    run_images = {}
    for fuzzer in fuzzers:
        for target in fuzz_targets:
            container_name = f"{fuzzer}_{target}"
            image_name = os.path.join(DOCKER_IMAGE_BASE_TAG, container_name)
            run_images[container_name] = image_name

    for c in run_images.keys():
        container_name = c 
        image_name = run_images[c]
        if "coverage" in container_name:
            pass 
        else:
            if check_image_exist(image_name):
                code, _ = popen(f"docker run -d --name {container_name} --cpus {cpus} --memory {memory} --volume $PWD/output:{SHARED_DIR} {image_name} /bin/bash /run_fuzz.sh")
                if code != 0:
                    exit(code)
            else:
                print(f"Can find image {image_name}")

    if "coverage" in fuzzers:
        for t in fuzz_targets:
            image_name = os.path.join(DOCKER_IMAGE_BASE_TAG, f"coverage_{t}")
            if check_image_exist(image_name):
                code, _ = popen(f"docker run -d --name coverage_{t} --cpus {cpus} --memory {memory} --volume $PWD/output:{SHARED_DIR} {image_name} /bin/sh /run_monitor.sh")
                if code != 0:
                    exit(code)
            else:
                print(f"Can find image {image_name}")
