import json
import subprocess

# Using the result of a hmyGetDelegatorsByValidator rpc request, work out value of missed block rewards
# and create a json file to be used with hmy CLI for sending transactions: https://github.com/harmony-one/go-sdk

passphrase_file = './passphrase.txt' # File containing the wallet passphrase
working_directory = '~/harmony/'
validator_address = 'one1w7nvheulzwprf9d9a3r8sqtv5q47qlqx7kured' # address to send rewards from

file_name = "data.json"
with open(file_name) as f:
    data = json.load(f)
  
count = 0
total_stake = 0
total_reward = 0
hrs_not_signing = 18.2
blocks_missed = 133376
transactions = list()
apr = 0.1
seconds_per_year = 365 * 24 * 60 * 60
blocks_per_second = 0.5
rewards_multiplier = (apr / seconds_per_year) * blocks_missed * blocks_per_second

for delegator in data['result']:
    #if delegator['delegator_address'] == 'one1w7nvheulzwprf9d9a3r8sqtv5q47qlqx7kured' :
    stake = delegator['amount'] / 1000000000000000000
    if stake > 99 and delegator['delegator_address'] != 'one1w7nvheulzwprf9d9a3r8sqtv5q47qlqx7kured'  :
        total_stake += stake
        reward = stake * rewards_multiplier
        total_reward += reward
        count += 1
        transaction = {
            "from": validator_address,
            "to": delegator['delegator_address'],
            "from-shard" : "0",
            "to-shard": "0",
            "amount": reward,
            "passphrase-file": passphrase_file
        }
        transactions.append(transaction)

transactions.sort(key=lambda transaction: transaction.get('amount')) 

#for transaction in transactions:
#    print(transaction)

with open("./rewards-epoch-test.json", "w") as file:
    json.dump([ob for ob in transactions], file)


print('Total Stake', total_stake)
print('Total Reward', total_reward)
print('Delegators', count)

