import sys, os
sys.path.append( os.path.join( os.path.dirname(__file__), '..' ) )
sys.path.append( os.path.join( os.path.dirname(__file__), '..', 'dashlib' ) )

import re
from mnb_makemnb import *

def start_masternode(mns_to_start, access, client, announce):
    if announce:
        print('\n[making mnbs and relay]')
    else:
        print('\n[making mnbs and quit]')

    masternodebroadcast = []
    for alias in sorted(mns_to_start):
        mnbhex = make_mnb(mns_to_start[alias].get('alias'), mns_to_start[alias], access, client)
        masternodebroadcast.append(mnbhex)
    
    vc = num_to_varint(len(masternodebroadcast)).hex()
    vm = ''.join(masternodebroadcast)

    verify = access.masternodebroadcast("decode", vc + vm)
    match1 = re.search('^Successfully decoded broadcast messages for (.*) masternodes, failed to decode (.*), total (.*)$', verify.get('overall'))
    
    decoded = {}
    decoded['success'] = match1.group(1)
    decoded['failed']  = match1.group(2)
    decoded['total']   = match1.group(3)

    print('\n---> verify(decoding mnb)')
    print('\t---> total   : ' + decoded['total'])
    print('\t---> success : ' + decoded['success'])
    print('\t---> failed  : ' + decoded['failed'])
    print()

    print(json.dumps(verify, sort_keys=True, indent=4, separators=(',', ': ')))

    if decoded['success'] != decoded['total']:
        sys.exit('error occurred while verifying mnb hex')

    if announce:
        
        user_input = input('\nRelay broadcast messages ? [ Yes / (any key to no) ] + enter : ')
        if user_input == 'Yes':
            print('Yes, will relay')
        else:
            print('No.')
            return
        
        relay  = access.masternodebroadcast("relay", vc + vm)
        match2 = re.search('^Successfully relayed broadcast messages for (.*) masternodes, failed to relay (.*), total (.*)$', relay.get('overall'))

        relayed = {}
        relayed['success'] = match1.group(1)
        relayed['failed']  = match1.group(2)
        relayed['total']   = match1.group(3)

        print('\n---> relay(announcing mnb)')
        print('\t---> total   : ' + relayed['total'])
        print('\t---> success : ' + relayed['success'])
        print('\t---> failed  : ' + relayed['failed'])
        print()

        print(json.dumps(relay, sort_keys=False, indent=4, separators=(',', ': ')))

# end