# config.py

# start of config
# network
MAINNET = True  # mainnet


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
USE_SSH_TUNNEL = True  # True or False
SSH_IDENTITYFILE = '~/.ssh/xxxx.pem'
SSH_USER = 'xxxx'
SSH_SERVER = '10.10.10.10'
SSH_LOCAL_PORT = '29998'

# masternode_config
masternode_conf_file = 'masternode.conf'

# default address to send coins in hw wallet if reveiving_address in masternode.conf is blank
# this is not chaing payment address of mn
default_receiving_address = ''

#
max_gab = 20     # number of keys used on mn config

max_amounts = 50     # max amounts of each unspent tx
max_unspent = 20
min_unspent = 1

# if config.py and masternode.x.conf unchanged, recheck config every 7
# day, and 6 hour
config_cache_refresh_interval_hour = 7 * 24

# txs
txs_cache_refresh_interval_hour = 6

#
errorsnprogress = []

# caution this config move 1K collateral to configured address with fee 0.0001
MOVE_1K_COLLATERAL = False


# don't change
# dash mainnet
wif_prefix = 204  # cc
addr_prefix = 76   # 4c
coin_name = 'Dash'
min_fee = 10000  # fee for tx
# don't change

# end of config.py
