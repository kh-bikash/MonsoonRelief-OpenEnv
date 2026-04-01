from app.models import State, Zone, Shelter, ResourceCount

def get_task_1_state() -> State:
    return State(
        zones=[
            Zone(zone_id="Z1-North", water_level_m=0.5, stranded_population=100, elderly_count=10, child_count=20, medical_emergencies=0, roads_blocked=False),
            Zone(zone_id="Z2-East", water_level_m=3.5, stranded_population=400, elderly_count=50, child_count=100, medical_emergencies=15, roads_blocked=True),
            Zone(zone_id="Z3-South", water_level_m=1.2, stranded_population=50, elderly_count=5, child_count=5, medical_emergencies=2, roads_blocked=False)
        ],
        shelters=[],
        unallocated_resources=ResourceCount()
    )

def get_task_2_state() -> State:
    s = get_task_1_state()
    s.unallocated_resources = ResourceCount(boats=10, trucks=5, ambulances=3, volunteers=50)
    return s

def get_task_3_state() -> State:
    s = get_task_2_state()
    s.shelters = [
        Shelter(shelter_id="S1-HighSchool", capacity=500),
        Shelter(shelter_id="S2-Stadium", capacity=2000)
    ]
    return s
