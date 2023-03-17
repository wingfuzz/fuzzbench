from logger import logger

import argparse
from utils import compression_work_dir_code
from config import SHARED_DIR
from runDocker import run_docker
from process import popen

def main():
    logger.info("start.")
    parser = argparse.ArgumentParser(description='Open source fuzzbench')
    parser.add_argument("-f", "--fuzzers", nargs='+', type=str, required=False, default=[], help="fuzzers list")
    parser.add_argument("-t", "--fuzz_targets", nargs='+', type=str, required=False, default=[], help="fuzz target project names")
    parser.add_argument("-r", "--rebuild", type=str, required=False, default="OFF", help="rebuild images (ON | OFF)")
    parser.add_argument("-c", "--cpus", type=int, required=False, default=2, help="Number of CPUs. Number is a fractional number. 0.000 means no limit.")
    parser.add_argument("-m", "--memory", type=str, required=False, default="4G", help="Memory limit (format: <number>[<unit>]). Number is a positive integer. Unit can be one of b, k, m, or g. Minimum is 6M.")
    parser.add_argument("-v", "--volume", type=str, required=False, default=SHARED_DIR, help="""The shared directory where the output is collected""")
    parser.add_argument("-st", "--stop_timeout", type=int, required=False, default=300, help="""Docker container run timeout""")
    
    args, other_args = parser.parse_known_args()
    # if len(args.fuzzers) == 0:
    #     logger.info("Please input fuzzer")
    #     parser.print_help()
    #     return 1
    
    # if len(args.fuzz_targets) == 0:
    #     logger.info("Please input fuzz target projects")
    #     parser.print_help()
    #     return 1
    
    compression_work_dir_code()
    #popen("python3 stopDocker.py")
    run_docker(args.fuzzers, args.fuzz_targets, args.rebuild, args.cpus, args.memory, args.stop_timeout)
    #logger.info("Fuzzbench run end.")
    
    
    

if __name__ == "__main__":
    main()
