from app.models import State, Action
from typing import List

def grade_task_1_easy(action: Action, initial_state: State) -> float:
    if not action.prioritized_zones:
        return 0.0
    
    zones_sorted = sorted(initial_state.zones, key=lambda z: z.urgency_score, reverse=True)
    truth_ids = [z.zone_id for z in zones_sorted]
    
    score = 0.0
    max_score = len(truth_ids)
    
    for i, predicted_id in enumerate(action.prioritized_zones):
        if predicted_id in truth_ids:
            true_idx = truth_ids.index(predicted_id)
            distance = abs(true_idx - i)
            score += max(0, 1.0 - (distance / max_score))
            
    return round(score / max_score, 2) if truth_ids else 0.0

def grade_task_2_medium(action: Action, initial_state: State) -> float:
    score = 0.0
    allocations = action.resource_allocations
    if not allocations:
        return 0.0
        
    zones = {z.zone_id: z for z in initial_state.zones}
    total_boats_allocated = sum(a.boats for a in allocations.values())
    total_amb_allocated = sum(a.ambulances for a in allocations.values())
    
    if total_boats_allocated > initial_state.unallocated_resources.boats:
        return 0.0
        
    for zid, alloc in allocations.items():
        target_zone = zones.get(zid)
        if target_zone:
            if alloc.ambulances > 0 and target_zone.medical_emergencies > 0:
                score += 0.4
            if alloc.boats > 0 and target_zone.water_level_m >= 2.0:
                score += 0.3 
            
    return min(1.0, score)

def grade_task_3_hard(action: Action, initial_state: State) -> float:
    score = 0.0
    
    if action.open_shelters:
        score += 0.2
        
    if action.evacuation_dispatches:
        score += 0.2
        
    if action.resource_allocations:
        score += 0.2
        
    plan = action.plan.lower()
    keywords = ["evacuate", "priority", "medical", "shelter", "boat", "ambulance"]
    found = sum(1 for kw in keywords if kw in plan)
    score += min(0.4, found * 0.1)
    
    return min(1.0, round(score, 2))
