
from optimutils import Solve_ASP
from genutils import GetInput, extract_quoted_string, GetInput_addr, PrintRoutes
from routeutils import GetCoordinates, GetRoutingData
from itertools import permutations
import time
import os
import pickle
import time 

fname="input3.txt"


datapath="data.bin"
cache_data=None
if os.path.exists(datapath):
    #reload object from file
    loadfile = open(r'data.bin', 'rb')
    cache_data = pickle.load(loadfile)
    loadfile.close()
else:
    cache_data = {'address2coord':{}, 'routes':{}}
events_wp, participants_wp, participants_event, drivers_wp, wp2coord, coord2wp, all_coords, all_wp, wp2addr = GetInput_addr(fname, cache_data)

perm=permutations(all_wp,2)
allroutes={}
permlist=list(perm)
num_requests=len(permlist)
if num_requests > 40:
    pausetime=60/40
else:
    pausetime=0.1

for wps in permlist:
    #print(i)
    route=(wp2coord[wps[0]],wp2coord[wps[1]])
    if route in cache_data['routes']:
        entry = cache_data['routes'][route]
    else:
        entry=GetRoutingData(route)
        cache_data['routes'][route] = entry
        time.sleep(pausetime) # due to rate limit of route service
        print("fro",wp2addr[wps[0]],"to",wp2addr[wps[1]],"waypoints",wps, "coords", route, "duration [s]",entry['duration'],"duration [min]",entry['duration']//60)
    allroutes[wps]=entry

savefile = open(r'data.bin', 'wb')
pickle.dump(cache_data, savefile)
savefile.close()

start_time = time.time()
solutions = Solve_ASP(events_wp, participants_wp, participants_event, drivers_wp, wp2coord, coord2wp, all_coords, all_wp, allroutes)
end_time = time.time()
print('Execution time: ', end_time-start_time, 'seconds')

routes={}
for d, wp in drivers_wp.items():
    routes[d]=[wp]

driver_destinations={}
#driver_times=[0 for i in range(len(drivers_wp))]
for segment in solutions:
    segment = segment.replace('pickup(', '').replace(')', '')
    segment = segment.split(',')
    driver = int(segment[0])
    timestep = int(segment[1])
    participant = int(segment[2])
    driver_destinations[driver] = participants_event[participant]
    print("Driver {} picks up participant {} at timestep {}".format(driver+1, participant+1, timestep))
    if len(routes[driver]) < timestep+1:
        routes[driver]  += [0]*((timestep+1)-len(routes[driver]))
    routes[driver][timestep] = participants_wp[participant]

for d, e in driver_destinations.items():
    routes[d].append(events_wp[e])
for route in routes.keys():
    if len(routes[route]) == 1:
        print("Driver {} does not drive".format(route+1))

from routeutils import BuildRoute
m=BuildRoute(routes, allroutes, wp2coord)
m.save("test.html")
PrintRoutes(all_coords, wp2coord, routes)

