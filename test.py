from logger import logger

import argparse
from utils import compression_work_dir_code
from config import SHARED_DIR
from runDocker import run_docker_fuzz
from process import popen

def main():
    logger.info("start test")
    parser = argparse.ArgumentParser(description='Open source fuzzbench')
    parser.add_argument("-f", "--fuzzers", nargs='+', type=str, required=False, default=[], help="fuzzers list")
    parser.add_argument("-t", "--fuzz_targets", nargs='+', type=str, required=False, default=[], help="fuzz target project names")
    parser.add_argument("-c", "--cpus", type=int, required=False, default=2, help="Number of CPUs. Number is a fractional number. 0.000 means no limit.")
    parser.add_argument("-m", "--memory", type=str, required=False, default="2G", help="Memory limit (format: <number>[<unit>]). Number is a positive integer. Unit can be one of b, k, m, or g. Minimum is 6M.")
    
    args, other_args = parser.parse_known_args()
    # if len(args.fuzzers) == 0:
    #     logger.info("Please input fuzzer")
    #     parser.print_help()
    #     return 1
    
    # if len(args.fuzz_targets) == 0:
    #     logger.info("Please input fuzz target projects")
    #     parser.print_help()
    #     return 1
    
    run_docker_fuzz(args.fuzzers, args.fuzz_targets, args.cpus, args.memory)
    #logger.info("Fuzzbench run end.")
    
    
    

if __name__ == "__main__":
    main()
