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
    $ sudo apt-get install libudev-dev libusb-1.0-0-dev libfox-1.6-dev
    $ sudo apt-get install autotools-dev autoconf automake libtool
    $ sudo apt-get -y install python3-pip git
    $ sudo pip3 install virtualenv


### 1. Install Prerequisites (Mac oS)

Install brew and python3

    $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"    
    $ brew install python3 git
    $ pip3 install virtualenv


### 2. Install dashmnb

Clone the dashmnb repo and install Python dependencies.

    $ git clone https://github.com/chaeplin/dashmnb && cd dashmnb
    $ virtualenv -p python3 venv3
    $ . venv3/bin/activate
    $ pip install -r requirements.txt


## Configuration

- Move dashlib/config.sample.py to dashlib/config.py and edit parameters

- Use python bin/hw-wallet-for-mn.py to gen a list of address

        $ cd dashmnb
        $ . venv3/bin/activate
        $ python bin/hw-wallet-for-mn.py

- Send 1k tDash to Address

- Set up remote masternode, add following to dashd.conf.

        addressindex=1
        spentindex=1
        timestampindex=1
        txindex=1

- Run once with -rescan, to make index

        $ dashd -rescan

- Move mnconf/masternode.conf.sample to mnconf/masternode.conf and edit

- Run dashmnb.py

        $ cd dashmnb
        $ . venv3/bin/activate
        $ python bin/dashmnb.py



###### Thanks to
- codes form https://github.com/dashpay/electrum-dash
- ref : https://github.com/dashpay/dash/blob/v0.12.1.x/dash-docs/protocol-documentation.md by 

