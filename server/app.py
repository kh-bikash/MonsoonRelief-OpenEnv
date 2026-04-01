import uvicorn
from fastapi import FastAPI
from app.models import Action
from app.env import MonsoonEnv
from app.tasks import get_task_1_state

app = FastAPI()
# Using task 1 as default for the endpoints
env = MonsoonEnv(get_task_1_state())

@app.get("/")
def ping():
    return {"status": "ok"}

@app.post("/reset")
def reset():
    obs = env.reset()
    return obs.model_dump()

@app.get("/state")
def state():
    obs = env.state()
    return obs.model_dump()

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.model_dump(),
        "reward": reward,
        "done": done,
        "info": info
    }

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
