import jieba.analyse
import re
true_list = []
false_list = []
result_list = []
score = 0

with open('中文测试集结果.txt', 'r') as f:
    for each in f:
        result_list.append(each.strip())
    f.close()

flag = None
with open('中文测试数据.txt', 'r') as f:
    YY=0
    YN=0
    NY=0
    NN=0
    one = 0.0
    while one <= 15:#通过循环调整阈值
        for i, each in enumerate(f):
            each = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", '', each)#除去句子中的符号
            if not i % 2:
                # 记录第一条记录
                flag = {}
                for item in jieba.analyse.tfidf(each.strip(), withWeight=True,topK=30):
                    flag.setdefault(item[0], item[1])#存入提取的词语权值
            else:
                # 计算标准差
                tmp = 0
                # 相同的词数
                same_len = 0
                for item in jieba.analyse.tfidf(each.strip(), withWeight=True, topK=30):
                    try:
                        tmp += pow(item[1] - flag[item[0]], 2)#计算平方差
                        same_len += 1
                    except KeyError:
                        continue

                if not same_len:
                    tmp = 99
                else:
                    tmp /= same_len
                if (tmp <= one and result_list[int(i / 2)] == 'Y'):#one为阈值
                    score += 1
                    YY+=1
                elif (tmp > one and result_list[int(i / 2)] == 'N'):
                    score+=1
                    NN+=1
                elif (tmp <= one and result_list[int(i / 2)] == 'N'):
                    YN +=1
                elif (tmp > one and result_list[int(i / 2)] == 'Y'):
                    NY+=1
                # print(flag,each)


        py = YY / (YY + NY)
        ry = YY / (YY + YN)
        F1 = 2 * py * ry / (py + ry)
        pn = NN / (NN + YN)
        rn = NN / (NN + NY)
        F2 = 2 * pn * rn / (pn + rn)

        print((F1 + F2) / 2)
        print(one, score / len(result_list))
        one += 0.5#阈值
        score = 0
        f.seek(0)
