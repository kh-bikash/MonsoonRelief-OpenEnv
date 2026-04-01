"""
Strongly typed Pydantic models mapping the Observation and Action spaces.
These strictly enforce OpenEnv schema validation.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class ResourceCount(BaseModel):
    """Represents deployable disaster response vehicles and personnel capacities."""
    boats: int = 0
    trucks: int = 0
    ambulances: int = 0
    volunteers: int = 0

class Zone(BaseModel):
    zone_id: str
    water_level_m: float
    stranded_population: int
    elderly_count: int
    child_count: int
    medical_emergencies: int
    roads_blocked: bool
    current_resources: ResourceCount = Field(default_factory=ResourceCount)

    @property
    def urgency_score(self) -> float:
        # Higher score means more urgent
        score = self.medical_emergencies * 10
        score += (self.elderly_count + self.child_count) * 2
        score += self.stranded_population * 0.5
        score += self.water_level_m * 5
        if self.roads_blocked:
            score += 15
        return score

class Shelter(BaseModel):
    shelter_id: str
    capacity: int
    current_occupancy: int = 0
    is_open: bool = False

class State(BaseModel):
    step_count: int = 0
    weather_severity: str = "Moderate" # Moderate, Severe, Critical
    zones: List[Zone]
    shelters: List[Shelter]
    unallocated_resources: ResourceCount
    rescued_count: int = 0
    is_done: bool = False

class Action(BaseModel):
    prioritized_zones: List[str] = Field(default_factory=list, description="List of zone IDs from most to least urgent.")
    resource_allocations: Dict[str, ResourceCount] = Field(default_factory=dict, description="Map of zone_id to resources allocated this step.")
    open_shelters: List[str] = Field(default_factory=list, description="List of shelter IDs to open.")
    evacuation_dispatches: List[str] = Field(default_factory=list, description="List of zone IDs to order evacuation.")
    plan: str = Field(default="", description="Detailed step-by-step strategy (mainly for Hard task).")
