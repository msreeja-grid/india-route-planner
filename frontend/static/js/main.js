document.addEventListener("DOMContentLoaded", () => {
    const map = L.map('map', {zoomControl: false}).setView([20.59, 78.96], 5);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png').addTo(map);
    const layers = L.layerGroup().addTo(map);

    document.getElementById('mainBtn').onclick = async () => {
        const start = document.getElementById('startCity').value;
        const end = document.getElementById('endCity').value;
        const algos = Array.from(document.querySelectorAll('.algo:checked')).map(c => c.value);

        if (!start || !end || !algos.length) return alert("Select start, end, and algos!");

        const btn = document.getElementById('mainBtn');
        btn.innerText = "Analyzing...";
        btn.disabled = true;

        try {
            const res = await fetch('/api/analyze', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ start, end, algos })
            });

            const data = await res.json();
            layers.clearLayers();
            document.getElementById('results-container').classList.remove('hidden');
            const tbody = document.getElementById('res-table-body');
            tbody.innerHTML = "";

            const colors = {"A*": "#10b981", "Dijkstra": "#3b82f6", "BFS": "#f59e0b", "DFS": "#ef4444"};

            algos.forEach(a => {
                const r = data.results[a];
                if (r.path.length) {
                    const latlngs = r.path.map(c => [data.coords[c][0], data.coords[c][1]]);
                    L.polyline(latlngs, {color: colors[a], weight: 4, opacity: 0.8}).addTo(layers);
                    tbody.innerHTML += `<tr><td style="color:${colors[a]}"><b>${a}</b></td><td>${r.dist}</td><td>${r.nodes}</td><td>${r.comp}</td></tr>`;
                }
            });

            const group = new L.featureGroup(layers.getLayers());
            if (group.getLayers().length) map.fitBounds(group.getBounds(), {padding:[50,50]});
        } finally {
            btn.innerText = "START ANALYSIS";
            btn.disabled = false;
        }
    };
});