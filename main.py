import json
import requests

import pycurl
from urllib.parse import urlencode

if __name__ == '__main__':
    routing = {
        "priority": 40000,
        "timeout": 0,
        "isPermanent": True,
        "deviceId": "of:0000000000000003",
        "treatment": {
            "instructions": [
                {
                    "type": "OUTPUT",
                    "port": "5"
                }
            ]
        },
        "selector": {
            "criteria": [
                {
                    "type": "IN_PORT",
                    "port": "1"
                },
                {
                    "type": "ETH_TYPE",
                    "ethType": "0x0800"
                },
                {
                    "type": "IPV4_DST",
                    "ip": "10.0.0.6/32"
                }
            ]
        }
    }
    routing["deviceId"] = "of:000000000000000" + str(3)
    routing["selector"]["criteria"][0]["port"] = 1;
    routing["treatment"]["instructions"][0]["port"] = 3;
    routing["selector"]["criteria"][2]["ip"] = "10.0.0." + str(6);
    # print(routing)


    c = pycurl.Curl()
    # initializing the request URL
    c.setopt(c.URL, 'http://192.168.147.164:8181/onos/v1/flows/of:0000000000000003')
    # the data that we need to Post
    post_data = {'field': 'value'}
    # encoding the string to be used as a query
    postfields = urlencode(routing)
    # setting the cURL for POST operation
    c.setopt(c.POSTFIELDS, postfields)
    # perform file transfer
    c.perform()
    # Ending the session and freeing the resources
    c.close()

    headers = {'content-type': 'application/json', "Accept": "application/json"}
    requests.post('http://192.168.147.164:8181/onos/v1/flows/of:0000000000000003', auth=('onos', 'rocks'), data=json.dumps(routing), headers=headers)

