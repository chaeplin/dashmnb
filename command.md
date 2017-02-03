```
~ $ cd dashmnb/
~/dashmnb $ . venv3/bin/activate
(venv3) ~/dashmnb $ python bin/hw-wallet-for-mn.py 
    ____             __  
   / __ \____ ______/ /_ 
  / / / / __ `/ ___/ __ \
 / /_/ / /_/ (__  ) / / /
/_____/\__,_/____/_/ /_/ 
                         
    __  ___           __                            __   
   /  |/  /___ ______/ /____  _________  ____  ____/ /__ 
  / /|_/ / __ `/ ___/ __/ _ \/ ___/ __ \/ __ \/ __  / _ \
 / /  / / /_/ (__  ) /_/  __/ /  / / / / /_/ / /_/ /  __/
/_/  /_/\__,_/____/\__/\___/_/  /_/ /_/\____/\__,_/\___/ 
                                                         
           _ __  __       __  ___       __   _       __      ____     __ 
 _      __(_) /_/ /_     / / / / |     / /  | |     / /___ _/ / /__  / /_
| | /| / / / __/ __ \   / /_/ /| | /| / /   | | /| / / __ `/ / / _ \/ __/
| |/ |/ / / /_/ / / /  / __  / | |/ |/ /    | |/ |/ / /_/ / / /  __/ /_  
|__/|__/_/\__/_/ /_/  /_/ /_/  |__/|__/     |__/|__/\__,_/_/_/\___/\__/  
                                                                         

      by : chaeplin

Network : TESTNET
===> keepkey HW Wallet found
Passphrase required: 

Confirm your Passphrase: 

**** ====> use following address for 1K collateral of masternode
.....

**** ====> use following address for trezor/keepkey wallet(default path)
.....

```



```
(venv3) ~/dashmnb $ python bin/dashmnb.py 
usage: dashmnb.py [-h] [-c] [-s] [-a] [-b] [-m] [-x]
                  [masternode_alias_to_start/spend [masternode_alias_to_start/spend ...]]

positional arguments:
  masternode_alias_to_start/spend

optional arguments:
  -h, --help            show this help message and exit
  -c, --check           check masternode config
  -s, --status          show masternode status
  -a, --anounce         anounce missing masternodes
  -b, --balance         show masternodes balance
  -m, --maketx          make signed raw tx
  -x, --xfer            broadcast signed raw tx


  version  : 0.2a
  caller   : <module>
  function : parse_args
  ===> print help

```


```

(venv3) ~/dashmnb $ python bin/dashmnb.py -c
    ____             __  
   / __ \____ ______/ /_ 
  / / / / __ `/ ___/ __ \
 / /_/ / /_/ (__  ) / / /
/_____/\__,_/____/_/ /_/ 
                         
    __  ___           __                            __   
   /  |/  /___ ______/ /____  _________  ____  ____/ /__ 
  / /|_/ / __ `/ ___/ __/ _ \/ ___/ __ \/ __ \/ __  / _ \
 / /  / / /_/ (__  ) /_/  __/ /  / / / / /_/ / /_/ /  __/
/_/  /_/\__,_/____/\__/\___/_/  /_/ /_/\____/\__,_/\___/ 
                                                         
           _ __  __       __  ___       __   _       __      ____     __ 
 _      __(_) /_/ /_     / / / / |     / /  | |     / /___ _/ / /__  / /_
| | /| / / / __/ __ \   / /_/ /| | /| / /   | | /| / / __ `/ / / _ \/ __/
| |/ |/ / / /_/ / / /  / __  / | |/ |/ /    | |/ |/ / /_/ / / /  __/ /_  
|__/|__/_/\__/_/ /_/  /_/ /_/  |__/|__/     |__/|__/\__,_/_/_/\___/\__/  
                                                                         

      by : chaeplin

Network : TESTNET

---> checking dashd syncing status 

-> protocolv : 70206
-> blockcnt  : 146823
-> blockhash : 00000003a24273220f22df0db174fccb5a5749820281d954dbaebde0b745e7b2

===> keepkey HW Wallet found
Passphrase required: 

Confirm your Passphrase: 

---> get address from hw wallet : 20
---> processing ████████████████████████████████ 100%


  version  : 0.2a
  caller   : main
  function : checking_mn_config
  ===> no masternode.testnet.conf file

```



```
(venv3) ~/dashmnb $ python bin/dashmnb.py -c
    ____             __  
   / __ \____ ______/ /_ 
  / / / / __ `/ ___/ __ \
 / /_/ / /_/ (__  ) / / /
/_____/\__,_/____/_/ /_/ 
                         
    __  ___           __                            __   
   /  |/  /___ ______/ /____  _________  ____  ____/ /__ 
  / /|_/ / __ `/ ___/ __/ _ \/ ___/ __ \/ __ \/ __  / _ \
 / /  / / /_/ (__  ) /_/  __/ /  / / / / /_/ / /_/ /  __/
/_/  /_/\__,_/____/\__/\___/_/  /_/ /_/\____/\__,_/\___/ 
                                                         
           _ __  __       __  ___       __   _       __      ____     __ 
 _      __(_) /_/ /_     / / / / |     / /  | |     / /___ _/ / /__  / /_
| | /| / / / __/ __ \   / /_/ /| | /| / /   | | /| / / __ `/ / / _ \/ __/
| |/ |/ / / /_/ / / /  / __  / | |/ |/ /    | |/ |/ / /_/ / / /  __/ /_  
|__/|__/_/\__/_/ /_/  /_/ /_/  |__/|__/     |__/|__/\__,_/_/_/\___/\__/  
                                                                         

      by : chaeplin

Network : TESTNET

---> checking dashd syncing status 

-> protocolv : 70206
-> blockcnt  : 146823
-> blockhash : 00000003a24273220f22df0db174fccb5a5749820281d954dbaebde0b745e7b2

===> keepkey HW Wallet found
Passphrase required: 

Confirm your Passphrase: 

---> get address from hw wallet : 20
---> processing ████████████████████████████████ 100%

---> checking masternode config using masternode.testnet.conf ....
  masternode : mn5
  masternode : mn6
  masternode : mn7
  masternode : mn8

[masternodes config]
  configured : 4
  passed     : 4

[masternodes status]
alias ip (m: ip/port match) collateral address       status
mn5 15.15.133.185:19999:m  yUduzrCkiLRYeN2dXenW5vT79D73A7GZw8 ENABLED
mn6 23.210.103.78:19999:m  yUKUDGVc2AzHeZZLGfCz7c313AZMZoBn1k ENABLED
mn7 23.210.97.225:19999:m  yRzYTUdLCAWVfvZ9WhJi5CrxcsU68DVox2 ENABLED
mn8 15.15.138.230:19999:m  ybv3cX4Gmn1ZK2ZgFgu51NADe3MXrtT7qP ENABLED



  version  : 0.2a
  caller   : <module>
  function : main
  ===> end of pg

```


```

(venv3) ~/dashmnb $ python bin/dashmnb.py -s
    ____             __  
   / __ \____ ______/ /_ 
  / / / / __ `/ ___/ __ \
 / /_/ / /_/ (__  ) / / /
/_____/\__,_/____/_/ /_/ 
                         
    __  ___           __                            __   
   /  |/  /___ ______/ /____  _________  ____  ____/ /__ 
  / /|_/ / __ `/ ___/ __/ _ \/ ___/ __ \/ __ \/ __  / _ \
 / /  / / /_/ (__  ) /_/  __/ /  / / / / /_/ / /_/ /  __/
/_/  /_/\__,_/____/\__/\___/_/  /_/ /_/\____/\__,_/\___/ 
                                                         
           _ __  __       __  ___       __   _       __      ____     __ 
 _      __(_) /_/ /_     / / / / |     / /  | |     / /___ _/ / /__  / /_
| | /| / / / __/ __ \   / /_/ /| | /| / /   | | /| / / __ `/ / / _ \/ __/
| |/ |/ / / /_/ / / /  / __  / | |/ |/ /    | |/ |/ / /_/ / / /  __/ /_  
|__/|__/_/\__/_/ /_/  /_/ /_/  |__/|__/     |__/|__/\__,_/_/_/\___/\__/  
                                                                         

      by : chaeplin

Network : TESTNET

---> checking dashd syncing status 

-> protocolv : 70206
-> blockcnt  : 146823
-> blockhash : 00000003a24273220f22df0db174fccb5a5749820281d954dbaebde0b745e7b2

===> keepkey HW Wallet found
Passphrase required: 

Confirm your Passphrase: 

---> get address from hw wallet : 20
---> processing ████████████████████████████████ 100%

---> checking masternode config using cache ....

[masternodes config]
  configured : 4
  passed     : 4

[masternodes status]
alias ip (m: ip/port match) collateral address       status
mn5 15.15.133.185:19999:m  yUduzrCkiLRYeN2dXenW5vT79D73A7GZw8 ENABLED
mn6 23.210.103.78:19999:m  yUKUDGVc2AzHeZZLGfCz7c313AZMZoBn1k ENABLED
mn7 23.210.97.225:19999:m  yRzYTUdLCAWVfvZ9WhJi5CrxcsU68DVox2 ENABLED
mn8 15.15.138.230:19999:m  ybv3cX4Gmn1ZK2ZgFgu51NADe3MXrtT7qP ENABLED



  version  : 0.2a
  caller   : <module>
  function : main
  ===> end of pg

```


```

(venv3) ~/dashmnb $ python bin/dashmnb.py -a mn7
    ____             __  
   / __ \____ ______/ /_ 
  / / / / __ `/ ___/ __ \
 / /_/ / /_/ (__  ) / / /
/_____/\__,_/____/_/ /_/ 
                         
    __  ___           __                            __   
   /  |/  /___ ______/ /____  _________  ____  ____/ /__ 
  / /|_/ / __ `/ ___/ __/ _ \/ ___/ __ \/ __ \/ __  / _ \
 / /  / / /_/ (__  ) /_/  __/ /  / / / / /_/ / /_/ /  __/
/_/  /_/\__,_/____/\__/\___/_/  /_/ /_/\____/\__,_/\___/ 
                                                         
           _ __  __       __  ___       __   _       __      ____     __ 
 _      __(_) /_/ /_     / / / / |     / /  | |     / /___ _/ / /__  / /_
| | /| / / / __/ __ \   / /_/ /| | /| / /   | | /| / / __ `/ / / _ \/ __/
| |/ |/ / / /_/ / / /  / __  / | |/ |/ /    | |/ |/ / /_/ / / /  __/ /_  
|__/|__/_/\__/_/ /_/  /_/ /_/  |__/|__/     |__/|__/\__,_/_/_/\___/\__/  
                                                                         

      by : chaeplin

Network : TESTNET

---> checking dashd syncing status 

-> protocolv : 70206
-> blockcnt  : 146823
-> blockhash : 00000003a24273220f22df0db174fccb5a5749820281d954dbaebde0b745e7b2

===> keepkey HW Wallet found
Passphrase required: 

Confirm your Passphrase: 

---> get address from hw wallet : 20
---> processing ████████████████████████████████ 100%

---> checking masternode config using cache ....

[masternodes config]
  configured : 4
  passed     : 4

[masternodes status]
alias ip (m: ip/port match) collateral address       status
mn5 15.15.133.185:19999:m  yUduzrCkiLRYeN2dXenW5vT79D73A7GZw8 ENABLED
mn6 23.210.103.78:19999:m  yUKUDGVc2AzHeZZLGfCz7c313AZMZoBn1k ENABLED
mn7 23.210.97.225:19999:m  yRzYTUdLCAWVfvZ9WhJi5CrxcsU68DVox2 ENABLED
mn8 15.15.138.230:19999:m  ybv3cX4Gmn1ZK2ZgFgu51NADe3MXrtT7qP ENABLED


[making mnbs and relay]
---> making mnb for mn7
---> check hw wallet, check message on screen and press button
  if PIN protected, wallet ask your PIN(once per session)
  if Passphrase protected, wallet ask your Passphrase(once per session)
  check message on screen and press button on hw wallet to proceed(all signing)

---> mnb hex for mn7 : b1a6b9f80be726455f29353fd295f78a7d21878db5f48a087d2f935f5e6e95380000000000ffffffff00000000000000000000ffff858261e14e1f210294ac0a0e95e61a6cab53bedcdda4a26543a7ba199a393ef8f660aa923b1dc59441041708bfbf96c2d35a48a1db88add3bdaaa8c222b0ebdaff77ed822c5c56222c47324c965afffa0e0891e9476854cae531e4447ae973941bef53bcf147b0fc29c5411fefd8f2931461d2374592056c9f4663a0a4a59bc6e6de6e5987895250eaf62d1e627fd4a4c91189c8e01e89e954a8b170005ce9512f14fcb3a831fce5bc6d875a6b439458000000003e120100b1a6b9f80be726455f29353fd295f78a7d21878db5f48a087d2f935f5e6e95380000000000ffffffff02c2fd5b63a8117b39a41096cd002c7373d5ea09191a69e4e443c8fd0c0000006b43945800000000411b2db75a3f6e509bbe43a025475f76a5c4ae06c56c5368ba1aac0aa151ae90a0106995944699a490fd9d81f1f4e853c68ea361dbef15b013502e08a1aaf94e5cf8


---> verify(decoding mnb)
  ---> total   : 1
  ---> success : 1
  ---> failed  : 0

{
    "51af1013db185018b16684b369de74269c5d7a95671e4a042842f0aee72ff828": {
        "addr": "23.210.97.225:19999",
        "lastPing": {
            "blockHash": "0000000cfdc843e4e4691a1909ead573732c00cd9610a4397b11a8635bfdc202",
            "sigTime": 1486111595,
            "vchSig": "Gy23Wj9uUJu+Q6AlR192pcSuBsVsU2i6GqwKoVGukKAQaZWURpmkkP2dgfH06FPGjqNh2+8VsBNQLgihqvlOXPg=",
            "vin": "CTxIn(COutPoint(38956e5e5f932f7d088af4b58d87217d8af795d23f35295f4526e70bf8b9a6b1, 0), scriptSig=)"
        },
        "nLastDsq": 0,
        "protocolVersion": 70206,
        "pubKeyCollateralAddress": "yRzYTUdLCAWVfvZ9WhJi5CrxcsU68DVox2",
        "pubKeyMasternode": "yi3JF94TwqfqWiNhUEMvQ2iot1W9o3Jj8o",
        "sigTime": 1486111595,
        "vchSig": "H+/Y8pMUYdI3RZIFbJ9GY6CkpZvG5t5uWYeJUlDq9i0eYn/UpMkRicjgHonpVKixcABc6VEvFPyzqDH85bxth1o=",
        "vin": "CTxIn(COutPoint(38956e5e5f932f7d088af4b58d87217d8af795d23f35295f4526e70bf8b9a6b1, 0), scriptSig=)"
    },
    "overall": "Successfully decoded broadcast messages for 1 masternodes, failed to decode 0, total 1"
}

Relay broadcast messages ? [ Yes / (any key to no) ] + enter : Yes
Yes, will relay

---> relay(announcing mnb)
  ---> total   : 1
  ---> success : 1
  ---> failed  : 0

{
    "51af1013db185018b16684b369de74269c5d7a95671e4a042842f0aee72ff828": {
        "vin": "CTxIn(COutPoint(38956e5e5f932f7d088af4b58d87217d8af795d23f35295f4526e70bf8b9a6b1, 0), scriptSig=)",
        "addr": "23.210.97.225:19999",
        "51af1013db185018b16684b369de74269c5d7a95671e4a042842f0aee72ff828": "successful"
    },
    "overall": "Successfully relayed broadcast messages for 1 masternodes, failed to relay 0, total 1"
}


  version  : 0.2a
  caller   : <module>
  function : main
  ===> end of pg

```


```

(venv3) ~/dashmnb $ python bin/dashmnb.py -s
    ____             __  
   / __ \____ ______/ /_ 
  / / / / __ `/ ___/ __ \
 / /_/ / /_/ (__  ) / / /
/_____/\__,_/____/_/ /_/ 
                         
    __  ___           __                            __   
   /  |/  /___ ______/ /____  _________  ____  ____/ /__ 
  / /|_/ / __ `/ ___/ __/ _ \/ ___/ __ \/ __ \/ __  / _ \
 / /  / / /_/ (__  ) /_/  __/ /  / / / / /_/ / /_/ /  __/
/_/  /_/\__,_/____/\__/\___/_/  /_/ /_/\____/\__,_/\___/ 
                                                         
           _ __  __       __  ___       __   _       __      ____     __ 
 _      __(_) /_/ /_     / / / / |     / /  | |     / /___ _/ / /__  / /_
| | /| / / / __/ __ \   / /_/ /| | /| / /   | | /| / / __ `/ / / _ \/ __/
| |/ |/ / / /_/ / / /  / __  / | |/ |/ /    | |/ |/ / /_/ / / /  __/ /_  
|__/|__/_/\__/_/ /_/  /_/ /_/  |__/|__/     |__/|__/\__,_/_/_/\___/\__/  
                                                                         

      by : chaeplin

Network : TESTNET

---> checking dashd syncing status 

-> protocolv : 70206
-> blockcnt  : 146823
-> blockhash : 00000003a24273220f22df0db174fccb5a5749820281d954dbaebde0b745e7b2

===> keepkey HW Wallet found
Passphrase required: 

Confirm your Passphrase: 

---> get address from hw wallet : 20
---> processing ████████████████████████████████ 100%

---> checking masternode config using cache ....

[masternodes config]
  configured : 4
  passed     : 4

[masternodes status]
alias ip (m: ip/port match) collateral address       status
mn5 15.15.133.185:19999:m  yUduzrCkiLRYeN2dXenW5vT79D73A7GZw8 ENABLED
mn6 23.210.103.78:19999:m  yUKUDGVc2AzHeZZLGfCz7c313AZMZoBn1k ENABLED
mn7 23.210.97.225:19999:m  yRzYTUdLCAWVfvZ9WhJi5CrxcsU68DVox2 PRE_ENABLED
mn8 15.15.138.230:19999:m  ybv3cX4Gmn1ZK2ZgFgu51NADe3MXrtT7qP ENABLED



  version  : 0.2a
  caller   : <module>
  function : main
  ===> end of pg

```


```

(venv3) ~/dashmnb $ python bin/dashmnb.py -b
    ____             __  
   / __ \____ ______/ /_ 
  / / / / __ `/ ___/ __ \
 / /_/ / /_/ (__  ) / / /
/_____/\__,_/____/_/ /_/ 
                         
    __  ___           __                            __   
   /  |/  /___ ______/ /____  _________  ____  ____/ /__ 
  / /|_/ / __ `/ ___/ __/ _ \/ ___/ __ \/ __ \/ __  / _ \
 / /  / / /_/ (__  ) /_/  __/ /  / / / / /_/ / /_/ /  __/
/_/  /_/\__,_/____/\__/\___/_/  /_/ /_/\____/\__,_/\___/ 
                                                         
           _ __  __       __  ___       __   _       __      ____     __ 
 _      __(_) /_/ /_     / / / / |     / /  | |     / /___ _/ / /__  / /_
| | /| / / / __/ __ \   / /_/ /| | /| / /   | | /| / / __ `/ / / _ \/ __/
| |/ |/ / / /_/ / / /  / __  / | |/ |/ /    | |/ |/ / /_/ / / /  __/ /_  
|__/|__/_/\__/_/ /_/  /_/ /_/  |__/|__/     |__/|__/\__,_/_/_/\___/\__/  
                                                                         

      by : chaeplin

Network : TESTNET

---> checking dashd syncing status 

-> protocolv : 70206
-> blockcnt  : 146823
-> blockhash : 00000003a24273220f22df0db174fccb5a5749820281d954dbaebde0b745e7b2

===> keepkey HW Wallet found
Passphrase required: 

Confirm your Passphrase: 

---> get address from hw wallet : 20
---> processing ████████████████████████████████ 100%

---> checking masternode config using cache ....

[masternodes config]
  configured : 4
  passed     : 4

[masternodes status]
alias ip (m: ip/port match) collateral address       status
mn5 15.15.133.185:19999:m  yUduzrCkiLRYeN2dXenW5vT79D73A7GZw8 ENABLED
mn6 23.210.103.78:19999:m  yUKUDGVc2AzHeZZLGfCz7c313AZMZoBn1k ENABLED
mn7 23.210.97.225:19999:m  yRzYTUdLCAWVfvZ9WhJi5CrxcsU68DVox2 PRE_ENABLED
mn8 15.15.138.230:19999:m  ybv3cX4Gmn1ZK2ZgFgu51NADe3MXrtT7qP ENABLED

[masternodes balance]
alias cnt balance   address to send
mn5  6  1056.25021282 yUivY45DcZkJ34nPdxCXFTo6QfZtG5XBjm
mn6 23  1247.50053690 yTagztqtBTKMcKRuw8QphRtUT5xCEcy71J
mn7  3  1022.50019410 ye3eBg1SrP74awLHbEgg8PTHKzeYUBi3B3
mn8  3  1022.50026940 yNYJy9ShtJWo2NFcT7sjRa2ucktTFFe71b

* count / balance : including collateral and unmature mn payment
* can be inaccurate after transfer(xfer), need 1 confirmation


  version  : 0.2a
  caller   : <module>
  function : main
  ===> end of pg

```


```

(venv3) ~/dashmnb $ python bin/dashmnb.py -x mn5
    ____             __  
   / __ \____ ______/ /_ 
  / / / / __ `/ ___/ __ \
 / /_/ / /_/ (__  ) / / /
/_____/\__,_/____/_/ /_/ 
                         
    __  ___           __                            __   
   /  |/  /___ ______/ /____  _________  ____  ____/ /__ 
  / /|_/ / __ `/ ___/ __/ _ \/ ___/ __ \/ __ \/ __  / _ \
 / /  / / /_/ (__  ) /_/  __/ /  / / / / /_/ / /_/ /  __/
/_/  /_/\__,_/____/\__/\___/_/  /_/ /_/\____/\__,_/\___/ 
                                                         
           _ __  __       __  ___       __   _       __      ____     __ 
 _      __(_) /_/ /_     / / / / |     / /  | |     / /___ _/ / /__  / /_
| | /| / / / __/ __ \   / /_/ /| | /| / /   | | /| / / __ `/ / / _ \/ __/
| |/ |/ / / /_/ / / /  / __  / | |/ |/ /    | |/ |/ / /_/ / / /  __/ /_  
|__/|__/_/\__/_/ /_/  /_/ /_/  |__/|__/     |__/|__/\__,_/_/_/\___/\__/  
                                                                         

      by : chaeplin

Network : TESTNET

---> checking dashd syncing status 

-> protocolv : 70206
-> blockcnt  : 146823
-> blockhash : 00000003a24273220f22df0db174fccb5a5749820281d954dbaebde0b745e7b2

===> keepkey HW Wallet found
Passphrase required: 

Confirm your Passphrase: 

---> get address from hw wallet : 20
---> processing ████████████████████████████████ 100%

---> checking masternode config using cache ....

[masternodes config]
  configured : 4
  passed     : 4

[masternodes status]
alias ip (m: ip/port match) collateral address       status
mn5 15.15.133.185:19999:m  yUduzrCkiLRYeN2dXenW5vT79D73A7GZw8 ENABLED
mn6 23.210.103.78:19999:m  yUKUDGVc2AzHeZZLGfCz7c313AZMZoBn1k ENABLED
mn7 23.210.97.225:19999:m  yRzYTUdLCAWVfvZ9WhJi5CrxcsU68DVox2 PRE_ENABLED
mn8 15.15.138.230:19999:m  ybv3cX4Gmn1ZK2ZgFgu51NADe3MXrtT7qP ENABLED

[masternodes balance]
alias cnt balance   address to send
mn5  6  1056.25021282 yUivY45DcZkJ34nPdxCXFTo6QfZtG5XBjm
mn6 23  1247.50053690 yTagztqtBTKMcKRuw8QphRtUT5xCEcy71J
mn7  3  1022.50019410 ye3eBg1SrP74awLHbEgg8PTHKzeYUBi3B3
mn8  3  1022.50026940 yNYJy9ShtJWo2NFcT7sjRa2ucktTFFe71b

* count / balance : including collateral and unmature mn payment
* can be inaccurate after transfer(xfer), need 1 confirmation
[making txs]
---> signing txs for mn mn5: 

  send 44.99999380
  4 txs to yUivY45DcZkJ34nPdxCXFTo6QfZtG5XBjm
  with fee of 0.0001
  total amount : 45.00009380

---> check hw wallet, check message on screen and press button
  if PIN protected, wallet ask your PIN(once per session)
  if Passphrase protected, wallet ask your Passphrase(once per session)
  check message on screen and press button on hw wallet to proceed(all signing)

Use the numeric keypad to describe number positions. The layout is:
    7 8 9
    4 5 6
    1 2 3
Please enter current PIN: 

RECEIVED PART OF SERIALIZED TX (152 BYTES)
RECEIVED PART OF SERIALIZED TX (148 BYTES)
RECEIVED PART OF SERIALIZED TX (148 BYTES)
RECEIVED PART OF SERIALIZED TX (148 BYTES)
RECEIVED PART OF SERIALIZED TX (39 BYTES)
SIGNED IN 26.785 SECONDS, CALLED 47 MESSAGES, 635 BYTES

verify tx for mn5
[
    {
        "n": 0,
        "scriptPubKey": {
            "addresses": [
                "yUivY45DcZkJ34nPdxCXFTo6QfZtG5XBjm"
            ],
            "asm": "OP_DUP OP_HASH160 5c31af76967eed641bf109253b3003d15883db30 OP_EQUALVERIFY OP_CHECKSIG",
            "hex": "76a9145c31af76967eed641bf109253b3003d15883db3088ac",
            "reqSigs": 1,
            "type": "pubkeyhash"
        },
        "value": 44.99999380,
        "valueSat": 4499999380
    }
]

Broadcast signed raw tx ? [ Yes / (any key to no) ] + enter : Yes

Yes, will broadcast

====> txid : f10f34a65455068bf59febfb2da1c6ead813b391e9c28e58d9664ee3fce2ad59


  f10f34a65455068bf59febfb2da1c6ead813b391e9c28e58d9664ee3fce2ad59


  version  : 0.2a
  caller   : <module>
  function : main
  ===> end of pg

  ```