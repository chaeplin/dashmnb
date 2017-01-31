import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

import re
import binascii
import hashlib
import simplejson as json

from dash_hashs import *
from dash_script import *


def deserialize_script(script):
    if isinstance(script, str) and re.match('^[0-9a-fA-F]*$', script):
        return json_changebase(deserialize_script(bytes.fromhex(script)),
                               lambda x: safe_hexlify(x))
    #   return json_changebase(deserialize_script(binascii.unhexlify(script)),
    #                          lambda x: safe_hexlify(x))
    out, pos = [], 0
    while pos < len(script):
        code = from_byte_to_int(script[pos])
        if code == 0:
            out.append(None)
            pos += 1
        elif code <= 75:
            out.append(script[pos + 1:pos + 1 + code])
            pos += 1 + code
        elif code <= 78:
            szsz = pow(2, code - 76)
            sz = decode(script[pos + szsz: pos:-1], 256)
            out.append(script[pos + 1 + szsz:pos + 1 + szsz + sz])
            pos += 1 + szsz + sz
        elif code <= 96:
            out.append(code - 80)
            pos += 1
        else:
            out.append(code)
            pos += 1
    return out


def deserialize(tx):
    if isinstance(tx, str) and re.match('^[0-9a-fA-F]*$', tx):
        return json_changebase(deserialize(bytes.fromhex(tx)),
                               lambda x: safe_hexlify(x))
        # return json_changebase(deserialize(binascii.unhexlify(tx)),
        #                      lambda x: safe_hexlify(x))
    pos = [0]

    def read_as_int(bytez):
        pos[0] += bytez
        return decode(tx[pos[0] - bytez:pos[0]][::-1], 256)

    def read_var_int():
        pos[0] += 1

        val = from_byte_to_int(tx[pos[0] - 1])
        if val < 253:
            return val
        return read_as_int(pow(2, val - 252))

    def read_bytes(bytez):
        pos[0] += bytez
        return tx[pos[0] - bytez:pos[0]]

    def read_var_string():
        size = read_var_int()
        return read_bytes(size)

    obj = {"ins": [], "outs": []}
    obj["version"] = read_as_int(4)
    ins = read_var_int()
    for i in range(ins):
        obj["ins"].append({
            "outpoint": {
                "hash": read_bytes(32)[::-1],
                "index": read_as_int(4)
            },
            "script": read_var_string(),
            "sequence": read_as_int(4)
        })
    outs = read_var_int()
    for i in range(outs):
        obj["outs"].append({
            "n": i,
            "value": read_as_int(8),
            "script": read_var_string()
        })
    obj["locktime"] = read_as_int(4)
    return obj


def decoderawtx(rawtx):
    txo = deserialize(rawtx)
    txid = format_hash(double_sha256(bytes.fromhex(rawtx)))
#    txid = format_hash(double_sha256(binascii.unhexlify(rawtx)))

    # print(txid)
    #print(json.dumps(txo, sort_keys=True, indent=4, separators=(',', ': ')))

    addrcheck = {}
    for x in txo.get('ins'):
        hashn = x.get('outpoint')['hash']
        if hashn != '0000000000000000000000000000000000000000000000000000000000000000':
            des_script = deserialize_script(x.get('script'))
            addrn = script_to_addr(des_script)
            if (addrn != 'pay_to_pubkey'
                    and addrn != 'unspendable'
                    and addrn != 'nulldata'
                    and addrn != 'invalid'):
                addrcheck['good'] = {
                    "hashin": hashn + '-' + str(x.get('outpoint')['index']),
                    "addrfrom": addrn
                }

            elif (addrn == 'pay_to_pubkey'):
                addrcheck['pubkey'] = {
                    "hashin": hashn + '-' + str(x.get('outpoint')['index']),
                    "addrfrom": addrn
                }
        else:
            addrcheck['coinbase'] = {
                "hashin": '0000000000000000000000000000000000000000000000000000000000000000' +
                '-' +
                str(0),
                "addrfrom": 'coinbase'}

    if addrcheck.get('coinbase', None) is not None:
        hashin = addrcheck.get('coinbase')['hashin']
        addrfrom = addrcheck.get('coinbase')['addrfrom']

    if addrcheck.get('pubkey', None) is not None:
        hashin = addrcheck.get('pubkey')['hashin']
        addrfrom = addrcheck.get('pubkey')['addrfrom']

    if addrcheck.get('good', None) is not None:
        hashin = addrcheck.get('good')['hashin']
        addrfrom = addrcheck.get('good')['addrfrom']

    #print(json.dumps(addrcheck, sort_keys=True, indent=4, separators=(',', ': ')))

    addrval = {}

    for x in txo.get('outs'):
        script = x.get('script')
        valout = x.get('value')
        outno = x.get('n')
        value = str('{0:.8f}'.format(float(valout / 1e8)))
        addrto = script_to_addr(script)

        hashout = txid + '-' + str(outno)

        #print(hashout, addrto, value)
        addrval[addrto] = {
            "from": addrfrom,
            "hashin": hashin,
            "txid": hashout,
            "to": addrto,
            "value": value
        }

    return addrval
