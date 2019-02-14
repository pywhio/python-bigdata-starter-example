import xml.etree.ElementTree as ET
import os, csv , sys
from collections import OrderedDict

sys.path.append('../')
from cp03.merge_csv  import get_FileSize

import ticket_infofield

class Ticket(object):
    """parse file to ticket data."""
    def __init__(self, filename, header_def=ticket_infofield.ticket_infofield):
        self.filename = filename
        self.header_def = header_def
        self.header = None
        self.records = None
        self.parsed = False
        ext = os.path.splitext(self.filename)[1].lower()
        if ext == '.xml' : self.parse_xml()
        #此处可以编写根据文件扩展名，分别调用不同的parser。
        #另外，Python 没有Switch语法，实现Switch Case需要被判断的变量是可哈希的和可比较的，这与Python倡导的灵活性有冲突。 参考PEP 3103-A Switch/Case Statement
        print("header: %s" % self.header)
        print("records: %s" % self.records)

    def parse_xml(self):
        header = OrderedDict() # OrderdDict是顺序存储字典，Dict能够有效映射半结构数据，但Python的默认Dict是随机存储。
        records = []
        record = OrderedDict()
        for event, elem in ET.iterparse(self.filename):
            # iterparse 默认使用end event, 即碰到尾标签后生成对应的elem。因此，解析逻辑可以从相关叶子结点写，想当于树遍历算法的【后序遍历】(Postorder Traversal)
            if elem.tag == 'N' :
                header[elem.attrib['i']] = elem.text
            if elem.tag == 'TicketName' :
                self.header = header
                if not self.header_check() :
                    print('Header Error File:{}\nFile Header:{}\nDefined Header:{}'.format(self.filename, list(self.header.values()), self.header_def))
                    self.parsed = False
                    return
            if elem.tag == 'V' :
                colname = header[elem.attrib['i']]
                record[colname] = elem.text.strip()
            if elem.tag == 'Ticket' :
                records.append(record)
            if elem.tag == 'TicketData' :
                self.records = records
            elem.clear()  #在处理完当前标签数据后，立即清理内存，可显著节省内存开销。
        self.parsed = True

    def header_check(self):
        header_def = set(self.header_def) #将Dict转换为Set，便于进行比较操作。
        header = set(self.header.values()) #Dict的keys()和values()返回iter key or value
        return header <= header_def #Python Set 可以使用 <= 表达 issubset操作。

    def to_csv(self,filename=None):
        filename = filename if filename else self.filename
        filename = os.path.splitext(filename)[0]+'.csv'
        with open(filename, 'w', newline='', encoding="gbk") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(self.header_def)
            for record in self.records:
                row = [ record[colname] for colname in self.header_def]
                csvwriter.writerow(row)
        print("To_CSV File:{}, Size:{}".format(filename, get_FileSize(filename)))

def xml_parser(filelist, dist_dir=None):
    result = []
    for fn in filelist :
        print("Xml File:{}, Size:{}".format(fn, get_FileSize(fn)))
        ticket = Ticket(fn)
        fn_csv = dist_dir + os.path.basename(fn) if dist_dir else fn
        fn_csv = os.path.splitext(fn_csv)[0]+'.csv'
        if ticket.parsed:
            ticket.to_csv(fn_csv)
            result.append([0, get_FileSize(fn_csv)])
        else :
            result.append([1,0])
    return result

if __name__ == '__main__':
    filelist = ['QLR2019020710-001.xml','QLR2019020710-002.xml','QLR2019020710-003.xml']
    print("Result: %s" % xml_parser(filelist[0:1]) )

# 测试结果如下：
# python parser.py
# Xml File:QLR2019020710-001.xml, Size:1.27
# To_CSV File:QLR2019020710-001.csv, Size:0.18
# Xml File:QLR2019020710-002.xml, Size:1.29
# Header Error File:QLR2019020710-002.xml
# File Header:['交易序号', '交易时间', '交易网点', '操作员编号', '客户id-test', '客户名称', '交易类型', '交易金额']
# Defined Header:['交易序号', '交易时间', '交易网点', '操作员编号', '客户id', '客户名称', '交易类型', '交易金额']
# Xml File:QLR2019020710-003.xml, Size:1.28
# To_CSV File:QLR2019020710-003.csv, Size:0.18
# Result: [[0, 0.18], [1, 0], [0, 0.18]]


# Xml File:QLR2019020710-001.xml, Size:1.27
# header: OrderedDict([('1', '交易序号'), ('2', '交易时间'), ('3', '交易网点'), ('4', '操作员编号'), ('5', '客户id'), ('6', '客户名称'), ('7', '交易类型'), ('8', '交易金额')])
# records: [OrderedDict([('交易序号', 'tac-002'), ('交易时间', '201802071004'), ('交易网点', 'QLR'), ('操作员编号', 'op01'), ('客户id', 'cu01'), ('客户名称', '张三'), ('交易类型', 'deposit'), ('交易金额', '5000')]), OrderedDict([('交易序号', 'tac-002'), ('交易时间', '201802071004'), ('交易网点', 'QLR'), ('操作员编号', 'op01'), ('客户id', 'cu01'), ('客户名称', '张三'), ('交易类型', 'deposit'), ('交易金额', '5000')])]
# To_CSV File:QLR2019020710-001.csv, Size:0.18
# Result: [[0, 0.18]]
