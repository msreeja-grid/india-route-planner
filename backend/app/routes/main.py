from flask import Blueprint, render_template, request, jsonify
from backend.app.services.algorithms import run_dijkstra, run_astar, run_bfs, run_dfs
from backend.app.services.route_engine import engine
import time

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('index.html', cities=sorted(engine.adj.keys()))


@main.route('/api/analyze', methods=['POST'])
def route_api():
    data = request.json

    s = data.get('src') or data.get('start')
    e = data.get('dest') or data.get('end')
    algos = data.get('algos') or data.get('algorithms')

    funcs = {
        "Dijkstra": run_dijkstra,
        "A*": run_astar,
        "BFS": run_bfs,
        "DFS": run_dfs
    }

    res = {}

    for a in algos:
        if a in funcs:
            start_t = time.perf_counter()

            path, dist, nodes, big_o = funcs[a](s, e)

            end_t = time.perf_counter()
            ms = (end_t - start_t) * 1000

            res[a] = {
                "path": path,
                "dist": dist,
                "nodes": nodes,
                "comp": f"{ms:.3f} ms ({big_o})"
            }

    return jsonify({
        "results": res,
        "coords": engine.coords
    })