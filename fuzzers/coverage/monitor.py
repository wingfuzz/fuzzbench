import asyncio
import os
from config import SHARED_DIR
import re
from process import popen
from datetime import datetime


async def write_coverage(fuzzer:str, cov:tuple[str]):
    with open(os.path.join(SHARED_DIR, "coverage", "coverage.txt"), mode="a+", encoding="utf-8") as f:
        project = os.environ["FUZZ_PROJECT"]
        current_dt = datetime.now()
        row = f"{current_dt},{fuzzer},{project}," + ",".join(cov) + "\n"
        f.write(row) 


async def get_coverage(fuzzer, stdout:str):
    print(stdout)
    pattern = re.compile(r'[\s\S]*A coverage of (\d+) edges were achieved out of (\d+) existing \((\d+.\d+)%\) with \d+ input files')
    print(pattern.match(stdout))
    print(pattern.match(stdout).groups())
    await write_coverage(fuzzer, pattern.match(stdout).groups())


async def monitor_queue(fuzzer, output_path:str):
    """ 监控case目录
    Args:
        output_path (str): 需要监控的目录
    """
    code, out = popen(f"/afl/afl-showmap -C -i {output_path} -o /dev/null -- fuzz-target @@")
    if code == 0:
        await get_coverage(fuzzer, out)
    await asyncio.sleep(60)
    await monitor_queue(fuzzer, output_path)


async def write_crashe(fuzzer:str, crashe_number:int):
    with open(os.path.join(SHARED_DIR, "coverage", "crashe.txt"), mode="a+", encoding="utf-8") as f:
        project = os.environ["FUZZ_PROJECT"]
        current_dt = datetime.now()
        row = f"{current_dt},{fuzzer},{project}," + str(crashe_number) + "\n"
        f.write(row) 


async def monitor_crashes(fuzzer, output_path:str):
    """ 监控crashe目录
    Args:
        output_path (str): 需要监控的目录
    """
    ls = os.listdir(output_path)
    await write_crashe(fuzzer, len(ls))
    await asyncio.sleep(60)
    await monitor_crashes(fuzzer, output_path)


async def main():
    coverage_path = os.path.join(SHARED_DIR, "coverage")
    if not os.path.exists(coverage_path):
        os.mkdir(coverage_path)
    
    fuzzers_output = os.listdir(SHARED_DIR)
    print(fuzzers_output)
    futures = []
    for fuzzer in fuzzers_output:
        if (fuzzer == "coverage"):
            continue

        monitor_queue_dir = os.path.join(SHARED_DIR, fuzzer, os.environ["FUZZ_PROJECT"], "output", "queue")
        if os.path.exists(monitor_queue_dir):
            futures.append(monitor_queue(fuzzer, monitor_queue_dir))

        monitor_crashe_dir = os.path.join(SHARED_DIR, fuzzer, os.environ["FUZZ_PROJECT"], "output", "crashes")
        if os.path.exists(monitor_crashe_dir):
            futures.append(monitor_crashes(fuzzer, monitor_crashe_dir))
        
    await asyncio.gather(*futures)


if __name__ == "__main__":
    asyncio.run(main())
