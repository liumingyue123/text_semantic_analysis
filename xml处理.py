import xml.sax


class datahandle(xml.sax.ContentHandler):
    def __init__(self):
        self.currentdata = ''
        self.t1 = ''
        self.t2 = ''

    def startElement(self, name, attrs):
        self.currentdata = name
        if name == 'pair':
            label = attrs['label']
            #print(label)
            file2.write(label + '\n')#存储标签，即实际结果

    def endElement(self, name):#分别存入两个句子，根据标签t1,t2
        if self.currentdata == 't1':
            #print(self.t1)
            file1.write(self.t1 + '\n')
        elif self.currentdata == 't2':
            #print(self.t2)
            file1.write(self.t2+'\n')
        self.currentdata = ''

    def characters(self, content):
        if self.currentdata == 't1':
            self.t1 = content
        elif self.currentdata == 't2':
            self.t2 = content


if (__name__ == "__main__"):
    file1= open('中文测试数据', 'w')
    file2=open('中文测试集结果','w')
    parser = xml.sax.make_parser()#创建一个新的解析器对象并返回

    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = datahandle()
    parser.setContentHandler(Handler)

    parser.parse("rite2014测试数据（有标签）.xml")
