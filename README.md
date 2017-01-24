Run Dash Masternode with Hardware Wallet
=========================================

#### TESTNET ONLY ####

###### Q : why firmware update ?
    - To support Dash testnet, both trezor and keepkey has only Mainnet.
    - With Mainnet, no need to update firmware. Use official firmware.


###### Q : what can dashmnb do
    - config check (alias, address, ip, key, pkey, hw wallet path)
    - start masternode missing, selected
    - show masternode status
    - send coins(mn payment) in hw wallet
    - send collateral + coins(mn payment) in hw wallet


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
mn5  1   1000.00000000   1011.25000000
mn6  1   1000.00000000   1011.25000000
mn7  1   1000.00000000   1011.25000000
mn8  1   1000.00000000   1011.25000000

* count / balance of dashd is spendable
(over [6 - received, 100 - mnpayment] confirmations)



  version  : 0.1a
  caller   : <module>
  function : main
  ===> need HW wallet to spend

```


###### re anounnunce mn 7 (now hardware wallet)
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
---> check keepkey and press button
Use the numeric keypad to describe number positions. The layout is:
    7 8 9
    4 5 6
    1 2 3
Please enter current PIN: 

Passphrase required: 

Confirm your Passphrase: 

---> mnb hex for mn7 : b1a6b9f80be726455f29353fd295f78a7d21878db5f48a087d2f935f5e6e95380000000000ffffffff00000000000000000000ffff858261e14e1f210294ac0a0e95e61a6cab53bedcdda4a26543a7ba199a393ef8f660aa923b1dc59441041708bfbf96c2d35a48a1db88add3bdaaa8c222b0ebdaff77ed822c5c56222c47324c965afffa0e0891e9476854cae531e4447ae973941bef53bcf147b0fc29c5412017f08f7911c24c501c51bcbb43c3eff65b0168f123ad45fdd37c2465c33ad29a1dd9fb33bc3b4db7c7b5a56a7f36cf3e39dc9f776b0fe76c196af99443ec7077c6758758000000003c120100b1a6b9f80be726455f29353fd295f78a7d21878db5f48a087d2f935f5e6e95380000000000ffffffff83003c0a9eeeea274efc4ab2366a4ea17da17b2db87bbe4d39accb170a000000c675875800000000411cfcf2572cf1a5128be955ff005f2e5772cb23e3d52e45ba5620b4a2df1599f8a67a80b3f3fdf8116f4e228920665fb5bddc4e30121ec7bba209001e126d72c300


---> verify(decoding mnb)
  ---> total   : 1
  ---> success : 1
  ---> failed  : 0

{
    "0ee9155594b786f8367410af021406fc3aa030950ea750410f8396ce4dd315cd": {
        "addr": "123.123.125.225:19999",
        "lastPing": {
            "blockHash": "0000000a17cbac394dbe7bb82d7ba17da14e6a36b24afc4e27eaee9e0a3c0083",
            "sigTime": 1485272518,
            "vchSig": "HPzyVyzxpRKL6VX/AF8uV3LLI+PVLkW6ViC0ot8VmfimeoCz8/34EW9OIokgZl+1vdxOMBIex7uiCQAeEm1ywwA=",
            "vin": "CTxIn(COutPoint(38956e5e5f932f7d088af4b58d87217d8af795d23f35295f4526e70bf8b9a6b1, 0), scriptSig=)"
        },
        "nLastDsq": 0,
        "protocolVersion": 70204,
        "pubKeyCollateralAddress": "yRzYTUdLCAWVfvZ9WhJi5CrxcsU68DVox2",
        "pubKeyMasternode": "yi3JF94TwqfqWiNhUEMvQ2iot1W9o3Jj8o",
        "sigTime": 1485272518,
        "vchSig": "IBfwj3kRwkxQHFG8u0PD7/ZbAWjxI61F/dN8JGXDOtKaHdn7M7w7TbfHtaVqfzbPPjncn3drD+dsGWr5lEPscHc=",
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
    "0ee9155594b786f8367410af021406fc3aa030950ea750410f8396ce4dd315cd": {
        "0ee9155594b786f8367410af021406fc3aa030950ea750410f8396ce4dd315cd": "successful",
        "addr": "123.123.125.225:19999",
        "vin": "CTxIn(COutPoint(38956e5e5f932f7d088af4b58d87217d8af795d23f35295f4526e70bf8b9a6b1, 0), scriptSig=)"
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
mn5  1   1000.00000000   1011.25000000
mn6  1   1000.00000000   1011.25000000
mn7  1   1000.00000000   1011.25000000
mn8  1   1000.00000000   1011.25000000

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

