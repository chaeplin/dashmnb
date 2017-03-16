# block
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import binascii
import hashlib
import x11_hash
import struct

from dash_hashs import *


def calc_difficulty(nBits):
    nShift = (nBits >> 24) & 0xff
    dDiff = float(0x0000ffff) / float(nBits & 0x00ffffff)
    while nShift < 29:
        dDiff *= 256.0
        nShift += 1
    while nShift > 29:
        dDiff /= 256.0
        nShift -= 1
    return dDiff


def decode_uint32(data):
    assert(len(data) == 4)
    return struct.unpack("<I", data)[0]


def decode_varint(data):
    assert(len(data) > 0)
    size = int(data[0])
    assert(size <= 255)

    if size < 253:
        return size, 1

    format_ = None
    if size == 253:
        format_ = '<H'
    elif size == 254:
        format_ = '<I'
    elif size == 255:
        format_ = '<Q'
    else:
        assert 0, "unknown format_ for size : %s" % size

    size = struct.calcsize(format_)
    return struct.unpack(format_, data[1:size + 1])[0], size + 1


def Inputfromhex(raw_hex):
    _script_length, varint_length = decode_varint(raw_hex[36:])
    _script_start = 36 + varint_length
    _size = _script_start + _script_length + 4
    _hex = raw_hex[:_size]
    return _size, _hex


def Outputfromhex(raw_hex):
    script_length, varint_size = decode_varint(raw_hex[8:])
    script_start = 8 + varint_size
    _script_hex = raw_hex[script_start:script_start + script_length]
    _size = script_start + script_length
    _hex = raw_hex[:8]
    return _size, _hex


def Transactionfromhex(raw_hex):
    n_inputs = 0
    n_outputs = 0

    offset = 4
    n_inputs, varint_size = decode_varint(raw_hex[offset:])
    offset += varint_size

    for i in range(n_inputs):
        input = Inputfromhex(raw_hex[offset:])
        offset += input[0]

    n_outputs, varint_size = decode_varint(raw_hex[offset:])
    offset += varint_size

    for i in range(n_outputs):
        output = Outputfromhex(raw_hex[offset:])
        offset += output[0]

    _size = offset + 4
    _hex = raw_hex[:_size]
    return _size, _hex


def decoderawblock(rawblock):
    #block_hex = binascii.unhexlify(rawblock)
    block_hex = bytes.fromhex(rawblock)
    bversion = block_hex[:4]
    bpbhash = block_hex[4:36]
    bmkroot = block_hex[36:68]
    btime = block_hex[68:72]
    bbits = block_hex[72:76]
    bnonce = block_hex[76:80]

    block = {}
    block['hash'] = format_hash(x11_hash.getPoWHash(block_hex[:80]))
    block['version'] = decode_uint32(bversion)
    block['p_b_hash'] = format_hash(bpbhash)
    block['merkleroot'] = format_hash(bmkroot)
    block['time'] = decode_uint32(btime)
    block['difficulty'] = calc_difficulty(decode_uint32(bbits))
    block['nonce'] = decode_uint32(bnonce)

    transaction_data = block_hex[80:]
    n_transactions, offset = decode_varint(transaction_data)

    txs = {}
    for i in range(n_transactions):
        transaction = Transactionfromhex(transaction_data[offset:])
        offset += transaction[0]
        #rawtx = binascii.hexlify(transaction[1]).decode("utf-8")
        rawtx = transaction[1].hex()
        rawtx_hash = format_hash(double_sha256(transaction[1]))
        txs[rawtx_hash] = rawtx

    block['txs'] = txs

    return block


if __name__ == "__main__":

    rawblock = '000000205fcd1f4de715f248d8049bae9aaa127cd3e8d6a79dac7dfa6087000000000000a3e6e5b7d383cd98fdd2f7450e0dd1cc8c6dbb099a929883d01992c92ea7faccab3dc958c9b4001b45571ef60401000000010000000000000000000000000000000000000000000000000000000000000000ffffffff1f033db70904ab3dc9580867ffe608130000000c2f436f696e4d696e65504c2f00000000025118be0a000000001976a914ee5c2e032d02f6f7b08fcc21e0025f0baeb056b088ac4d18be0a000000001976a9140d1d2311f3abc4e2967ee3c33220a9c04771325b88ac0000000001000000029df219ffd0e1039230c474677ebb65e9d80f6010126d61db4c2f03d57732220d010000006b483045022100ccaf5cf949022d824037ef96cd16caea2a899776c60d72b10474be50fa6c848302201c4eb3ed5769b66082c8a2405a73492aee6540cceab067bb69640c691bd86d5a0121038820c65af793b0360ee5caded304dee8c0a1ac144b08a5fc9f075c4ca6d8e222feffffffb69fc42c846a01c3aab5847b08edd566444b152463bb0c38431a819b01b0d7f8010000006b483045022100e8bf056f19f417713c8e70b51abd5d5d77786e1e23086e77ca33f7f41388db130220285b6c50a018934ee051384ee216d61911128cc974122a4367e94bb1972d6a590121034682acd89cb9794cc5e65eb8e71273411d64e028d188b91cd3acf5f244b6fbf7feffffff025bb83001000000001976a91476a93a3951c0a769e5dd1cefd5c0751845eda47d88ac00943577000000001976a9143027a6c0d85b04eae237d778f04cb43630e3af1788ac3bb70900010000000140c74ee87f1c1d7921b2b665f6e349095ab4bc65f9d27635a3e038fdf9aa77be000000006b483045022100c84c06c26a8a08c1bd24af1dee68542ace7fb0010acd14bcc6c0845dd102735102203fde216c351ebef18ba798b7cc6ff302717c3f1dba63ff1a88d034262faad9eb01210334284deb6c80e986a0dde1ebb567092315fb061f2218a86de7f58f05c50fc925feffffff02806b8000000000001976a914b77dd71001fd6582e2f79983f5c50b5e3305d35988ac525e9601000000001976a914ec1c3bf6a58c0d7b874dfd3fc7d0d487943a7da388ac3ab70900010000000177f3c60fae4ebb3b8d90e6df00548360a1daecaa436a33e5da3b6a15a0b7ec20010000006a4730440220074f2d90b51a9bf3137243ee8115d64665e8f8e66e55780e2f5af1b6829f49fe0220138ff1903f1df771fe06fd762845600e0dd151aba26dc6d7cdad6ab998d9d09501210360dded694661011fba4a24f05c5af32846607471438221b161a9b3c4b837607efeffffff021f23fd3c000000001976a9145742bffc43d287489805f2da54f4a2edd3c6155d88acb0cf134a0b0000001976a914a4472543fc0c707bbf8bb0c9d50b9829de72459388ac3bb70900'

    print(decoderawblock(rawblock))

