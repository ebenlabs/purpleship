SCHEMAS=./schemas
LIB_MODULES=./dhl_germany_lib
mkdir -p $LIB_MODULES
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \;
touch "${LIB_MODULES}/__init__.py"

generateDS --no-namespace-defs -o "${LIB_MODULES}/business_interface.py" "${SCHEMAS}/geschaeftskundenversand-api-3.3.2-schema-bcs_base.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/customer_interface.py" "${SCHEMAS}/geschaeftskundenversand-api-3.3.2-schema-cis_base.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/tracking_request.py" "${SCHEMAS}/tracking-request.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/tracking_response.py" "${SCHEMAS}/tracking-response.xsd"
