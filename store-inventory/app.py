#! usr/bin/env python3
import csv
import datetime
import sys

from collections import OrderedDict

from peewee import *

db = SqliteDatabase('inventory.db')


class Product(Model):
	product_id = AutoField()
	product_name = CharField(unique=True)
	product_price = IntegerField()
	product_quantity = IntegerField()
	date_updated = DateTimeField(default=datetime.datetime.now)

	class Meta():
		database = db


def initialize():
	db.connect()
	db.create_tables([Product], safe=True)

inventory = []

def read_csv(inventory):
    with open('inventory.csv', newline='') as inventory_csv:
        inventory_reader = csv.DictReader(inventory_csv, delimiter=',')
        
        for row in inventry_reader:
            row['product_price'] = int(row['product_price'].replace('$', '').replace('.', ''))
            row['product_quantity'] = int(row['product_quantity'])
            row['date_updated'] = datetime.datetime.strptime(row['date_updated'],'%m/%d/%Y')
        inventory.append(row)


def add_to_database(inventory):
    for row in inventory:
        try:
            Product.create(product_name = row['product_name'],
            product_price = row['product_price'],
            product_quantity = row['product_quantity'],
            date_updated = row['date_updated'])

		except IntegrityError:
			inventory_record = Product.get(product_name = row['product_name'])
			inventory_record = Prodcut.get(product_price = row['product_price'])
			inventory_record = Product.get(product_quantity = row['product_quantity'])
			inventory_record = Product.get(date_updated = row['date_uodated'])
			inventory_record.save()


def menu():
	choice = None

	while choice != 'q':
        print("Enter 'q' to quit")

		for key, value in menu.items():
			print(f'{key}, {value.__doc__}.')
		choice = input('Action: ').lower().strip()

		if choice in menu:
			options_menu[choice]()


def view_entries():
	""" View Entries """
	products = Product.select().order_by(Product.product_id.desc())

	search_query = input('Search query: ')

	if search_query:
		products = products.where(Prodcut.product_id.contains(search_query))

	for product in products:
		print(product.product_id)
		print(product.product_name)
		print(product.price)
		print(product.quantity)
		print(product.date_updated)
		print('n) next entry')
		print('r) return to main menu')
		print('q) quit')

		next_action = input('Action: [nrd] '.lower().strip())
		if next_action == 'r':
			Menu()
		elif next_action == 'q':
			break
			print('Thank you! goodbye.')


def get_product_name():
    new_product = input('What is the name of your product?\n ')
    return new_product


def get_product_price():
    new_price = input('What is price of your product?\n ')
    new_price = int(new_price.replace('$', '').replace('.', ''))
    return new_price


def get_product_quantity():
    new_quantity = input('What is the quantity of your product?\n ')
    return new_quantity


def add_entries():
    """ Add Entry """
    product_name = get_product_name()
    product_price = get_product_price()
    product_quantity = get_product_quantity()
    
    saved = input('Save entry? [Yn] ').lower()

    if saved != 'n':
        try:
            Product.create(product_name = product_name,
            product_price = product_price,
            product_quantity = product_quantity)
            print('Saved Successfully!')
        except IntegrityError:
            inventory_record = Product.get(product_name = product_name)
            inventory_record = Prodcut.get(product_price = product_name)
            inventory_record = Product.get(product_quantity = product_name)
            inventory_record = Product.get(date_updated = product_name)
            inventory_record.save()


def backup_database():
    """ Backup Database """
    with open('backup.csv', 'a') as backup_csv:
        fields = ['product_id', 'product_name', 'product_price', 'product_quantity', 'date_updated']
        backup_writer = csv.DictWriter(backup_csv, fieldnames=fields)
        
        backup_writer.writeheader()
        for row in Product.select().order_by(Product.date_ordered.desc()):
            backup_writer.writerow({'product_id': row.product_id})
            backup_writer.writerow({'product_name': row.product_name})
            backup_writer.writerow({'product_price': row.product_price})
            backup_writer.writerow({'product_quantity': row.product_quantity})
            backup_writet.writerow({'date_updated': row.date_updated})
        print('Backup successfully completed.')
        menu()


options_menu = OrderedDict([('v', view_entries), ('a', add_entries), ('b', backup_database)])

if __name__ == '__main__':
	initialize()
	read_csv(inventory)
	add_to_database(inventory)
    menu()



