import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import re
import time
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
        # time.sleep(1)


def display_votes(
        mn_config,
        proposal_hash,
        access):

    voteresult = rpc_getcurrentvotes(proposal_hash, access)
    proposalvotes = {}

    for v in voteresult:
        match = re.search('^CTxIn\(COutPoint\((.*), (.*)\), scriptSig=\):(.*):(.*):(.*)', voteresult[v])
        if match:
            vtxid = match.group(1)
            vtxidn = match.group(2)
            vvote = match.group(4)
            vsignal = match.group(5)
            vtxidvtxidn = get_txidtxidn(vtxid, vtxidn)
            proposalvotes[vtxidvtxidn] = vvote

    for m in mn_config:
        txidtxidn = m.get('collateral_txidtxidn')
        if txidtxidn in proposalvotes:
            print('%s - %s - %s' % (m.get('alias'), proposal_hash, proposalvotes[txidtxidn]))
