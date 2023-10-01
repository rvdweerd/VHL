import clingo

def Solve_ASP(events_wp, participants_wp, participants_event, drivers_wp, wp2coord, coord2wp, all_coords, all_wp, allroutes):
    asp_program = "#const num_nodes={}.\n".format(len(all_coords))
    asp_program += "node(0..(num_nodes-1)).\n"
    #for n,c in enumerate(all_coords):
        #asp_program += "coord("+str(coord2wp[c])+","+str(c[0])+","+str(c[1])+").\n"
        #asp_program += "edge("+str(n)+","+str(e[0])+").\n"
    for segment,data in allroutes.items():
        #pass
        #asp_program += "dist("+str(segment[0])+","+str(segment[1])+","+str(data['duration']//100)+").\n"
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
#const num_timesteps=2.
timestep(1..2).
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
:- picked_up(N), N != num_participants.

% EACH DRIVER CAN ONLY PICK UP A MAXIUM OF 3
picked_up(D,N) :- N = #count{ ID : pickup(D,_,ID)}, driver(D).
:- picked_up(D,N), driver(D), N>3.

% EACH PASSENGER MUST HAVE THE SAME DESTINATION
targets(D,E) :- pickup(D,_,P), participant(P,_,E).
:- N=#count{TGT : targets(D,TGT)}, driver(D), N>1.

% ACCOUNT FOR TRAVEL DISTANCES PER DRIVER
distances(D,0,KM) :- driver(D), pickup(D,1,P), driver(D,SRC), participant(P,TGT,E), dist(SRC,TGT,KM).
distances(D,T1,KM) :- driver(D), pickup(D,T1,P1), pickup(D,T2,P2), (T2-T1)==1, participant(P1,SRC,E), participant(P2,TGT,E), dist(SRC,TGT,KM).
max_t(D,T) :- T = #max{ TT : pickup(D,TT,_) }, driver(D).
distances(D,TMAX,KM) :- max_t(D,TMAX), driver(D), pickup(D,TMAX,P), participant(P,SRC,EVT), event(EVT,TGT), dist(SRC,TGT,KM).

distances(KM) :- KM = #sum{ K,D,T : distances(D,T,K)}. %, driver(D), timestep(T)}.
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
