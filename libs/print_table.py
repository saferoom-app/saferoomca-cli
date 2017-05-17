# Import TextTable
from libs.texttable import Texttable
from libs.functions import print_message


# This method is used to show the object and its values
def show_item(item):
    table = Texttable()
    table.set_cols_align(["c","c"])
    table.set_cols_valign(["m","m"])
    table.add_row(["Field", "Value"])
    table.set_cols_width([30,60])
    keys = sort_keys(sorted(item.__dict__.keys()))
    for key in keys:
               
        # Processing the key
        if "inherit" in key:
        	continue
        
        # Checking if AIA and OCSP are in key
        field = key.title().replace("Aia","AIA").replace("Crl","CRL").replace("Cdp","CDP").replace("Url","URL")

        
    	table.add_row([field.replace("_"," "),item.__dict__[key]])
    return table

def print_items(items,sort=True):

	# Initializing table
	table = Texttable(max_width=200)
	row = []

	# Checking the length
	if not items:
		table.add_row(["No items found"])
		print table.draw()
		exit()

	# Getting the length of collection item
	length = len(items[0].keys())

	# Making columns
	table.set_cols_align(["c"]*length)
	table.set_cols_valign(["m"]*length)

	# Reordering the keys
	if sort == True:
	    keys = sort_keys(items[0].keys())
	else:
		keys = items[0].keys()

	# Printing the row
	table.add_row([key.title() for key in keys])

	# Listing the items
	for item in items:
		row = []
		for key in keys:
			row.append(item[key])
		table.add_row(row)

	print table.draw()

def sort_keys(keys):
	sorted_keys = keys
	col_id = sorted_keys[keys.index("id")]
	col_name = sorted_keys[keys.index("name")]
	sorted_keys.remove(col_name)
	sorted_keys.insert(0,col_name)
	sorted_keys.remove(col_id)
	sorted_keys.insert(0,col_id)
	return sorted_keys