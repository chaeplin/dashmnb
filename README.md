Run Dash Masternode with Hardware Wallet
=========================================

#### TESTNET ONLY ####

###### Q : why firmware update ?
    - to support Dash testnet, both trezor and keepkey has only Mainnet.
    - with Mainnet, no need to update firmware. Use official firmware.


###### Q : what can dashmnb do
    - config check (alias, address, ip, key, pkey, hw wallet path)
    - start masternode missing, selected
    - show masternode status
    - send coins(mn payment) in hw wallet
    - send collateral + coins(mn payment) in hw wallet
    - ssh tunnel to use remote dashd

###### Q : why Dash-QT or dashd needed ?
    - instead of block explorer 
    - to sign mnp included in mnb(mnb signed by hw wallet)
    - to check address, collateral, masternode status
    - to get unspent tx of collateral using watch only address
    - to relay mnb and txs


###### Q : why do -rescan
    - -rescan means restaring dashd or Dash-QT with -rescan option
    - while dashmnb do importaddress, dashmnb set rescan 'False' cause rescan usually takes more than 30 secs and rpc timeout occured.
    - after initial checking of masternode config, dashmnb will ask you to do rescan


###### help
```
(venv3)  > $ python dashmnb.py 
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


  version  : 0.1a
  caller   : <module>
  function : parse_args
  ===> print help
```



###### show masternode status and balance
````

(venv3)  > $ python dashmnb.py  -b
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
===> No HW Wallet found
---> checking dashd syncing status 
---> checking masternode config ....
  masternode : mn5
  masternode : mn6
  masternode : mn7
  masternode : mn8

[masternodes config]
  configured : 4
  passed     : 4


[masternodes status]
alias ip (m: ip/port match) collateral address       status
mn5 123.123.123.185:19999:m  yUduzrCkiLRYeN2dXenW5vT79D73A7GZw8 ENABLED
mn6 123.123.124.178:19999:m  yUKUDGVc2AzHeZZLGfCz7c313AZMZoBn1k ENABLED
mn7 123.123.125.225:19999:m  yRzYTUdLCAWVfvZ9WhJi5CrxcsU68DVox2 ENABLED
mn8 123.123.128.230:19999:m  ybv3cX4Gmn1ZK2ZgFgu51NADe3MXrtT7qP ENABLED

[masternodes balance]
alias cnt balance(dashd)  balance(explorer)
mn5  2  1011.25000000 1022.50000000
mn6  2  1011.25000000 1033.75000000
mn7  2  1011.25000000 1011.25000000
mn8  2  1011.25000000 1022.50006680

* count / balance of dashd is spendable
(over [6 - received, 100 - mnpayment] confirmations)



  version  : 0.1a
  caller   : <module>
  function : main
  ===> need HW wallet to spend

```


###### re anounnunce mn 7 (no hardware wallet)
````
(venv3)  > $ python dashmnb.py  -a mn7
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
===> No HW Wallet found
---> checking dashd syncing status 
---> checking masternode config ....
  masternode : mn5
  masternode : mn6
  masternode : mn7
  masternode : mn8

[masternodes config]
  configured : 4
  passed     : 4


[masternodes status]
alias ip (m: ip/port match) collateral address       status
mn5 123.123.123.185:19999:m  yUduzrCkiLRYeN2dXenW5vT79D73A7GZw8 ENABLED
mn6 123.123.124.178:19999:m  yUKUDGVc2AzHeZZLGfCz7c313AZMZoBn1k ENABLED
mn7 123.123.125.225:19999:m  yRzYTUdLCAWVfvZ9WhJi5CrxcsU68DVox2 ENABLED
mn8 123.123.128.230:19999:m  ybv3cX4Gmn1ZK2ZgFgu51NADe3MXrtT7qP ENABLED



  version  : 0.1a
  caller   : <module>
  function : main
  ===> need HW wallet to anounce

```

###### re anounnunce mn 7
````
(venv3)  > $ python dashmnb.py  -a mn7
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
===> trezor HW Wallet found
---> checking dashd syncing status 
---> checking masternode config ....
  masternode : mn5
  masternode : mn6
  masternode : mn7
  masternode : mn8

[masternodes config]
  configured : 4
  passed     : 4


[masternodes status]
alias ip (m: ip/port match) collateral address       status
mn5 123.123.123.185:19999:m  yUduzrCkiLRYeN2dXenW5vT79D73A7GZw8 ENABLED
mn6 123.123.124.178:19999:m  yUKUDGVc2AzHeZZLGfCz7c313AZMZoBn1k ENABLED
mn7 123.123.125.225:19999:m  yRzYTUdLCAWVfvZ9WhJi5CrxcsU68DVox2 ENABLED
mn8 123.123.128.230:19999:m  ybv3cX4Gmn1ZK2ZgFgu51NADe3MXrtT7qP ENABLED


[making mnbs and relay]
---> making mnb for mn7
---> check hw wallet, check message on screen and press button
  if PIN protected, wallet ask your PIN(once per session)
  if Passphrase protected, wallet ask your Passphrase(once per session)
  check message on screen and press button on hw wallet to proceed(all signing)

Use the numeric keypad to describe number positions. The layout is:
    7 8 9
    4 5 6
    1 2 3
Please enter current PIN: 

Passphrase required: 

Confirm your Passphrase: 

---> mnb hex for mn7 : b1a6b9f80be726455f29353fd295f78a7d21878db5f48a087d2f935f5e6e95380000000000ffffffff00000000000000000000ffff858261e14e1f210294ac0a0e95e61a6cab53bedcdda4a26543a7ba199a393ef8f660aa923b1dc59441041708bfbf96c2d35a48a1db88add3bdaaa8c222b0ebdaff77ed822c5c56222c47324c965afffa0e0891e9476854cae531e4447ae973941bef53bcf147b0fc29c5411f815cfa0cd8bac5977d2fd7f42c1d7bbcc70339c1830d75084a39623723c57ee3646644943c04f3f7d54af5e0144f75b3fd13b69e717967aa879bd4cbf77739b131a08758000000003c120100b1a6b9f80be726455f29353fd295f78a7d21878db5f48a087d2f935f5e6e95380000000000ffffffff3c47f192e6e02bf0b9c833208c6b66be550e63a3646b29c11b51f95a6800000031a0875800000000411b11ff7dea3ddac07badbaffc2d97bc0eb1482ae972a87d2f7ef2a059dd7771823263946ca225eb06c47efca430de51b74d366944dd9fb893fc65a91ddc5f22fb5


---> verify(decoding mnb)
  ---> total   : 1
  ---> success : 1
  ---> failed  : 0

{
    "bd845160b6fdfc8f45da6a2aa6f6274724a16236e7a1e018c4babe8807e5115a": {
        "addr": "123.123.125.225:19999",
        "lastPing": {
            "blockHash": "000000685af9511bc1296b64a3630e55be666b8c2033c8b9f02be0e692f1473c",
            "sigTime": 1485283377,
            "vchSig": "GxH/feo92sB7rbr/wtl7wOsUgq6XKofS9+8qBZ3XdxgjJjlGyiJesGxH78pDDeUbdNNmlE3Z+4k/xlqR3cXyL7U=",
            "vin": "CTxIn(COutPoint(38956e5e5f932f7d088af4b58d87217d8af795d23f35295f4526e70bf8b9a6b1, 0), scriptSig=)"
        },
        "nLastDsq": 0,
        "protocolVersion": 70204,
        "pubKeyCollateralAddress": "yRzYTUdLCAWVfvZ9WhJi5CrxcsU68DVox2",
        "pubKeyMasternode": "yi3JF94TwqfqWiNhUEMvQ2iot1W9o3Jj8o",
        "sigTime": 1485283377,
        "vchSig": "H4Fc+gzYusWXfS/X9Cwde7zHAznBgw11CEo5YjcjxX7jZGZElDwE8/fVSvXgFE91s/0Ttp5xeWeqh5vUy/d3ObE=",
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
    "bd845160b6fdfc8f45da6a2aa6f6274724a16236e7a1e018c4babe8807e5115a": {
        "vin": "CTxIn(COutPoint(38956e5e5f932f7d088af4b58d87217d8af795d23f35295f4526e70bf8b9a6b1, 0), scriptSig=)",
        "bd845160b6fdfc8f45da6a2aa6f6274724a16236e7a1e018c4babe8807e5115a": "successful",
        "addr": "123.123.125.225:19999"
    },
    "overall": "Successfully relayed broadcast messages for 1 masternodes, failed to relay 0, total 1"
}


  version  : 0.1a
  caller   : <module>
  function : main
  ===> end of pg

```

###### status
````
(venv3)  > $ python dashmnb.py  -s
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
===> trezor HW Wallet found
---> checking dashd syncing status 
---> checking masternode config ....
  masternode : mn5
  masternode : mn6
  masternode : mn7
  masternode : mn8

[masternodes config]
  configured : 4
  passed     : 4


[masternodes status]
alias ip (m: ip/port match) collateral address       status
mn5 123.123.123.185:19999:m  yUduzrCkiLRYeN2dXenW5vT79D73A7GZw8 ENABLED
mn6 123.123.124.178:19999:m  yUKUDGVc2AzHeZZLGfCz7c313AZMZoBn1k ENABLED
mn7 123.123.125.225:19999:m  yRzYTUdLCAWVfvZ9WhJi5CrxcsU68DVox2 PRE_ENABLED
mn8 123.123.128.230:19999:m  ybv3cX4Gmn1ZK2ZgFgu51NADe3MXrtT7qP ENABLED



  version  : 0.1a
  caller   : <module>
  function : main
  ===> end of pg

````


###### show status and balance
```
(venv3)  > $ python dashmnb.py  -b
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
===> trezor HW Wallet found
---> checking dashd syncing status 
---> checking masternode config ....
  masternode : mn5
  masternode : mn6
  masternode : mn7
  masternode : mn8

[masternodes config]
  configured : 4
  passed     : 4


[masternodes status]
alias ip (m: ip/port match) collateral address       status
mn5 123.123.123.185:19999:m  yUduzrCkiLRYeN2dXenW5vT79D73A7GZw8 ENABLED
mn6 123.123.124.178:19999:m  yUKUDGVc2AzHeZZLGfCz7c313AZMZoBn1k ENABLED
mn7 123.123.125.225:19999:m  yRzYTUdLCAWVfvZ9WhJi5CrxcsU68DVox2 PRE_ENABLED
mn8 123.123.128.230:19999:m  ybv3cX4Gmn1ZK2ZgFgu51NADe3MXrtT7qP ENABLED

[masternodes balance]
alias cnt balance(dashd)  balance(explorer)
mn5  2  1011.25000000 1022.50000000
mn6  2  1011.25000000 1033.75000000
mn7  2  1011.25000000 1011.25000000
mn8  2  1011.25000000 1022.50006680

* count / balance of dashd is spendable
(over [6 - received, 100 - mnpayment] confirmations)



  version  : 0.1a
  caller   : <module>
  function : main
  ===> end of pg
```


###### transfer mn payment
```
(venv3)  > $ python dashmnb.py -x mn5
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
===> trezor HW Wallet found
---> checking dashd syncing status 
---> checking masternode config ....
  masternode : mn5
  masternode : mn6
  masternode : mn7
  masternode : mn8

[masternodes config]
  configured : 4
  passed     : 4


[masternodes status]
alias ip (m: ip/port match) collateral address       status
mn5 123.123.123.185:19999:m  yUduzrCkiLRYeN2dXenW5vT79D73A7GZw8 ENABLED
mn6 123.123.124.178:19999:m  yUKUDGVc2AzHeZZLGfCz7c313AZMZoBn1k ENABLED
mn7 123.123.125.225:19999:m  yRzYTUdLCAWVfvZ9WhJi5CrxcsU68DVox2 PRE_ENABLED
mn8 123.123.128.230:19999:m  ybv3cX4Gmn1ZK2ZgFgu51NADe3MXrtT7qP ENABLED


[masternodes balance]
alias cnt balance(dashd)  balance(explorer)
mn5  2  1011.25000000 1022.50000000
mn6  2  1011.25000000 1033.75000000
mn7  2  1011.25000000 1011.25000000
mn8  1  1000.00000000 1022.50006680

* count / balance of dashd is spendable
(over [6 - received, 100 - mnpayment] confirmations)

[making txs]
---> signing txs for mn mn5: 
  send 11.24990000, 1 txs to yUv7gWUhFk8iZv141FW5QncFLwpD73y9Ne with fee of 0.0001 : total amount : 11.25000000

---> check hw wallet, check message on screen and press button
  if PIN protected, wallet ask your PIN(once per session)
  if Passphrase protected, wallet ask your Passphrase(once per session)
  check message on screen and press button on hw wallet to proceed(all signing)

Use the numeric keypad to describe number positions. The layout is:
    7 8 9
    4 5 6
    1 2 3
Please enter current PIN: 

Passphrase required: 

Confirm your Passphrase: 

RECEIVED PART OF SERIALIZED TX (152 BYTES)
RECEIVED PART OF SERIALIZED TX (39 BYTES)
SIGNED IN 50.316 SECONDS, CALLED 11 MESSAGES, 191 BYTES

verify tx for mn5
[
    {
        "n": 0,
        "scriptPubKey": {
            "addresses": [
                "yUv7gWUhFk8iZv141FW5QncFLwpD73y9Ne"
            ],
            "asm": "OP_DUP OP_HASH160 5e4f90a49c1c0da034320b35ce5ef813311e9ba6 OP_EQUALVERIFY OP_CHECKSIG",
            "hex": "76a9145e4f90a49c1c0da034320b35ce5ef813311e9ba688ac",
            "reqSigs": 1,
            "type": "pubkeyhash"
        },
        "value": 11.24990000,
        "valueSat": 1124990000
    }
]

Broadcast signed raw tx ? [ Yes / (any key to no) ] + enter : Yes

Yes, will broadcast

====> txid : 1e07a3ded6ec6ba768b1e7334141a8074590a487003b313d7776fd94e313d6b2


  1e07a3ded6ec6ba768b1e7334141a8074590a487003b313d7776fd94e313d6b2


  version  : 0.1a
  caller   : <module>
  function : main
  ===> end of pg






(venv3)  > $ python dashmnb.py -b
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
===> trezor HW Wallet found
---> checking dashd syncing status 
---> checking masternode config ....
  masternode : mn5
  masternode : mn6
  masternode : mn7
  masternode : mn8

[masternodes config]
  configured : 4
  passed     : 4


[masternodes status]
alias ip (m: ip/port match) collateral address       status
mn5 123.123.123.185:19999:m  yUduzrCkiLRYeN2dXenW5vT79D73A7GZw8 ENABLED
mn6 123.123.124.178:19999:m  yUKUDGVc2AzHeZZLGfCz7c313AZMZoBn1k ENABLED
mn7 123.123.125.225:19999:m  yRzYTUdLCAWVfvZ9WhJi5CrxcsU68DVox2 ENABLED
mn8 123.123.128.230:19999:m  ybv3cX4Gmn1ZK2ZgFgu51NADe3MXrtT7qP ENABLED

[masternodes balance]
alias cnt balance(dashd)  balance(explorer)
mn5  1  1000.00000000 1022.50000000
mn6  2  1011.25000000 1033.75000000
mn7  2  1011.25000000 1011.25000000
mn8  2  1011.25000000 1022.50006680

* count / balance of dashd is spendable
(over [6 - received, 100 - mnpayment] confirmations)



  version  : 0.1a
  caller   : <module>
  function : main
  ===> end of pg


```






###### requirement
- Dash-QT or dashd
- Keepkey, Trezor
- keepkey-firmware
- Trezor-firmware
- rpc conn to Dash-QT or dashd
- python3
- python-keepkey [for keepkey]
- python-trezor [for trezor]
- python-bitcoinrpc
- python-progress
- python-pyfiglet
- python-bip32utils

###### Keepkey firmware
- Build your own firmware
- https://github.com/chaeplin/dash-testnet/tree/master/keepkey_firmware [for keepkey]
- https://github.com/chaeplin/trezor-mcu or https://github.com/dashpay/trezor-mcu [for trezor]

###### python lib
- use python-virtualenv3
- https://github.com/chaeplin/python-keepkey [for keepkey]
- https://github.com/chaeplin/python-trezor  [for trezor]
- https://github.com/chaeplin/python-bitcoinrpc
- https://github.com/verigak/progress
- https://github.com/pwaller/pyfiglet
- https://github.com/chaeplin/bip32utils
- lib (sub dir)

```
virtualenv -p python3 venv3
source venv3/bin/activate
python "pg to run"
```

###### How to
- use hw-wallet-for-mn.py to gen a list of address (change key path = mpath)
- send 1k tDash to Address
- set up remote masternode
- move config.py.sample to config.py and edit parameters
- move masternode.conf.sample to masternode.conf and edit
- run Dash-QT or dashd
- run dashmnb.py


######
    https://test.explorer.dash.org/tx/dec9c5ef0b4f82b77107f29e0096a30faacbf068f5b46a106726b02036caaeb4#o0
    https://test.explorer.dash.org/tx/82552b6626c9d2ea35c5295135b09acd351a28f552d3a666612d85e36f805e26#o0
    https://test.explorer.dash.org/tx/11c3467a318e33d5b45c588c1676b9d09f4999a96c8ce720b9d4d5815181e28a#o0
    https://test.explorer.dash.org/tx/b7910641dcc640154947d8610ebbdc1e52b7c43383a8b4e96cde6fbd089780a2#o0

