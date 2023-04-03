from logger import logger

import argparse
from utils import compression_work_dir_code
from config import SHARED_DIR
from runDocker import run_docker_build
from process import popen

def main():
    logger.info("start build")
    parser = argparse.ArgumentParser(description='Open source fuzzbench')
    parser.add_argument("-f", "--fuzzers", nargs='+', type=str, required=False, default=[], help="fuzzers list")
    parser.add_argument("-t", "--fuzz_targets", nargs='+', type=str, required=False, default=[], help="fuzz target project names")
    parser.add_argument("-r", "--rebuild", type=str, required=False, default="OFF", help="rebuild images (ON | OFF)")
    
    args, other_args = parser.parse_known_args()
    
    if len(args.fuzzers) == 0:
        logger.info("Please input fuzzer")
        parser.print_help()
        return 1
    
    if len(args.fuzz_targets) == 0:
        logger.info("Please input fuzz target projects")
        parser.print_help()
        return 1
    
    compression_work_dir_code()
    run_docker_build(True, args.fuzzers, args.fuzz_targets, args.rebuild)    

if __name__ == "__main__":
    main()
