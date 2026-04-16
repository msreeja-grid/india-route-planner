import pandas as pd
import math
from config import Config


class RouteEngine:
    def __init__(self):
        self.adj = {}
        self.coords = {}

    def load_data(self):
        try:
            # ✅ Using config file instead of hardcoding path
            df = pd.read_csv(Config.CSV_PATH)

            for _, r in df.iterrows():
                city = str(r['city'])
                self.coords[city] = (float(r['lat']), float(r['lng']))
                self.adj[city] = {}

            nodes = list(self.adj.keys())

            # Build graph: connect each city to 6 nearest neighbors
            for i, c1 in enumerate(nodes):
                dists = []

                for j, c2 in enumerate(nodes):
                    if i == j:
                        continue

                    d = self.haversine(self.coords[c1], self.coords[c2])
                    dists.append((d, c2))

                dists.sort()

                for d, c2 in dists[:6]:
                    self.adj[c1][c2] = d
                    self.adj[c2][c1] = d

            print(f"✅ Loaded {len(nodes)} cities and built road network.")

        except Exception as e:
            print(f"❌ Error loading CSV: {e}")

    def haversine(self, p1, p2):
        lat1, lon1 = p1
        lat2, lon2 = p2

        R = 6371  # Earth radius in KM

        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)

        dphi = math.radians(lat2 - lat1)
        dlam = math.radians(lon2 - lon1)

        a = (
            math.sin(dphi / 2) ** 2
            + math.cos(phi1)
            * math.cos(phi2)
            * math.sin(dlam / 2) ** 2
        )

        return R * 2 * math.asin(math.sqrt(a))


# ✅ GLOBAL ENGINE (IMPORTANT: used by algorithms)
engine = RouteEngine()
engine.load_data()