import socket
import sys, os
from datetime import datetime
from colorama import Fore, Back, Style
from serializer import serialize, deserialize

# def recvall(sock, bufsize=10240):
#     total_data = b''
#     while True:
#         data = sock.recv(bufsize)
#         if not data : break
#         total_data += data
#     return total_data

def remote_decompress(zipfilename, distdir, host = 'localhost', port = 9999):
    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((host, port))
        with open(zipfilename,'rb') as f :
            sock.sendall( f.read() )
        # Receive data from the server and shut down
        received = sock.recv(102400000)  # socket接收结束方式待修正
        result = deserialize(received)
    subfilenum , successnum = len(result), 0
    for filename , filebyte in result.items():
        if filebyte :
            if not os.path.isdir(distdir) : os.mkdir(distdir)
            with open(os.path.join(distdir,filename), 'wb') as f:
                f.write(filebyte)
            successnum +=1
    status = 2 if successnum == 0 else  0 if subfilenum == successnum else 1
    return [status, subfilenum, successnum]

def decompress_fun(zipfile_path, unzipfile_path, if_unzip_cfg):
    print(f'{Fore.GREEN} zipfile_path: %s \n unzipfile_path: %s \n if_unzip_cfg: %s {Style.RESET_ALL}' % (zipfile_path, unzipfile_path, if_unzip_cfg))
    filelist = [os.path.join(zipfile_path,fn) for fn in os.listdir(zipfile_path)]
    filelist = [fn for fn in filelist if os.path.isfile(fn)]
    zipfilelist = [fn for fn in filelist if os.path.splitext(fn)[-1].lower() == '.zip']
    print('zipfilelist: %s' % zipfilelist)
    results = {}
    for zipfilename in zipfilelist :
        starttime = datetime.now()
        status, sunfilenum, successnum = remote_decompress(zipfilename, os.path.join(unzipfile_path, os.path.splitext(os.path.basename(zipfilename))[0]), *if_unzip_cfg)
        endtime = datetime.now()
        results[zipfilename] = [status, if_unzip_cfg, starttime, endtime, sunfilenum, successnum]
    return results


if __name__ == '__main__':
    zipfile_path = './zipfile_path'
    unzipfile_path = './unzipfile_path'
    if_unzip_cfg = ('localhost', 9999)
    results = decompress_fun(zipfile_path, unzipfile_path, if_unzip_cfg)
    print(f'{Fore.GREEN} results: %s{Style.RESET_ALL}' % results)
