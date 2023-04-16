import logging
import os, time
import json
from datetime import datetime, timedelta
from web3 import Web3
from telegram import __version__ as TG_VER
from dotenv import load_dotenv

load_dotenv()  
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

w3 = Web3(Web3.HTTPProvider('https://testnet-rpc.jaihoscan.com/'))
sender_address = "0xfc3e5C537bC66D283E8648A109d75F27b1DEc1E4"
sender_private_key = os.environ.get('sender_private_key')
token_contract_address = '0x5A89F7e45D659695E98148aF069B24c529DBc4fC'
nft_contract_address = '0x18605d4c483AA343CAF971E8462213b1ed302bce'
contract_abi = [
 {
		"inputs": [
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_symbol",
				"type": "string"
			},
			{
				"internalType": "uint8",
				"name": "_decimals",
				"type": "uint8"
			},
			{
				"internalType": "uint256",
				"name": "_totalSupply",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_burnFee",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_devFee",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "_devAddress",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "_burnAddress",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Approval",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Transfer",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			}
		],
		"name": "allowance",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "approve",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "account",
				"type": "address"
			}
		],
		"name": "balanceOf",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "burnAddress",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "burnFee",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "decimals",
		"outputs": [
			{
				"internalType": "uint8",
				"name": "",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "devAddress",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "devFee",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "name",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "symbol",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "totalSupply",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "recipient",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "transfer",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "sender",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "recipient",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "transferFrom",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]


token_contract = w3.eth.contract(address=token_contract_address, abi=contract_abi)
nft_contract = w3.eth.contract(address=nft_contract_address, abi=contract_abi)
claim_limit = 2
limit_duration = timedelta(hours=24)
user_claims = {}

def send(to_address, amount,command_name):
    if command_name == "token":
        amount_in_smallest_unit = amount * (10 ** token_contract.functions.decimals().call())
        transfer_tx = token_contract.functions.transfer(to_address, amount_in_smallest_unit)
        tx = transfer_tx.build_transaction({
            'from': sender_address,
            'nonce': w3.eth.get_transaction_count(sender_address),
            'gas': 100000,
            'gasPrice': w3.eth.gas_price,
        })
    else:
        value_in_wei = w3.to_wei(amount, 'ether')
        tx = {
            'from': sender_address,
            'to': to_address,
            'value': value_in_wei,
            'nonce': w3.eth.get_transaction_count(sender_address),
            'gas': 21000,
            'gasPrice': w3.eth.gas_price, 
            'chainId': 5991,
        }
    signed_tx = w3.eth.account.sign_transaction(tx, sender_private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    start_text = rf"Hi {user.mention_html()}!"
    start_text += "\nWelcome to the JaiHoChain testnet faucet bot!\n \n"
    start_text += "This faucet bot allow only 2 chance to claim in 24H \n"
    start_text+= "send /help command to display use manual"
    await update.message.reply_html(
        start_text 
        #,reply_markup=ForceReply(selective=True),
    )

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) > 0 and w3.is_address(context.args[0]):
        token_balance = token_contract.functions.balanceOf(context.args[0]).call()
        balance_token = token_balance / 10 ** token_contract.functions.decimals().call()
        coin_balance = w3.eth.get_balance(context.args[0])
        balance_coin = w3.from_wei(coin_balance, 'ether')
        nft_balance = nft_contract.functions.balanceOf(context.args[0]).call()
        balance_text = f'{context.args[0]} Balance :\n \nJaiHo Coin : {balance_coin} \n{token_contract.functions.name().call()} ({token_contract.functions.symbol().call()}) : {balance_token} \n{nft_contract.functions.name().call()} ({nft_contract.functions.symbol().call()}) : {nft_balance}'
    else:
        balance_text = "Please provide an valid address\n"
        balance_text+= "(format : /balance 0xfc............Ec1E4)"
    await update.message.reply_text(balance_text) 

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = "The following commands are available:\n\n"
    help_text += "/start - Start the bot \n\n"
    help_text += f"/token - To claim {token_contract.functions.symbol().call()} \n(format : /token 0xfc............Ec1E4)\n \n"
    help_text += f"/coin - To claim JaiHo testnet coin \n(format : /coin 0xfc............Ec1E4)\n \n"
    help_text += f"/balance - Check your balance \n(format : /balance 0xfc............Ec1E4)\n \n"
    help_text += "/help - Display this help message"
    await update.message.reply_text(help_text)

#async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE, command_name: str) -> None:
    user_id = update.effective_user.id
    if user_id not in user_claims:
            user_claims[user_id] = []
    if len(context.args) > 0 and w3.is_address(context.args[0]):
        wallet_address = context.args[0]
        nft_balance = nft_contract.functions.balanceOf(wallet_address).call()
        if len(user_claims[user_id]) < claim_limit or datetime.now() - user_claims[user_id][-1] > limit_duration:
            if command_name == "coin":
                if nft_balance > 0:
                    amount = 0.001
                    tx_hash = send(context.args[0], amount,command_name)
                    confirmation_text = f'{amount} JaiHo Coin sent to: {wallet_address}\n \nTransaction hash: {tx_hash.hex()}'
                    user_claims[user_id].append(datetime.now())
                else:
                    confirmation_text = f"Sorry can't claim coin, only {nft_contract.functions.name().call()} ({nft_contract.functions.symbol().call()}) members can claim coin \n \n"
                    confirmation_text+= f'To become member of {nft_contract.functions.name().call()} ({nft_contract.functions.symbol().call()})\n Please ask in JaiHo Telegram Community (https://t.me/JaiHoOfficial) for {nft_contract.functions.symbol().call()} ({nft_contract.functions.symbol().call()})'
            else:
                amount = 500
                tx_hash = send(context.args[0], amount,command_name) 
                confirmation_text = f'{amount} {token_contract.functions.symbol().call()} sent to: {wallet_address} \n \nTransaction hash: {tx_hash.hex()}'
                user_claims[user_id].append(datetime.now())
        else:
            confirmation_text = f'Sorry, you have reached the maximum number of claims ({claim_limit}) within the past {limit_duration}. Please try again later.'
    else:
        confirmation_text = "Please provide an valid address to claim \n"
        confirmation_text+= "/help command to display use manual"
    await update.message.reply_text(confirmation_text)


def main() -> None:
    application = Application.builder().token(os.environ.get('bot_key')).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    #application.add_handler(CommandHandler("token", echo )) 
    #application.add_handler(CommandHandler("coin", echo)) 
    application.add_handler(CommandHandler("token", lambda update, context: echo(update, context, "token")))
    application.add_handler(CommandHandler("coin", lambda update, context: echo(update, context, "coin")))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, help_command))
    application.run_polling()

if __name__ == "__main__":
    main()
