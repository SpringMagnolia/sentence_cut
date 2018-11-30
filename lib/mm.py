"""
正向和逆向最大匹配方法
"""

# Maximum Match Method 最大匹配法

class MM:
    def __init__(self,dict,window_size):
        self.dict = dict
        self.window_size = window_size

    def cut(self, text):
        result = []
        index = 0
        text_lenght = len(text)

        not_matched = ""
        while text_lenght > index:
            # range(3,0,-1)
            # print(self.window_size,index,index)
            for size in range(self.window_size + index, index, -1): #从大到小
                piece = text[index:size]
                # print("size:", size, piece)
                if piece.lower() in self.dict:

                    piece = tuple([piece,self.dict[piece.lower()]])
                    # piece = tuple([piece,"NE"])
                    index = size - 1  #匹配到结果
                    break
            index = index + 1  # 没有匹配到index+1，匹配到了index
            if isinstance(piece,tuple): #如果匹配到内容
            # piece = piece if isinstance(piece,tuple) else [piece]
                if len(not_matched)>=1: #先把not_matched中长度大于0的值放入result中
                    result.append([not_matched])
                    not_matched = ""  #之后设置为空
                result.append(piece) #添加匹配到的结果
            else:  #没有匹配到不停的天啊及
                not_matched+=piece

        if len(not_matched) >= 1:  #最后的文本添加到结果中
            result.append([not_matched])
        # print(result)
        return result


# RMM:Reverse Maxmium Match method 逆向最大匹配

class RMM:
    def __init__(self,dict,window_size):
        self.window_size = window_size
        self.dict = dict

    def cut(self, text):
        result = []
        index = len(text)
        not_matched = ""
        while index > 0:
            for size in range(index - self.window_size, index):
                piece = text[size:index]
                # print("size:", size, piece)
                if piece.lower() in self.dict:
                    index = size + 1
                    piece = tuple([piece,self.dict[piece.lower()]])
                    # piece = tuple([piece,"NE"])
                    break
                # print("index:", index)

            index = index - 1
            if isinstance(piece,tuple):
                if len(not_matched)>=1:
                    result.append([not_matched[::-1]])
                    not_matched = ""
                result.append(piece)
            else:
                not_matched+=piece


        if len(not_matched) >= 1:
            result.append([not_matched[::-1]])
        result.reverse()
        # print(result)
        return result


class MCut():
    def __init__(self,dict,window_size):
        """
        最大匹配和逆向最大匹配
        :param dict: {"词语":"标识",...}
        :param window_size: 最大的窗口长度，默认等于词典中最大的词语长度，如果句子长度短，则是句子的长度
        """
        self.mm = MM(dict,window_size)
        self.rmm = RMM(dict,window_size)

    def cut(self, sentence):
        """
        1. 词语数量不相同，选择分词后词语数量少的
        2. 如果词语数量相同，返回单字数量少的
        :param sentence:
        :return: [(词组,标识),[未匹配到的句子]]
        """
        mm_ret = self.mm.cut(sentence)
        rmm_ret = self.rmm.cut(sentence)
        return mm_ret if len(mm_ret) < len(rmm_ret) else rmm_ret


if __name__ == '__main__':
    user_dict = {'qq': 'cymc', 'wx': 'cymc', '微信': 'cymc', 'Knowledge Graph': 'cymc', 'TBD云集中心': 'jgmc'}
    text = 'Knowledge Graph在tbd云集中心'
    mm = MM(user_dict,window_size=len("Knowledge Graph"))
    # mm = RMM()
    ret = mm.cut(text)
    print(ret)
    # rmm = RMM()
    # rmm.cut(text)
    # mcut = MCut()
    # ret = mcut.cut(text)
    # print(ret)