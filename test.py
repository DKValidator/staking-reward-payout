import json
import subprocess

file_name = "data.json"
with open(file_name) as f:
    data = json.load(f)
  
count = 0
total_stake = 0
total_reward = 0
hrs_not_signing = 18.2
blocks_missed = 133376
list_of_payouts = list()
apr = 0.1
seconds_per_year = 365 * 24 * 60 * 60
blocks_per_second = 0.5
rewards_multiplier = (apr / seconds_per_year) * blocks_missed * blocks_per_second

for delegator in data['result']:
    #if delegator['delegator_address'] == 'one1w7nvheulzwprf9d9a3r8sqtv5q47qlqx7kured' :
    stake = delegator['amount'] / 1000000000000000000
    if stake > 99 :
        total_stake += stake
        reward = stake * rewards_multiplier
        total_reward += reward
        count += 1
        payout = {
            "address": delegator['delegator_address'],
            "stake": stake,
            "reward": reward
        }
        list_of_payouts.append(payout)

list_of_payouts.sort(key=lambda payout: payout.get('reward')) 

for payout in list_of_payouts:
    print(payout['address'], payout['reward'])


print('Total Stake', total_stake)
print('Total Reward', total_reward)
print('Delegators', count)

# to-do use suprocess to call hmy send transaction
#subprocess.run(['notepad'])