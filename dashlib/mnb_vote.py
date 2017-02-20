import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import re
from mnb_makevote import *
from mnb_misc import *
from mnb_rpc import *
import simplejson as json

def start_votes(
        mn_config,
        proposal_hash,
        vote,
        access):

    
    listforvotes = []

    for m in mn_config:
        votedict = make_vote(
            m.get('alias'),
            proposal_hash,
            vote,
            m)

        listforvotes.append(votedict)


    print('\n[relaying vote(s)]')
    for voteconf in listforvotes:
        r = rpc_voteraw(voteconf, access)
        print('%s - %s' % (voteconf['alias'], r))


