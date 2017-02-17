ubuntu-16.04 
=============================================

### 1) open Terminal
![1](./u01.png)


### 2) open dashmnb page
![1](./u02.png)
![1](./u03.png)


### 3) download installation script
```
wget https://raw.githubusercontent.com/chaeplin/dashmnb/master/others/linux/ubuntu-16-04.sh
```
![1](./u04.png)

### 4) excute ubuntu-16-04.sh
```
sh ./ubuntu-16-04.sh
```
![1](./u05.png)

### 5) when finished following screen will appear

![1](./u06.png)


### 6) open folder ~/dashmnb/dashlib and duoble click config.py

gedit will open it

edit redd box and save it

https://github.com/chaeplin/dashmnb/tree/master/others/pics/trezor has example
![1](./u07.png)



### 6) open folder ~dashmnb/mnconf and rename masternode.conf.sample to masternode.conf

duoble click masternode.conf, gedit will open it

edit redd box and save it

![1](./u08.png)

### 7) use following command to start
```
cd ~/dashmnb
. venv3/bin/activate
python bin/dashmnb.py


python bin/dashmnb.py -c


python bin/dashmnb.py -b
```


![1](./u09.png)

