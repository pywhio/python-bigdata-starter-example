import ftputil
import ftputil.session
import os,sys
from ftp_conn_info import conn_info

sys.path.append('../')
from cp03.merge_csv  import get_FileSize


class ftpconn():
    def __init__(self,ip,port,user,password,mode):
        use_passive_mode = True if mode == 'passive' else False
        my_session_factory = ftputil.session.session_factory(port=port ,
                               use_passive_mode = use_passive_mode) # use_passive_mode=False 强制使用主动模式
        self.ftphost = ftputil.FTPHost(ip,user,password,session_factory=my_session_factory)

    def listdir(self, path):
        filelist = []
        dirlist = [path]
        while dirlist != []:
            absdir = dirlist.pop(0)
            try :
                names = self.ftphost.listdir(absdir)
            except :
                names = []
            for name in names :
                fullname = os.path.join(absdir,name)
                if os.path.splitext(name)[-1] == '':
                    dirlist.append(fullname)
                else:
                    filelist.append(fullname)
        return filelist

    def download(self,remote,local):
        d = os.path.split(local)[0]
        # 如果下载文件目录不存在，则使用os.makedirs创建多层目录。
        if not os.path.isdir(d) : os.makedirs(d, exist_ok=True)
        self.ftphost.download(remote,local)

    def close(self):
        self.ftphost.close()

def getter(buffer_path = './buffer_path'):
    results = []
    for servername, ftpinfo in conn_info.items():
        result = [servername,1,0,[]]
        print('connecting ftpserver: %s(%s:%s@%s:%s)' % (servername,ftpinfo['username'],ftpinfo['pswd'], ftpinfo['ip'],ftpinfo['port']))
        try:
            ftp = ftpconn(ftpinfo['ip'],ftpinfo['port'],ftpinfo['username'],ftpinfo['pswd'],ftpinfo['mode'])
        except :
            print('%s connect error!' % servername )
            results.append(result)
            break
        result[1] = 0
        print("scan %s's path: %s" % (servername, ftpinfo['path']))
        filelist = ftp.listdir(ftpinfo['path'])
        print("filelist: %s" % filelist)
        def to_local(filename):
            #转换远程文件名为本地文件名
            localfile = filename.replace(ftpinfo['path'] + ('' if ftpinfo['path'][-1]=='/' else '/'), '',1)
            print(buffer_path, servername, localfile)
            return os.path.join(buffer_path, servername, localfile)

        for filename in filelist:
            localfilename = to_local(filename)
            print('downloading file: %s' % filename)
            try:
                ftp.download(filename,localfilename)
            except :
                print('%s download failed' % localfilename)
            result[2] += 1
            result[3].append([localfilename, get_FileSize(localfilename)])
            print('downloaded file: %s' % localfilename)
        results.append(result)
    return results


if __name__ == '__main__':
    print("results: %s" % getter())


# results: [['server1', 0, 9, [['./buffer_path/server1/compress.py', 5.24], ['./buffer_path/server1/destinationQLR2019020710-001.xml', 1.27], ['./buffer_path/server1/destinationQLR2019020710-002.xml', 1.28], ['./buffer_path/server1/destinationQLR2019020710-003.xml', 1.27], ['./buffer_path/server1/recieverzipfile-15b14629-5573-551e-8876-7c577bfce2c6.zip', 4.6], ['./buffer_path/server1/senderzipfile-15b14629-5573-551e-8876-7c577bfce2c6.zip', 4.6], ['./buffer_path/server1/sourceQLR2019020710-001.xml', 1.27], ['./buffer_path/server1/sourceQLR2019020710-002.xml', 1.28], ['./buffer_path/server1/sourceQLR2019020710-003.xml', 1.27]]], ['server2', 0, 9, [['./buffer_path/server2/compress.py', 5.24], ['./buffer_path/server2/destinationQLR2019020710-001.xml', 1.27], ['./buffer_path/server2/destinationQLR2019020710-002.xml', 1.28], ['./buffer_path/server2/destinationQLR2019020710-003.xml', 1.27], ['./buffer_path/server2/recieverzipfile-15b14629-5573-551e-8876-7c577bfce2c6.zip', 4.6], ['./buffer_path/server2/senderzipfile-15b14629-5573-551e-8876-7c577bfce2c6.zip', 4.6], ['./buffer_path/server2/sourceQLR2019020710-001.xml', 1.27], ['./buffer_path/server2/sourceQLR2019020710-002.xml', 1.28], ['./buffer_path/server2/sourceQLR2019020710-003.xml', 1.27]]]]
