from lib.cut_sentence import  cut_sentence


if __name__ == '__main__':
    #Knowledge Graph，TBD云集中心在词典中，hello-world不在词典中
    s = "Knowledge Graph在TBD云集中心，hello-world"
    ret=  cut_sentence(s)
    print(ret)