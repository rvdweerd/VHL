import matplotlib.pyplot as plt
import clingo
colors=['red','blue','orange','green']

def GetInput():

    # Create an empty dictionary to store the coordinates
    events_wp = {}
    participants_wp = {}
    participants_event = {}
    drivers_wp = {}
    all_coords = set()
    all_wp = set()
    wp2coord = {}
    coord2wp = {}

    # Open the text file for reading
    with open('input2.txt', 'r') as file:
        # Read each line from the file
        for line in file:
            if line.startswith('#') or line.startswith('\n'):
                continue
            parts = line.split()
            
            if parts[0] == "EVENT":
                event_num = int(parts[1])-1
                coord = parts[3].replace('(', '').replace(')', '')
                coord = coord.split(',')
                x = int(coord[0])  
                y = int(coord[1])  
                event_coord = (x,y)
                if event_coord in all_coords:
                    events_wp[event_num] = coord2wp[event_coord]
                else:
                    events_wp[event_num] = len(all_coords)
                    all_coords.add(event_coord)
                    wp2coord[len(all_coords)-1] = event_coord
                    coord2wp[event_coord] = len(all_coords)-1
                    all_wp.add(len(all_coords)-1)
                    all_coords.add((x,y))

            if parts[0] == "PARTICIPANT":  
                part_num = int(parts[1])-1
                coord = parts[2].replace('(', '').replace(')', '')
                coord = coord.split(',')
                x = int(coord[0])  
                y = int(coord[1])  
                part_coord = (x,y)
                eventnr = int(parts[3])-1
                participants_event[part_num] = eventnr
                if part_coord in all_coords:
                    participants_wp[part_num] = coord2wp[part_coord]
                else:  
                    participants_wp[part_num] = len(all_coords)
                    all_coords.add(part_coord)
                    wp2coord[len(all_coords)-1] = part_coord
                    coord2wp[part_coord] = len(all_coords)-1
                    all_wp.add(len(all_coords)-1)
                    all_coords.add((x,y))
            
            if parts[0] == "DRIVER":  
                driver_num = int(parts[1])-1
                coord = parts[2].replace('(', '').replace(')', '')
                coord = coord.split(',')
                x = int(coord[0])  
                y = int(coord[1])  
                driver_coord = (x,y)
                if driver_coord in all_coords:
                    drivers_wp[driver_num] = coord2wp[driver_coord]
                else:
                    drivers_wp[driver_num] = len(all_coords)
                    all_coords.add(driver_coord)
                    wp2coord[len(all_coords)-1] = driver_coord
                    coord2wp[driver_coord] = len(all_coords)-1
                    all_wp.add(len(all_coords)-1)
                    all_coords.add((x,y))

    # Print the dictionary
    return events_wp, participants_wp, participants_event, drivers_wp, wp2coord, coord2wp, list(all_coords), list(all_wp)
import re
def extract_quoted_string(input_string):
    # Define a regular expression pattern to match strings between double or single quotes
    pattern = r'"([^"]*)"|\'([^\']*)\''
    
    # Use re.findall to find all matching substrings
    matches = re.findall(pattern, input_string)
    
    # Extract and return the first match (if any)
    if matches:
        return matches[0][0] or matches[0][1]
    else:
        return None

from routeutils import GetCoordinates

def GetInput_addr():

    # Create an empty dictionary to store the coordinates
    events_wp = {}
    participants_wp = {}
    participants_event = {}
    drivers_wp = {}
    all_coords = set()
    all_wp = set()
    wp2coord = {}
    coord2wp = {}

    # Open the text file for reading
    with open('input2.txt', 'r') as file:
        # Read each line from the file
        for line in file:
            if line.startswith('#') or line.startswith('\n'):
                continue
            address = extract_quoted_string(line)
            coord = GetCoordinates(address)
            line=line.replace(address,"")
            line = line.replace("''","")
            parts = line.split()
            
            if parts[0] == "EVENT":
                event_num = int(parts[1])-1
                #coord = parts[3].replace('(', '').replace(')', '')
                #coord = coord.split(',')
                x = float(coord[0])
                y = float(coord[1])
                event_coord = (x,y)
                if event_coord in all_coords:
                    events_wp[event_num] = coord2wp[event_coord]
                else:
                    events_wp[event_num] = len(all_coords)
                    all_coords.add(event_coord)
                    wp2coord[len(all_coords)-1] = event_coord
                    coord2wp[event_coord] = len(all_coords)-1
                    all_wp.add(len(all_coords)-1)
                    all_coords.add((x,y))

            if parts[0] == "PARTICIPANT":  
                part_num = int(parts[1])-1
                #coord = parts[2].replace('(', '').replace(')', '')
                #coord = coord.split(',')
                x = float(coord[0])  
                y = float(coord[1])  
                part_coord = (x,y)
                eventnr = int(parts[3])-1
                participants_event[part_num] = eventnr
                if part_coord in all_coords:
                    participants_wp[part_num] = coord2wp[part_coord]
                else:  
                    participants_wp[part_num] = len(all_coords)
                    all_coords.add(part_coord)
                    wp2coord[len(all_coords)-1] = part_coord
                    coord2wp[part_coord] = len(all_coords)-1
                    all_wp.add(len(all_coords)-1)
                    all_coords.add((x,y))
            
            if parts[0] == "DRIVER":  
                driver_num = int(parts[1])-1
                #coord = parts[2].replace('(', '').replace(')', '')
                #coord = coord.split(',')
                x = float(coord[0])  
                y = float(coord[1])  
                driver_coord = (x,y)
                if driver_coord in all_coords:
                    drivers_wp[driver_num] = coord2wp[driver_coord]
                else:
                    drivers_wp[driver_num] = len(all_coords)
                    all_coords.add(driver_coord)
                    wp2coord[len(all_coords)-1] = driver_coord
                    coord2wp[driver_coord] = len(all_coords)-1
                    all_wp.add(len(all_coords)-1)
                    all_coords.add((x,y))

    # Print the dictionary
    return events_wp, participants_wp, participants_event, drivers_wp, wp2coord, coord2wp, list(all_coords), list(all_wp)


def PrintRoutes(all_coords, wp2coord, routes):
    #routes={}
    #routes[1]=[7,3,4,0]
    #routes[2]=[6,2,5,1]

    fig, ax = plt.subplots()
    # Plot every possible connection in light grey
    for i in range(len(all_coords)):
        for j in range(i + 1, len(all_coords)):
            x1, y1 = all_coords[i]
            x2, y2 = all_coords[j]
            ax.plot([x1, x2], [y1, y2], color='lightgrey', linewidth=0.5)

    for car, route in routes.items():
            route_c = [wp2coord[i] for i in route]  # Convert waypoint numbers to coordinates
            route_x, route_y = zip(*route_c)  # Split coordinates into x and y
            ax.plot(route_x, route_y, label=car, color=colors[car%len(colors)], linewidth=2)

    # Plot the waypoints as blue dots
    #for waypoint in waypoints:
    #    ax.plot(waypoint[0], waypoint[1], 'ro')

    # Set axis limits
    ax.set_xlim(min(x for x, y in all_coords) - 1, max(x for x, y in all_coords) + 1)
    ax.set_ylim(min(y for x, y in all_coords) - 1, max(y for x, y in all_coords) + 1)

    ax.set_xlabel("X-coordinate")
    ax.set_ylabel("Y-coordinate")
    ax.set_title("Routes of Different Cars to Waypoints")
    ax.legend()


    # Show the plot
    plt.show()

def Solve_ASP(events_wp, participants_wp, participants_event, drivers_wp, wp2coord, coord2wp, all_coords, all_wp, allroutes):
    asp_program = "#const num_nodes={}.\n".format(len(all_coords))
    asp_program += "node(0..(num_nodes-1)).\n"
    #for n,c in enumerate(all_coords):
        #asp_program += "coord("+str(coord2wp[c])+","+str(c[0])+","+str(c[1])+").\n"
        #asp_program += "edge("+str(n)+","+str(e[0])+").\n"
    for segment,data in allroutes.items():
        #pass
        asp_program += "dist("+str(segment[0])+","+str(segment[1])+","+str(data['duration'])+").\n"
    asp_program += """
\n"""
    #asp_program += """
#dist(N1,N2,X) :- node(N1), node(N2), N1!=N2, coord(N1,AX,AY), coord(N2,BX,BY), X=(BX-AX)**2+(BY-AY)**2.
#sdist(N1,N2,X) :- dist(N1,N2,X), node(N1), node(N2), N2>N1.\n\n"""

    asp_program += "#const num_events={}.\n".format(len(events_wp))
    asp_program += "event(0..(num_events-1)).\n"
    for n,c in events_wp.items():
        asp_program += "event("+str(n)+","+str(c)+").\n"

    asp_program += "\n#const num_participants={}.\n".format(len(participants_wp))
    asp_program += "participant(0..(num_participants-1)).\n"
    for n,c in participants_wp.items():
        asp_program += "participant("+str(n)+","+str(c)+","+str(participants_event[n])+").\n"

    asp_program += "\n#const num_drivers={}.\n".format(len(drivers_wp))
    asp_program += "driver(0..(num_drivers-1)).\n"
    for n,c in drivers_wp.items():
        asp_program += "driver("+str(n)+","+str(c)+").\n"
    
    asp_program += """
% GENERATE PICKUP(driverID, T, participantID)
#const num_timesteps=4.
timestep(1..4).
%1{ pickup(1..D, 1..T, 1..P) : driver(D), timestep(T), participant(P) }num_participants .%: driver(D).%, timestep(T).
{pickup(D, T, P) : driver(D), timestep(T), participant(P)}.

% DIFFERENT DRIVERS CANNOT PICKUP THE SAME PARTICIPANT
:- pickup(D1,_,X), pickup(D2,_,X), driver(D1), driver(D2), participant(X), D1!=D2.

% SAME DRIVER CANNOT PICKUP SAME PARTICIPANT TWICE
:- pickup(D,T1,X), pickup(D,T2,X), driver(D), timestep(T1), timestep(T2), participant(X), T1!=T2.

% SAME DRIVER CANNOT HAVE SAME TIMESTAMPS
:- pickup(D,T1,X1), pickup(D,T2,X2), driver(D), timestep(T1), timestep(T2), participant(X1), participant(X2), T1==T2, X1!=X2.

% EACH DRIVER STARTS AT TIMESTEP 1
:- not pickup(D,1,_), pickup(D,T,X).

% PICKUP TIMES MUST BE CONSECUTIVE FOR EACH DRIVER
:- pickup(D,T1,_), pickup(D,T2,_), T2-T1>1, not pickup(D,T1+1,_).

% ALL PARTICIPANTS MUST BE PICKED UP
picked_up(N) :- N = #count{ ID : pickup(_,_,ID) }.
:- picked_up(N), N<num_participants.

% EACH DRIVER CAN ONLY PICK UP A MAXIUM OF 3
picked_up(D,N) :- N = #count{ ID : pickup(D,_,ID)}, driver(D).
:- picked_up(D,N), driver(D), N>3.

% EACH PASSENGER MUST HAVE THE SAME DESTINATION
targets(D,E) :- pickup(D,_,P), participant(P,_,E).
:- N=#count{TGT : targets(D,TGT)}, driver(D), N>1.

% ACCOUNT FOR TRAVEL DISTANCES PER DRIVER
distances(D,0,KM) :- driver(D), pickup(D,1,P), driver(D,SRC), participant(P,TGT,E), dist(SRC,TGT,KM).
distances(D,T1,KM) :- driver(D), pickup(D,T1,P1), pickup(D,T2,P2), T2-T1=1, participant(P1,SRC,E), participant(P2,TGT,E), dist(SRC,TGT,KM).
max_t(D,T) :- T = #max{ TT : pickup(D,TT,_) }, driver(D).
distances(D,TMAX,KM) :- max_t(D,TMAX), driver(D), pickup(D,TMAX,P), participant(P,SRC,EVT), event(EVT,TGT), dist(SRC,TGT,KM).

%distances_per_driver(D,KM) :- KM = #sum{ K : distances(D,_,K)}, driver(D).
distances(KM) :- KM = #sum{ K,D : distances(D,_,K), driver(D)}.
%total_distance(KM) :- KM = #sum{ K,D : distances_per_driver(D,K)}, driver(D).

#minimize {KM : distances(KM)}.
#show pickup/3."""    
    # control = clingo.Control()
    # control.add("base", [], asp_program)
    # control.ground([("base", [])])
    # control.configuration.solve.models = 0
    # solutions=[]
    # with control.solve(yield_ = True) as handle:
    #     for model in handle:
    #         solution = []
    #         for atom in model.symbols(shown = True):
    #             if atom.name == "choose":
    #                 solution.append(atom.arguments[0].number)
    #         print("Solution: \n")
    #         print(solution)
    #         solutions.append(solution)
    #         #yield(solution)
    # return solutions
    print(asp_program)
    control = clingo.Control()
    control.add("base", [], asp_program)
    control.ground([("base", [])])
    # Define a function that will be called when an answer set is found
    # This function sorts the answer set alphabetically, and prints it
    solutions=[]
    def on_model(model):
        if model.optimality_proven == True:
            sorted_model0 = [str(atom) for atom in model.symbols(shown=True)]
            #sorted_model = [atom.arguments[0].number if atom.name == "pickup" else "" for atom in model.symbols(shown=True)]
            #sorted_model.sort()
            solutions.append(sorted_model0)
            
            #print("Optimal answer set: {{{}}}".format(", ".join(sorted_model)))
    # Ask clingo to find all optimal models (using an upper bound of 0 gives all models)
    control.configuration.solve.opt_mode = "optN"
    control.configuration.solve.models = 0
    # Call the clingo solver, passing on the function on_model for when an answer set is found
    answer = control.solve(on_model=on_model)
    # Print a message when no answer set was found
    #if answer.satisfiable == False:
    #    print("No answer sets")
    return solutions[0]

events_wp, participants_wp, participants_event, drivers_wp, wp2coord, coord2wp, all_coords, all_wp = GetInput_addr()

from itertools import permutations
from routeutils import GetRoutingData   
perm=permutations(all_wp,2)
allroutes={}
permlist=list(perm)
num_requests=len(permlist)
if num_requests > 40:
    pausetime=60/40
else:
    pausetime=0.1

import time
for wps in permlist:
    #print(i)
    route=(wp2coord[wps[0]],wp2coord[wps[1]])
    entry=GetRoutingData(route)
    time.sleep(pausetime)
    allroutes[wps]=entry
    print(route)

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
    print("Driver {} picks up participant {} at timestep {}".format(driver, participant, timestep))
    routes[driver].append(participants_wp[participant])

for d, e in driver_destinations.items():
    routes[d].append(events_wp[e])

PrintRoutes(all_coords, wp2coord, routes)

