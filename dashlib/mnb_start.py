import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import re
from mnb_makemnb import *
from mnb_misc import *
from mnb_rpc import *
import simplejson as json


def start_masternode(
        mns_to_start,
        protocolversion,
        blockcount,
        access,
        client,
        announce,
        mpath):
    if announce:
        print('\n[making mnbs and relay]')
    else:
        print('\n[making mnbs and quit]')

    print_hw_wallet_check()

    masternodebroadcast = []

    for m in mns_to_start:
        mnbhex = make_mnb(
            m.get('alias'),
            protocolversion,
            blockcount,
            m,
            access,
            client,
            mpath)

        masternodebroadcast.append(mnbhex)

    mnbsublist = [masternodebroadcast[i:i + 10]
                  for i in range(0, len(masternodebroadcast), 10)]

    for mnbs in mnbsublist:

        vc = num_to_varint(len(mnbs)).hex()
        vm = ''.join(mnbs)

        print('mnb_hex : ', vc + vm)


        verify = rpc_masternode("decode", vc + vm, access)
        match1 = re.search(
            '^Successfully decoded broadcast messages for (.*) masternodes, failed to decode (.*), total (.*)$',
            verify.get('overall'))

        decoded = {}
        decoded['success'] = match1.group(1)
        decoded['failed'] = match1.group(2)
        decoded['total'] = match1.group(3)

        print('\n---> verify(decoding mnb)')
        print('\t---> total   : ' + decoded['total'])
        print('\t---> success : ' + decoded['success'])
        print('\t---> failed  : ' + decoded['failed'])
        print()

        if decoded['success'] != decoded['total']:

            print(
                json.dumps(
                    verify,
                    sort_keys=True,
                    indent=4,
                    separators=(
                        ',',
                        ': ')))

            err_msg = 'error occurred while verifying mnb hex'
            print_err_exit(
                get_caller_name(),
                get_function_name(),
                err_msg)

        if announce:

            user_input = input(
                '\nRelay broadcast messages ? [ Yes / (any key to no) ] + enter : ')
            if user_input == 'Yes':
                print('Yes, will relay')
            else:
                print('No.')
                return

            relay = rpc_masternode("relay", vc + vm, access)
            match2 = re.search(
                '^Successfully relayed broadcast messages for (.*) masternodes, failed to relay (.*), total (.*)$',
                relay.get('overall'))

            relayed = {}
            relayed['success'] = match1.group(1)
            relayed['failed'] = match1.group(2)
            relayed['total'] = match1.group(3)

            print('\n---> relay(announcing mnb)')
            print('\t---> total   : ' + relayed['total'])
            print('\t---> success : ' + relayed['success'])
            print('\t---> failed  : ' + relayed['failed'])
            print()

            if relayed['success'] != relayed['total']:
                print(
                    json.dumps(
                        relay,
                        sort_keys=True,
                        indent=4,
                        separators=(
                            ',',
                            ': ')))


# end
