
from subprocess import Popen, PIPE, SubprocessError, TimeoutExpired
from typing import Tuple, Union, List
from logger import logger
import os 
import signal

def timeout_popen(command:str, timeout:float) -> Tuple[int, str]:
    """执行一个带有时间限制的指令"""
    p = Popen(f"{command} &", shell=True, preexec_fn=os.setsid)
    try:
        p.wait(timeout=timeout)
        return 0, '{} is completed'.format(command)
    except TimeoutExpired as te:
        print(te)
        os.killpg(os.getpgid(p.pid), signal.SIGKILL)
        return 0, '{} execution timed out'.format(command)

def popen_with_output(command: str, input:Union[bytes,None]=None, timeout:Union[None, float]=None) -> Tuple[int, str]:
    """创建一个子进程执行一个指令"""
    if timeout:
        return timeout_popen(command, timeout)
    try:
        logger.info('Command: {}, input: {}'.format(command, input))
        p = Popen(command, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)   
        stdout, stderr = p.communicate(input=input)
        logger.info('Command finished: {}'.format(p.returncode))
        if stderr:
            out = stderr.decode("utf-8")
            out_lines = out.split("\n")
            for line in out_lines:
                logger.error('Status: {} output: {}'.format(1, line))
            return 1, out
        out = stdout.decode("utf-8")
        out_lines = out.split("\n")
        for line in out_lines:
            logger.info('Status: {} output: {}'.format(0, line))
        return 0, out
    except SubprocessError as spe:
        logger.error(spe)
        return 1, spe

def popen(command: str, input:Union[bytes,None]=None, timeout:Union[None, float]=None) -> Tuple[int, str]:
    """创建一个子进程执行一个指令"""
    if timeout:
        return timeout_popen(command, timeout)
    try:
        logger.info('Command: {}, input: {}'.format(command, input))
        p = Popen(command, stdout=None, stdin=PIPE, stderr=None, shell=True)   
        p.communicate(input=input)
        logger.info('Command finished: {}'.format(p.returncode))
        return p.returncode, None
        # if stderr:
        #     out = stderr.decode("utf-8")
        #     out_lines = out.split("\n")
        #     for line in out_lines:
        #         logger.error('Status: {} output: {}'.format(1, line))
        #     return 1, out
        # out = stdout.decode("utf-8")
        # out_lines = out.split("\n")
        # for line in out_lines:
        #     logger.info('Status: {} output: {}'.format(0, line))
        # return 0, out
    except SubprocessError as spe:
        logger.error(spe)
        return 1, spe


def test_popen():
    popen("ls -l", input=b'')


if __name__ == "__main__":
    test_popen()
