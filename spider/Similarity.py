import jieba


def remove_list():
    """
    将下列列表的中午符号过滤
    如果有缺失，可自行添加
    :return:
    """
    remove_list = ['，', '：', '。', '《', '》', '\n', '—', '“', '”', '、', ' ']
    return remove_list


def jieba_result(content):
    """
    获取jieba分词结果，并去掉中文符号
    :param content: 为read_file返回的文章内容
    :return:
    """
    res = jieba.lcut(content)
    for i in remove_list():
        while i in res:
            res.remove(i)
    # print(res)
    return res


def top_n(res, res_all, n):
    """
    获得分词的Top n 词频，得出词频向量
    :param res: jieba_res  安徽  jieba_res 国务院
    :param res_all: 合并后的报告
    :param n:
    :return:
    """
    dic = {}
    for i in res_all:
        if i not in res:
            dic[i] = 0
        else:
            dic[i] = res.count(i)

    sort_res = sorted(dic.items(), key=lambda x: x[1], reverse=True)  # 排序

    top_n = sort_res[:n]  # 获取Top n
    # print(top_n)
    top_n_res = []
    for i in top_n:
        top_n_res.append(i[1])
    # print(top_n_res)
    return top_n_res


def CalculateCos(gwyList, subList):
    """
    根据两个词频向量，算出cos值
    :param gwyList:
    :param subList:
    :return:
    """
    gwyLen = 0
    for gwynum in gwyList:
        gwyLen = gwyLen + gwynum ** 2
    gwyLen = gwyLen ** 0.5
    subLen = 0
    for sub in subList:
        subLen = subLen + sub ** 2
    subLen = subLen ** 0.5
    # return subLen
    totalLen = len(gwyList)
    fenmu = 0
    for i in range(0, totalLen):
        fenmu = fenmu + subList[i] * gwyList[i]
    print(fenmu / (subLen * gwyLen))
    return fenmu / (subLen * gwyLen)


if __name__ == '__main__':
    s1 = "8月31日下午，十三届全国人大常委会第五次会议闭幕后，全国人大常委会办公厅在人民大会堂举行新闻发布会，有关方面负责人就个人所得税法修改、电子商务法、土壤污染防治法等相关问题回答记者提问。"
    s2 = "个税法修改是本次常委会会议上最受关注的话题之一。“仅以基本减除费用标准提高到每月5000元这一项因素来测算，修法后个人所得税的纳税人占城镇就业人员的比例将由现在的44%降至15%。”财政部副部长程丽华在回答关于个税起征点的问题时表示，5000元的基本减除费用标准是统筹考虑了城镇居民人均基本消费支出、每个就业者平均负担的人数、居民消费价格指数等因素后综合确定的，不仅覆盖了人均消费支出，而且体现了一定的前瞻性。"
    s3 = "程丽华介绍，这次修法除调整基本减除费用标准外，还新增了多项专项附加扣除，扩大了低档税率级距，广大纳税人都能够不同程度地享受到减税的红利，特别是中等以下收入群体获益更大，月收入在两万元以下的纳税人税负可降低50%以上。"
    s4 = "程丽华还特别说明，5000元的标准不是固定不变的，今后还将结合深化个人所得税改革以及城镇居民基本消费支出水平的变化情况进行动态调整，个人所得税法实施以来的几次基本减除费用标准调整就能充分说明这一点。"
    s5 = "电子商务法历经四审最终表决通过，对于这部法律，全国人大财政经济委员会副主任委员尹中卿认为，“包容审慎”是其亮点之一。“目前我们国家电子商务正处于蓬勃发展的时期，渗透广、变化快，新情况、新问题层出不穷，在立法中既要解决电子商务领域的突出问题，也要为未来发展留出足够的空间。”尹中卿说，电子商务法不仅重视开放性，而且更加重视前瞻性，以鼓励创新和竞争为主，同时兼顾规范和管理的需要，这就为电子商务未来的发展奠定了体制框架。"
    s6 = "关于土壤污染防治法，全国人大常委会法工委行政法室副主任张桂龙表示，土壤污染不同于大气污染、水污染，具有隐蔽性、滞后性和累积性的特点。以往在环保法等法律中，关于防范治理土壤污染的相关规定比较原则、分散，且侧重于预防，因此需要制定专门的法律。(张 璁)"
    print(jieba_result(s1))