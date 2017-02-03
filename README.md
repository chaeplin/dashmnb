Run Dash Masternode with Hardware Wallet
=========================================

#### TESTNET ONLY ####

###### Q : why firmware update ?
    - to support Dash testnet, both trezor and keepkey has only Mainnet.
    - with Mainnet, no need to update firmware. Use official firmware.

###### Q : which hw wallet supported ?
    - Trezor
    - Keepkey
    - dashmnb will not run without hw wallet

###### Q : what can dashmnb do
    - config check (alias, address, ip, key, pkey, hw wallet path)
    - start masternode missing, selected
    - show masternode status
    - send coins(mn payment) in hw wallet
    - send collateral + coins(mn payment) in hw wallet
    - ssh tunnel to use remote dashd

###### Q : why Dash-QT or dashd needed ?
    - instead of block explorer 
    - to check address, collateral, masternode status
    - to get unspent tx of collateral
    - to relay mnb and txs

###### Q : why do -rescan
    - -rescan means restaring dashd or Dash-QT with -rescan option
    - after initial checking of masternode config, dashmnb will ask you to do rescan
    - add following to dash.con and run dashd with dashd -rescan
    
```
    addressindex=1
    spentindex=1
    timestampindex=1
    txindex=1
```

## Installation

### 1. Install Prerequisites (Ubuntu/Debian)

Make sure Python version 3.x or above is installed:

    python --version

Update system packages and ensure virtualenv is installed:

    $ sudo apt-get update
    $ sudo apt-get -y install python3-pip
    $ sudo pip3 install virtualenv


### 1. Install Prerequisites (Mac oS)

Install brew
    $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"    
    $ brew install python3
    $ pip3 install virtualenv


### 2. Install dashmnb

Clone the dashmnb repo and install Python dependencies.

    $ git clone https://github.com/chaeplin/dashmnb && cd dashmnb
    $ virtualenv -p python3 venv3
    $ . venv3/bin/activate
    $ pip install -r requirements.txt


## Configuration

Use pythin bin/hw-wallet-for-mn.py to gen a list of address
    $ cd dashmnb
    $ . venv3/bin/activate
    $ pythin bin/hw-wallet-for-mn.py

Send 1k tDash to Address

Set up remote masternode

Move dashlib/config.sample.py to dashlib/config.py and edit parameters

Move mnconf/masternode.conf.sample to mnconf/masternode.conf and edit

Run dashmnb.py
    $ cd dashmnb
    $ . venv3/bin/activate
    $ pythin bin/dashmnb.py


###### Thanks to
- codes form https://github.com/dashpay/electrum-dash
- ref : https://github.com/dashpay/dash/blob/v0.12.1.x/dash-docs/protocol-documentation.md by 

######
    https://test.explorer.dash.org/tx/dec9c5ef0b4f82b77107f29e0096a30faacbf068f5b46a106726b02036caaeb4#o0
    https://test.explorer.dash.org/tx/82552b6626c9d2ea35c5295135b09acd351a28f552d3a666612d85e36f805e26#o0
    https://test.explorer.dash.org/tx/11c3467a318e33d5b45c588c1676b9d09f4999a96c8ce720b9d4d5815181e28a#o0
    https://test.explorer.dash.org/tx/b7910641dcc640154947d8610ebbdc1e52b7c43383a8b4e96cde6fbd089780a2#o0

