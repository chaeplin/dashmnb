ubuntu-16.04 
=============================================

### 1) open Terminal
![1](./01.png)


### 2) download installation script
```
wget https://raw.githubusercontent.com/chaeplin/dashmnb/master/others/linux/ubuntu-14-04.sh
```
![1](./02.png)

### 3) excute ubuntu-14-04.sh

```
sh ./ubuntu-14-04.sh
```
![1](./03.png)


### 4) when finished following screen will appear

![1](./04.png)


### 5) open folder ~/dashmnb/dashlib and duoble click config.py

gedit will open it

edit following and save it
```
account_no
TYPE_HW_WALLET
masternode_conf_file
default_receiving_address
max_gab
```

https://github.com/chaeplin/dashmnb/tree/master/others/pics/trezor has example
![1](./05.png)
![1](./06.png)
![1](./07.png)
![1](./08.png)



### 6) open folder ~dashmnb/mnconf and rename masternode.conf.sample to masternode.conf

duoble click masternode.conf, gedit will open it

edit redd box and save it

![1](./09.png)
![1](./10.png)
![1](./11.png)


### 7) use following command to start
```
cd ~/dashmnb
. venv3/bin/activate
python bin/dashmnb.py


python bin/dashmnb.py -c


python bin/dashmnb.py -b
```

