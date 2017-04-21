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

            # Initializing config
            config = ConfigParser.RawConfigParser()
            config.read(file)

            # Initializing template
            template = CertificateTemplate()
            # Getting name and description
            template.name = config.get("general","name")
            template.description = config.get("general","dscr")
            	        
	        # Getting extensions
            template.extensions['keylen'] = config.get("keylen","length")
            template.extensions['altname'] = config.get("general","alt")
            value = config.get("key_usages","key_usage")
            template.extensions['ku'] = ([] if value == "" else value.split(","))
            value = config.get("key_usages","ext_key_usage")
            template.extensions['sku'] = ([] if value == "" else value.split(","))
            value = config.get("policy","policies")
            template.extensions['policies'] = ([] if value == "" else value.split(","))
            template.extensions['altname'] = config.get("general","alt")
            template.extensions['crl']['inherit'] = config.get("crl","inherit")
            template.extensions['crl']['full'] = config.get("crl","full")
            template.extensions['crl']['freshest'] = config.get("crl","freshest")
            template.extensions['aia']['inherit'] = config.get("aia","inherit")
            template.extensions['aia']['ocsp'] = config.get("aia","ocsp")
            template.extensions['aia']['issuers'] = config.get("aia","issuers")
            return template
        except Exception as e:
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

    def to_dict(self):
    	return {"name":self.name,"dscr":self.description,\
    	"extensions":{"altname":self.alt_name,"ku":self.key_usage,\
    	"sku":self.extended_key_usage,"policies":self.policies,\
    	"crl":{"inherit":self.inherit_crl,"full":self.full_crl,\
    	"freshest":self.freshest_crl},"aia":{"inherit":self.inherit_aia,\
    	"ocsp":self.aia_ocsp,"issuers":self.aia_issuers},"keylen":self.key_length}}