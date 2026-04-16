import heapq
import collections
from backend.app.services.route_engine import engine

# ---------------- DIJKSTRA ----------------
def run_dijkstra(start, end):
    pq = [(0, start, [start])]
    visited = {}
    nodes_explored = 0

    while pq:
        cost, curr, path = heapq.heappop(pq)

        if curr in visited and visited[curr] <= cost:
            continue

        visited[curr] = cost
        nodes_explored += 1

        if curr == end:
            return path, round(cost, 2), nodes_explored, r"O((V+E) log V)"

        for nbr, d in engine.adj[curr].items():
            heapq.heappush(pq, (cost + d, nbr, path + [nbr]))

    return [], 0, nodes_explored, r"O((V+E) log V)"


# ---------------- A* ----------------
def run_astar(start, end):
    goal = engine.coords[end]
    pq = [(0, start, [start], 0)]
    visited = {}
    nodes_explored = 0

    while pq:
        f, curr, path, g = heapq.heappop(pq)

        if curr in visited and visited[curr] <= g:
            continue

        visited[curr] = g
        nodes_explored += 1

        if curr == end:
            return path, round(g, 2), nodes_explored, "O(E)"

        for nbr, d in engine.adj[curr].items():
            new_g = g + d
            h = engine.haversine(engine.coords[nbr], goal)
            heapq.heappush(pq, (new_g + h, nbr, path + [nbr], new_g))

    return [], 0, nodes_explored, "O(E)"


# ---------------- BFS ----------------
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
                vis.add(nbr)
                q.append((nbr, path + [nbr]))

    return [], 0, nodes_explored, "O(V+E)"


# ---------------- DFS ----------------
def run_dfs(start, end):
    stack = [(start, [start])]
    vis = set()
    nodes_explored = 0

    while stack:
        curr, path = stack.pop()

        if curr in vis:
            continue

        vis.add(curr)
        nodes_explored += 1

        if curr == end:
            d = sum(engine.adj[path[i]][path[i+1]] for i in range(len(path)-1))
            return path, round(d, 2), nodes_explored, "O(V+E)"

        for nbr in engine.adj[curr]:
            if nbr not in vis:
                stack.append((nbr, path + [nbr]))

    return [], 0, nodes_explored, "O(V+E)"