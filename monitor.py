import asyncio
import time
import os

async def monitor_dir():
    stats = os.stat(os.getcwd())
    print(stats.st_mtime)
    print(time.time())
    await asyncio.sleep(5)
    await monitor_dir()
    

async def main():
    task = asyncio.create_task(monitor_dir())
    await task


if __name__ == "__main__":
    asyncio.run(main())
