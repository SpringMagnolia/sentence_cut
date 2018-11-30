'''
切分句子
返回结果：[('Knowledge Graph', 'cymc'), ['在'], ('TBD云集中心', 'jgmc')]
类型：列表
元素类型：
    列表：非核心词，用结巴切出，长度为1
    元组：标识匹配出的核心词，比如课程名（kc），纯数字（N），数字+字母（A) ，长度为2

'''

import re
import jieba
import os
from .mm import MCut

__abs_path = os.path.split(os.path.abspath(__file__))[0]

# jieba.load_userdict("./词典/课程名词_kc.txt")

_re_match_number = re.compile("\d+")
_re_match_letter_number = re.compile("[a-zA-Z0-9_\-/]+",re.S)

def extract_letter_number_from_sentence(sentence):
    ret_findall = _re_match_letter_number.findall(sentence)
    ret_split = _re_match_letter_number.split(sentence)
    # print(ret_split)
    # print(ret_findall)
    assert len(ret_split)-1 == len(ret_findall),"split之后的结果减去1:{} 应该和查到到的结果：{}相同".format(len(ret_split)-1,len(ret_findall))
    _list = []
    for i in range(len(ret_split)-1):
        if ret_findall[i]!="":
            _list.append([ret_split[i]])
        _found_str = [ret_findall[i]]
        _found_str.append("N" if ret_findall[i].isdigit() else "A")
        _found_str = tuple(_found_str)  #tuple 表示是英文和数字，后续进行命名体识别时候进行替换
        _list.append(_found_str)
    if ret_split[-1] != "":
        _list.append([ret_split[-1]])
    return _list

def load_user_dict(path="./词典"):
    file_list = [os.path.join(path,i) for i in os.listdir(path)]
    total_lines = []
    [total_lines.extend(open(file).readlines()) for file in file_list]
    user_dict = {}
    for i in total_lines:
        # print(i.split())
        if len(i.strip())>=1:
            user_dict[i.rsplit(maxsplit=1)[0].strip().lower()]=i.rsplit(maxsplit=1)[1].strip()
    return user_dict


def mm_rmm_match(sentence,user_dcit):
    """
    调用正向、反向最大匹配方法进行名词的匹配
    :param sentence:
    :param user_dcit:
    :return:
    """
    print(user_dcit)
    window_size = max([len(i) for i in user_dcit])
    if len(sentence)<window_size:
        window_size = len(sentence)
    m_cut = MCut(user_dcit,window_size)
    ret = m_cut.cut(sentence)
    print("mm_rmm_match_ret:",ret)
    return ret


def cut_sentence(sentence):
    '''
    对文本进行分词
    0. 对句子根据自定义的词典 按照正向反向最大匹配进行配
    1. 先提取文本中的英文和数字
    2. 对文本中除了英文和数字的内容进行分词
    :param sentence:
    :return:
    '''
    #0. 对句子根据自定义的词典 按照正向反向最大匹配进行配
    user_dict_path = "../词典"
    user_dict_path = os.path.join(__abs_path,user_dict_path)
    user_dict = load_user_dict(user_dict_path)
    mm_cut_ret = mm_rmm_match(sentence,user_dict)

    #1. 先提取文本中的英文和数字
    cut_ret = []
    for i in mm_cut_ret:
        if isinstance(i,tuple):
            cut_ret.append(i)
        elif isinstance(i,list):
            assert len(i) == 1, "未匹配到的字符列表中只有一个元素"

            #extracted_letters_sentence: [['我的微信是'], ('Ws23sf9', 'A'), ['，我的电话是'], ('13146128763', 'N')]
            extracted_letters_sentence = extract_letter_number_from_sentence(i[0])
            cut_ret += extracted_letters_sentence

    #2.对文本中除了英文和数字的内容进行分词
    final_cut_ret = []
    for i in cut_ret:
        if isinstance(i,tuple):
            final_cut_ret.append(i)
        elif isinstance(i,list):
            assert len(i) == 1, "未匹配到的字符列表中只有一个元素"
            jieba_cut_ret = [[i] for i in jieba.cut(i[0])]
            final_cut_ret += jieba_cut_ret
    return final_cut_ret


if __name__ == '__main__':
    text  = "我的微信是Ws23sf9，我的电话是13146128763，我想从事UI/UE设计"
    # text = "我想了解人工智能+Python这个学科的学费"
    # text = "你好，世界"
    # print(text)
    ret  = cut_sentence(text)
    print(ret)
    # print(__abs_path)

