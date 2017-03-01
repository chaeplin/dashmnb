Debian 8.7.1
=============================================

* Debian 8 has python 3.4.2, so we need install python 3.5.3
* Sometimes Debian 8 has no sudo command

### 1) if system has no sudo, install sudo 
- as normal user use `su -` to get root
- add your user name to sudo list
```
su -
apt-get install sudo
adduser your_normal_user_name_here sudo
```

- then logout system and relogin 


### 2) check of you have python3 version abobe 3.5.1
```
python3 -V
```

- if version is 3.4.2 : follow Ubuntu-14.04 install 

[Ubuntu 14.04 --> use this link](https://github.com/chaeplin/dashmnb/tree/master/others/pics/ubuntu-14.04)

- if version is above 3.5.1 : follow Ubuntu 16.04 install
[Ubuntu 16.04 --> use this link](https://github.com/chaeplin/dashmnb/tree/master/others/pics/ubuntu-16.04)


