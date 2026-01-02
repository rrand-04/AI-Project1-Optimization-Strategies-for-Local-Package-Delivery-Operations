# AI-Project1-Optimization-Strategies-for-Local-Package-Delivery-Operations

This project solves the **package-to-vehicle assignment and routing** problem for a local delivery shop:
- Assign packages to vehicles without exceeding **vehicle capacity**
- Minimize the **total traveled distance** (Euclidean distance on a 2D grid)
- Prefer delivering **higher-priority** packages earlier when possible

Algorithms implemented:
- **Simulated Annealing (SA)**
- **Genetic Algorithm (GA)**

---

## Problem Summary
Each package has:
- Destination `(x, y)` on a 2D plane
- `weight` (kg)
- `priority` (1 = highest, 5 = lowest)

Each vehicle has:
- A limited `capacity` (kg)

Goal: minimize total distance traveled by all vehicles while respecting constraints and considering priority.

---

## Project Files
- `main.py` → menu to choose SA or GA
- `simulated_annealing_module.py` → SA implementation + plotting
- `genetic_algorithm_module.py` → GA implementation
- `utils.py` → distance calculations / helper functions
- `models.py` → data structures

---

## How to Run
```bash
# 1) (Optional) Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
# venv\Scripts\activate    # Windows

# 2) Install requirements
pip install matplotlib

# 3) Run
python main.py

