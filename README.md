# 分词

### 能够实现如下功能：
1. 根据词典和词典中的词性 进行正向和反向的最大匹配，
2. 根据能够自动把英文数字和连接符下划线在没有词典的情况下最大的匹配出阿里
3. 返回分词后的结果包含词语、词性（如果有词性的话）

### 如何实现
0. 对句子根据自定义的词典 按照正向反向最大匹配进行配
1. 先提取文本中的英文和数字
2. 对文本中除了英文和数字的内容进行分词

### 使用示例
```python
from lib.cut_sentence import  cut_sentence

if __name__ == '__main__':
    #Knowledge Graph，TBD云集中心在词典中，hello-world不在词典中
    s = "Knowledge Graph在TBD云集中心，hello-world"
    ret=  cut_sentence(s)
    print(ret)
```
### 返回结果分析
返回结果为

```
[('Knowledge Graph', 'cymc'), ['在'], ('TBD云集中心', 'jgmc'), ['，'], ('hello-world', 'A')]
```
其中

```
类型：列表
元素类型：
    列表：非核心词，用结巴切出，长度为1
    元组：标识匹配出的核心词，比如机构名称（jgmc），纯数字（N），数字+字母（A) ，长度为2

```