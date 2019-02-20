# Docker vimagick/dockerfiles(无效)

![img](https://www.pureftpd.org/images/pure-ftpd.png)

Github:[vimagick/dockerfiles](https://www.github.com/vimagick/dockerfiles)

[Pure-FTPd](https://www.pureftpd.org/project/pure-ftpd) is a free (BSD), secure, production-quality and standard-conformant FTP server. It doesn't provide useless bells and whistles, but focuses on efficiency and ease of use. It provides simple answers to common needs, plus unique useful features for personal users as well as hosting providers.

## ~/fig/pureftpd/docker-compose.yml

```yaml
pureftpd:
  image: vimagick/pure-ftpd
  ports:
    - "21:21"
  volumes:
    - ./data/ftpuser:/home/ftpuser
    - ./data/pure-ftpd:/etc/pure-ftpd
  privileged: true
  restart: always
```

> We only need to expose port `21` to accept client ftp connection. Pure-FTPd will open random port to accept client ftp-data connection. At this time, host machine is a router for DNAT.
>
> 经测试只暴露21端口，被动端口无法连接使用。entrypoint: pure-ftpd -l puredb:/etc/pure-ftpd/pureftpd.pdb -E -j -R -P localhost -s -A -j -Z -H -4 -E -R -G -X -x   -p 30000:30009 -c 5 -C 5

## server

```bash
$ cd ~/fig/pureftpd/
$ docker-compose up -d
$ docker-compose exec pureftpd bash
>>> pure-pw useradd kev -u ftpuser -d /home/ftpuser/kev -t 1024 -T 1024 -y 1 -m
>>> pure-pw list
>>> pure-pw show kev
>>> pure-pw passwd kev -m
>>> pure-pw userdel kev -m
>>> pure-ftpwho -n
>>> exit
$ tree -F
.
├── docker-compose.yml
└── data/
    ├── ftpuser/
    │   └── kev/
    │       └── file.txt
    └── pure-ftpd/
        ├── pureftpd.passwd
        └── pureftpd.pdb
```

## client

```bash
$ ftp remote-server
Name: kev
Password: ******
ftp> !touch file.txt
ftp> !ls
ftp> put file.txt
ftp> !rm file.txt
ftp> get file.txt
ftp> del file.txt
ftp> ls
ftp> bye
```



# Docker stilliard/pure-ftpd/（有效）

https://hub.docker.com/r/stilliard/pure-ftpd/

Pull down latest version with docker:

```bash
docker pull stilliard/pure-ftpd:hardened
```

**If you want to make changes, my advice is to either change the run command when running it or extend this image to make any changes rather than forking the project.**

This is because rebuilding the entire docker image via a fork can be *very* slow as it rebuilds the entire pure-ftpd package from source.

To change the command run on start you could use the `command:` option if using `docker-compose`, or with [`docker run`](https://docs.docker.com/engine/reference/run/) directly you could use:

```
docker run --rm -d --name ftpd_server -p 21:21 -p 30000-30009:30000-30009 stilliard/pure-ftpd:hardened bash /run.sh -c 30 -C 10 -l puredb:/etc/pure-ftpd/pureftpd.pdb -E -j -R -P localhost -p 30000:30059
```

To extend it you can create a new project with a `DOCKERFILE` like so:

```
FROM stilliard/pure-ftpd

# e.g. you could change the defult command run:
CMD /run.sh -c 30 -C 10 -l puredb:/etc/pure-ftpd/pureftpd.pdb -E -j -R -P $PUBLICHOST -p 30000:30059
```

*Then you can build your own image, docker build --rm -t my-pure-ftp ., where my-pure-ftp is the name you want to build as*

------

## Starting it

```
docker run -d --name ftpd_server -p 21:21 -p 30000-30009:30000-30009 -e "PUBLICHOST=localhost" stilliard/pure-ftpd:hardened
```

*Or for your own image, replace stilliard/pure-ftpd with the name you built it with, e.g. my-pure-ftp*

You can also pass ADDED_FLAGS as an env variable to add additional options such as --tls to the pure-ftpd command.
e.g. `-e "ADDED_FLAGS=--tls=2"`

## Operating it

```
docker exec -it ftpd_server /bin/bash
```

## Setting runtime FTP user

To create a user on the ftp container, use the following environment variables: `FTP_USER_NAME`, `FTP_USER_PASS`and `FTP_USER_HOME`.

`FTP_USER_HOME` is the root directory of the new user.

Example usage:

```
docker run -e FTP_USER_NAME=bob -e FTP_USER_PASS=12345 -e FTP_USER_HOME=/home/bob stilliard/pure-ftpd
```

If you wish to set the `UID` & `GID` of the FTP user, use the `FTP_USER_UID` & `FTP_USER_GID` environment variables.

## Using different passive ports

To use passive ports in a different range (*eg*: `10000-10009`), use the following setup:

```
docker run -e FTP_PASSIVE_PORTS=10000:10009 --expose=10000-10009 -p 21:21 -p 10000-10009:10000-10009
```

You may need the `--expose=` option, because default passive ports exposed are `30000` to `30009`.

## Example usage once inside

Create an ftp user: `e.g. bob with chroot access only to /home/ftpusers/bob`

```bash
pure-pw useradd bob -f /etc/pure-ftpd/passwd/pureftpd.passwd -m -u ftpuser -d /home/ftpusers/bob
```

*No restart should be needed.*

*If you have any trouble with volume permissions due to the **uid** or **gid** of the created user you can change the **-u** flag for the uid you would like to use and/or specify **-g** with the group id as well. For more information see issue #35.*

More info on usage here: <https://download.pureftpd.org/pure-ftpd/doc/README.Virtual-Users>

## Docker compose

Docker compose can help you simplify the orchestration of your containers.
We have a simple [example of the docker compose](https://github.com/stilliard/docker-pure-ftpd/blob/master/docker-compose.yml).
& here's a [more detailed example using wordpress](https://github.com/stilliard/docker-pure-ftpd/wiki/Docker-stack-with-Wordpress-&-FTP) with ftp using this image.





# mac ftp命令安装即使用

```
brew install telnet 
brew install inetutils 
brew link --overwrite inetutils
```



# mac docker-machine创建多台虚拟机搭建环境

```sh
docker-machine create --driver vmwarefusion vm1
docker-machine regenerate-certs vm1

docker-machine create --driver vmwarefusion vm2
docker-machine regenerate-certs vm2

docker-machine ssh vm1
docker run -d --name ftpd_server -p 21:21 -p 30000-30009:30000-30009 -v /home/docker/cp05:/home/root -e FTP_USER_NAME=root -e FTP_USER_PASS=passw0rd -e FTP_USER_HOME=/home/root -e PUBLICHOST=172.16.247.132 stilliard/pure-ftpd:hardened

docker-machine ssh vm2
docker run -d --name ftpd_server -p 21:21 -p 30000-30009:30000-30009 -v /home/docker/cp05:/home/root -e FTP_USER_NAME=root -e FTP_USER_PASS=p@ssword -e FTP_USER_HOME=/home/root -e PUBLICHOST=172.16.247.134 stilliard/pure-ftpd:hardened
```

https://github.com/docker/for-mac/issues/67  Cannot create a multi-node swarm in Docker for Mac

