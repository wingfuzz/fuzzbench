
import logging


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('fuzzbench')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


def test_log() -> None:
    logger.info("test info")
    logger.debug("debug test")
    logger.warning("warning test")
    logger.error("error test")
    logger.critical("critical test")


if __name__ == "__main__":
    test_log()