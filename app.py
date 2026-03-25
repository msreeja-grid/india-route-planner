from flask import Flask, render_template, request, jsonify
import pandas as pd
import math, heapq, time, collections

app = Flask(__name__)

class RouteEngine:
    def __init__(self):
        self.adj = {}
        self.coords = {}

    def load_data(self):
        try:
            # Loading the CSV file
            df = pd.read_csv('india_cities_final.csv')
            for _, r in df.iterrows():
                city = str(r['city'])
                self.coords[city] = (float(r['lat']), float(r['lng']))
                self.adj[city] = {}
            
            # Connect each city to its 6 nearest neighbors to build the Graph network
            nodes = list(self.adj.keys())
            for i, c1 in enumerate(nodes):
                dists = []
                for j, c2 in enumerate(nodes):
                    if i == j: continue
                    d = self.haversine(self.coords[c1], self.coords[c2])
                    dists.append((d, c2))
                dists.sort()
                
                # Connect to top 6 nearest cities
                for d, c2 in dists[:6]:
                    self.adj[c1][c2] = d
                    self.adj[c2][c1] = d
            print(f"✅ Loaded {len(nodes)} cities and built road network.")
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")

    def haversine(self, p1, p2):
        lat1, lon1 = p1; lat2, lon2 = p2
        R = 6371 # Earth radius in KM
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi, dlam = math.radians(lat2-lat1), math.radians(lon2-lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
        return R * 2 * math.asin(math.sqrt(a))

engine = RouteEngine()
engine.load_data()

# --- ALGORITHMS ---

def run_dijkstra(start, end):
    pq = [(0, start, [start])]
    visited = {}
    nodes_explored = 0
    while pq:
        cost, curr, path = heapq.heappop(pq)
        if curr in visited and visited[curr] <= cost: continue
        visited[curr] = cost
        nodes_explored += 1
        # Using raw string r"" to avoid SyntaxWarning for \log
        if curr == end: return path, round(cost, 2), nodes_explored, r"O((V+E) \log V)"
        for nbr, d in engine.adj[curr].items():
            heapq.heappush(pq, (cost + d, nbr, path + [nbr]))
    return [], 0, nodes_explored, r"O((V+E) \log V)"

def run_astar(start, end):
    goal = engine.coords[end]
    pq = [(0, start, [start], 0)]
    visited = {}
    nodes_explored = 0
    while pq:
        f, curr, path, g = heapq.heappop(pq)
        if curr in visited and visited[curr] <= g: continue
        visited[curr] = g
        nodes_explored += 1
        if curr == end: return path, round(g, 2), nodes_explored, "O(E)"
        for nbr, d in engine.adj[curr].items():
            new_g = g + d
            h = engine.haversine(engine.coords[nbr], goal)
            heapq.heappush(pq, (new_g + h, nbr, path + [nbr], new_g))
    return [], 0, nodes_explored, "O(E)"

def run_bfs(start, end):
    q = collections.deque([(start, [start])])
    vis = {start}
    nodes_explored = 0
    while q:
        curr, path = q.popleft()
        nodes_explored += 1
        if curr == end:
            d = sum(engine.adj[path[i]][path[i+1]] for i in range(len(path)-1))
            return path, round(d, 2), nodes_explored, "O(V+E)"
        for nbr in engine.adj[curr]:
            if nbr not in vis:
                vis.add(nbr); q.append((nbr, path + [nbr]))
    return [], 0, nodes_explored, "O(V+E)"

def run_dfs(start, end):
    stack = [(start, [start])]
    vis = set()
    nodes_explored = 0
    while stack:
        curr, path = stack.pop()
        if curr in vis: continue
        vis.add(curr); nodes_explored += 1
        if curr == end:
            d = sum(engine.adj[path[i]][path[i+1]] for i in range(len(path)-1))
            return path, round(d, 2), nodes_explored, "O(V+E)"
        for nbr in engine.adj[curr]:
            if nbr not in vis: stack.append((nbr, path + [nbr]))
    return [], 0, nodes_explored, "O(V+E)"

@app.route('/')
def home():
    return render_template('index.html', cities=sorted(engine.adj.keys()))

@app.route('/api/analyze', methods=['POST'])
def route_api():
    data = request.json
    s = data.get('src') or data.get('start')
    e = data.get('dest') or data.get('end')
    algos = data.get('algos') or data.get('algorithms')
    
    funcs = {"Dijkstra": run_dijkstra, "A*": run_astar, "BFS": run_bfs, "DFS": run_dfs}
    res = {}
    
    for a in algos:
        if a in funcs:
            # Measuring real-time performance
            start_t = time.perf_counter()
            path, dist, nodes, big_o = funcs[a](s, e)
            end_t = time.perf_counter()
            
            # Calculating execution time in milliseconds
            ms = (end_t - start_t) * 1000
            
            # Combining Time and Complexity as per Mentor's request
            combined_comp = f"{ms:.3f} ms ({big_o})"
            
            res[a] = {
                "path": path, 
                "dist": dist, 
                "nodes": nodes, 
                "comp": combined_comp
            }
            
    return jsonify({"results": res, "coords": engine.coords})

if __name__ == '__main__':
    app.run(debug=True, port=5001)