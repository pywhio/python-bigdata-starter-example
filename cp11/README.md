# 用例故事

1. 可以通过多进程设置，连接多个ftp服务器。
2. 采用多线程设置，下载每个ftp服务的目标文件。
3. 通过配置文件配置ftp服务器信息。
4. 下载后的文件按ftp服务器名称，分别载至对应位置。
5. 通过filelist对象记录文件下载情况。

# 环境准备
- Python3
```sh
pip install -r requirement.txt
```

- docker
```sh
docker-compose up -d
```

# 程序运行
```Python3
python ftp_mp_con.py
```
