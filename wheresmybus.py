import os.path
import sys
import requests

KEY = 'SVJGw4c6iT8wFnBSg4r2CapRd'

import json

'''
Method to get Bus Routes
'''
def getroutes():
    resp = requests.get('http://realtime.portauthority.org/bustime/api/v3/getroutes?key=' + KEY + '&format=json')
    routes = resp.json()['bustime-response']['routes']
    data = []
    for route in routes:
        rt = route['rt']
        rtnm = route['rtnm']
        print(rt + ', ' + rtnm)
        data.append({'rt': rt, 'rtnm': rtnm})
    f = open('allroutes.json', 'w')
    f.write(json.dumps(data, indent=4))
    f.close()
    if resp.status_code != 200:
        raise APIError('GET /tasks/ {}'.format(resp.status_code))

'''
Method to get Bus Routes with Directions
'''
def getdirections():
    if not os.path.exists('allroutes.json'):
        print('file allroutes.json does not exist')
        return
    f = open('allroutes.json', 'r')
    routes = json.load(f)
    f.close()
    data = []
    for route in routes:
        rt = route['rt']
        rtnm = route['rtnm']
        resp = requests.get('http://realtime.portauthority.org/bustime/api/v3/getdirections?key=' + KEY + '&format=json' + '&rt=' + rt + '&rtpidatafeed=Port Authority Bus')
        directions = resp.json()['bustime-response']['directions']
        for direction in directions:
            dir = direction['id']
            print(rt + ', ' + rtnm + ', ' + dir)
            data.append({'rt': rt, 'rtnm': rtnm, 'dir': dir})
    f = open('6routes.json', 'w')
    f.write(json.dumps(data, indent=4))
    f.close()
    if resp.status_code != 200:
        raise APIError('GET /tasks/ {}'.format(resp.status_code))

'''
Method to get Bus Stops along routeID in direction
'''
def getstops(routeID, direction):
    if not os.path.exists('6routes.json'):
        print('file 6routes.json does not exist')
        return
    f = open('6routes.json', 'r')
    routes = json.load(f)
    f.close()
    data = []
    for route in routes:
        rt = route['rt']
        rtnm = route['rtnm']
        dir = route['dir']
        if (rt == routeID and dir == direction):
            resp = requests.get('http://realtime.portauthority.org/bustime/api/v3/getstops?key=' + KEY + '&format=json' + '&rt=' + rt + '&dir=' + dir + '&rtpidatafeed=Port Authority Bus')
            stops = resp.json()['bustime-response']['stops']
            stop_data = []
            for stop in stops:
                stpid = stop['stpid']
                stpnm = stop['stpnm']
                print(stpid + ', ' + stpnm)
                stop_data.append({'stpid': stpid, 'stpnm': stpnm})
            data.append({'rt': rt, 'dir': dir, 'stops': stop_data})
    if len(data) == 0:
        print('invalid route/direction combination: ' + routeID + '/' + direction)
    else:
        f = open('mystops.json', 'w')
        f.write(json.dumps(data, indent=4))
        f.close()
    if resp.status_code != 200:
        raise APIError('GET /tasks/ {}'.format(resp.status_code))

'''
Method to get Bus Arrivals at stopID
'''
def getarrivals(stopID):
    if not os.path.exists('6routes.json'):
        print('file 6routes.json does not exist')
        return
    f = open('6routes.json', 'r')
    routes = json.load(f)
    f.close()
    resp = requests.get('http://realtime.portauthority.org/bustime/api/v3/getpredictions?key=' + KEY + '&format=json' + '&stpid=' + stopID + '&rtpidatafeed=Port Authority Bus')
    arrivals = resp.json()['bustime-response']['prd']
    data = []
    for arrival in arrivals:
        rt = arrival['rt']
        rtnm = 'TBD'
        rtdir = arrival['rtdir']
        stpid = arrival['stpid']
        stopnm = arrival['stpnm']
        timstmp = arrival['tmstmp']
        for route in routes:
            if rt == route['rt']:
                rtnm = route['rtnm']
        print(rt + ', ' + rtnm + ', ' + rtdir + ', ' + stpid + ', ' + stopnm + ', ' + timstmp)
        data.append({'rt': rt, 'rtnm': rtnm, 'rtdir': rtdir, 'stpid': stpid, 'stopnm': stopnm, 'timstmp': timstmp}) 
    f = open('myarrivals.json', 'w')
    f.write(json.dumps(data, indent=4))
    f.close()
def getpredictions():
    pass

'''
Main Program Execution
'''
if len(sys.argv) >= 2:
    if (sys.argv[1] == 'getroutes'):
        getroutes()
    elif (sys.argv[1] == 'getdirections'):
        getdirections()
    elif (sys.argv[1] == 'getstops'):
        if (len(sys.argv) == 4):
            rt = sys.argv[2]
            dir = sys.argv[3]
            getstops(rt, dir)
        else:
            print("Invalid parameters for getstops")
            print("wheresmybus.py getstops routeID direction")
    elif (sys.argv[1] == 'getarrivals'):
        if (len(sys.argv) == 3):
            stpid = sys.argv[2]
            getarrivals(stpid)
        else:
            print("Invalid parameters for getarrivals")
            print("wheresmybus.py getarrivals stopID")
