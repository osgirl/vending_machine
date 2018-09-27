#!/usr/bin/env python

import json
from pathlib import Path
import sys

# To test, follow the instructions in the provided README.md

# Assumptions and Design Decisions

# Use vending machine class
# A vending machine class allowed me to abstract that logic away from the main
# function

# In my program I assumed that a transaction would have certain attributes,
# such as a valid structure. I don't explicity check, for example, that a
# transaction has a name, I assume it does. I would say, from a design
# perspective, that the structure of the transaction should be verified
# before being sent to the vending machine in the first place.

# I assume that the vending machine has an infinite supply of coins from which
# to provide change

# I chose to work with money as coin values rather than dollar values

class VendingMachine(object):

	# Assuming we can return dollar bills, quarters, dimes, nickels, pennies
	coin_values = [100, 25, 10, 5, 1]

	def __init__(self, inventory):
		self.inventory = inventory

	def buy(self, txn):
		# How much money did they give us
		money_given = sum(txn['funds'])

		# Do we have the item
		if (txn['name'] not in self.inventory):
			return (False, txn['funds'])
		# Do we the item in stock
		if (self.inventory[txn['name']]['quantity'] <= 0):
			return (False, txn['funds'])
		# Did they give us enough money?
		if (money_given < self.inventory[txn['name']]['price'] * 100):
			return (False, txn['funds'])

		# If we are here, there is at least one of the item in the inventory,
		# and they have given us enough money

		# Remove 1 item
		self.inventory[txn['name']]['quantity'] -= 1
		# Coin value to return
		coin_value_to_return = money_given - \
			self.inventory[txn['name']]['price'] * 100
		return (True, self.value_to_coins(coin_value_to_return))

	def value_to_coins(self, coin_amount):
		coins = []
		for val in self.coin_values:
			while coin_amount - val >= 0:
				coins.append(val)
				coin_amount -= val
		return coins


def append_json(txn_result, completed_transactions):
	completed_transactions.append({
		'product_delivered': txn_result[0],
		'change': txn_result[1]
	})


completed_transactions = []
# Use below two lines for testing
#with open('test/03/inventory.json') as f_inventory:
#	with open('test/03/transactions.json') as f_transactions:
with open(sys.argv[1]) as f_inventory:
	with open(sys.argv[2]) as f_transactions:
		inventory = json.load(f_inventory)
		transactions = json.load(f_transactions)
		vending = VendingMachine(inventory)
		for txn in transactions:
			#pdb.set_trace()
			txn_result = vending.buy(txn)
			append_json(txn_result, completed_transactions)
print(json.dumps(completed_transactions, indent=4))