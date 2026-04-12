from app.models import State, Zone, Shelter, ResourceCount

def get_task_1_state() -> State:
    return State(
        zones=[
            Zone(zone_id="Mumbai-Dharavi-Sector4", water_level_m=2.3, stranded_population=1850, elderly_count=240, child_count=350, medical_emergencies=12, roads_blocked=True),
            Zone(zone_id="Mumbai-AndheriEast-Subway", water_level_m=3.8, stranded_population=890, elderly_count=85, child_count=120, medical_emergencies=24, roads_blocked=True),
            Zone(zone_id="Mumbai-BKC-Commercial", water_level_m=1.5, stranded_population=420, elderly_count=15, child_count=5, medical_emergencies=2, roads_blocked=False),
            Zone(zone_id="Mumbai-Juhu-Coastal", water_level_m=0.8, stranded_population=150, elderly_count=40, child_count=30, medical_emergencies=0, roads_blocked=False)
        ],
        shelters=[],
        unallocated_resources=ResourceCount()
    )

def get_task_2_state() -> State:
    s = get_task_1_state()
    # Realistic resource constraints for a major municipal response
    s.unallocated_resources = ResourceCount(boats=25, trucks=15, ambulances=8, volunteers=350)
    return s

def get_task_3_state() -> State:
    s = get_task_2_state()
    s.shelters = [
        Shelter(shelter_id="Sion-Hospital-Emergency-Wing", capacity=450),
        Shelter(shelter_id="BKC-JioGarden-Relief-Camp", capacity=3500),
        Shelter(shelter_id="Andheri-Sports-Complex", capacity=1200)
    ]
    return s
