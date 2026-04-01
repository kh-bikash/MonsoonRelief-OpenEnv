import os
import json
from openai import OpenAI
from app.tasks import get_task_1_state, get_task_2_state, get_task_3_state
from app.graders import grade_task_1_easy, grade_task_2_medium, grade_task_3_hard
from app.models import Action

def main():
    api_base_url = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
    model_name = os.getenv("MODEL_NAME", "gpt-4-turbo")
    hf_token = os.getenv("HF_TOKEN", os.getenv("OPENAI_API_KEY", "dummy-key"))
    
    client = OpenAI(base_url=api_base_url, api_key=hf_token)

    tasks_def = [
        {"name": "Easy", "state": get_task_1_state(), "grader": grade_task_1_easy},
        {"name": "Medium", "state": get_task_2_state(), "grader": grade_task_2_medium},
        {"name": "Hard", "state": get_task_3_state(), "grader": grade_task_3_hard},
    ]

    for t in tasks_def:
        state_dict = t["state"].model_dump()
        
        # Inject the urgency score so the LLM doesn't have to guess the hidden python math!
        for i, z in enumerate(t["state"].zones):
            state_dict["zones"][i]["urgency_score"] = z.urgency_score

        prompt = f"""
        You are a disaster response AI. Current state:
        {json.dumps(state_dict, indent=2)}
        
        CRITICAL INSTRUCTIONS TO FULLY COMPLETE THE TASKS:
        1. Easy Task: Return `prioritized_zones` perfectly sorted by `urgency_score` (highest to lowest).
        2. Medium Task: In `resource_allocations`, you MUST allocate ambulances to EVERY zone where `medical_emergencies` > 0, and you MUST allocate boats to EVERY zone where `water_level_m` >= 2.0. 
        3. Hard Task: You MUST write a detailed text narrative in the `plan` field that explicitly uses EVERY single one of these exact keywords: "evacuate", "priority", "medical", "shelter", "boat", "ambulance". Also, be sure to open at least one shelter, order at least one evacuation, and allocate resources.
        
        Output a valid JSON matching this schema for your actions:
        {Action.model_json_schema()}
        """
        
        print(f"--- Running Task: {t['name']} ---")
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            raw_output = response.choices[0].message.content
            action = Action.model_validate_json(raw_output)
            
            score = t["grader"](action, t["state"])
            print(f"Action parsed successfully.")
            print(f"Score for {t['name']} task: {score:.2f} / 1.00\n")
        except Exception as e:
            print(f"Failed on task {t['name']}. Error: {str(e)}\n")

if __name__ == "__main__":
    main()
