

# 🇮🇳 India Route Planner: High-Performance Pathfinding System

[](https://www.python.org/downloads/)
[](https://flask.palletsprojects.com/)
[](https://opensource.org/licenses/MIT)

A high-performance **graph-based route planning system** that compares classical pathfinding algorithms (**A*, Dijkstra, BFS, DFS**) on a real-world dataset of **6,800+ Indian cities** using geospatial distance computation.

---

# 🚀 Features

* 🗺️ Real-world graph built from 6,896 Indian cities
* 📍 Geospatial distance using **Haversine Formula**
* ⚡ Live benchmarking of algorithm performance
* 📊 Comparison of time complexity vs actual execution time
* 🌐 Interactive web dashboard (Flask + JavaScript)
* 🔁 Asynchronous API-based architecture
* 🧠 Modular backend design (services, routes, config)

---

# 🏗️ System Architecture

## 1. Data Layer (Graph Engine)

* Dataset: `india_cities_final.csv`
* 6,896 cities with latitude & longitude
* Graph built using **Adjacency List**
* Each city connects to its **6 nearest neighbors**
* Distance calculated using:

[
R = 6371 \text{ km (Earth radius)}
]

* Efficient spatial graph representation for fast traversal

---

## 2. Backend Layer (Flask API)

* Built using **Flask Blueprint architecture**
* Centralized configuration via `config.py`
* Modular structure:

  * `routes.py` → API endpoints
  * `algorithms.py` → pathfinding logic
  * `route_engine.py` → graph builder
* Performance tracking using:

  * `time.perf_counter()`

---

## 3. Algorithms Implemented

| Algorithm | Strategy               | Data Structure | Complexity     |
| --------- | ---------------------- | -------------- | -------------- |
| A*        | Heuristic-based search | Min Heap       | O(E)           |
| Dijkstra  | Shortest path          | Min Heap       | O((V+E) log V) |
| BFS       | Level-order traversal  | Queue          | O(V+E)         |
| DFS       | Depth-first traversal  | Stack          | O(V+E)         |

---

## 4. Frontend Layer

* Built with **HTML + CSS + JavaScript**
* Uses **Leaflet.js** for map rendering
* Fetch API for async communication:

  * `/api/analyze`
* Displays:

  * Path visualization
  * Distance
  * Nodes explored
  * Execution time comparison

---

# 📁 Project Structure (UPDATED)

```text
india-route-planner/
│
├── run.py
├── config.py
├── README.md
├── requirements.txt   (recommended)
│
├── backend/
│   └── app/
│       ├── __init__.py          # Flask app factory
│       │
│       ├── routes/
│       │   └── main.py          # API + web routes (Blueprint)
│       │
│       └── services/
│           ├── algorithms.py    # BFS, DFS, A*, Dijkstra
│           └── route_engine.py  # Graph + Haversine engine
│
├── frontend/
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
│
└── data/
    └── india_cities_final.csv
```

---

# 🔧 Installation & Setup

## 1. Clone Repository

```bash
git clone https://github.com/msreeja-grid/india-route-planner.git
cd india-route-planner
```

---

## 2. Install Dependencies

```bash
pip install flask pandas
```

---

## 3. Run Project

```bash
python3 run.py
```

---

## 🌐 Access Application

```
http://127.0.0.1:5001
```

---

# ⚙️ Configuration (config.py)

All global settings are managed in one file:

```python
class Config:
    DEBUG = True
    PORT = 5001
    CSV_PATH = "data/india_cities_final.csv"
```

---

# 📊 Key Insights

### Why 6 Nearest Neighbors?

* Reduces graph complexity
* Simulates realistic road networks
* Avoids full mesh explosion (O(n²))

---

### Why A* is faster?

* Uses heuristic (straight-line distance)
* Avoids unnecessary node exploration
* More directed search vs Dijkstra

---

### Why BFS & DFS included?

* For **algorithm comparison study**
* To visualize uninformed vs informed search

---

# 🧠 Learning Outcomes

This project demonstrates:

* Graph theory in real-world systems
* Heuristic search optimization
* Backend API design with Flask
* Modular Python architecture
* Performance benchmarking techniques


