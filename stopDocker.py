from process import popen
from config import *
from utils import readCsv, writeCsv
import time 
import asyncio


async def stop_container() -> None:
    """ 检查容器运行时长，超时则停止运行
    """
    res = readCsv(DOCKER_CONTAINER_CSV)
    if len(res) == 0:
        print("Not container in running")
        exit(0)
    new_data = []
    for row in res:
        if (time.time() - float(row[1])) > int(row[2]):
            container_name = row[0]
            code, _ = popen(f'docker stop {container_name}')
            if code:
                exit(code)
        else:
            new_data.append(row)
    writeCsv(DOCKER_CONTAINER_CSV, new_data)
    await asyncio.sleep(5)
    await stop_container()
    
    
async def main():
    task = asyncio.create_task(stop_container())
    await task


if __name__ == "__main__":
    asyncio.run(main())