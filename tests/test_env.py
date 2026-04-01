from app.env import MonsoonEnv
from app.tasks import get_task_2_state
from app.models import Action, ResourceCount

def test_environment_step():
    state = get_task_2_state()
    env = MonsoonEnv(state)
    
    action = Action(
        prioritized_zones=["Z2-East"],
        resource_allocations={"Z2-East": ResourceCount(boats=5, ambulances=2)},
        evacuation_dispatches=["Z2-East"]
    )
    
    next_state, reward, done, info = env.step(action)
    
    assert next_state.step_count == 1
    assert next_state.rescued_count > 0
    assert next_state.unallocated_resources.boats == 5
