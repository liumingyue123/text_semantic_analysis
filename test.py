from word_similarity import WordSimilarity2010
import jieba
from scipy.linalg import norm
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import numpy as np
ws_tool = WordSimilarity2010()


b_a = "手语"
b_b = "语言"
sim_b = ws_tool.similarity(b_a, b_b)
print(b_a, b_b, '相似度为', sim_b)

def cosine_similarity_tf(s1, s2):
    """
    计算两个句子的TF余弦相似度
    :param s1:
    :param s2:
    :return:
    """
    vectorizer = CountVectorizer(tokenizer=lambda s: s.split(' '))
    corpus = [s1, s2]
    vectors = vectorizer.fit_transform(corpus).toarray()
    return np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))
str1 = '手语主要使用者是失聪者。'
str2 = '手语主要使用者是有听觉障碍的人。'
result1 = jieba.cut(str1, cut_all=False)
result2 = jieba.cut(str2, cut_all=False)
a=[]
b=[]
for i in result1:
    a.append(i)

for i in result2:
    b.append(i)
print(a)
print(b)

a1 = ' '.join(a)
b1 = ' '.join(b)


def getwordsim(a,b):
    result = 0
    for i in range(len(a)):
        if a[i]==b[i]:
            result+=1
        else:
            if (ws_tool.similarity(a[i], b[i]))<=0.5:
                return 0
            else:
                result+=ws_tool.similarity(a[i], b[i])
    return result/len(a)
if __name__ == '__main__':
    if len(a)==len(b):
        print(getwordsim(a,b))
    else:
        print(cosine_similarity_tf(a1,b1))


#print(cosine_similarity_tf(a1,b1))
