from logger import logger
from buildImages import build_images
import argparse


def main():
    logger.info("start.")
    parser = argparse.ArgumentParser(description='Open source fuzzbench')
    parser.add_argument("-f", "--fuzzers", nargs='+', type=str, default=[], help="fuzzers list")
    parser.add_argument("-t", "--fuzz_targets", nargs='+', type=str, default=[], help="fuzz target project names")
    parser.add_argument("-r", "--rebuild", type=str, required=False, default="ON", help="rebuild images (ON | OFF)")
    args, other_args = parser.parse_known_args()
    if len(args.fuzzers) == 0:
        logger.info("Please input fuzzer")
        parser.print_help()
        return 1
    
    if len(args.fuzz_targets) == 0:
        logger.info("Please input fuzz target projects")
        parser.print_help()
        return 1
    
    build_images(args.fuzzers, args.fuzz_targets, args.rebuild)
    
    

if __name__ == "__main__":
    main()
