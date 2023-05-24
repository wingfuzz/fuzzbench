import os 

# 环境配置，可以根据实际环境情况进行修改
# 所有镜像的前缀
DOCKER_IMAGE_PREFIX = "dev.shuimuyulin.com/fuzzbench/"
# 构建镜像时，使用的Ubuntu镜像源
UBUNTU_MIRROR = "http://mirrors.aliyun.com/ubuntu/"
# 构建镜像时，使用的pypi镜像源
PYPI_MIRROR = "http://mirrors.aliyun.com/pypi/simple"
# 临时目录位置
SHARED_DIR = "/tmp/fuzzbench/"


#以下的配置项请不要修改
ROOT_DIR_PATH = os.getcwd()
DOCKER_CONTAINER_CSV = "docker_container.csv"
DOCKER_CONTAINER_CSV_HEADER = ["container name", "start time", "timeout"]
BASE_IMAGE_NAME = DOCKER_IMAGE_PREFIX + "base-image"
