## 功能特性
* 基于自然语言处理工具ltp构建的GWT2RUCM转换工具
* 支持导入领域背景信息，具体可为分词词典和词性标注词典
* 分词词典本身是一个文本文件（plain text），每行指定一个词，编码须为 UTF-8，样例如下所示
>苯并芘<br>亚硝酸盐
* 词性标注词典同样为一个UTF-8文本文件，每行指定一个词，第一列指定单词，第二列之后指定该词的候选词性（可以有多项，每一项占一列），列与列之间用空格区分。示例如下
>雷人 v a<br>】 wp
## 使用说明
* ltp_data文件夹保存ltp模型，由于模型文件较大未随代码附上，可以[点击这里下载](https://pan.baidu.com/share/link?shareid=1988562907&uk=2738088569#list/path=%2Fltp-models&parentPath=%2F)
* 运行run.py并传入参数
>python run.py [-s segdict] [-p posdict] -i gwtfile

其中<br>-s 指定分词词典文件segdict<br>-p 指定词性标注词典文件posdict<br>-i 指定待转换的GWT文件gwtfile<br>对转换的中间结果及最终结果文件会给出提示，如
> ./1548036141.839682.taggedout<br>./1548036143.316624.taggedout<br>./1548036143.509132.taggedout<br>./1548036143.512663.rucmout

其中.taggedout为中间结果，.rucmout为最终输出，均为UTF-8文本文件。
* 更多关于ltp的说明可以参照https://pyltp.readthedocs.io/zh_CN/develop/api.html
