# Import TextTable
from libs.texttable import Texttable


# This method is used to show the object and its values
def show_item(item):
    
    table = Texttable()
    table.set_cols_align(["c","c"])
    table.set_cols_valign(["m","m"])
    table.add_row(["Field", "Value"])
    for key in item.__dict__.keys():
    	table.add_row([key.title(),item.__dict__[key]])
    print table.draw()

