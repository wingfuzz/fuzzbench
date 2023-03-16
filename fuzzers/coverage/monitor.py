import asyncio
import os
from config import SHARED_DIR
import re
from process import popen
from datetime import datetime


async def write_coverage(fuzzer:str, cov):
    with open(os.path.join(SHARED_DIR, "coverage", os.environ["FUZZ_PROJECT"], "coverage.txt"), mode="a+", encoding="utf-8") as f:
        project = os.environ["FUZZ_PROJECT"]
        current_dt = datetime.now()
        row = f"{current_dt},{fuzzer},{project}," + ",".join(cov) + "\n"
        f.write(row) 


async def get_coverage(fuzzer, stdout:str):
    print(stdout)
    pattern = re.compile(r'[\s\S]*A coverage of (\d+) edges were achieved out of (\d+) existing \((\d+.\d+)%\) with \d+ input files')
    print(pattern.match(stdout))
    cov = pattern.match(stdout)
    if cov != None:
        await write_coverage(fuzzer, cov.groups())


async def monitor_queue(fuzzer, output_path:str, fuzz_target:str):
    """ 监控case目录
    Args:
        output_path (str): 需要监控的目录
    """
    code, out = popen(f"/afl/afl-showmap -C -i {output_path} -o /dev/null -- {fuzz_target} @@")
    if code == 0:
        await get_coverage(fuzzer, out)


async def write_crashe(fuzzer:str, crashe_number:int):
    with open(os.path.join(SHARED_DIR, "coverage", os.environ["FUZZ_PROJECT"], "crashe.txt"), mode="a+", encoding="utf-8") as f:
        project = os.environ["FUZZ_PROJECT"]
        current_dt = datetime.now()
        row = f"{current_dt},{fuzzer},{project}," + str(crashe_number) + "\n"
        f.write(row) 


async def get_crashe(output_ls:str):
    """ bug去重

    Args:
        output_ls (str): 所有的case输出

    Returns:
        int : 去重后的数量
    """
    pattern = re.compile(r"([\s\S]+)\+0x([0-9a-fA-F]+)")
    problems = set()
    for i in output_ls:
        lines = i.split("\n")
        stacks = []
        for line in lines:
            bo = pattern.match(line)
            if bo != None:
                binary, offset = bo.groups()
                stacks.append([binary, offset])
        if len(stacks) != 0:
            problems.add(tuple(stacks))

    return len(problems)
            

async def monitor_crashes(fuzzer, fuzz_target, output_path:str):
    """ 监控crashe目录
    Args:
        output_path (str): 需要监控的目录
    """
    ls = os.listdir(output_path)
    output_ls = []
    for i in ls:
        case_path = os.path.join(output_path, i)
        code, out = popen(f"{fuzz_target} {case_path}")
        if code == 0:
            if len(out) != 0 and "Execution successful." not in out:
                output_ls.append(out)
        
    problem_number = await get_crashe(fuzzer, out)

    await write_crashe(fuzzer, problem_number)


async def run(crashes_output_path:str, coverage_output_path:str, fuzz_target:str):
    coverage_path = os.path.join(SHARED_DIR, "coverage")
    if not os.path.exists(coverage_path):
        os.mkdir(coverage_path)

    futures = []
    for fuzzer in os.listdir(SHARED_DIR):
        if fuzzer == "coverage":
            continue
        monitor_queue_dir = os.path.join(SHARED_DIR, fuzzer, os.environ["FUZZ_PROJECT"], coverage_output_path)
        if os.path.exists(monitor_queue_dir):
            futures.append(monitor_queue(fuzzer, monitor_queue_dir, fuzz_target))

        monitor_crashe_dir = os.path.join(SHARED_DIR, fuzzer, os.environ["FUZZ_PROJECT"], crashes_output_path)
        if os.path.exists(monitor_crashe_dir):
            futures.append(monitor_crashes(fuzzer, fuzz_target, monitor_crashe_dir))
        
    await asyncio.gather(*futures)



if __name__ == "__main__":
    asyncio.run(run("./output/crashes", "./output/queue", "/out/fuzz_target"))
