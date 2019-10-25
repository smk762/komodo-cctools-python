import re
import os
import http
import platform
from slickrpc import Proxy
import bitcoin
from bitcoin.wallet import P2PKHBitcoinAddress
from bitcoin.core import x
from bitcoin.core import CoreMainParams

class CoinParams(CoreMainParams):
    MESSAGE_START = b'\x24\xe9\x27\x64'
    DEFAULT_PORT = 7770
    BASE58_PREFIXES = {'PUBKEY_ADDR': 60,
                       'SCRIPT_ADDR': 85,
                       'SECRET_KEY': 188}
bitcoin.params = CoinParams

def unlock_wallet(rpc_connection):
    chances = 3
    while True:
        passphrase = input(colorize("Please enter your wallet passphrase: ",'input'))
        timeout = input(colorize("Please enter seconds to unlock (recommended 1800): ",'input'))
        try:
            resp = rpc_connection.walletpassphrase(passphrase, int(timeout))
            print(colorize("Wallet unlocked, you may now proceed!",'success'))
            return
        except Exception as e:
            if chances == 0:
                print(colorize("Incorrect! No TUI for you!",'red'))
                sys.exit()
            print(colorize("Incorrect! You have "+str(chances)+" chances remaining...: ",'red'))
            print(colorize(e,'red'))
            chances -= 1
            pass

def get_radd_from_pub(pub):
    try:
        radd = str(P2PKHBitcoinAddress.from_pubkey(x(pub)))
    except:
        radd = pub
    return str(radd)

# RPC connection
def get_rpc_details(chain):
    rpcport =''
    rpcuser =''
    rpcpassword =''
    bad_conf = False
    operating_system = platform.system()
    if operating_system == 'Darwin':
        ac_dir = os.environ['HOME'] + '/Library/Application Support/Komodo'
    elif operating_system == 'Linux':
        ac_dir = os.environ['HOME'] + '/.komodo'
    elif operating_system == 'Win64' or operating_system == 'Windows':
        ac_dir = '%s/komodo/' % os.environ['APPDATA']
    if chain == 'KMD':
        coin_config_file = str(ac_dir + '/komodo.conf')
    else:
        coin_config_file = str(ac_dir + '/' + chain + '/' + chain + '.conf')
    with open(coin_config_file, 'r') as f:
        for line in f:
            l = line.rstrip()
            if re.search('rpcuser', l):
                rpcuser = l.replace('rpcuser=', '')
            elif re.search('rpcpassword', l):
                rpcpassword = l.replace('rpcpassword=', '')
            elif re.search('rpcport', l):
                rpcport = l.replace('rpcport=', '')
    if rpcport == '':
        if chain == 'KMD':
            rpcport = 7771
        else:
            print("rpcport not in conf file, exiting")
        bad_conf = True
    if rpcuser == '':
        print("rpcuser not in conf file, exiting")
        bad_conf = True
    if rpcpassword == '':
        print("rpcpassword not in conf file, exiting")
        bad_conf = True
    if bad_conf:
        print("check "+coin_config_file)
        exit(1)
    return rpcuser, rpcpassword, rpcport

def def_credentials(chain):
    rpc = get_rpc_details(chain)
    try:
        rpc_connection = Proxy("http://%s:%s@127.0.0.1:%d"%(rpc[0], rpc[1], int(rpc[2])))
    except Exception:
        raise Exception("Connection error! Probably no daemon on selected port.")
    return rpc_connection

def rpc_connect(rpc_user, rpc_password, port):
    try:
        rpc_connection = Proxy("http://%s:%s@127.0.0.1:%d"%(rpc_user, rpc_password, port))
    except Exception:
        raise Exception("Connection error! Probably no daemon on selected port.")
    return rpc_connection


# Non CC calls
def getinfo(rpc_connection):
    try:
        getinfo = rpc_connection.getinfo()
    except Exception:
        raise Exception("Connection error!")
    return getinfo

def sendrawtransaction(rpc_connection, hex):
    tx_id = rpc_connection.sendrawtransaction(hex)
    return tx_id


def gettransaction(rpc_connection, tx_id):
    transaction_info = rpc_connection.gettransaction(tx_id)
    return transaction_info


def getrawtransaction(rpc_connection, tx_id):
    rawtransaction = rpc_connection.getrawtransaction(tx_id)
    return rawtransaction


def getbalance(rpc_connection):
    balance = rpc_connection.getbalance()
    return balance

# Token CC calls
def token_create(rpc_connection, name, supply, description):
    token_hex = rpc_connection.tokencreate(name, supply, description)
    return token_hex


def token_info(rpc_connection, token_id):
    token_info = rpc_connection.tokeninfo(token_id)
    return token_info


#TODO: have to add option with pubkey input
def token_balance(rpc_connection, token_id):
    token_balance = rpc_connection.tokenbalance(token_id)
    return token_balance

def token_list(rpc_connection):
    token_list = rpc_connection.tokenlist()
    return token_list


def token_convert(rpc_connection, evalcode, token_id, pubkey, supply):
    token_convert_hex = rpc_connection.tokenconvert(evalcode, token_id, pubkey, supply)
    return token_convert_hex

def get_rawmempool(rpc_connection):
    mempool = rpc_connection.getrawmempool()
    return mempool

# Oracle CC calls
def oracles_create(rpc_connection, name, description, data_type):
    oracles_hex = rpc_connection.oraclescreate(name, description, data_type)
    return oracles_hex

def oracles_fund(rpc_connection, oracle_id):
    oracles_fund_hex = rpc_connection.oraclesfund(oracle_id)
    return oracles_fund_hex

def oracles_register(rpc_connection, oracle_id, data_fee):
    oracles_register_hex = rpc_connection.oraclesregister(oracle_id, data_fee)
    return oracles_register_hex


def oracles_subscribe(rpc_connection, oracle_id, publisher_id, data_fee):
    oracles_subscribe_hex = rpc_connection.oraclessubscribe(oracle_id, publisher_id, data_fee)
    return oracles_subscribe_hex


def oracles_info(rpc_connection, oracle_id):
    oracles_info = rpc_connection.oraclesinfo(oracle_id)
    return oracles_info


def oracles_data(rpc_connection, oracle_id, hex_string):
    oracles_data = rpc_connection.oraclesdata(oracle_id, hex_string)
    return oracles_data


def oracles_list(rpc_connection):
    oracles_list = rpc_connection.oracleslist()
    return oracles_list


def oracles_samples(rpc_connection, oracletxid, batonutxo, num):
    oracles_samples = rpc_connection.oraclessamples(oracletxid, batonutxo, num)
    return oracles_samples

# TODO: add this RPC to TUI
def oracles_sample(rpc_connection, oracletxid, sample_txid):
    oracles_sample = rpc_connection.oraclessample(oracletxid, sample_txid)
    return oracles_sample


# Gateways CC calls
# Arguments changing dynamically depends of M N, so supposed to wrap it this way
# token_id, oracle_id, coin_name, token_supply, M, N + pubkeys for each N
def gateways_bind(rpc_connection, *args):
    gateways_bind_hex = rpc_connection.gatewaysbind(*args)
    return gateways_bind_hex


def gateways_deposit(rpc_connection, gateway_id, height, coin_name,\
                     coin_txid, claim_vout, deposit_hex, proof, dest_pub, amount):
    gateways_deposit_hex = rpc_connection.gatewaysdeposit(gateway_id, str(height), coin_name,\
                     coin_txid, str(claim_vout), deposit_hex, proof, dest_pub, str(amount))
    return gateways_deposit_hex


def gateways_claim(rpc_connection, gateway_id, coin_name, deposit_txid, dest_pub, amount):
    gateways_claim_hex = rpc_connection.gatewaysclaim(gateway_id, coin_name, deposit_txid, dest_pub, str(amount))
    return gateways_claim_hex


def gateways_withdraw(rpc_connection, gateway_id, coin_name, withdraw_pub, amount):
    gateways_withdraw_hex = rpc_connection.gatewayswithdraw(gateway_id, coin_name, withdraw_pub, amount)
    return gateways_withdraw_hex

def gateways_list(rpc_connection):
    gateways_list = rpc_connection.gatewayslist()
    return gateways_list

def pegs_fund(rpc_connection, pegs_txid, token_txid, amount):
    pegsfund_hex = rpc_connection.pegsfund(pegs_txid, token_txid, str(amount))
    return pegsfund_hex

def pegs_get(rpc_connection, pegs_txid, token_txid, amount):
    pegsget_hex = rpc_connection.pegsget(pegs_txid, token_txid, str(amount))
    return pegsget_hex

# Import Gateways CC calls

def importgw_processed(rpc_connection, bindtxid, coin):
    resp = rpc_connection.importgatewayprocessed(bindtxid, coin)
    return resp

def importgw_pendingwithdraws(rpc_connection, bindtxid, coin):
    resp = rpc_connection.importgatewaypendingwithdraws(bindtxid, coin)
    return resp

#use 'importgatewaybind coin orcletxid M N pubkeys pubtype p2shtype wiftype [taddr]' to bind an import gateway
#use 'importgatewaydeposit bindtxid height coin burntxid nvout rawburntx rawproof destpub amount' to import deposited coins

#importgatewaycompletesigning withdrawtxid coin hex

#importgatewaymarkdone completesigningtx coin
#importgatewayspartialsign txidaddr refcoin hex

#importgatewayinfo bindtxid
#importgatewayddress [pubkey]
