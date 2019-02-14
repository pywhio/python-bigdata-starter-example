"""merge some tiny csv files to one file."""
import csv,os

def get_FileSize(filename):
    fsize = os.path.getsize(filename)
    fsize = fsize/float(1024)
    return round(fsize,2)


def csv_reader(filename):
    """csv file read.
    >>> list(spamreader)
    [['交易序号', '交易时间', '交易网点', '操作员编号', '客户id', '客户名称', '交易类型', '交易金额'],
     ['tac-001', '201802071002 ', 'QLR', 'op01', 'cu01', '张三', 'deposit', '1000'],
     ['tac-002', '201802071004 ', 'QLR', 'op01', 'cu01', '张三', 'deposit', '5000']]
    """
    with open(filename, newline='', encoding="gbk") as csvfile:
        spamreader = csv.reader(csvfile)
        return list(spamreader)

def merge(filelist, dist):
    """merge function."""
    header=[]
    with open(dist, 'w', newline='', encoding="gbk") as distfile:
        csvwriter = csv.writer(distfile)
        for filename in filelist:
            print("File:{}, Size:{}".format(filename, get_FileSize(filename)))
            csv_rows = csv_reader(filename)
            if header == [] and len(csv_rows)>0:
                header = csv_rows[0]
                csvwriter.writerow(header)
            else :
                if csv_rows[0] != header :  return 1
            for row in csv_rows[1:]:
                csvwriter.writerow(row)
    print("Merged File:{}, Size:{}".format(dist, get_FileSize(dist)))
    return 0

if __name__ == '__main__':
    file_list = ['QLR2019020710-001.csv','QLR2019020710-002.csv','QLR2019020710-003.csv']
    merge(file_list, 'QLR2019020710-merged.csv')

# python merge_csv.py
# File:QLR2019020710-001.csv, Size:0.18
# File:QLR2019020710-002.csv, Size:0.18
# File:QLR2019020710-003.csv, Size:0.18
# Merged File:QLR2019020710-merged.csv, Size:0.4
# 因为表头的字符重复，合并后的文件略小于3个文件总大小。
