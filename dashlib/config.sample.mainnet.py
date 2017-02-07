# config.py

# start of config

############  for main net #################

# https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki
# purpose' / coin_type' / account' / change / address_index
# Dash  : 44'/5'/account'/0/0
# tDash : 44'/165'/account'/0/0
# bip32 path
# 1 is selected to use trezor's web wallet and Keepkey's client
account_no = 1

# HW WALLET TYPE
# Keepkey [ keepkey ], Trezor [ trezor ]
TYPE_HW_WALLET = 'Trezor'          

# rpc
rpcuser = 'xxxx'
rpcpassword = 'xxxxx'
rpcbindip = '127.0.0.1'
rpcport = 9998

# ssh tunnel
USE_SSH_TUNNEL = True    # True or False

# if you connect remote server with IDENTITYFILE
# like ssh -i ~/.ssh/xxxx.pem myid@x.x.x.x
# 2 option
# 1)
# USE_IDENTITYFILE = False
# SSH_IDENTITYFILE = ''
# then use ssh-add -K ~/.ssh/xxxx.pem 
# ssh-add : adds private key identities to the authentication agent
#
# 2)
# USE_IDENTITYFILE = True
# SSH_IDENTITYFILE = '~/.ssh/xxxx.pem'

USE_IDENTITYFILE = False # True or False
SSH_IDENTITYFILE = ''

#USE_IDENTITYFILE = True
#SSH_IDENTITYFILE = '~/.ssh/xxxx.pem' or '~/.ssh/id_rsa'

SSH_USER = 'xxxx'
SSH_SERVER = '10.10.10.10'
SSH_LOCAL_PORT = '29998'

# masternode_config
masternode_conf_file = 'masternode.conf'

# default address to send payout coins in hw wallet if reveiving_address in masternode.conf is blank.
# this is not changing payment address of mn
# command -m and -x will use
default_receiving_address = ''

#
# how many mns do you have, to check address on hw wallet
# if bip32 path last used address for mn is like 44'/5'/1'/0/10 : address_index is 10
# use max_gab = 11 (address_index + 1)
max_gab = 5     

# settings to control send payout coins
# when if MOVE_1K_COLLATERAL = True will not used to check

# if a unspent tx(or payout or deposit on mn address) has amount more han this, will not touch
max_amounts = 50

# number of inputs to include in a tx
max_unspent = 20

# if number of payout is less than this, will not touch
min_unspent = 1

# if config.py and masternode.x.conf unchanged, recheck config every 7
# day, and 6 hour
config_cache_refresh_interval_hour = 7 * 24

# txs
txs_cache_refresh_interval_hour = 6

# caution this config move 1K collateral to configured address with fee 0.0001
MOVE_1K_COLLATERAL = False

# don't change
# dash mainnet
# network
MAINNET = True  # mainnet
wif_prefix = 204  # cc
addr_prefix = 76   # 4c
coin_name = 'Dash'
min_fee = 10000  # fee for tx
# to display err on masternode.conf
errorsnprogress = []
# don't change

# end of config.py
