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

#
