

# 🇮🇳 India Route Planner: High-Performance Pathfinding Analysis

[](https://www.python.org/downloads/)
[](https://flask.palletsprojects.com/)
[](https://opensource.org/licenses/MIT)

A sophisticated geographical pathfinding visualizer and benchmarking tool. This system analyzes four core graph traversal algorithms—**A\*, Dijkstra, BFS, and DFS**—across a real-world dataset of **6,800+ Indian cities**.


### 1\. Data Layer (Graph Construction)

  * **Dataset:** Uses a CSV containing 6,896 Indian cities with precision Geo-coordinates.
  * **Adjacency List:** On initialization, the system builds a **Weighted Cyclic Graph**.
  * **Spatial Connectivity:** Instead of arbitrary edges, every city is linked to its **6 nearest neighbors** using the **Haversine Formula** (calculating distance over the Earth's curvature, $R = 6371$ km).

### 2\. Backend Logic (Algorithm Kernels)

  * **Performance Benchmarking:** Uses `time.perf_counter()` to capture sub-millisecond execution times.
  * **Search Strategies:**
      * **A\* & Dijkstra:** Utilize a **Priority Queue (Min-Heap)** for optimal pathfinding.
      * **BFS:** Utilizes a **Queue (FIFO)** for level-order exploration.
      * **DFS:** Utilizes a **Stack (LIFO)** to handle deep-path backtracking in a cyclic environment.

### 3\. Frontend Dashboard

  * **Leaflet.js Integration:** Renders interactive map tiles and draws dynamic polylines.
  * **Asynchronous Analysis:** Uses the `fetch` API to communicate with the Flask `/api/analyze` endpoint without reloading the page.

-----

## 📊 Algorithm Performance Comparison

The project focuses on validating **Theoretical Complexity** against **Practical Execution Time**.

| Algorithm | Strategy | Data Structure | Complexity (Big O) |
| :--- | :--- | :--- | :--- |
| **A\*** | Heuristic-Based | Min-Heap | $O(E)$ |
| **Dijkstra** | Shortest Path | Min-Heap | $O((V+E) \log V)$ |
| **BFS** | Breadth-First | Queue | $O(V+E)$ |
| **DFS** | Depth-First | **Stack** | $O(V+E)$ |

-----

## 🚀 Installation & Setup

### Prerequisites

  * Python 3.8+
  * `pip` (Python package manager)

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/msreeja-grid/india-route-planner.git
    cd india-route-planner
    ```
2.  **Install Dependencies:**
    ```bash
    pip install flask pandas
    ```

### Running the Project

```bash
python3 app.py
```

  * Access the dashboard at: `http://127.0.0.1:5001`

-----

## 📁 Repository Structure

```text
.
├── app.py                  # Backend Engine (Algorithms & Flask API)
├── india_cities_final.csv  # Dataset (6896 Geo-coded records)
├── static/
│   ├── css/main.css        # UI/UX Styling
│   └── js/main.js          # Leaflet.js Mapping & State Management
└── templates/
    └── index.html          # Responsive Web Dashboard
```

-----

## 🔍 Implementation Insights

  * **Why Stack for DFS?** Unlike a Tree, a Map is a **Graph** with cycles. A Stack allows the algorithm to dive deep and backtrack efficiently when hitting a dead-end.
  * **The Heuristic Advantage:** A\* is significantly faster than Dijkstra in this project because it uses the "Crow-flies" distance to ignore cities in the opposite direction of the destination.

