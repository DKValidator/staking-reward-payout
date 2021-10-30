import json

# Using the result of a hmyGetDelegatorsByValidator rpc request, work out value of missed block rewards
# and create a json file to be used with hmy CLI for sending transactions: https://github.com/harmony-one/go-sdk

passphrase_file = 'passphrase.txt' # File containing the wallet passphrase
validator_address = 'one1w7nvheulzwprf9d9a3r8sqtv5q47qlqx7kured' # address to send rewards from

#file_name = "snapshot epoch 740.json"
file_name = "snapshot epoch 739.json"
with open(file_name) as f:
    data = json.load(f)
  
count = 0
total_stake = 0
total_reward = 0
hrs_not_signing = 18.2
#blocks_missed = 133376 # epoch 740 - based on blocks requested in epoch 741
blocks_missed = 50416 # epoch 139
transactions = list()
apr = 0.1051 # apr of epoch 741
seconds_per_year = 365 * 24 * 60 * 60
blocks_per_second = 0.5
rewards_multiplier = (apr / seconds_per_year) * blocks_missed * blocks_per_second

for delegator in data['result']:
    stake = delegator['amount'] / 1000000000000000000
    if stake > 99 and delegator['delegator_address'] != validator_address  :
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

#with open("./rewards-epoch-740.json", "w") as file:
with open("./rewards-epoch-739.json", "w") as file:
    json.dump([ob for ob in transactions], file)


print('Total Stake', total_stake)
print('Total Reward', total_reward)
print('Delegators', count)

