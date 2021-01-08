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


def read_csv():
	
	with open('inventory.csv', newline='') as inventory_csv:
		inventory_reader = csv.DictReader(inventory_csv, delimiter=',')
		rows = list(inventory_reader)

		for row in rows:
			row['product_price'] = int(row['product_price'].replace('$', '').replace('.', ''))
			row['product_quantity'] = int(row['product_quantity'])
			row['date_updated'] = datetime.datetime.strptime(row['date_updated'],'%m/%d/%Y')

			
def add_to_database(read_csv):
	
	for row in rows:
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
	# this will prompt the user for a action, with only v a and b being acceptable inputs
	# if the user selects v, view the details of a single product in the database
	# if the user selects a, this will add a new product to the database
	# if the user selects b, this will backup the database 

	choice = None

	while choice != 'q':
		print("Enter 'q' to quit")

		for key, value in menu.items():
			print(f'{key}, {value.__doc__}.')
		choice = input('Action: ').lower().strip()

		if choice in menu:
			menu[choice]()


def view_entries():
	""" View Entries """
	# dispaly the products from the database
	# will want to show latest to oldest first
	# get and display a product by its product id

	products = Product.select().order_by(Product.date_ordered.desc())

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



def add_entries():
	""" Add Entry """
	# a new variable which will equal to none
	# while loop to say while variable not equal q, print enter q to quit 
	# product_name = input product name 
	# product price = input product price show example of format, we need to change $2.99 to 299
	# product quantity = input the product quantity
	# add this to our database .create() with add_data function
	active = True
	while active:
		product_name = input('What is the name of your product?\n ')
		product_price = input('What is the price of your prodcut?\n ')
		product_quantity = input('What is the quantity of your product?\n ')

        saved = input('Save entry? [Yn] ').lower()

        if saved != 'n':
            Product.create(product_name=product_name,
            product_price=product_price,
            product_quantity=product_quantity)
            print('Saved Successfully!')


def backup_database():
	""" Backup Database """
    with open('backup.csv', 'a') as backup_csv:
        fields = ['product_id', 'product_name', 'product_price', 'product_quantity', 'date_updated']
        backup_writer = csv.DictWriter(backup_csv, fieldnames=fields)
        
        backup_writer.writeheader()
        backup_writer.writerow(rows)




menu = OrderedDict([('v', view_entries), ('a', add_entries), ('b', backup_database)])

if __name__ == '__main__':
	initialize()
	read_csv()
	add_to_database(read_csv)




