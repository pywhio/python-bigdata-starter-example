"""
利用BytesIO，实现无落地文件二层压缩操作如下：
>>> subzipfile = io.BytesIO()
>>> subzip = ZipFile(subzipfile, 'w')
>>> subzip.write('QLR2019020710-001.xml')
>>> subzip.close()
>>> subzipfile.seek(0)
0
>>> myzip = ZipFile('spam.zip','w')
>>> myzip.writestr('QLR2019020710-001.zip',subzipfile.read())
>>> myzip.close()
>>> subzipfile.close()
>>>
"""
from zipfile import ZipFile
import io,uuid , os, sys, shutil

sys.path.append('../')
from cp03.merge_csv  import get_FileSize

def compress(filelist,zipfilename = None):
    zipfilename = zipfilename if zipfilename else 'zipfile-%s.zip' % uuid.uuid5(uuid.NAMESPACE_URL,str(filelist)) #如不定义压缩文件名，则在当前目录生成zipfile-uuid.zip文件
    with ZipFile(zipfilename, 'w') as myzip:
        print('gen Zip File: %s' % zipfilename)
        for filename in filelist:
            subzipfile = io.BytesIO() #定义子压缩文件的内存file-like对象，实现无落地文件多层压缩
            with ZipFile(subzipfile, 'w') as subzip:
                subzip.write(filename, arcname=os.path.basename(filename)) #将xml文件加入到subzip内存对象
            subzipfile.seek(0)
            subzipfilename = os.path.splitext(filename)[0] + '.zip'
            subzipfilename = os.path.basename(subzipfilename)
            myzip.writestr(subzipfilename, subzipfile.read()) #将内存中的subzip写入zip文件
            subzipfile.close()
            print('add SubZip File: %s' % subzipfilename)
    return True

def decompress(zipfilename,distdir):
    result = {}
    def unzip(fn):
        # 定义递归解压，遍历所有多层压缩，并解压到distdir下
        with ZipFile(fn) as myzip:
            for filename in myzip.namelist() :
                ext = os.path.splitext(filename)[-1].lower()
                if ext == '.zip' :
                    subzip = io.BytesIO(myzip.read(filename))
                    unzip(subzip)  #如碰到subzip文件，递归调用
                else :
                    result[filename] = False
                    try:
                        myzip.extract(filename,distdir)  #解压对应文件到distdir
                    except :
                        print('Extract failed file: %s' % filename)
                        continue
                    result[filename] = True
                    print('Extracted file: %s' % filename)
    unzip(zipfilename)
    print('decompress return: %s' % result)
    return result

def get_filelist(dir, ext):
    filelist = [os.path.join(dir,f) for f in os.listdir(dir)]
    filelist = [f for f in filelist if os.path.splitext(f)[-1].lower() == ext]
    return filelist

def print_result(start,result,end):
    print('{:#^30}\n#{:^28}#\n{:#^30}'.format(start,result,end) )

def agg(source,sender):
    filelist = get_filelist(source, '.xml')
    zipfilename = 'zipfile-%s.zip' % uuid.uuid5(uuid.NAMESPACE_URL,str(filelist))
    zipfilename = os.path.join(sender, zipfilename)
    if compress(filelist, zipfilename):
        result = [0, len(filelist), get_FileSize(zipfilename)]
        print_result('1 agg','return: %s' % result,'end')
        return result

def recieve(sender,reciever):
    filelist = get_filelist(sender, '.zip')
    print('copy %d file(s) to reciever folder.' % len(filelist))
    for filename in filelist:
        shutil.copy(filename, reciever)
        print('copied file: %s' % os.path.join(reciever,os.path.basename(filename) ) )
    print_result('2 recieve','return: 0','end')
    return 0

def extract(reciever,destination):
    filelist = get_filelist(reciever, '.zip')
    for filename in filelist :
        print('decompressing file: %s' % filename)
        unzipresult = decompress(filename,destination)
        filenum = len(unzipresult)
        filedonenum = len([v for v in unzipresult.values() if v == True])
        result = [
            0 if filenum==filedonenum else 1 if filedonenum==0 else 2 ,
            filenum, filedonenum,
        ]
        print_result('3 extract','return: %s' % result,'end')


def init(dirs):
    for d in dirs:
        shutil.rmtree(d,ignore_errors=True)
        if not os.path.isdir(d) : os.mkdir(d)

def main(source,sender,reciever,destination):
    init([sender,reciever,destination])
    agg(source,sender)
    recieve(sender,reciever)
    extract(reciever,destination)

if __name__ == '__main__':
    main('source','sender','reciever','destination')


# python compress.py
# gen Zip File: sender/zipfile-15b14629-5573-551e-8876-7c577bfce2c6.zip
# add SubZip File: QLR2019020710-001.zip
# add SubZip File: QLR2019020710-003.zip
# add SubZip File: QLR2019020710-002.zip
# ############1 agg#############
# #    return: [0, 3, 4.6]     #
# #############end##############
# copy 1 file(s) to reciever folder.
# copied file: reciever/zipfile-15b14629-5573-551e-8876-7c577bfce2c6.zip
# ##########2 recieve###########
# #         return: 0          #
# #############end##############
# decompressing file: reciever/zipfile-15b14629-5573-551e-8876-7c577bfce2c6.zip
# Extracted file: QLR2019020710-001.xml
# Extracted file: QLR2019020710-003.xml
# Extracted file: QLR2019020710-002.xml
# decompress return: {'QLR2019020710-001.xml': True, 'QLR2019020710-003.xml': True, 'QLR2019020710-002.xml': True}
# ##########3 extract###########
# #     return: [0, 3, 3]      #
# #############end##############
