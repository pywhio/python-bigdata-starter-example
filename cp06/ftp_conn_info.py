# encoding: utf8

conn_info = {
    "server1":  {"ip":"172.16.247.132", "username":"root", "port":21, "pswd":"passw0rd", "mode":"active",  "path":"/"},
    "server2": {"ip":"172.16.247.134", "username":"root", "port":21, "pswd":"p@ssword", "mode":"passive", "path":"/"}
}

server1_ip = conn_info['server1']['ip']
server1_username = conn_info['server1']['username']
server1_port = conn_info['server1']['port']
server1_pswd = conn_info['server1']['pswd']
server1_mode = conn_info['server1']['mode']
server1_path = conn_info['server1']['path']


# print(server1_ip, server1_username, server1_port, server1_pswd, server1_mode, server1_path, sep=',')

# from ftplib import FTP
# ftp_conn = FTP()
# # 连接
# ftp_conn.connect(server1_ip, server1_port)
# # 登陆
# ftp_conn.login(server1_username, server1_pswd)
