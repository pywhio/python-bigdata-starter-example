from joblib import Parallel, delayed, parallel_backend
import sys,os, traceback
from colorama import Fore, Back, Style
from ftp_conn_info import conn_info

sys.path.append('../')
from cp03.merge_csv  import get_FileSize
from cp06.ftpconn import ftpconn

def mt_getter(ftp_cfg, filelist, buffer_path = './buffer_path'):
    '''single ftp multi-threading download.'''
    def download(remote, local):
        try:
            ftp = ftpconn(ftp_cfg['ip'],ftp_cfg['port'],ftp_cfg['username'],ftp_cfg['pswd'],ftp_cfg['mode'])
        except :
            print(traceback.format_exc())
            return False
        try:
            ftp.download(remote, local)
            print(f'{Fore.GREEN}%s downloaded file: %s{Style.RESET_ALL}' % (ftp_cfg['name'], local))
        except:
            print(traceback.format_exc())
            ftp.close()
            return False
        ftp.close()
        return  True

    def to_local(filename):
        #转换远程文件名为本地文件名
        localfile = filename.replace(ftp_cfg['path'] + ('' if ftp_cfg['path'][-1]=='/' else '/'), '',1)
        # print(buffer_path, ftp_cfg['name'], localfile)
        return os.path.join(buffer_path, ftp_cfg['name'], localfile)

    local_filelist = [to_local(fn) for fn in filelist]

    with parallel_backend('threading', n_jobs=2):
        # 使用多线程，2个并发启动下载任务
        status = Parallel()(delayed(download)(remote,local) for remote, local  in zip(filelist, local_filelist))
    fileinfo = [[os.path.basename(fn), get_FileSize(fn)] for fn,case in zip(local_filelist,status) if case == True ]
    result = [2, len(filelist), os.path.join(buffer_path,ftp_cfg['name']), fileinfo]
    if all(result) :
        result[0] = 0
    elif any(result):  #部分成功
        result[0] = 1
    return result

def mp_getter(ftps_cfg=conn_info, buffer_path = './buffer_path'):
    '''multiple ftps , multi-processing get filelist'''
    def ftp_getter(ftp_cfg):
        try:
            ftp = ftpconn(ftp_cfg['ip'],ftp_cfg['port'],ftp_cfg['username'],ftp_cfg['pswd'],ftp_cfg['mode'])
        except :
            print(traceback.format_exc())
            return [2, 0, '' , []]
        filelist = ftp.listdir(ftp_cfg['path'])
        print(f'{Fore.RED}%s filelist: %s{Style.RESET_ALL}' % (ftp_cfg['name'], filelist))
        return mt_getter(ftp_cfg, filelist, buffer_path)
    with parallel_backend('threading', n_jobs=2):
        # 使用多线程，2个并发启动下载任务
        status = Parallel()(delayed(ftp_getter)(ftp_cfg) for ftp_cfg in ftps_cfg.values() )
    result = dict(zip(ftps_cfg.keys(), status))
    print(f'{Fore.RED}result: %s{Style.RESET_ALL}' % result)
    return result

if __name__ == '__main__':
    mp_getter()
