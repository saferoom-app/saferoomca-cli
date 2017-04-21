# Import section
from libs.parser_init import init_parser
from libs.functions import send_request,send_file_request,send_json_request,print_message
from libs.texttable import Texttable
import config.caconfig as config

# Initializing the parser
new_parser = init_parser()
option = new_parser.parse_args()

#########################################################
#	              Template operations                   #
#########################################################

if option.which == "template":
	pass

#########################################################
#	              User operations                       #
#########################################################

elif option.which == "user":
	
	###### Listing users
    if option.operation == "list":
    	try:
            data = send_request("POST","users/list",hostname=option.hostname,port=option.port)
            table = Texttable()
            table.set_cols_align(["c", "c","c","c"])
            table.set_cols_valign(["m", "m","m","m"])
            table.add_row(["Id", "Name","Email","Subject"])
            for user in data['users']:
                table.add_row([user['id'], user['name'],user['email'],user['subject']])
            print table.draw()
        except Exception as e:
        	print_message(message=str(e),level="ERROR")

    ###### Creating user
    elif option.operation == "create":
        
        # Checking input data
        if not option.name:
            print_message(config.error_name_mandatory)
            exit()

        # Generating Subject DN
        subject = []
        if option.name:
            subject.append("CN=%s" % option.name)
        if option.email:
            subject.append("E=%s" % option.email)
        if option.country:
            subject.append("C=%s" % option.country)
        if option.org:
            subject.append("O=%s" % option.org)
        if option.dep:
            subject.append("OU=%s" % option.dep)
        if option.state:
            subject.append("ST=%s" % option.state)
        if option.city:
            subject.append("L=%s" % option.city)

        # Preparing data for the JSON request
        user = {"name":option.name,"email":option.email,"subject":",".join(subject)}
        
        # Sending request to user
        print "\n\t" + send_json_request("POST","users/create",params=user,hostname=option.hostname,port=option.port)

    #### Deleting users
    elif option.operation == "delete":
        if not option.user_id:
            print_message(config.error_field_mandatory % ("user_id"))
            exit()
        proceed = raw_input("Do you really want to delete specified user(s)? [y/n]: ")
        if proceed.lower() == "y":
            
            # Sending request to create template
            print "\n\t"+send_json_request("DELETE","users/delete",params=([] if option.user_id == "" else option.user_id.split(",")),hostname=option.hostname,port=option.port)