# Import section
from libs.parser_init import init_parser
from libs.functions import send_request,send_file_request,send_json_request,print_message,get_key_usage
from libs.texttable import Texttable
from libs.print_table import show_item
import config.caconfig as config
from libs.CertificateTemplate import CertificateTemplate
import json,datetime
from libs.entities import User,Template

# Initializing the parser
new_parser = init_parser()
option = new_parser.parse_args()

#########################################################
#	              Template operations                   #
#########################################################

if option.which == "template":
	
    #### Listing the templates
    if option.operation == "list":
        data = send_request("GET","tpls/list",hostname=option.hostname,port=option.port)
        # Preparing the table
        table = Texttable()
        table.set_cols_align(["c", "c","c"])
        table.set_cols_valign(["m", "m","m"])
        table.add_row(["Id", "Name","Description"])
        for tpl in data['templates']:
            table.add_row([tpl['id'], tpl['name'],tpl['dscr']])
        print table.draw()

    #### Displaying the specific template
    elif option.operation == "show":
        if not option.id:
            print_message(config.error_field_mandatory % "id",level="ERROR")
            exit()
        try: 
            data = send_request("GET","tpls/get/%s" % option.id, hostname=option.hostname,port=option.port)
            table = Texttable()
            table.set_cols_align(["c", "c"])
            table.set_cols_valign(["m", "m"])
            table.add_row(["Field", "Value"])
            table.add_row(["Name", data['template']['name']])
            table.add_row(["Description", data['template']['dscr']])
            table.add_row(["Key Usage", ", ".join([get_key_usage(key,config.key_usages) for key in data['template']['extensions']['ku']])])
            table.add_row(["Extended Key Usage", ", ".join([get_key_usage(key,config.ext_key_usages) for key in data['template']['extensions']['sku']])])
            table.add_row(["CRL Distribution Point",data['template']['extensions']['crl']['full']])
            table.add_row(["Freshest CRL (Delta) Distribution Point",data['template']['extensions']['crl']['freshest']])
            table.add_row(["Certificate policies",", ".join(data['template']['extensions']['policies'])])
            table.add_row(["OCSP URL",data['template']['extensions']['aia']['ocsp']])
            table.add_row(["CA Issuers URL",data['template']['extensions']['aia']['issuers']])
            table.add_row(["Subject Alternative name",data['template']['extensions']['altname']])
            table.add_row(["Key Length",data['template']['extensions']['keylen']])
            print table.draw()
        except Exception as e:
            print_message(str(e),level="ERROR")

    #### Deleting templates
    elif option.operation == "delete":
    	if not option.id:
    		print_message(config.error_field_mandatory % "id")
    		exit()
        proceed = raw_input("Do you really want to delete specified template(s)? [y/n]: ")
    	if proceed.lower() == "y":
            # Sending request to create template
            print_message(send_json_request("DELETE","tpls/delete",params=json.dumps(([] if option.id == "" else option.id.split(","))),hostname=option.hostname,port=option.port),level="INFO")

    # Creating templates
    elif option.operation == "create":

    	try:

            # Checking if name is specified
            template = {}

            # Checking if file is specified
            if option.file:
                if os.path.exists(option.file) == False:
                    print_message(config.error_file_notfound % option.file)
                    exit()
                template = CertificateTemplate.from_file(option.file)
            else:
                if not option.name:
                    print_message(config.error_field_mandatory % "name")
                    exit()

                # Getting the template data from CLI params
                template = Template.from_option(option)
                print template.to_dict()

            if not template:
                print_message(config.error_template_init)
                exit() 

            # Sending request to create template
            print_message(send_json_request("POST","tpls/create",params=json.dumps(template.to_dict()),hostname=option.hostname,port=option.port),level="INFO")
               
        except Exception as e:
        	print_message(str(e))
        
        

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

        # Initializing user        
        user = User.from_option(option)
        
        # Sending request to user
        print "\n\t" + send_json_request("POST","users/create",params=json.dumps(user.to_dict()),hostname=option.hostname,port=option.port)

    #### Deleting users
    elif option.operation == "delete":
        if not option.user_id:
            print_message(config.error_field_mandatory % ("user_id"))
            exit()
        proceed = raw_input("Do you really want to delete specified user(s)? [y/n]: ")
        if proceed.lower() == "y":
            
            # Sending request to create template
            print "\n\t"+send_json_request("DELETE","users/delete",params=json.dumps(([] if option.user_id == "" else option.user_id.split(","))),hostname=option.hostname,port=option.port)

#########################################################
#	              CA operations                         #
#########################################################

elif option.which == "ca":

    #### Listing CAs
    if option.operation == "list":
        try:
            headers = {'Content-Type': 'application/json'}
            data = send_request("POST","ca/list",params=json.dumps({"search":""}),headers=headers,hostname=option.hostname,port=option.port)
            table = Texttable()
            table.set_cols_align(["c", "c","c","c"])
            table.set_cols_valign(["m", "m","m","m"])
            table.add_row(["Id", "Name","Description","Root CA"])
            for ca in data['cas']:
                table.add_row([ca['id'], ca['name'],ca['dscr'],ca['root_ca']])
            print table.draw()
        except Exception as e:
        	print_message(str(e))

    #### Creating CA
    elif option.operation == "create":

    	# Checking the mandatory fields
        if not option.name:
            print_message(config.error_field_mandatory % "name")
            exit()
        if not option.password:
            print_message(config.error_field_mandatory % "password")
            exit()

        # Initializing the request object
        ca = {}
        ca['name'] = option.name
        ca['dscr'] = option.description
        ca['pass'] = option.password
        ca['keylen'] = option.keylen
        ca['hash'] = option.hashalg
        ca['subjectDN'] = {}
        ca['extensions'] = {}
        ca['extensions']['crl'] = ""
        ca['extensions']['ocsp'] = ""
        ca['extensions']['issuers'] = ""

        # Setting the Subject DN
        ca['subjectDN']['CN'] = option.name
        if option.email:
            ca['subjectDN']['E'] = option.email
        if option.country:
            ca['subjectDN']['C'] = option.country
        if option.org:
            ca['subjectDN']['O'] = option.org
        if option.dep:
            ca['subjectDN']['OU'] = option.dep
        if option.state:
            ca['subjectDN']['ST'] = option.state
        if option.city:
            ca['subjectDN']['L'] = option.city

        # Setting validity
        ca['valid'] = option.valid

        # Setting the Root CA
        ca['root_ca'] = {}
        ca['root_ca']['ca_id'] = option.root_ca
        ca['root_ca']['pass'] = option.root_password
        if option.root_ca > 0 and option.root_password == "":
            print_message(config.error_field_mandatory % "root_ca and root_password")
            exit()

        # Setting extensions
        if option.include_crl == True:
            ca['extensions']['crl'] = config.server_url % (option.hostname,option.port ) + config.crl_prefix
        if option.include_ocsp == True:
            ca['extensions']['ocsp'] = config.server_url % (option.hostname,option.port ) + config.ocsp_prefix
        if option.include_issuers == True:
            ca['extensions']['issuers'] = config.server_url % (option.hostname,option.port ) + config.issuers_prefix

        print_message(send_json_request("POST","ca/create",params=json.dumps(ca),hostname=option.hostname,port=option.port),level="INFO")

    #### Displaying information about CA
    elif option.operation == "show":
        
        # Checking if ID is specified
        if not option.id:
            print_message(config.error_field_mandatory % "id")
        
        try:
            # Getting CA information
            data = send_request("GET","ca/get/%s" % option.id,hostname=option.hostname,port=option.port)

            # Displaying the CA information
            table = Texttable()
            table.set_cols_align(["c", "c"])
            table.set_cols_valign(["m", "m"])
            table.add_row(["Field", "Value"])
            table.add_row(["ID", data['ca']['id']])
            table.add_row(["Name", data['ca']['name']])
            table.add_row(["Subject DN",data['ca']['subject_dn'] ])
            table.add_row(["Description", data['ca']['dscr']])
            table.add_row(["Expires", datetime.datetime.fromtimestamp(data['ca']['expires']).strftime('%Y-%m-%d %H:%M:%S')])
            table.add_row(["CRL Distribution Point", data['ca']['extensions']['crl'].replace("<ca_id>",str(data['ca']['id']))])
            table.add_row(["OCSP URL", data['ca']['extensions']['ocsp'].replace("<ca_id>",str(data['ca']['id']))])
            table.add_row(["Issuers URL", data['ca']['extensions']['issuers'].replace("<ca_id>",str(data['ca']['id']))])
            print table.draw()

        except Exception as e:
        	print_message(str(e))

    #### Getting CA certificate
    elif option.operation == "get-cert":
    	if not option.id:
            print_message(config.error_field_mandatory % "id")
            exit()
        print send_file_request("GET","ca/%s/crt" % option.id,hostname=option.hostname,port=option.port)
        exit()

    #### Getting CA's private key
    elif option.operation == "get-private":
    	
    	# Checking that CA ID is specified
    	if not option.id:
            print_message(config.error_field_mandatory % "id")
            exit()

        print send_file_request("GET","ca/%s/pkey" % option.id,hostname=option.hostname,port=option.port)
        exit()

    ####  Generating new CRL
    elif option.operation == "generate-crl":
        
        # Checking if ID is specified
        if not option.id:
            print_message(config.error_field_mandatory % "id")
            exit()

        # Checking if ID is specified
        if not option.password:
            print_message(config.error_field_mandatory % "password")
            exit()

        # Sending request to generate CRL
        print_message(send_json_request("POST","ca/%s/crl/generate" % option.id,params=json.dumps({"pass":option.password}),hostname=option.hostname,port=option.port),level="INFO")

    #### Listing the CRLs for specific CA
    elif option.operation == "list-crl":
        # Checking if ID is specified
        if not option.id:
            print_message(config.error_field_mandatory % "id")
            exit()

        # Sending request
        try:
            data = send_request("GET","ca/%s/crl/list" % option.id,hostname=option.hostname,port=option.port)
            table = Texttable()
            table.set_cols_align(["c", "c"])
            table.set_cols_valign(["m", "m"])
            table.add_row(["Id", "Created"])
            for crl in data['crls']:
                table.add_row([crl['id'], crl['created']])
            print table.draw()
        except Exception as e:
        	print_message(str(e),level="ERROR")
        finally:
        	exit()

    # Downloading CRL
    elif option.operation == "get-crl":
        
        # Checking if ID is specified
        if not option.id:
            print_message(config.error_field_mandatory % "id")
            exit()

        # Getting the CRL
        print send_file_request("GET","ca/crl/get/%s" % option.id,hostname=option.hostname,port=option.port)
        exit()

#########################################################
#                 Certificate operations                #
######################################################### 

elif option.operation == "":
	pass
