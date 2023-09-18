
from optimutils import Solve_ASP
from genutils import GetInput, extract_quoted_string, GetInput_addr, PrintRoutes
from routeutils import GetCoordinates, GetRoutingData
from itertools import permutations
import time


fname="input3.txt"
events_wp, participants_wp, participants_event, drivers_wp, wp2coord, coord2wp, all_coords, all_wp, wp2addr = GetInput_addr(fname)

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
    entry=GetRoutingData(route)
    time.sleep(pausetime)
    allroutes[wps]=entry
    print("fro",wp2addr[wps[0]],"to",wp2addr[wps[1]],"waypoints",wps, "coords", route, "duration [s]",entry['duration'],"duration [min]",entry['duration']//60)

solutions = Solve_ASP(events_wp, participants_wp, participants_event, drivers_wp, wp2coord, coord2wp, all_coords, all_wp, allroutes)

routes={}
for d, wp in drivers_wp.items():
    routes[d]=[wp]

driver_destinations={}
for segment in solutions:
    segment = segment.replace('pickup(', '').replace(')', '')
    segment = segment.split(',')
    driver = int(segment[0])
    timestep = int(segment[1])
    participant = int(segment[2])
    driver_destinations[driver] = participants_event[participant]
    print("Driver {} picks up participant {} at timestep {}".format(driver+1, participant+1, timestep))
    routes[driver].append(participants_wp[participant])

for d, e in driver_destinations.items():
    routes[d].append(events_wp[e])

from routeutils import BuildRoute
m=BuildRoute(routes, allroutes)
m.save("test.html")
PrintRoutes(all_coords, wp2coord, routes)

