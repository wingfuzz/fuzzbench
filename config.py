
import os 

ROOT_DIR_PATH = os.getcwd()

DOCKER_IMAGE_BASE_TAG = 'dev.shuimuyulin.com/fuzzbench'

BASE_IMAGE_NAME = os.path.join(DOCKER_IMAGE_BASE_TAG, "base-image")

SHARED_DIR = "/tmp/fuzzbench/"

DOCKER_CONTAINER_CSV = "docker_container.csv"
DOCKER_CONTAINER_CSV_HEADER = ["container name", "start time", "timeout"]


