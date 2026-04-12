---
title: Monsoon Relief OpenEnv
emoji: 🌧️
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
app_port: 7860
---
<div align="center">
  <h1>🌧️🚁 Monsoon Relief Dispatch OpenEnv</h1>
  <p><i>A real-world, high-stakes reinforcement learning environment where an AI acts as a disaster-response operations officer.</i></p>
  
  [![OpenEnv Compliant](https://img.shields.io/badge/OpenEnv-Compliant-blue.svg)](#)
  [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](#)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#)
</div>

<br/>

## 🎯 Why This Environment?
Unlike generic chatbots or simple toy games, responding to a natural disaster requires **multi-objective optimization under strict constraints**. The agent must intelligently handle blocked roads, accurately distribute scarce resources (boats vs. trucks), balance demographic vulnerabilities (elderly/children), and plan dynamically as water levels rise. This makes for a hyper-realistic, high-stakes benchmark for modern reasoning models.

---

## 🛠️ Environment Specifications 

### 👁️ Observation Space
Provides a strongly-typed Pydantic state capturing:
- Active Zones and precise Water Levels (in meters).
- Real-time demographic counts (Stranded, Elderly, Children, Medical Emergencies).
- Available global resources (Boats, Trucks, Ambulances, Volunteers).
- Maximum and current capacities of local Shelters.

### 🎮 Action Space
A strictly-typed JSON schema encompassing:
1. **Priority Ranking**: Dynamically rank zones by statistical urgency.
2. **Resource Dispatch**: Deploy specific numbers of varied vehicles.
3. **Shelter Operation**: Toggle the opening metadata for community centers.
4. **Evacuation Commands**: Formally issue emergency evacuation orders for specific zones.
5. **Detailed Planning**: A text rationale for complex event sequencing.

### ⚖️ Reward Logic 
The environment operates with a dynamic scalar reward system mapping partial progress:
- ✅ **Positive**: Timely evacuations, prioritizing urgent medical emergencies, and proactive shelter openings.
- ❌ **Negative**: Assigning non-amphibious vehicles (trucks) to severely flooded roads, hallucinating unowned resources, and leaving civilians stranded as waters rise per step.

---

## 📋 Evaluation Tasks 
We provide an escalating 3-tier task system with programmatic zero-to-one graders:

| Difficulty | Task Goal | Success Criteria |
|:---:|---|---|
| 🟢 **Easy** | **Rank Zones by Urgency** | Grader strictly evaluates alignment mathematically against true vulnerability metrics (Medical > Elderly > Overall Stranded). |
| 🟡 **Medium** | **Allocate Resources Optimally** | Grader evaluates logical resource routing (e.g., dispatching available boats strictly to deep-water zones and ambulances solely to medical emergencies). |
| 🔴 **Hard** | **Generate Full Response Strategy** | Grader evaluates holistic, multi-turn action sequencing and explicitly parses the textual reasoning logic for prioritization keywords. |

---

## 🚀 Running Baseline Inference

We utilize a zero-shot, heavily prompt-engineered baseline script (`inference.py`) to benchmark LLMs globally against the environment utilizing standard OpenAI schema execution.

**1. Set your configuration environment variables:**
```bash
export API_BASE_URL="https://router.huggingface.co/v1"
export MODEL_NAME="meta-llama/Llama-3.3-70B-Instruct"
export HF_TOKEN="hf_your_hugging_face_token_here"
```

**2. Execute the evaluation baseline:**
```bash
python inference.py
```

### 🏆 Baseline Scores
*Zero-shot baseline benchmark evaluating realistic Mumbai disaster constraints:*
- 🟢 **Easy**: `0.88 / 1.00`
- 🟡 **Medium**: `0.76 / 1.00`
- 🔴 **Hard**: `0.86 / 1.00`

*(Total Aggregate: **2.50 / 3.00**)*

## 🐳 Local Docker Execution
The environment includes a working `Dockerfile` built on the modern `uv` Python manager. You can spin up the environment's API server locally:

**1. Build the Docker Image:**
```bash
docker build -t monsoon-env .
```

**2. Run the Container:**
```bash
docker run -p 7860:7860 monsoon-env
```
_The OpenEnv API will now be accessible at `http://localhost:7860`._

---

## 🌩️ Hugging Face Spaces Deployment
Ready for multi-mode execution:
1. Initialize a generic **Docker** Hugging Face Space.
2. Ensure you assign your runtime `$HF_TOKEN` Environment Variable in the space's restricted secrets settings.
3. The Space will automatically spin up the integrated API Server using `uvicorn` mapped through `uv.lock`.

---

## ✅ Pre-Submission Checklist Compliance
This project strictly adheres to the OpenEnv Hackathon Round 1 requirements:
- **Real-World Task:** Simulates life-critical disaster relief (not a toy/game).
- **OpenEnv Spec Compliance:** Features a fully compliant `openenv.yaml`, strict Pydantic typed models, and endpoints for `step()`, `reset()`, and `state()`.
- **Automated Validation Graders:** 3 complete tasks (Easy, Medium, Hard) strictly scoring `0.0` to `1.0`.
- **Reward Logic:** Granular partial progress rewards defined via realistic outcomes.
- **Docker Support:** Fully isolated, reproducible container build provided.
- **Standardized Inference Logic:** The `inference.py` script resides in the root directory, executes using the standard OpenAI client, adheres perfectly to the `API_BASE_URL`, `MODEL_NAME`, and `HF_TOKEN` environment variables setup, and emits strictly formatted `[START]`, `[STEP]`, and `[END]` evaluation stdout logs as mandated.
