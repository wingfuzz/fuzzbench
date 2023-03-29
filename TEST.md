1. 从 https://dev.shuimuyulin.com/liuyingchao/opensourcefuzzbench 下载测试脚本：

   ```
   git clone git@dev.shuimuyulin.com:liuyingchao/opensourcefuzzbench.git
   ```

2. 挑选一个项目，将自己的名字记在最左边，防止大家选重了。

3. 将这个项目右边所有的docker镜像下载下来，例如：

   ````
   docker pull dev.shuimuyulin.com/fuzzbench/aflplusplus_freetype2-2017
   docker pull ...
   ````

4. 进入项目目录，启动脚本：

   ```bash
   python3 start.py \
       -f afl aflplusplus libfuzzer eclipser honggfuzz coverage \
       -t freetype2-2017
   ```

   其中`-f`参数后的列表需要跟表格中存在的镜像匹配，有些镜像缺失，启动脚本中，就不写对应的fuzzer。例如`libxml2-v2.9.2`项目缺少`afl`的镜像，`-f`参数后面就不写`afl`。

   `-t`参数后是你选择的项目。

5. 启动后，应该有和-f参数列表相同的docker容器，定期查看一下他们是否是UP状态。启动后，当前目录下会出现一个output目录，里面有fuzzer的列表，请检查列表是否完整。其中./output/coverage目录是第10分钟才会出现。里面会有两个csv，其中每一行是这个样子：`2023-03-29 13:12:54.021472,honggfuzz,freetype2-2017,25363,184256,13.77`，这个数据是我们最终需要的数据，请确认10分钟后确实出现了这个文件。如果有问题，联系英超。

6. 项目需要执行24小时，大家只要放后台运行着即可。结束时间不需要精确控制，多跑了也没关系，结束后将output目录打包发送给英超。注意，output目录是root权限的，如果你不是root用户，可能会出现某些文件缺少权限读不出来的问题。使用root打包即可。