Run Dash Masternode with Hardware Wallet
=========================================

#### TESTNET ONLY ####

```
$ python dashmnb.py
usage: dashmnb.py [-h] [-c] [-s] [-a] [-b] [-m] [-x]

optional arguments:
  -h, --help     show this help message and exit
  -c, --check    check masternode config
  -s, --status   show masternode status
  -a, --anounce  anounce missing masternodes
  -b, --balance  show masternodes balance
  -m, --maketx   make signed raw tx
  -x, --xfer     broadcast signed raw tx
```

```

$ python dashmnb.py -s
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
---> checking masternode config

[masternodes config]
  configured : 4
  passed     : 4


[masternodes status]
alias ip (m: ip/port match) collateral address       status
mn1 167.12.133.185:19999:-  yWZJ6fUGrFX4S1ubDgqW7ZCcLBCt89BLt1 -------
mn2 123.123.103.78:19999:-  yZvTMpTyNEpXxkh52ksg7trfQfoweuTsHe -------
mn3 123.123.97.225:19999:-  yM56Ai6pHh7NzsYF5SLGMHq25Hd4noHoo6 -------
mn4 167.12.138.230:19999:-  yfaCDjViCUsZNsPdmKDchBTS38bYNizvAa -------

```


```
$ python dashmnb.py -a
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
---> checking masternode config

[masternodes config]
  configured : 4
  passed     : 4


[masternodes status]
alias ip (m: ip/port match) collateral address       status
mn1 167.12.133.185:19999:-  yWZJ6fUGrFX4S1ubDgqW7ZCcLBCt89BLt1 -------
mn2 123.123.103.78:19999:-  yZvTMpTyNEpXxkh52ksg7trfQfoweuTsHe -------
mn3 123.123.97.225:19999:-  yM56Ai6pHh7NzsYF5SLGMHq25Hd4noHoo6 -------
mn4 167.12.138.230:19999:-  yfaCDjViCUsZNsPdmKDchBTS38bYNizvAa -------


[making mnbs and relay]
---> making mnb for mn1
---> check keepkey and press button
Passphrase required: 

Confirm your Passphrase: 

---> mnb hex for mn1 : 18735b18d410dea62eba1dc3e36fd27a5a543962cc1177ba0da7decd53c4d18a0000000000ffffffff00000000000000000000ffff965f85b94e1f2103e0fe533b6003a64528c5ed548a516f61e0099fb6eb9011daa79254eb2d9f902d41046e5dac3d27c86b2afd98850755a74298547da52efd7e6c8c0854999fe9f09043c0942a7d9b0f6fd0a6091a2f5d4aef1e24892e88e6acc61a3ba0181970fd5c1e4120ea7ef82c8ea8bbca154c0e01729f529c1cc4cf49d0d4bf395f349c40dd46754005e5022607eaeb9064d1be4c397b1b9d46c36b57c8f8bf10325e9df091a3d507ce257d58000000003c12010018735b18d410dea62eba1dc3e36fd27a5a543962cc1177ba0da7decd53c4d18a0000000000ffffffffdf0369aac1cea74ef617e3ea73a1ff79c8f1f020a584e7b3e3567bd460000000ce257d5800000000411c7b69e9278a64f91db00ef1e7e8bbc146491fbe99adfba840e1eafc0ad6cfcd3305f376f050d9002a4cf804378317da68b49faf8c7046d8ef0c9549da1084fa68

---> making mnb for mn2
---> check keepkey and press button
---> mnb hex for mn2 : 1a3b8717ee81e8c32d44e7f958701c751a79e3490bb60f5182f9ef5272fa70a50000000000ffffffff00000000000000000000ffff8582674e4e1f2102e215bd16259ca594156053ca0d936278b7a53408aaddec14dc5ab4c3ffebc2c541041477bf3f056c4620de103174ba4b3eaf1600e0d7f9b1dde9a270eb370ffc2e27ef642bf961f96bd289fad25aa57fc757c9a234a986ece3bb330d8f4d999f6771411f9dff148708ca9a79d02f94a290bcd85f650f70f56a03fedd64939778d75aebde23f35600da0020d343f34f0a50e4f2a960fafeed49a9b025570ee8c29d47e30edd257d58000000003c1201001a3b8717ee81e8c32d44e7f958701c751a79e3490bb60f5182f9ef5272fa70a50000000000ffffffffdf0369aac1cea74ef617e3ea73a1ff79c8f1f020a584e7b3e3567bd460000000dd257d5800000000411cf4c6d26518ed64877ef1e08e05c92ee1af7afb0d1436017c1e215129f9c5b4d44527d8396e929c8444301edc7c08d25fc615f9e3ffb48aebeb7a3daaec3b57e7

---> making mnb for mn3
---> check keepkey and press button
---> mnb hex for mn3 : d52420a97b19871379b5657ed9ccbb879d55d73c3e5ad347fa5c70e2efc834cd0100000000ffffffff00000000000000000000ffff858261e14e1f2103873f3508a52cecf642809a31f5bed08f6271041e5d0f4ff9666ccf95fdacbcaa4104a3f5440a94533269141ae0848fe01dfa895631ff28df1e4682b32953c4b5595f54f0cc521c677e560ae8ce3aa4724c14efe932e9cb48437137930e4af55e973341202b4d2025af91becd6c40bac391025894d0eb73f1a0662860bf60a4093623699b201c834b3ec945be5027bef0736e2e35b802d304be8d533408a2a1b02b1e7ae7e2257d58000000003c120100d52420a97b19871379b5657ed9ccbb879d55d73c3e5ad347fa5c70e2efc834cd0100000000ffffffffdf0369aac1cea74ef617e3ea73a1ff79c8f1f020a584e7b3e3567bd460000000e2257d5800000000411b35bd1ecf9d80a86b7d769ad72bd10f63b6ecbed25ff8e1fe4f18a072173bdfde61fc7f014af42f60041b1645df80fbfa43c0593efbb0b7f807ed8c1a9f2787a4

---> making mnb for mn4
---> check keepkey and press button
---> mnb hex for mn4 : f8d181c08eaff42b0af1c797273e3faefd9cb156710341ed51ced9260e493cd40100000000ffffffff00000000000000000000ffff965f8ae64e1f2103fbc9d592c66b2489074e4c798a12a1c470afc5647767a4931add0f36ed7ece3941042bad256d62548585b97165efca20a15390dda25e5a63e9e8f2658936ffcd394f68899201125522ca06f123b930e58e7da5a6343b44c53611395dafb39dd070324120251d73e3ffe59d72eb9b88c15e8ad408e4c5a086004ae8457c62743effefa0f60fbb448a54951187437f465a18a7c7cd989f5dea80a2fe26ca807f1cf88528a1e5257d58000000003c120100f8d181c08eaff42b0af1c797273e3faefd9cb156710341ed51ced9260e493cd40100000000ffffffffdf0369aac1cea74ef617e3ea73a1ff79c8f1f020a584e7b3e3567bd460000000e5257d5800000000411c645391bde25abf804cf86b3bd117f8cd30a8aad3856a96236749be04a321a5883b6718507f09e09d06450d4952ad25e148337b9d80c869d4268775d9e0a475f3


---> verify(decoding mnb)
  ---> total   : 4
  ---> success : 4
  ---> failed  : 0

{
    "32919a98950dec41a3d75dc3790063fb009a514fbc1fb2cf9402aab86fd1b0b3": {
        "addr": "167.12.138.230:19999",
        "lastPing": {
            "blockHash": "00000060d47b56e3b3e784a520f0f1c879ffa173eae317f64ea7cec1aa6903df",
            "sigTime": 1484596709,
            "vchSig": "HGRTkb3iWr+ATPhrO9EX+M0wqKrThWqWI2dJvgSjIaWIO2cYUH8J4J0GRQ1JUq0l4Ugze52AyGnUJod12eCkdfM=",
            "vin": "CTxIn(COutPoint(d43c490e26d9ce51ed41037156b19cfdae3f3e2797c7f10a2bf4af8ec081d1f8, 1), scriptSig=)"
        },
        "nLastDsq": 0,
        "protocolVersion": 70204,
        "pubKeyCollateralAddress": "yfaCDjViCUsZNsPdmKDchBTS38bYNizvAa",
        "pubKeyMasternode": "ybpS2bbyKbnQHwJkuQC8TMJUkhNNqqtXMr",
        "sigTime": 1484596709,
        "vchSig": "ICUdc+P/5Z1y65uIwV6K1AjkxaCGAEroRXxidD7/76D2D7tEilSVEYdDf0ZaGKfHzZifXeqAov4myoB/HPiFKKE=",
        "vin": "CTxIn(COutPoint(d43c490e26d9ce51ed41037156b19cfdae3f3e2797c7f10a2bf4af8ec081d1f8, 1), scriptSig=)"
    },
    "35c68ff77763b8cacac09c7dba3d603dc8af9779fe72a11f4fe3443d405e3c18": {
        "addr": "123.123.103.78:19999",
        "lastPing": {
            "blockHash": "00000060d47b56e3b3e784a520f0f1c879ffa173eae317f64ea7cec1aa6903df",
            "sigTime": 1484596701,
            "vchSig": "HPTG0mUY7WSHfvHgjgXJLuGvevsNFDYBfB4hUSn5xbTURSfYOW6SnIREMB7cfAjSX8YV+eP/tIrr63o9quw7V+c=",
            "vin": "CTxIn(COutPoint(a570fa7252eff982510fb60b49e3791a751c7058f9e7442dc3e881ee17873b1a, 0), scriptSig=)"
        },
        "nLastDsq": 0,
        "protocolVersion": 70204,
        "pubKeyCollateralAddress": "yZvTMpTyNEpXxkh52ksg7trfQfoweuTsHe",
        "pubKeyMasternode": "yccPZy54vMrCpKfHf7BD9q4DtPdQekPY97",
        "sigTime": 1484596701,
        "vchSig": "H53/FIcIypp50C+UopC82F9lD3D1agP+3WSTl3jXWuveI/NWANoAINND808KUOTyqWD6/u1JqbAlVw7owp1H4w4=",
        "vin": "CTxIn(COutPoint(a570fa7252eff982510fb60b49e3791a751c7058f9e7442dc3e881ee17873b1a, 0), scriptSig=)"
    },
    "886c905afcb3b8878d79112e3717da16a51760b4e8b233239ca5323803ddb836": {
        "addr": "123.123.97.225:19999",
        "lastPing": {
            "blockHash": "00000060d47b56e3b3e784a520f0f1c879ffa173eae317f64ea7cec1aa6903df",
            "sigTime": 1484596706,
            "vchSig": "GzW9Hs+dgKhrfXaa1yvRD2O27L7SX/jh/k8YoHIXO9/eYfx/AUr0L2AEGxZF34D7+kPAWT77sLf4B+2MGp8nh6Q=",
            "vin": "CTxIn(COutPoint(cd34c8efe2705cfa47d35a3e3cd7559d87bbccd97e65b5791387197ba92024d5, 1), scriptSig=)"
        },
        "nLastDsq": 0,
        "protocolVersion": 70204,
        "pubKeyCollateralAddress": "yM56Ai6pHh7NzsYF5SLGMHq25Hd4noHoo6",
        "pubKeyMasternode": "yiko1kF1HzvDsyNwkcUjE7iJgUvPqwqp8e",
        "sigTime": 1484596706,
        "vchSig": "ICtNICWvkb7NbEC6w5ECWJTQ63PxoGYoYL9gpAk2I2mbIByDSz7JRb5QJ77wc24uNbgC0wS+jVM0CKKhsCseeuc=",
        "vin": "CTxIn(COutPoint(cd34c8efe2705cfa47d35a3e3cd7559d87bbccd97e65b5791387197ba92024d5, 1), scriptSig=)"
    },
    "9a5dcc9e692e3a0d737707ccf1de8cc3c4022bc12b600f393838f24506299d9c": {
        "addr": "167.12.133.185:19999",
        "lastPing": {
            "blockHash": "00000060d47b56e3b3e784a520f0f1c879ffa173eae317f64ea7cec1aa6903df",
            "sigTime": 1484596686,
            "vchSig": "HHtp6SeKZPkdsA7x5+i7wUZJH76ZrfuoQOHq/ArWz80zBfN28FDZACpM+AQ3gxfaaLSfr4xwRtjvDJVJ2hCE+mg=",
            "vin": "CTxIn(COutPoint(8ad1c453cddea70dba7711cc6239545a7ad26fe3c31dba2ea6de10d4185b7318, 0), scriptSig=)"
        },
        "nLastDsq": 0,
        "protocolVersion": 70204,
        "pubKeyCollateralAddress": "yWZJ6fUGrFX4S1ubDgqW7ZCcLBCt89BLt1",
        "pubKeyMasternode": "yfUmjuXkFDCy7a3Gs5CFQqp8f3eFzbAMXK",
        "sigTime": 1484596686,
        "vchSig": "IOp++CyOqLvKFUwOAXKfUpwcxM9J0NS/OV80nEDdRnVABeUCJgfq65Bk0b5MOXsbnUbDa1fI+L8QMl6d8JGj1Qc=",
        "vin": "CTxIn(COutPoint(8ad1c453cddea70dba7711cc6239545a7ad26fe3c31dba2ea6de10d4185b7318, 0), scriptSig=)"
    },
    "overall": "Successfully decoded broadcast messages for 4 masternodes, failed to decode 0, total 4"
}

Relay broadcast messages ? [ Yes / (any key to no) ] + enter : Yes
Yes, will relay

---> relay(announcing mnb)
  ---> total   : 4
  ---> success : 4
  ---> failed  : 0

{
    "overall": "Successfully relayed broadcast messages for 4 masternodes, failed to relay 0, total 4",
    "35c68ff77763b8cacac09c7dba3d603dc8af9779fe72a11f4fe3443d405e3c18": {
        "35c68ff77763b8cacac09c7dba3d603dc8af9779fe72a11f4fe3443d405e3c18": "successful",
        "addr": "123.123.103.78:19999",
        "vin": "CTxIn(COutPoint(a570fa7252eff982510fb60b49e3791a751c7058f9e7442dc3e881ee17873b1a, 0), scriptSig=)"
    },
    "9a5dcc9e692e3a0d737707ccf1de8cc3c4022bc12b600f393838f24506299d9c": {
        "9a5dcc9e692e3a0d737707ccf1de8cc3c4022bc12b600f393838f24506299d9c": "successful",
        "addr": "167.12.133.185:19999",
        "vin": "CTxIn(COutPoint(8ad1c453cddea70dba7711cc6239545a7ad26fe3c31dba2ea6de10d4185b7318, 0), scriptSig=)"
    },
    "32919a98950dec41a3d75dc3790063fb009a514fbc1fb2cf9402aab86fd1b0b3": {
        "addr": "167.12.138.230:19999",
        "vin": "CTxIn(COutPoint(d43c490e26d9ce51ed41037156b19cfdae3f3e2797c7f10a2bf4af8ec081d1f8, 1), scriptSig=)",
        "32919a98950dec41a3d75dc3790063fb009a514fbc1fb2cf9402aab86fd1b0b3": "successful"
    },
    "886c905afcb3b8878d79112e3717da16a51760b4e8b233239ca5323803ddb836": {
        "addr": "123.123.97.225:19999",
        "vin": "CTxIn(COutPoint(cd34c8efe2705cfa47d35a3e3cd7559d87bbccd97e65b5791387197ba92024d5, 1), scriptSig=)",
        "886c905afcb3b8878d79112e3717da16a51760b4e8b233239ca5323803ddb836": "successful"
    }
}

```

```

$ python dashmnb.py -b
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
---> checking masternode config

[masternodes config]
  configured : 4
  passed     : 4


[masternodes status]
alias ip (m: ip/port match) collateral address       status
mn1 167.12.133.185:19999:m  yWZJ6fUGrFX4S1ubDgqW7ZCcLBCt89BLt1 PRE_ENABLED
mn2 123.123.103.78:19999:m  yZvTMpTyNEpXxkh52ksg7trfQfoweuTsHe PRE_ENABLED
mn3 123.123.97.225:19999:m  yM56Ai6pHh7NzsYF5SLGMHq25Hd4noHoo6 PRE_ENABLED
mn4 167.12.138.230:19999:m  yfaCDjViCUsZNsPdmKDchBTS38bYNizvAa PRE_ENABLED

[masternodes balance]
alias cnt balance
mn1 0 1000
mn2 0 1000
mn3 0 1000
mn4 0 1000

```

#### requirement
- Dash-QT or dashd
- Keepkey, Trezor(not yet) 
- keepkey-firmware
- rpc conn to Dash-QT or dashd
- python3
- python-keepkey
- python-bitcoinrpc
- python-progress
- python-pyfiglet
- python-bip32utils

#### Keepkey firmware
- Build your own firmware
- https://github.com/chaeplin/dash-testnet/tree/master/keepkey_firmware

### python lib
- use python-virtualenv3
- https://github.com/chaeplin/python-keepkey
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

### How to
- use keepkey-for-mn.py to gen a list of address (change key path = mpath)
- send 1k tDash to Address
- set up remote masternode
- move config.py.sample to config.py and edit parameters
- move masternode.conf.sample to masternode.conf and edit
- run Dash-QT or dashd
- run dashmnb.py

### Using remote dashd
- ssh tunnel
- ssh -L 19998:localhost:19998 -N username@192.168.10.10 (-N(keep tunnel, not loggn in) -L local_port:dest_ip:dest_port )



####
    https://test.explorer.dash.org/tx/dec9c5ef0b4f82b77107f29e0096a30faacbf068f5b46a106726b02036caaeb4#o0
    https://test.explorer.dash.org/tx/82552b6626c9d2ea35c5295135b09acd351a28f552d3a666612d85e36f805e26#o0
    https://test.explorer.dash.org/tx/11c3467a318e33d5b45c588c1676b9d09f4999a96c8ce720b9d4d5815181e28a#o0
    https://test.explorer.dash.org/tx/b7910641dcc640154947d8610ebbdc1e52b7c43383a8b4e96cde6fbd089780a2#o0