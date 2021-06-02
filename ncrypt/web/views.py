from django.shortcuts import render
from django.http import JsonResponse
from web3 import Web3
from .abi import standard_abi as abi
import json
# url='https://api.s0.b.hmny.io/'
# url= 'https://mainnet.infura.io/v3/12bf32a5b691494da2fda4f3be4bad4e
# roposten

url='https://ropsten.infura.io/v3/12bf32a5b691494da2fda4f3be4bad4e'
web = Web3(Web3.HTTPProvider(url))

# used to get key and make account
def create_account(request,secret):
    account=web.eth.create()
    token=account.encrypt(secret+'8ak82;usentkqf8930w;luftn83902')
    return JsonResponse(token)

def token_balance(request,address,token_address): 
    contract=web.eth.contract(address=token_address,abi=abi)
    bal=contract.functions.balanceOf(address).call()
    bal=web.fromWei(bal,'ether')
    return JsonResponse(bal,safe=False)

def ether_balance(request,address): 
    balance=web.eth.get_balance(address)
    bal=web.fromWei(balance,'ether')
    return JsonResponse(bal,safe=False)

def transfer_money(request,address,to_address,token_address):
    nonce=web.eth.getTransactionCount(address)
    print(nonce)
    body_unicode = request.body.decode('utf-8')
    keystore = json.loads(body_unicode)
    print(keystore)
    contract=web.eth.contract(address=token_address,abi=abi)
    transaction = contract.functions.transfer(to_address, 100).buildTransaction({'chainId': 3, 
                   'gas':21000, 
                   'gasPrice':web.toWei('5','gwei'),
                   'nonce': nonce})

    # tx={
    #     'nonce':nonce,
    #     'to':to_address,
    #     'value':web.toWei(value,'ether'),
    #     'gas':16000,
    #     'chainId':3,
    #     'gasPrice':web.toWei('36','gwei')
    # }
    key=web.eth.account.decrypt(keystore,'optimus')
    print(key)
    print(type(key))
    signed=web.eth.account.sign_transaction(transaction,key)
    hash=web.eth.send_raw_transaction(signed.rawTransaction)
    print(hash)
    return hash


