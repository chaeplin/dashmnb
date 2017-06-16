import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from mnb_misc import *
from mnb_rpc import *

from bip32utils import BIP32Key

def bip32_getaddress(xpub, index_no):
    assert isinstance(index_no, int)
    acc_node = BIP32Key.fromExtendedKey(xpub)
    addr_node = acc_node.ChildKey(index_no)
    address = addr_node.Address()
    return address

def get_bip32_unused(xpub, access):
	first_unused = False
	checking_gap = 10
	i = 0
	while True:
		child_address = bip32_getaddress(xpub, i)
		r = getaddresstxids(child_address, access)
		child_usedtx_no = len(r)
		# debug
		#print(i, child_address, child_usedtx_no)

		if child_usedtx_no == 0:
			if first_unused:
				yield child_address

			else:
				first_unused = True

				if i == 0:
					yield child_address

				else:
					i = i - checking_gap			 

		if first_unused:
			i = i + 1

		else:		
			i = i + checking_gap