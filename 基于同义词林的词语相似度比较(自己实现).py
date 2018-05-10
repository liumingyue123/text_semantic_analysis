import codecs
import math

file=codecs.open('同义词词林.txt','r',encoding='gbk')
tmp=[]
for line in file:
    line.rstrip('\n')
    tmp.append(line)

file1=open('同义词编码.txt','r')
all=[]
for line in file1:
    all.append(line)


def getnum(string):#获取n
    count=0

    for i in all:
        if i[:len(string)]==string:
            count+=1
        else:
            continue

    return count

forest=[]
for i, each in enumerate(tmp):
    split0 = each.split(' ')
    forest.append(split0)#对训练集中的词脱去空格，分别存入数组




def getcode(t1):
    for i,each in enumerate(forest):
        if forest[i][0]==t1:
            return forest[i][2:]
        else:
            continue



a=0.65
b=0.8
c=0.9
d=0.96
f=0.1

def getsimilarty(code1,code2):
    if code1[0][0]!=code2[0][0]:#不在同一查树上
        return 0
    elif code1[0][0]==code2[0][0] and code1[0][1]!=code2[0][1]:#第一分支
        n=getnum(code1[0][:1])
        print(n)
        k=abs(ord(code1[0][1])-ord(code2[0][1]))
        print(k)
        return a*math.cos(n*math.pi/180)*((n-k+1)/n)
    elif code1[0][:2]==code2[0][:2] and code1[0][2:4]!=code2[0][2:4]:#第二分支
        n=getnum(code1[0][:2])
        print(n)
        k=abs(int(code1[0][2:4])-int(code2[0][2:4]))
        return b*math.cos(n*math.pi/180)*((n-k+1)/n)
    elif code1[0][:4]==code2[0][:4] and code1[0][4]!=code2[0][4]:#第三分支
        n = getnum(code1[0][:4])
        print(n)
        k=abs(ord(code1[0][4])-ord(code2[0][4]))
        print(k)
        return c*math.cos(n*math.pi/180)*((n-k+1)/n)
    elif code1[0][:5]==code2[0][:5] and code1[0][5:7]!=code2[0][5:7]:#第四分支
        n=getnum(code1[0][:5])
        print(code1[0][:5])

        k=abs(int(code1[0][5:7])-int(code2[0][5:7]))

        return d * math.cos(n * math.pi / 180) * ((n - k + 1) / n)
    elif code1[0][:7]==code2[0][:7] and code1[0][7]==code2[0][7]=='=':#最后一位符号有不同意义
        return 1
    elif code1[0][:7]==code2[0][:7] and code1[0][7]==code2[0][7]=='#':
        return 0.5
    elif code1[0][:7]==code2[0][:7] and (code1[0][7]=='@' or code2[0][7]=='@'):
        return 0

if __name__ == '__main__':
    t1 = '人民'
    t2 = '先锋'
    t = '啊'


    code1 = getcode(t1)
    print(code1[0])
    code2 = getcode(t2)
    print(code2[0])
    print(getsimilarty(code1,code2))


