# Key usages
key_usages = [{"name":"Digital Signature","key":"digsign","value":"digitalSignature","dscr":""},\
              {"name":"Non-Repudiation","key":"nonrep","value":"nonRepudiation","dscr":""},\
              {"name":"Certificate signing","key":"keysign","value":"keyCertSign","dscr":""},\
              {"name":"CRL Signing","key":"crlsign","value":"cRLSign","dscr":""},\
              {"name":"Key Encipherment","key":"keyenc","value":"keyEncipherment","dscr":""},\
              {"name":"Key Agreement","key":"keyag","value":"keyAgreement","dscr":""},\
              {"name":"Encipher Only","key":"enconly","value":"encipherOnly","dscr":""},\
              {"name":"Decipher only","key":"deconly","value":"decipherOnly","dscr":""}]

# Extended Key Usages
ext_key_usages = [{"name":"Server Authentication","key":"sa","value":"serverAuth","dscr":""},\
              {"name":"Client Authentication","key":"ca","value":"clientAuth","dscr":""},\
              {"name":"Code Signing","key":"code","value":"codeSigning","dscr":""},\
              {"name":"Email Protection","key":"email","value":"emailProtection","dscr":""},\
              {"name":"Timestamping","key":"time","value":"timeStamping","dscr":""}]

# Revocation reasons
reasons = {"-1":"","0":"Unspecified","1":"Key Compromise","2":"CA Compromise","3":"Affiliation Changed","4":"Superseeded","5":"Cessation of Operation","6":"Certificate Hold"}

# HTTP codes
http_created = 201
http_ok = 200
http_forbidden = 403
http_badrequest = 400
http_notfound = 404
http_notauthorized = 401
http_internal_error = 500
http_notimplemented = 501

### Error messages
error_name_mandatory = "Name is mandatory"
error_field_mandatory = "Field is mandatory: [ %s ]"
error_file_notfound = "File [%s] not found"
error_template_init = "Error while initializing the template"


#### URLs
server_url = "http://%s:%s"
crl_prefix = "/ca/<ca_id>/crl/full"
ocsp_prefix = "/ca/<ca_id>/ocsp"
issuers_prefix = "/ca/<ca_id>/aia"