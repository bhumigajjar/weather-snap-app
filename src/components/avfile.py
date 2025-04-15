import requests

url = "https://otx.alienvault.com//api/v1/pulses/my"

payload = "<taxii_11:Discovery_Request\nxmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\nxmlns:taxii=\"http://taxii.mitre.org/messages/taxii_xml_binding-1\" \nxmlns:taxii_11=\"http://taxii.mitre.org/messages/taxii_xml_binding-1.1\" \nxmlns:tdq=\"http://taxii.mitre.org/query/taxii_default_query-1\"\nxsi:schemaLocation=\"http://taxii.mitre.org/messages/taxii_xml_binding-1.1\" \nmessage_id=\"5267020880072015457\"/>"
headers = {
  'Content-Type': 'application/xml',
  'User-Agent': 'libtaxii.httpclient',
  'x-taxii-accept': 'urn:taxii.mitre.org:message:xml:1.1',
  'x-taxii-content-type': 'urn:taxii.mitre.org:message:xml:1.1',
  'x-taxii-protocol': 'urn:taxii.mitre.org:protocol:https:1.0',
  'x-taxii-services': 'urn:taxii.mitre.org:services:1.1',
  'Accept': 'application/xml',
  'Content-Type': 'application/xml',
  'Authorization': '••••••'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
