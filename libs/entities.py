# Import section
from libs.print_table import show_item
import os,ConfigParser,datetime

class User():

    def __init__(self):
    	self.name = ""
    	self.email = ""
        self.subject = []

    def __repr__(self):
        return "User, name=%r, email=%r, subject=%r" % (self.name,self.email,self.subject)

    @staticmethod
    def from_option(option):
        user = User()
        user.name = option.name
        user.subject.append("CN=%s" % option.name)
        user.email = option.email
        if option.email:
        	user.subject.append("E=%s" % option.email)
        if option.country:
        	user.subject.append("C=%s" % option.country)
        if option.org:
        	user.subject.append("O=%s" % option.org)
        if option.dep:
        	user.subject.append("OU=%s" % option.dep)
        if option.state:
        	user.subject.append("ST=%s" % option.state)
        if option.city:
        	user.subject.append("L=%s" % option.city)
        return user


    def to_dict(self):
    	return {"name":self.name,"email":self.email,"subject":",".join(self.subject)}


class Template():
    
    def __init__(self):
        pass	

    def __repr__(self):
    	return "<Template, name=%r, dscr=%r>" % (self.name,self.description)

    @staticmethod
    def from_file(file):
        try:
            if os.path.exists(file) == False:
                return None

            value = ""

            # Initializing config
            config = ConfigParser.RawConfigParser()
            config.read(file)

            # Initializing template
            template = Template()
            template.name = config.get("general","name")
            template.description = config.get("general","dscr")
            template.key_length = config.get("keylen","length")
            template.alt_name = config.get("general","alt")
            value = config.get("key_usages","key_usage")
            template.key_usage = ([] if value == "" else value.split(","))
            value = config.get("key_usages","ext_key_usage")
            template.extended_key_usage = ([] if value == "" else value.split(","))
            
            template.full_crl = config.get("crl","full")
            template.freshest_crl = config.get("crl","freshest")
            template.inherit_crl = config.get("crl","inherit")
            template.aia_ocsp = config.get("aia","ocsp")
            template.aia_issuers = config.get("aia","issuers")
            template.inherit_aia = config.get("aia","inherit")
            value = config.get("policy","policies")
            template.policies = ([] if value == "" else value.split(","))           
            return template
        except Exception as e:
            print e
            return None

    @staticmethod
    def from_option(option):
    	try:
            template = Template()
            template.name = option.name
            template.description = option.dscr
            template.key_length = option.keylen
            template.alt_name = option.altname
            template.key_usage = ([] if option.keyusage == "" else option.keyusage.split(","))
            template.extended_key_usage = ([] if option.extkeyusage == "" else option.extkeyusage.split(","))
            template.full_crl = option.fullcrl
            template.freshest_crl = option.deltacrl
            if option.fullcrl != "" and option.deltacrl != "":
    		    template.inherit_crl = 0
            else:
                template.inherit_crl = 1
                template.aia_ocsp = option.ocspurl
                template.aia_issuers = option.issuersurl
                if option.ocspurl != "" and option.issuersurl != "":
                    template.inherit_aia = 0
                else:
            	    template.inherit_aia = 1
            	template.policies = ([] if option.policies == "" else option.policies.split(","))
            return template
    	except Exception as e:
            raise e

    @staticmethod
    def from_json(json):
        try:
            template = Template()
            template.name = json['name']
            template.description = json['dscr']
            template.key_length = json['extensions']['keylen']
            template.alt_name = json['extensions']['altname']
            template.key_usage = ",".join(json['extensions']['ku'])
            template.extended_key_usage = ",".join(json['extensions']['sku'])
            template.inherit_crl = json['extensions']['crl']['inherit']
            template.full_crl = json['extensions']['crl']['full']
            template.freshest_crl = json['extensions']['crl']['freshest']
            template.inherit_aia = json['extensions']['aia']['inherit']
            template.aia_ocsp = json['extensions']['aia']['ocsp']
            template.aia_issuers = json['extensions']['aia']['issuers']
            template.policies = json['extensions']['policies']
            return template
        except Exception as e:
            raise e

    def to_dict(self):
    	return {"name":self.name,"dscr":self.description,\
    	"extensions":{"altname":self.alt_name,"ku":self.key_usage,\
    	"sku":self.extended_key_usage,"policies":self.policies,\
    	"crl":{"inherit":self.inherit_crl,"full":self.full_crl,\
    	"freshest":self.freshest_crl},"aia":{"inherit":self.inherit_aia,\
    	"ocsp":self.aia_ocsp,"issuers":self.aia_issuers},"keylen":self.key_length}}

    ### Method used to print the Template details
    def print_item(self):
        return show_item(self)

class CA():

    def __init__(self):
        pass

    @staticmethod
    def from_json(json):
        try:
            ca = CA()
            ca.id = str(json['id'])
            ca.name = json['name']
            ca.description = json['dscr']
            ca.subject_dn = json['subject_dn']  
            ca.expires = datetime.datetime.fromtimestamp(json['expires']).strftime('%Y-%m-%d %H:%M:%S')
            ca.cdp = json['extensions']['crl'].replace("<caid>",str(json['id']))
            ca.ocsp_url = json['extensions']['ocsp'].replace("<caid>",str(json['id']))
            ca.issuers_url = json['extensions']['issuers'].replace("<caid>",str(json['id']))            
            return ca
        except Exception as e:
            raise e

    ### Method used to print the Template details
    def print_item(self):
        return show_item(self)

class Certificate():

    status = {"1":"Active","2":"Revoked","3":"Paused","4":"Revoked"}
    reasons = {"-1":"","0":"Unspecified","1":"Key Compromise","2":"CA Compromise","3":"Affiliation Changed","4":"Superseeded","5":"Cessation of Operation","6":"Certificate Hold"}

    def __init__(self):
        pass

    @staticmethod
    def parse_items(items):
        certificates = []
        for item in items:
            certificates.append({"id":item['id'],"name":item['name'],\
                "status":Certificate.status[str(item['status'])],\
                "code":item['code'],\
                "reason":item['reason'],\
                "serial":item['serial']})
        return certificates

