from word_similarity import WordSimilarity2010
import jieba
from scipy.linalg import norm
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import numpy as np
ws_tool = WordSimilarity2010()


def word(a,b):#判断两句子中词语的相似度，a,b为两句子切分后存入的数组
    result = 0
    for i in range(len(a)):
        if a[i]==b[i]:#如果词语相同，权值设为1
            result+=1
        else:#若两词不同，则通过同义词林的编码对比两个词的相似度
            if (ws_tool.similarity(a[i], b[i]))<=0.9:#若两词的相似度小于0.9，则认为两句子相似度为0
                return 0
            else:
                result+=ws_tool.similarity(a[i], b[i])#计算相似度权值
    return result/len(a)#返回相似度均值

def cosine_similarity_tf(s1, s2):# 计算两个句子的TF余弦相似度
    vectorizer = CountVectorizer(tokenizer=lambda s: s.split(' '))
    corpus = [s1, s2]
    vectors = vectorizer.fit_transform(corpus).toarray()
    return np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))

def cosine_similarity_tfidf(s1, s2):#计算两个句子的TFIDF余弦相似度
    vectorizer = TfidfVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = vectorizer.fit_transform(corpus).toarray()
    return np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))

if __name__ == '__main__':
    file1 = open('中文测试数据.txt', 'r')
    file2 = open('中文测试集结果.txt', 'r')
    result = []#存放测试集已知结果
    resem = []
    t=0.7#阈值
    s=0#表示预测结果与实际结果相同的个数，即正确个数
    data = file1.readlines()#读入测试集数据

    for line in file2:
        result.append(line)

    for i in range(0, len(data), 2):#每次读入测试集的两行
        str1 = data[i]
        str2 = data[i + 1]
        result1 = jieba.cut(str1, cut_all=False)
        result2 = jieba.cut(str2, cut_all=False)
        list1 = []
        list2 = []
        for i in result1:
            list1.append(i)
        for i in result2:
            list2.append(i)

        if set(list1)>set(list2) or set(list2)>set(list1):#如果一个句子近似认为是另一个句子的缩句
            resem.append(1)

        elif len(list1)==len(list2):#若分词结果大小相同
            if word(list1,list2)==-1:#调用词语相似度对比函数，若遇到不同的词
                resem.append(0)
            else:
                resem.append(word(list1,list2))
        else:
            a = ' '.join(list1)
            b = ' '.join(list2)
            resem.append(cosine_similarity_tf(a, b))#两句子切分数组长度不同则使用TF余弦方法比较

    YY=0
    YN=0
    NY=0
    NN=0
    while t<1:#通过循环调整阈值t
        s=0
        for i in range(len(resem)):
            if resem[i]>=t and result[i]=='Y\n':#YY
                s+=1#预测值与实际结果相同
                YY+=1
            elif resem[i]<t and result[i]=='Y\n':#NY
                NY+=1
            elif resem[i] >=t and result[i] == 'N\n':#YN
                YN+=1

            elif resem[i] <t and result[i] == 'N\n':#NN
                NN+=1
                s+=1#预测值与实际结果相同

        py=YY/(YY+NY)
        ry=YY/(YY+YN)
        F1=2*py*ry/(py+ry)
        pn=NN/(NN+YN)
        rn=NN/(NN+NY)
        F2=2*pn*rn/(pn+rn)
        print('t2:',t)
        print('准确率:',s/len(resem))#正确率
        print('F值：',(F1+F2)/2,'\n')
        t=t+0.02#调整阈值，每次增加0.02