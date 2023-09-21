import re
import matplotlib.pyplot as plt
from routeutils import GetCoordinates, colors
import pickle 

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

def GetInput(filename="input2.txt"):
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
    with open(filename, 'r') as file:
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

def GetInput_addr(filename="input2.txt", cache_data=None):

    # Create an empty dictionary to store the coordinates
    events_wp = {}
    participants_wp = {}
    participants_event = {}
    drivers_wp = {}
    all_coords = set()
    all_wp = set()
    wp2coord = {}
    coord2wp = {}
    wp2addr = {}
    
    # Open the text file for reading
    with open(filename, 'r') as file:
        # Read each line from the file
        for line in file:
            if line.startswith('#') or line.startswith('\n'):
                continue
            address = extract_quoted_string(line)
            if address in cache_data['address2coord']:
                coord = cache_data['address2coord'][address]
            else:                
                coord = GetCoordinates(address)
                cache_data['address2coord'][address] = coord
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
                    wp2addr[len(all_coords)-1]=address
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
                    wp2addr[len(all_coords)-1]=address
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
                    wp2addr[len(all_coords)-1]=address
                    wp2coord[len(all_coords)-1] = driver_coord
                    coord2wp[driver_coord] = len(all_coords)-1
                    all_wp.add(len(all_coords)-1)
                    all_coords.add((x,y))

    # Print the dictionary
    
    return events_wp, participants_wp, participants_event, drivers_wp, wp2coord, coord2wp, list(all_coords), list(all_wp), wp2addr

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
    ax.set_title("Simplified routes of different cars to waypoints")
    ax.legend()


    # Show the plot
    plt.show()


