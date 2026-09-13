import traci
from dataclasses import dataclass

sumo_cmd = [
    "sumo-gui",
    "-c", "sumo/config/simulation.sumocfg","--delay", "50",
    "--start",
    "--quit-on-end",
]


# get the movement of the vehicle based on its route
def get_movement(route):

    start = route[0]
    end = route[1]

    if start == "-E5":
        if end == "E8":
            return "straight"
        elif end == "E6":
            return "left"
        elif end == "E7":
            return "right"

    elif start == "-E8":
        if end == "E5":
            return "straight"
        elif end == "E7":
            return "left"
        elif end == "E6":
            return "right"

    elif start == "-E6":
        if end == "E7":
            return "straight"
        elif end == "E5":
            return "right"
        elif end == "E8":
            return "left"

    elif start == "-E7":
        if end == "E6":
            return "straight"
        elif end == "E8":
            return "right"
        elif end == "E5":
            return "left"

    return "unknown"


#---------------------------------------------------------------

#creating a dataclass to store vehicle information
@dataclass
class VehicleInfo:
    vehicle_id: str
    vehicle_type: str
    current_lane: str
    intended_edge: str
    movement: str
    signal_index: int
    signal_color: str


#---------------------------------------------------------------
#incoming lanes to consider for the simulation
incoming_lanes = [
    "-E5_0", "-E5_1", "-E5_2",
    "-E6_0", "-E6_1", "-E6_2",
    "-E8_0", "-E8_1", "-E8_2",
    "-E7_0", "-E7_1", "-E7_2"
]

#---------------------------------------------------------------


traci.start(sumo_cmd)

# --------------------------------------------------
# 1. Get signal -> movement mapping
# --------------------------------------------------

controlled_links = traci.trafficlight.getControlledLinks("J6")

#creating a dictionary to store the signal index for each movement
movement_signal = {}

#getting the signal index for each movement based on the controlled links
for signal_index, links in enumerate(controlled_links):

    for link in links:

        incoming_lane = link[0]
        outgoing_lane = link[1]

        outgoing_edge = traci.lane.getEdgeID(outgoing_lane)

        movement_signal[(incoming_lane, outgoing_edge)] = signal_index


vehicle_data = {}
previous_phase = traci.trafficlight.getPhase("J6")
phase_info={}
i=0
phase_info[f"phase{i}"]={}

waiting_time={}
waiting_time[f"phase{i}"]={}
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    current_phase = traci.trafficlight.getPhase("J6")
    
    if(previous_phase != current_phase):
        i+=1
        phase_info[f"phase{i}"]={}
        waiting_time[f"phase{i}"]={}

    else:
        vehicles=traci.vehicle.getIDList()
        for vehicle in vehicles:
            lane=traci.vehicle.getLaneID(vehicle)
            if lane not in incoming_lanes:
                continue
            route=traci.vehicle.getRoute(vehicle)
            speed=traci.vehicle.getSpeed(vehicle)
            if(speed<0.1):
                if(vehicle not in phase_info[f"phase{i}"]):
                    phase_info[f"phase{i}"][vehicle]=lane
                    waiting_time[f"phase{i}"][vehicle]=0
                waiting_time[f"phase{i}"][vehicle]+=traci.simulation.getDeltaT()      
    previous_phase=current_phase        
traci.close()
for phase in waiting_time:

    print("\n", phase)

    for vehicle in waiting_time[phase]:

        lane = phase_info[phase][vehicle]
        wait = waiting_time[phase][vehicle]

        print(
            f"Vehicle {vehicle} | "
            f"Lane {lane} | "
            f"Waiting time {wait:.1f} seconds"
        )
