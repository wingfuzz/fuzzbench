# OpenSourceFuzzBench
## 构建镜像
```
python3 build.py -f <FUZZERS ...> -t <TARGETS ...>
```

FUZZERS是要构建的模糊测试器列表，有以下的选项：
`afl`, `aflplusplus`, `libfuzzer`, `honggfuzz`, `eclipser`, `coverage`

TARGETS是要构建的项目列表，可以从下面的测试项目中选择。

FUZZERS 和 TARGETS 都可以是多个，构建的时候会进行排列组合，例如，选择了2个fuzzers，5个targets，则一共会构建10个镜像。（除此之外，还有一个基础镜像，每个fuzzer一个模糊测试器镜像）

构建出的镜像名称为：`dev.shuimuyulin.com/fuzzbench/{fuzzer}_{target}`，例如`dev.shuimuyulin.com/fuzzbench/afl_freetype2-2017`。

* 构建镜像过程需要用到Ubuntu和Pypi软件源，如果默认软件源安装速度过慢，可以在config.py中设置

* 构建出的镜像前缀可以在config.py中设置

## 运行测试
```
python3 test.py -f <FUZZERS ...>-t <TARGETS ...>
```
### 全部运行的例子
```
python3 test.py -f afl aflplusplus coverage eclipser honggfuzz libfuzzer -t bloaty_fuzz_target curl_curl_fuzzer_http freetype2-2017 harfbuzz-1.3.2 jsoncpp_jsoncpp_fuzzer lcms-2017-03-21 libjpeg-turbo-07-2017 libpcap_fuzz_both libpng-1.2.56 libxml2-v2.9.2 mbedtls_fuzz_dtlsclient openssl_x509 openthread-2019-12-23 php_php-fuzz-parser proj4-2017-08-14 re2-2014-12-09 sqlite3_ossfuzz systemd_fuzz-link-parser vorbis-2017-12-11 woff2-2016-05-06 zlib_zlib_uncompress_fuzzer
```
启动列表中的测试，FUZZERS和TARGET和构建中的参数相同。注意，如果要收集覆盖率，则FUZZERS中必须包含`coverage`。启动的时候会在当前目录下创建output目录，其中包含了每个模糊测试器的输出结果。

## 测试项目
|项目|测试目标|字典|初始种子
|-|-|-|-|
|bloaty_fuzz_target|fuzz_target|无|94|
|curl_curl_fuzzer_http|curl_fuzzer_http|无|31|
|freetype2-2017|fuzz-target|无|2|
|harfbuzz-1.3.2|fuzz-target|无|58|
|jsoncpp_jsoncpp_fuzzer|jsoncpp_fuzzer|有|0|
|lcms-2017-03-21|fuzz-target|有|1|
|libjpeg-turbo-07-2017|fuzz-target|无|1|
|libpcap_fuzz_both|fuzz_both|无|0|
|libpng-1.2.56|fuzz-target|有|1|
|libxml2-v2.9.2|fuzz-target|有|0|
|mbedtls_fuzz_dtlsclient|fuzz_dtlsclient|无|1|
|openssl_x509|x509|有|2241|
|openthread-2019-12-23|fuzz-target|无|0|
|php_php-fuzz-parser|php-fuzz-parser|有|2782|
|proj4-2017-08-14|fuzz-target|有|44|
|re2-2014-12-09|fuzz-target|有|0|
|sqlite3_ossfuzz|ossfuzz|有|1258|
|systemd_fuzz-link-parser|fuzz-link-parser|无|6|
|vorbis-2017-12-11|fuzz-target|无|1|
|woff2-2016-05-06|fuzz-target|无|62|
|zlib_zlib_uncompress_fuzzer|zlib_uncompress_fuzzer|无|0|

## 基准测试方法

### 1.编译项目
    每一个测试项目将会编译成两个二进制文件：
        其一是用于模糊测试的二进制，每个模糊测试器的编译方式并不完全一致，插桩算法、边覆盖率算法也不完全一致，因此这个二进制用于模糊测试本身，但不会用来横向对比。
        其二是用于统计覆盖率的二进制，使用标准LLVM coverage-pc-guard的方式进行编译，每个二进制最终会有一个pc-guard的数量。这个数量是无冲突、标准化的，可以用来对不同测试器进行横向对比。

### 2.执行测试
    每个模糊测试器，对于每个测试项目，都会进行在【4核8G】环境上（是否需要定义标准硬件？），运行【4】个模糊测试器进行并行测试。每个测试持续【24】小时。

### 3.评估指标【准确性/性能/稳定性指标】
    收集覆盖率和BUG数量：在每个测试进行过程中，实时监控测试的输出目录，获取其已经发现的测试集。如果测试集中出现了新的测试样例，则会在覆盖率二进制上运行此样例，获取这个样例的覆盖率。计算方法为（已覆盖的边的数量/全部边的数量）。如果在运行此样例时，出现了崩溃，则记录为一次BUG。进行BUG去重。去重方式为获取BUG的调用堆栈，如果整个调用堆栈中出现了新的地址，则认为是新的BUG
    每【10分钟】，记录一次当前测试的覆盖率，用于后续打分计算。在测试完成时，记录总体覆盖率，用于后续打分计算。
    每【10分钟】，记录一次当前发现的去重后的错误数量，用于后续打分计算。在测试完成时，记录整体去重后的错误数量，用于后续打分计算。
    每【10分钟】，记录一次当前工具发生崩溃退出、无响应等稳定性问题的数量。发生问题后重启。


### 4.计算各个模糊测试器针对每个项目的性能指标性能指标由以下几个成分构成：

    a.全局覆盖率指标：测试完成时的整体覆盖率，用于评价模糊测试器的覆盖能力，范围为0~1，越高说明效果越好。
    b.【待完善：前期时间权重更高】时间平均覆盖率指标：首先计算每个时刻的权重，由于模糊测试的特点，前期发现速度比较快，越往后越慢。我们的权重也使用类似的方式，前期权重更高，后期权重更低。因此我们使用指数衰减公式来计算每个时刻的权重：

    其中t的单位为分钟，从0开始，每10分钟计算一个权重。其含义为每6小时（公式中的360，单位为分钟）权重下降一半。24小时最后时刻的权重仅为开始的16分之一。
    然后，使用每个时刻的权重，和每个时刻的覆盖率，计算加权平均数，即为时间平均覆盖率。

    c.全局BUG检出率指标：测试完成时的BUG检出率，用于评价模糊测试器检出能力，范围为0~1，越高说明效果越好。
    d.【待完善：前期时间权重更高】时间平均检出率指标：算法同时间平均覆盖率，只是对检出率指标进行加权平均

    e.稳定性指标：测试完成时的整体稳定性正常出现次数，除以时刻的数量（24*6=144），范围为0~1，越高说明效果越好。

### 5.计算每个项目的总分
#### 项目总分的范围为0~1，越高说明测试效果越好。
    
|项目|权重|
|-|-|
|准确性指标||	
|全局覆盖率|0.5|
|全局检出率|0.5|
|性能指标||	
|时间平均覆盖率|0.5|
|时间平均检出率|0.5|
|稳定性指标||
|稳定性正常率|1|


### 6.汇总项目得分
    由于每个项目的覆盖率、检出率基准值并不一致，不应当对所有项目的得分直接进行平均。我们选择了平均标准分的方式，对各个模糊测试器进行最终排名。具体操作方式如下：
    对于每一个项目，其项目总分最高的一个测试器，其得分为100。其余测试器的得分按此方式进行计算：【（当前测试器总分/最高的总分）*100】。这样，针对每个项目，都可以给每个测试器算一个标准分。
    然后，对于每个测试器，将其各个标准分算一个平均数，即为它最终的平均标准分。范围为0~100分，越高说明测试效果越好。