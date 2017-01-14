import sys, os
sys.path.append( os.path.join( os.path.dirname(__file__), '..' ) )
sys.path.append( os.path.join( os.path.dirname(__file__), '..', 'dashlib' ) )

import re
from mnb_makemnb import *

def start_masternode(mns_to_start, access, client):
    masternodebroadcast = []
    for alias in sorted(mns_to_start):
        mnbhex = make_mnb(alias, mns_to_start[alias], access, client)
        masternodebroadcast.append(mnbhex)
    
    vc = num_to_varint(len(masternodebroadcast)).hex()
    vm = ''.join(masternodebroadcast)
    verify = access.masternodebroadcast("decode", vc + vm)
    match1 = re.search('^Successfully decoded broadcast messages for (.*) masternodes, failed to decode (.*), total (.*)$', verify.get('overall'))
    
    decoded = {}
    decoded['success'] = match1.group(1)
    decoded['failed']  = match1.group(2)
    decoded['total']   = match1.group(3)

    print('---> verify')
    print('---> total   : ' + decoded['total'])
    print('---> success : ' + decoded['success'])
    print('---> failed  : ' + decoded['failed'])
    print()
    
    if announce:
        relay  = access.masternodebroadcast("relay", vc + vm)
        match2 = re.search('^Successfully relayed broadcast messages for (.*) masternodes, failed to relay (.*), total (.*)$', relay.get('overall'))

        relayed = {}
        relayed['success'] = match1.group(1)
        relayed['failed']  = match1.group(2)
        relayed['total']   = match1.group(3)

        print('---> relay')
        print('---> total   : ' + relayed['total'])
        print('---> success : ' + relayed['success'])
        print('---> failed  : ' + relayed['failed'])
        print()

