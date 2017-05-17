# Import section
from libs.parser_init import init_parser
from libs.functions import send_request,send_file_request,send_json_request,print_message,get_key_usage
from libs.texttable import Texttable
from libs.print_table import show_item,print_items
import config.caconfig as config
from libs.CertificateTemplate import CertificateTemplate
import json,datetime
from libs.entities import User,Template,CA,Certificate

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
        print_items(data['templates'])

    #### Displaying the specific template
    elif option.operation == "show":
        if not option.id:
            print_message(config.error_field_mandatory % "id",level="ERROR")
            exit()
        try: 
            data = send_request("GET","tpls/get/%s" % option.id, hostname=option.hostname,port=option.port)
            template = Template.from_json(data['template'])
            print template.print_item().draw()            
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
                template = Template.from_file(option.file)
            else:
                if not option.name:
                    print_message(config.error_field_mandatory % "name")
                    exit()

                # Getting the template data from CLI params
                template = Template.from_option(option)                       

            if not template:
                print_message(config.error_template_init)
                exit() 

            # Sending request to create template
            print_message(send_json_request("POST","tpls/create",params=json.dumps(template.to_dict()),hostname=option.hostname,port=option.port),level="INFO")
               
        except Exception as e:
        	print_message(e)
        
#########################################################
#	              User operations                       #
#########################################################

elif option.which == "user":
	
	###### Listing users
    if option.operation == "list":
    	try:
            data = send_request("POST","users/list",hostname=option.hostname,port=option.port)
            print_items(data['users'])
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
        print_message(send_json_request("POST","users/create",params=json.dumps(user.to_dict()),hostname=option.hostname,port=option.port),level="INFO")        

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
            print_items(data['cas'])
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
            ca = CA.from_json(data['ca'])
            print ca.print_item().draw()        

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

    #### Downloading CRL
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

elif option.which == "certificate":
    
    ### Listing certificates
    if option.operation == "list":
        
        # Getting certificates
        try:
            search = {"search":option.name,"status":option.status,"ca":option.caid,"page":option.page}
            headers = {'Content-Type': 'application/json'}
            data = send_request("POST","certificates/list",params=json.dumps(search),headers=headers,hostname=option.hostname,port=option.port)            

            # Processing the collection of items
            certificates = Certificate.parse_items(data['certificates'])
            print_items(certificates)
        except Exception as e:
            print_message(str(e))

    
	### Revoking certificate
    elif option.operation == "revoke":
        try:
            # Certificate ID is mandatory
            if not option.certificate_id:
                print_message(config.error_field_mandatory % "certificate_id")
                exit()

            # Sending revocation request
            rev_request = {"certs":[option.certificate_id],"reason":option.reason_revoke,"comment":option.comment}
            print_message(send_json_request("POST","certificates/revoke",params=json.dumps(rev_request),hostname=option.hostname,port=option.port),level="INFO")
        except Exception as e:
            print_message(str(e))


    #### Restoring the certificate
    elif option.operation == "restore": 
        try:
            # Certificate ID is mandatory
            if not option.certificate_id:
                print_message(config.error_field_mandatory % "certificate_id")
                exit()

            # Sending request
            print_message(send_json_request("POST","certificates/restore",params=json.dumps({"id":option.certificate_id}),hostname=option.hostname,port=option.port),level="INFO")

        except Exception as e:
            print_message(str(e))

    #### Generating certificate
    elif option.operation == "generate":
        
        try:
            import uuid

            # Template ID is mandatory
            if not option.template_id or not option.caid or not option.user_id:
                print_message(config.error_field_mandatory % "template_id, caid, user_id")
                exit()

            # Creating the request object to send
            cert_request = {"sid":"","certificates":[]}
            cert_request['sid'] = str(uuid.uuid4())
            cert_request['pass'] = option.password
            cert_request['certificates'].append({"uid":option.user_id,"valid":option.valid,"tpl":option.template_id,"ca":option.caid,"pass":option.pfxpassword})

            # Sending request to create Certificate Authority
            headers = {'Content-Type': 'application/json'}
            print_message(send_json_request("POST","certificates/generate",params=json.dumps(cert_request),hostname=option.hostname,port=option.port),level="INFO")             

        except Exception as e:
            print_message(str(e))

    # Getting public key
    elif option.operation == "get-public":

        # Certificate ID is mandatory
        if not option.certificate_id:
            print_message(config.error_field_mandatory % "certificate_id")
            exit()

        # Sending file request
        print send_file_request("GET","certificates/download/public/%s" % option.certificate_id,hostname=option.hostname,port=option.port)

    # Getting public key
    elif option.operation == "get-pfx":
        # Certificate ID is mandatory
        if not option.certificate_id:
            print_message(config.error_field_mandatory % "certificate_id")
            exit()

        # Import section
        import base64

        # Sending file request
        print base64.b64encode(send_file_request("GET","certificates/download/%s" % option.certificate_id,hostname=option.hostname,port=option.port))



#########################################################
#                 Helper operations                     #
#########################################################

elif option.which == "helper":

    ### List countries
    if option.operation == "list-countries":
        
        # Opening countries file
        countries = []
        with open("countries.json","r") as f:
            countries = json.loads(f.read())
        if option.name:
            print_items([{"code":country['code'],"name":country['name']} for country in countries if option.name in country['name']],sort=False)
        else:
            print_items(countries,sort=False)

    ### List revocation reasons
    elif option.operation == "list-reasons":
        reasons = config.reasons
        table = Texttable()
        table.set_cols_align(["c", "c"])
        table.set_cols_valign(["m", "m"])
        table.add_row(["Code", "Reason"])
        for key in sorted(reasons.keys()):
            table.add_row([key, reasons[key]])
        print table.draw()
        exit()

    ### List all Key Usage values
    elif option.operation == "list-ku":
        table = Texttable()
        table.set_cols_align(["c", "c","c"])
        table.set_cols_valign(["m", "m","m"])
        table.add_row(["Value", "Name","Description"])
        for ku in config.key_usages:
            table.add_row([ku['value'],ku['name'],ku['dscr']])
        print table.draw()
        exit()

    ### List Extended Key Usage values
    elif option.operation == "list-sku":
        table = Texttable()
        table.set_cols_align(["c", "c"])
        table.set_cols_valign(["m", "m"])
        table.add_row(["Value", "Name"])
        for ku in config.ext_key_usages:
            table.add_row([ku['value'],ku['name']])
        print table.draw()
        exit()
