# Import section
import requests,json
import config.caconfig as config

### Send common 
def send_request(method,url,params=[],headers=[],hostname="",port=""):
    try:

    	server_url = "http://%s:%s" % (hostname,port)
        
    	# Sending request
        if method == "GET":
    	    r = requests.get("%s/%s" % (server_url,url))
        elif method == "POST":
    	    r = requests.post("%s/%s" % (server_url,url),data=params,headers=headers)
        elif method == "DELETE":
    	    r = requests.delete("%s/%s" % (server_url,url),json=params,headers=headers)
        
        # Processing response
        data = json.loads(r.text)
    	if not data:
    		raise Exception("Error processing the JSON response from server: %s" % r.text)
    	
    	if r.status_code != config.http_ok and r.status_code != config.http_created:
    		raise Exception(data['message'])

    	return data

    except requests.exceptions.ConnectionError as e:
    	raise Exception(str(e))

### Send request to download specific file
def send_file_request(method,url,params=[],headers=[],hostname="",port=""):
    try:

    	server_url = "http://%s:%s" % (hostname,port)

        # Sending request
        if method == "GET":
            r = requests.get("%s/%s" % (server_url,url))
        elif method == "POST":
            r = requests.post("%s/%s" % (server_url,url),data=params,headers=headers)
        return r.text
    except requests.exceptions.ConnectionError as e:
        return str(e)

### Send JSON request for CRUD operations
def send_json_request(method,url,params=[],hostname="",port=""):
    try:
        headers = {'Content-Type': 'application/json'}
        data = send_request(method,url,params=params,headers=headers,hostname=hostname,port=port)
        return data['message']
    except Exception as e:
        return str(e)

def print_message(message,level="ERROR"):
    print "\n     [%s]: %s\n" % (level,message)

def get_key_usage(key,value_list=[]):
    for ku in value_list:
        if ku['value'] == key:
            return ku['name']
    return key

def template_from_file(file):
    
    try:
        template = {}
        template['extensions'] = {}
        template['extensions']['crl'] = {}
        template['extensions']['aia'] = {}
        # Initializing config
        config = ConfigParser.RawConfigParser()
        config.read(file)
        value = ""

        # Getting name and description
        template['name'] = config.get("general","name")
        template['dscr'] = config.get("general","dscr")
        
        # Getting extensions
        template['extensions']['altname'] = config.get("general","alt")
        value = config.get("key_usages","key_usage")
        template['extensions']['ku'] = ([] if value == "" else value.split(","))
        value = config.get("key_usages","ext_key_usage")
        template['extensions']['sku'] = ([] if value == "" else value.split(","))
        value = config.get("policy","policies")
        template['extensions']['policies'] = ([] if value == "" else value.split(","))
        template['extensions']['altname'] = config.get("general","alt")
        template['extensions']['crl']['inherit'] = config.get("crl","inherit")
        template['extensions']['crl']['full'] = config.get("crl","full")
        template['extensions']['crl']['freshest'] = config.get("crl","freshest")
        template['extensions']['aia']['inherit'] = config.get("aia","inherit")
        template['extensions']['aia']['ocsp'] = config.get("aia","ocsp")
        template['extensions']['aia']['issuers'] = config.get("aia","issuers")
        return template
        
    except Exception as e:
        print str(e)
        return None