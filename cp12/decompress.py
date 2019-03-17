import io, os
from zipfile import ZipFile

def decompress(zipfilename):
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
                    result[filename] = None
                    try:
                        result[filename] = myzip.read(filename)  #解压对应文件到distdir
                    except :
                        print('Extract failed file: %s' % filename)
                        continue
                    print('Extracted file: %s' % filename)
    unzip(zipfilename)
    print('decompress return: %s' % [(k,'File' if v else v ) for k,v in result.items() ])
    return result
