import codecs
import json
import subprocess

ip="192.168.147.149"

import sys
from heapq import heapify, heappush, heappop
import requests
import os


def dijsktra(graph, src, dest):
    inf = sys.maxsize
    node = {'1':{'cost':inf,'pred':[]},
                 '2':{'cost':inf,'pred':[]},
                 '4': {'cost': inf, 'pred': []},
                 '5': {'cost': inf, 'pred': []},
                 '8': {'cost': inf, 'pred': []},
                 '3': {'cost': inf, 'pred': []},
                 '7': {'cost': inf, 'pred': []},
                 'a': {'cost': inf, 'pred': []},
                 '6': {'cost': inf, 'pred': []},
                 '9': {'cost': inf, 'pred': []}
                 }
    node[src]['cost'] = 0
    visited = []
    temp = src
    for i in range(5):
        if temp not in visited:
            visited.append(temp)
            min_heap = []
            for j in graph[temp]:
                if j not in visited:
                    cost = node[temp]['cost'] + graph[temp][j]
                    if cost<node[j]['cost']:
                        node[j]['cost'] = cost
                        node[j]['pred'] = node[temp]['pred'] + list(temp)
                    heappush(min_heap,(node[j]['cost'],j))
        heapify(min_heap)
        temp = min_heap[0][1]
    print("Dystans: " + str(node[dest]['cost']))
    print("Sciezka: " + str(node[dest]['pred'] + list(dest)))
    return node[dest]['pred'] + list(dest)

def createJSON(IN, OUT, SWITCH, DST):
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
    routing["deviceId"] = "of:000000000000000" + str(SWITCH)
    routing["selector"]["criteria"][0]["port"] = IN;
    routing["treatment"]["instructions"][0]["port"] = OUT;
    routing["selector"]["criteria"][2]["ip"] = "10.0.0." + str(DST)+"/32";
#    headers = {'content-type': 'application/json', "Accept": "application/json"}
#    r = requests.post('http://' + ip + ':8181/onos/v1/flows/of:000000000000000' + str(SWITCH), auth=('onos', 'rocks'), json=routing, headers=headers)
    filename = str(int(SWITCH))+str(int(IN))+str(int(OUT))+".json"
    with open(filename, 'wb') as f:
        json.dump(routing, codecs.getwriter('utf-8')(f), ensure_ascii=False)
    file_object = open('set.bat', 'a')
    # Append 'hello' at the end of file
    file_object.write('curl --user onos:rocks -X POST "http://'+ip+':8181/onos/v1/flows/of:000000000000000'+str(SWITCH)+'" -d @'+filename+' -H "Content-Type: application/json" -H "Accept: application/json"\n')
    # Close the file
    file_object.close()

def count(source, destination):
    graph = {
        '1': {'a': 10.2, '9': 8.7, '2': 14.6, '5': 15.55, '8': 15.1, '4': 7},
        '2': {'3': 13.55, '9': 16.75, '4': 14, '1': 14.6},
        '4': {'3': 10.75, '1': 7, '2': 14},
        '5': {'7': 11.9, '8': 6.9, '3': 9.1, '1': 15.55},
        '8': {'6': 8.35, '7': 12.95, '5': 6.9, '1': 15.1},
        '3': {'5': 9.1, '7': 19.65, '4': 10.75, '2': 13.55},
        '7': {'6': 18.4, '8': 12.95, '5': 6.9, '3': 19.65},
        'a': {'9': 16.3, '6': 21.5, '1': 10.2},
        '9': {'1': 8.7, '2': 16.75, 'a': 16.3},
        '6': {'7': 18.4, '8': 8.35, 'a': 21.5}
    }
    d = dijsktra(graph, source, destination)
    l = []
    for i in range(0, len(d) - 1):
        r = requests.get(
            "http://" + ip + ":8181/onos/v1/links?device=of:000000000000000" + str(d[i]) + "&direction=EGRESS",
            auth=("onos", "rocks"))
        r2 = requests.get(
            "http://" + ip + ":8181/onos/v1/links?device=of:000000000000000" + str(d[i + 1]) + "&direction=EGRESS",
            auth=("onos", "rocks"))
        print(r.json())

        #createJSON(1, int(d[i]), int(d[i]), destination)

        for j in r.json()['links']:

            for k in r2.json()['links']:
                if (j["dst"]['device'] == k['src']['device'] and j['src']['port'] == k['src']['port']):
                    print("DST: " + str(k["src"]))
                    print("SRC: " + str(j["dst"]))
                    l.append(k['src']['port'])
                    l.append(j['dst']['port'])
    createJSON(1, l[0], d[0], destination)
    createJSON(l[0], 1, d[0], source)
    print(d)
    print(l)
    for n in range(1, len(d)-1):
        createJSON(l[2*n-1], l[2*n], d[n], destination)




# createJSON(1, 1, 1, 6)
if __name__ == "__main__":
    try:
        os.remove("set.bat")
    except:
        print("Nie znaleziono set.bat")
    source = input("Podaj host zrodlowy: ")
    destination = input("Podaj host docelowy: ")
    count(source, destination)
    count(destination, source)

