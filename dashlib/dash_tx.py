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
   #txid = format_hash(double_sha256(binascii.unhexlify(rawtx)))

    # print(txid)
    #print(json.dumps(txo, sort_keys=True, indent=4, separators=(',', ': ')))

    addrcheck = {}
    addrfromall = []

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
                addrfromall.append(addrn)

            elif (addrn == 'pay_to_pubkey'):
                addrcheck['pubkey'] = {
                    "hashin": hashn + '-' + str(x.get('outpoint')['index']),
                    "addrfrom": 'pay_to_pubkey'
                }
                addrfromall.append('pay_to_pubkey')
        else:
            addrcheck['coinbase'] = {
                "hashin": '0000000000000000000000000000000000000000000000000000000000000000' +
                '-' +
                str(0),
                "addrfrom": 'coinbase'
                }
            addrfromall.append('coinbase')

    # use last input
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
            "fromall": addrfromall,
            "hashin": hashin,
            "txid": hashout,
            "to": addrto,
            "value": value
        }

    return addrval


if __name__ == "__main__":

    def check_rawtx(data):
        x = decoderawtx(data)
        #print(json.dumps(x, sort_keys=True, indent=4, separators=(',', ': ')))
        return x
        

        #{
        #    "XpMzawqNtHuewvnvgaMPDGoP761R7MpkFV": {
        #        "from": "XgijdekDojPYXPBvdJqKND4LV41tV7EgZ6",
        #        "hashin": "a2b77a4c704b7044cc15a0a7a78c9848e5edf7630106f211d471a3a4aa6887e7-0",
        #        "to": "XpMzawqNtHuewvnvgaMPDGoP761R7MpkFV",
        #        "txid": "9f5fb5805f1c200e85ce92d5658c959329e3bac02ca5f21801ad9274f1bbc2a1-1",
        #        "value": "24.76163455"
        #    },
        #    "XubToXRwAVu3y4LuAQ6cPqfNnTGnM9uJ9w": {
        #        "from": "XgijdekDojPYXPBvdJqKND4LV41tV7EgZ6",
        #        "hashin": "a2b77a4c704b7044cc15a0a7a78c9848e5edf7630106f211d471a3a4aa6887e7-0",
        #        "to": "XubToXRwAVu3y4LuAQ6cPqfNnTGnM9uJ9w",
        #        "txid": "9f5fb5805f1c200e85ce92d5658c959329e3bac02ca5f21801ad9274f1bbc2a1-0",
        #        "value": "0.01000111"
        #    }
        #}

    check_rawtx('01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff06039ab7010101ffffffff0240230e4300000000232103717f7082f58395f02afb45b1ae871cae31293b33c64c8d9568d9cac09fa70c51ac40230e43000000001976a9146753f211b0fb9ec2b5db90a0a4e08169c25629a388ac00000000')
    check_rawtx('010000000128efb830f177a0fb4c4f0f3d7fee81e46a61c36ebd06b6d5ad5945f2f384f69d010000006b483045022100ea9275dad2aa4f17cd55409d87e1de80e86e14413f9419329dd06cb3f1fde35a0220535e251becb19eb3aec82ef28cdf8f60fe3eee8c9f08e0d7759d32a9e3fdf284012102d1c997d942867336302bd9e5c28f109cf851df0ceeee25563b4f36ae83a2bf2bffffffff020dc0530d000000001976a9147f561dc61197267f553385f53f8eb9623f0a472e88ac62d30928000000001976a914d36f11b42b491b9204d11c34f70f045271031e9988ac00000000')
    check_rawtx('010000000148de3fa6f33c9242450f3258c92ea07f8c74d76d389903e362d15dd9893f1f4a010000006a473044022034a8b4107fb6b25ce724ab7daa4217c9ca2f5c1b156066847afae3bef7bcd463022010b2ae51a9a6b5b344defe3d918e13a906cb3e75364680f3400d3accd22dc1a70121037d75a42ea77cb436fdfe04ac52fa708ec9a2534c082596430fd7da5214d46edcffffffff01f03dcd1d000000001976a914606b2b996ea1255b73fec47318589bd6d94c373388ac00000000')
    check_rawtx('01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff0603cb6a020101ffffffff0240230e43000000002321020c28102cb4f627e0760f167f85ce26fef587db4c60b9f6169cb8363ebab08e34ac40230e43000000001976a9143653b2eb98204e42b0a1ee143aabcad17ef3008a88ac00000000')
    
    y = check_rawtx('0100000009841b4c2286d71e3999a853a4af2a8ef211f6ad689c0dcd94a4793ae8a91ef509940400006a4730440220357af1247e26fb49ed16e67171e152953311b74750301f17e8bfaf802a436cc1022006856054b8e81bdd8c6945184adeef3aae88afa440d77cf689eebc1d6274f87b0121034c5f36809f0c77b3d09f9006a7c4756a85bbca700f87615dca153e7df5b83d93ffffffff0df38e8b4e91c081aa0d048bf75554a832ce3fa42aee7b161e54b23acf3c1947010000006a473044022005d147a984d15465a5acbab31e843c2efdf49f6b2fc369718e51069f739128ee022072854e97a4c7b61337b1c8319321f5e893054358cd22de68593360e1c0326343012102bbfd9d1b28bf9b10ef0c8d4902da1fb3ddc6677508615e3f78a12b2983546014ffffffff23fece7d8f4554fe8897b218ca3f57381e026749ab95df16da357cf798890935cc0100006b483045022100f84f8a65aa53d4ae9f617cf3245d187d6384697c11d06f73d71d39c8ac722b2b022065a33292553b52a5d121f455607c76dfc6ce97fe8e05548b613bd5f65b66c64201210265a4b95950f7ad12d2ab73da6bd299d59c7a69ec47a3fee33e9fcd004392755effffffff23fece7d8f4554fe8897b218ca3f57381e026749ab95df16da357cf7988909350c0200006a4730440220563fce2d03ea7b55e2bfaffe45302f0c57849de4ea88b20c0089c3ec7603df4602207bf4a41ee3c841d19fcdfaef2392b9d525cca2118372750c0d8eba444fbf05c2012103d2fb8a0aa072cbaae66193635a5eb9d426e8757581caa065a21208e4d69af360ffffffff23fece7d8f4554fe8897b218ca3f57381e026749ab95df16da357cf798890935f00400006b483045022100e6936362d0c58eb7a50765def3f5cab68625e28b07b4355c2d1952611758ec970220509c1755bfd0436d230c71deb0dcbbc1b9c3dd2ce1e7be10371a87238ab1b10401210235f28f89f7cbc6dd3ce6bd75d0f53bff0ee50d4e5a37697cd45d40ea57354b48ffffffff4436a7b04aaa0f7e81b7569f8034b54d19341cb6780aa0cec141a6d53f7281dbdb0100006b483045022100e34577fcc17c5d3a78228c89e409c3c8c0c412fb0527354153a0d47b263b03250220524230d2adab348f80152b986858625913e2b5a4dfe6afc07e7612f78c4362de01210236b9dd2a08c2c8e984314e7cfa44c68c7cc190c9a9f6c8535b356d07bae85471ffffffff5bf3871b3327cabf4e5a889a6d96bbff1a2aac9a30fd5ce5756566382faf9903010000006b483045022100cca94c953b916c7c719e25c941d430779d7073dae36514f1acd7e6554a52217f02207f36fe98c9af33aa0328f69f71b6961f011a291323a9aef1ae9880333c60c4680121030076ad42e6b867a67c64d2162cabbfe3c1bc10b74b929dbba84e8a1078014275ffffffff818bae67cfa20257360bb4e46a021acf69c496d123079c627d6869bba0e8d33f010000006b483045022100b306eb03f55bba8cb352e8b792da975cd2210d9d87f2d897564847e7b6df46bc022036e48d08d88862abd3582763544260cf6ceb8dd9309a362f6b2c4914a5d338230121030076ad42e6b867a67c64d2162cabbfe3c1bc10b74b929dbba84e8a1078014275ffffffffe78768aaa4a371d411f2060163f7ede548988ca7a7a015cc44704b704c7ab7a2000000006b483045022100b603160b54cc50cffae77880b6f526cb19023c82d97c8c273025815d1b647e450220528165b33d34f62f69608794f0dcd774825c98c9cfb6550473686dd0c371380a0121030d23a8a9eef8d67a9c15b95c276b66676ade4e4d4a17ad5808b54cdaa02810e7ffffffff02af420f00000000001976a914cf65eba85ceb2f0e2c9c9fb0f635e8548b5a301e88ac7f419793000000001976a91496012a2395d9bec24462531c3681077eedc43d1988ac00000000')

    assert y.get('XpMzawqNtHuewvnvgaMPDGoP761R7MpkFV').get('from')   == 'XgijdekDojPYXPBvdJqKND4LV41tV7EgZ6'
    assert y.get('XpMzawqNtHuewvnvgaMPDGoP761R7MpkFV').get('hashin') == 'a2b77a4c704b7044cc15a0a7a78c9848e5edf7630106f211d471a3a4aa6887e7-0'
    assert y.get('XpMzawqNtHuewvnvgaMPDGoP761R7MpkFV').get('to')     == 'XpMzawqNtHuewvnvgaMPDGoP761R7MpkFV'
    assert y.get('XpMzawqNtHuewvnvgaMPDGoP761R7MpkFV').get('txid')   == '9f5fb5805f1c200e85ce92d5658c959329e3bac02ca5f21801ad9274f1bbc2a1-1'
    assert y.get('XpMzawqNtHuewvnvgaMPDGoP761R7MpkFV').get('value')  == '24.76163455'


    assert y.get('XubToXRwAVu3y4LuAQ6cPqfNnTGnM9uJ9w').get('from')   == 'XgijdekDojPYXPBvdJqKND4LV41tV7EgZ6'
    assert y.get('XubToXRwAVu3y4LuAQ6cPqfNnTGnM9uJ9w').get('hashin') == 'a2b77a4c704b7044cc15a0a7a78c9848e5edf7630106f211d471a3a4aa6887e7-0'
    assert y.get('XubToXRwAVu3y4LuAQ6cPqfNnTGnM9uJ9w').get('to')     == 'XubToXRwAVu3y4LuAQ6cPqfNnTGnM9uJ9w'
    assert y.get('XubToXRwAVu3y4LuAQ6cPqfNnTGnM9uJ9w').get('txid')   == '9f5fb5805f1c200e85ce92d5658c959329e3bac02ca5f21801ad9274f1bbc2a1-0'
    assert y.get('XubToXRwAVu3y4LuAQ6cPqfNnTGnM9uJ9w').get('value')  == '0.01000111'





