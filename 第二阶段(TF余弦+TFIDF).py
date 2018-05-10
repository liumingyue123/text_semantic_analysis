import jieba
import numpy as np
from scipy.linalg import norm
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


def cosine_similarity_tf(s1, s2):#计算两个句子的TF余弦相似度
    vectorizer = CountVectorizer(tokenizer=lambda s: s.split(' '))
    corpus = [s1, s2]
    vectors = vectorizer.fit_transform(corpus).toarray()
    return np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))#计算矩阵中元素的余弦值

def cosine_similarity_tfidf(s1, s2):#计算两个句子的TFIDF余弦相似度
    vectorizer = TfidfVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = vectorizer.fit_transform(corpus).toarray()
    return np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))


if __name__ == '__main__':
    file1 = open('中文测试数据.txt', 'r')
    file2 = open('中文测试集结果.txt', 'r')
    result = []
    resem = []
    t=0.5#t表示阈值
    YY=0
    YN=0
    NY=0
    NN=0
    count=0
    data = file1.readlines()
    for line in file2:
        result.append(line)

    for i in range(0, len(data), 2):#每次读入两个句子，为一个句子对
        str1 = data[i]
        str2 = data[i + 1]
        result1 = jieba.cut(str1, cut_all=False)#对读入的句子进行切分
        result2 = jieba.cut(str2, cut_all=False)
        a = ' '.join(result1)
        b = ' '.join(result2)

        resem.append(cosine_similarity_tf(a, b))

    for i in range(len(result)):#计算YY，YN，NY，NN
        if result[i] == 'Y\n' and resem[i]>=t:
            YY+=1
            count+=1
        elif result[i] == 'Y\n' and resem[i]<t:
            NY+=1
        elif result[i] == 'N\n' and resem[i]<t:
            NN+=1
            count+=1
        elif result[i] == 'N\n' and resem[i]>=t:
            YN+=1
    py = YY / (YY + NY)
    ry = YY / (YY + YN)
    F1 = 2 * py * ry / (py + ry)
    pn = NN / (NN + YN)
    rn = NN / (NN + NY)
    F2 = 2 * pn * rn / (pn + rn)
    #print(s / len(resem))
    print('F值：',(F1 + F2) / 2)
    print('准确率：',count/len(resem))



