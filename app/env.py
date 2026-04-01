"""
MonsoonRelief OpenEnv Environment
Core logic for simulating disaster-response coordination.
"""
from typing import Tuple, Dict, Any
from app.models import State, Action, ResourceCount
import copy

class MonsoonEnv:
    """
    Main Environment Class simulating a monsoon flood emergency.
    Follows the standard OpenEnv step/reset/state interface.
    """
    def __init__(self, initial_state: State):
        self.initial_state = initial_state
        self.state_data = copy.deepcopy(initial_state)

    def reset(self) -> State:
        self.state_data = copy.deepcopy(self.initial_state)
        return self.state_data

    def state(self) -> State:
        return self.state_data

    def step(self, action: Action) -> Tuple[State, float, bool, Dict[str, Any]]:
        if self.state_data.is_done:
            return self.state_data, 0.0, True, {"msg": "Episode already done."}

        reward = 0.0
        info = {}

        # 1. Process Shelter Openings
        for sid in action.open_shelters:
            for shelter in self.state_data.shelters:
                if shelter.shelter_id == sid and not shelter.is_open:
                    shelter.is_open = True
                    reward += 0.5  # Small reward for proactive opening

        # 2. Process Resource Allocations
        for zid, alloc in action.resource_allocations.items():
            avail = self.state_data.unallocated_resources
            if (alloc.boats <= avail.boats and alloc.trucks <= avail.trucks and 
                alloc.ambulances <= avail.ambulances and alloc.volunteers <= avail.volunteers):
                
                avail.boats -= alloc.boats
                avail.trucks -= alloc.trucks
                avail.ambulances -= alloc.ambulances
                avail.volunteers -= alloc.volunteers

                for z in self.state_data.zones:
                    if z.zone_id == zid:
                        z.current_resources.boats += alloc.boats
                        z.current_resources.trucks += alloc.trucks
                        z.current_resources.ambulances += alloc.ambulances
                        z.current_resources.volunteers += alloc.volunteers
            else:
                reward -= 5.0 # Penalty for requesting resources we don't have
                info["error"] = f"Insufficient resources for {zid}"

        # 3. Process Evacuations
        for zid in action.evacuation_dispatches:
            for z in self.state_data.zones:
                if z.zone_id == zid:
                    # Logic: 1 boat rescues 5 people, 1 truck 10 people (if roads not blocked)
                    rescue_capacity = z.current_resources.boats * 5
                    if not z.roads_blocked:
                        rescue_capacity += z.current_resources.trucks * 10
                    
                    actual_rescued = min(rescue_capacity, z.stranded_population)
                    z.stranded_population -= actual_rescued
                    self.state_data.rescued_count += actual_rescued
                    
                    if z.medical_emergencies > 0 and z.current_resources.ambulances > 0:
                        med_rescued = min(z.current_resources.ambulances * 2, z.medical_emergencies)
                        z.medical_emergencies -= med_rescued
                        reward += med_rescued * 10 # High reward for medical rescue
                    
                    reward += actual_rescued * 1.0

        self.state_data.step_count += 1
        
        # Environmental progression
        self.state_data.weather_severity = "Severe" if self.state_data.step_count == 1 else "Critical"
        for z in self.state_data.zones:
            if z.stranded_population > 0:
                z.water_level_m += 0.5 # Water rises
                reward -= z.stranded_population * 0.1 # Continual penalty for stranded

        if self.state_data.step_count >= 5 or sum(z.stranded_population for z in self.state_data.zones) == 0:
            self.state_data.is_done = True

        return self.state_data, reward, self.state_data.is_done, info
