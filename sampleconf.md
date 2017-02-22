# without hw wallet
 _ |dash.conf|masternode.conf
--------|----------|---------
remote masternode | rpcuser=change-ths-username-alpah-number-digit<br />rpcpassword=change-ths-password-alpah-number-digit<br />rpcbind=127.0.0.1<br />rpcallowip=127.0.0.1<br />listen=1<br />server=1<br />daemon=1<br />logtimestamps=1<br />maxconnections=128<br />externalip=change-this-public-ip-address-of-masternode<br />masternode=1<br />masternodeprivkey=masternodeprivkey<br />  | 
local dashd(cold) | |MN1 change-this-public-ip-address-of-masternode:9999 masternodeprivkey collateral_output_txid collateral_output_index



#with hw wallet + local dashd
 _ |dash.conf|masternode.conf
--------|----------|---------
remote masternode | rpcuser=change-ths-username-alpah-number-digit<br />rpcpassword=change-ths-password-alpah-number-digit<br />rpcbind=127.0.0.1<br />rpcallowip=127.0.0.1<br />listen=1<br />server=1<br />daemon=1<br />logtimestamps=1<br />maxconnections=128<br />externalip=change-this-public-ip-address-of-masternode<br />masternode=1<br />masternodeprivkey=masternodeprivkey<br />  | 
local dashd(empty) | rpcuser=change-ths-username-alpah-number-digit<br />rpcpassword=change-ths-password-alpah-number-digit<br />rpcallowip=127.0.0.1<br />rpcbind=127.0.0.1<br />rpcport=9998<br />server=1<br />daemon=1<br />logtimestamps=1<br />addressindex=1<br />spentindex=1<br />timestampindex=1<br />txindex=1<br /> |
 

_ | dashmnb/mnconf/masternode.conf
--------|----------
dashmnb | MN1 change-this-public-ip-address-of-masternode:9999 masternodeprivkey collateral_output_txid collateral_output_index 