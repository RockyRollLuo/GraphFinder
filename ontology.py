"""Graph Problem Ontology — 55 classical graph theory problems with structured metadata."""
import json, os

ONTOLOGY_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Full Ontology: 55 problems in 5 families ──────────────────────────
ONTOLOGY = {
  # ===== PATH PROBLEMS (11) =====
  "shortest_path": {
    "name": "Shortest Path",
    "family": "path",
    "complexity": "P",
    "topological_skeleton": "Weighted directed/undirected graph. Single source, single or all targets. Non-negative weights.",
    "canonical_description": "Given a weighted graph, find the path between two vertices that minimizes the sum of edge weights.",
    "core_objective": "minimize sum of edge weights along a path from s to t",
    "key_algorithms": ["Dijkstra O(E+V log V)", "Bellman-Ford O(VE)", "A* Search"],
    "slot_template": {
      "ENTITY_SET_A": {"type": "source_locations", "maps_to": "source_nodes"},
      "ENTITY_SET_B": {"type": "target_locations", "maps_to": "target_nodes"},
      "RELATION_C": {"type": "connections", "maps_to": "directed_edges"},
      "ATTRIBUTE_D": {"type": "cost_or_distance", "maps_to": "edge_weights"},
      "OBJECTIVE": "minimize total path cost"
    },
    "application_domains": [
      "GPS navigation — find shortest driving route",
      "Network routing — minimize hop count between routers",
      "Currency exchange — find cheapest sequence of conversions",
      "Game AI — pathfinding for NPCs",
      "Supply chain — find cheapest transportation route"
    ]
  },
  "longest_path": {
    "name": "Longest Path",
    "family": "path", "complexity": "NP-hard",
    "topological_skeleton": "Weighted directed acyclic graph (DAG) for polynomial case; general graph is NP-hard.",
    "canonical_description": "Find the simple path between two vertices that maximizes the sum of edge weights.",
    "core_objective": "maximize sum of edge weights along a simple path",
    "key_algorithms": ["DP on DAG O(V+E)", "ILP / backtracking for general graphs"],
    "slot_template": {
      "ENTITY_SET_A": {"type": "start_nodes", "maps_to": "source"},
      "ENTITY_SET_B": {"type": "end_nodes", "maps_to": "target"},
      "RELATION_C": {"type": "dependencies_or_transitions", "maps_to": "edges"},
      "ATTRIBUTE_D": {"type": "value_or_duration", "maps_to": "edge_weights"},
      "OBJECTIVE": "maximize total path value"
    },
    "application_domains": [
      "Project scheduling — critical path in task dependency graph",
      "Game level design — longest possible sequence of moves",
      "Circuit design — longest propagation delay path"
    ]
  },
  "minimum_spanning_tree": {
    "name": "Minimum Spanning Tree",
    "family": "path", "complexity": "P",
    "topological_skeleton": "Undirected weighted connected graph. Find a tree spanning all vertices with minimum total weight.",
    "canonical_description": "Connect all vertices in a weighted graph with minimum total edge weight, forming a tree.",
    "core_objective": "minimize sum of selected edge weights covering all vertices",
    "key_algorithms": ["Kruskal O(E log E)", "Prim O(E log V)"],
    "slot_template": {
      "ENTITY_SET_A": {"type": "points_to_connect", "maps_to": "all_vertices"},
      "RELATION_C": {"type": "possible_connections", "maps_to": "undirected_edges"},
      "ATTRIBUTE_D": {"type": "connection_cost", "maps_to": "edge_weights"},
      "OBJECTIVE": "minimize total connection cost connecting all points"
    },
    "application_domains": [
      "Network design — minimum-cost cable/fiber layout",
      "Circuit board — minimize wire length connecting components",
      "Pipeline layout — minimum-cost pipe network",
      "Cluster analysis — single-linkage hierarchical clustering"
    ]
  },
  "steiner_tree": {
    "name": "Steiner Tree",
    "family": "path", "complexity": "NP-hard",
    "topological_skeleton": "Undirected weighted graph with required terminal vertices and optional Steiner vertices.",
    "canonical_description": "Connect a specified subset of terminal vertices with minimum total edge weight, optionally using additional Steiner vertices.",
    "core_objective": "minimize sum of edge weights connecting all terminal vertices",
    "key_algorithms": ["Dreyfus-Wagner DP O(3^k V + 2^k V^2)", "Approximation algorithms (2-1/k factor)"],
    "slot_template": {
      "ENTITY_SET_A": {"type": "mandatory_connection_points", "maps_to": "terminal_vertices"},
      "ENTITY_SET_B": {"type": "optional_relay_points", "maps_to": "steiner_vertices"},
      "RELATION_C": {"type": "possible_links", "maps_to": "edges"},
      "ATTRIBUTE_D": {"type": "link_cost", "maps_to": "edge_weights"},
      "OBJECTIVE": "minimize total connection cost spanning mandatory points"
    },
    "application_domains": [
      "VLSI design — route wires connecting chip components",
      "Telecom — connect cities with minimum fiber via optional relay stations",
      "Phylogenetic trees — minimum evolution tree connecting species"
    ]
  },
  "hamiltonian_path": {
    "name": "Hamiltonian Path",
    "family": "path", "complexity": "NP-complete",
    "topological_skeleton": "Undirected/directed graph. Find a path visiting every vertex exactly once.",
    "canonical_description": "Find a path that visits each vertex exactly once.",
    "core_objective": "existence / find a path visiting each vertex exactly once",
    "key_algorithms": ["Backtracking", "Held-Karp DP O(n^2 2^n)"],
    "slot_template": {
      "ENTITY_SET_A": {"type": "items_to_visit", "maps_to": "all_vertices"},
      "RELATION_C": {"type": "available_transitions", "maps_to": "edges"},
      "OBJECTIVE": "visit every item exactly once using available transitions"
    },
    "application_domains": [
      "Knight's tour — visit all chessboard squares once",
      "DNA fragment assembly — order fragments in a sequence",
      "Plot planning — visit all locations in a theme park"
    ]
  },
  "eulerian_path": {
    "name": "Eulerian Path",
    "family": "path", "complexity": "P",
    "topological_skeleton": "Undirected/directed graph. Find a path using every edge exactly once.",
    "canonical_description": "Find a trail that traverses each edge exactly once. Exists iff 0 or 2 vertices have odd degree (undirected).",
    "core_objective": "existence / find a trail using every edge exactly once",
    "key_algorithms": ["Hierholzer O(E)", "Fleury O(E^2)"],
    "slot_template": {
      "ENTITY_SET_A": {"type": "junctions", "maps_to": "vertices"},
      "RELATION_C": {"type": "segments_to_cover", "maps_to": "edges_must_use_all"},
      "OBJECTIVE": "traverse every segment exactly once"
    },
    "application_domains": [
      "Königsberg bridges — can you cross each bridge exactly once?",
      "Snow plow routing — clear every street once",
      "DNA sequencing (de Bruijn graphs) — traverse each k-mer once",
      "Postman problem — deliver to every street"
    ]
  },
  "chinese_postman": {
    "name": "Chinese Postman Problem",
    "family": "path", "complexity": "P",
    "topological_skeleton": "Undirected weighted graph. Find minimum-weight closed walk covering every edge at least once.",
    "canonical_description": "Find the shortest closed walk that traverses every edge at least once. Equivalent to minimum weight perfect matching on odd-degree vertices to make graph Eulerian.",
    "core_objective": "minimize total walk weight covering all edges at least once",
    "key_algorithms": ["Minimum weight perfect matching on odd vertices + Eulerian circuit O(V^3)"],
    "slot_template": {
      "ENTITY_SET_A": {"type": "intersections", "maps_to": "vertices"},
      "RELATION_C": {"type": "road_segments", "maps_to": "edges_must_cover_all"},
      "ATTRIBUTE_D": {"type": "segment_length", "maps_to": "edge_weights"},
      "OBJECTIVE": "minimize total distance covering all segments"
    },
    "application_domains": [
      "Street sweeping — cover all streets with minimum travel",
      "Mail delivery — deliver to every address on every street",
      "Infrastructure inspection — inspect all pipes/cables"
    ]
  },

  # ===== FLOW PROBLEMS (9) =====
  "max_flow": {
    "name": "Maximum Flow",
    "family": "flow", "complexity": "P",
    "topological_skeleton": "Directed graph with source s, sink t, and edge capacities. Maximize flow from s to t.",
    "canonical_description": "Find the maximum amount of flow that can be sent from a source vertex to a sink vertex without exceeding edge capacities.",
    "core_objective": "maximize total flow from source to sink subject to capacity and conservation constraints",
    "key_algorithms": ["Ford-Fulkerson O(E·max_flow)", "Edmonds-Karp O(VE^2)", "Dinic O(V^2 E)"],
    "slot_template": {
      "ENTITY_SET_A": {"type": "source_point", "maps_to": "source_node"},
      "ENTITY_SET_B": {"type": "destination_point", "maps_to": "sink_node"},
      "RELATION_C": {"type": "transport_channels", "maps_to": "directed_edges"},
      "ATTRIBUTE_D": {"type": "channel_capacity", "maps_to": "edge_capacities"},
      "OBJECTIVE": "maximize total throughput from source to destination"
    },
    "application_domains": [
      "Water distribution — maximize water flow through pipe network",
      "Data bandwidth — maximize data throughput in network",
      "Transportation — maximize vehicles through road network",
      "Bipartite matching — maximum matching as max flow"
    ]
  },
  "min_cost_flow": {
    "name": "Minimum Cost Flow",
    "family": "flow", "complexity": "P",
    "topological_skeleton": "Directed graph with edge capacities, edge costs, and vertex supplies/demands.",
    "canonical_description": "Find the cheapest way to send a specified amount of flow through a capacitated network from supply nodes to demand nodes.",
    "core_objective": "minimize sum(flow[e] × cost[e]) subject to capacity and conservation",
    "key_algorithms": ["Successive Shortest Path O(V^2 E log V)", "Cycle Canceling", "Network Simplex"],
    "slot_template": {
      "ENTITY_SET_A": {"type": "supply_points", "maps_to": "supply_nodes_positive_balance"},
      "ENTITY_SET_B": {"type": "demand_points", "maps_to": "demand_nodes_negative_balance"},
      "RELATION_C": {"type": "shipping_routes", "maps_to": "directed_edges"},
      "ATTRIBUTE_D": {"type": "shipping_capacity", "maps_to": "edge_capacities"},
      "ATTRIBUTE_E": {"type": "unit_shipping_cost", "maps_to": "edge_costs"},
      "OBJECTIVE": "minimize total shipping cost meeting all demand"
    },
    "application_domains": [
      "Logistics — minimize transportation cost warehouse→stores",
      "Production planning — minimize cost of material flow through factories",
      "Waste management — optimize waste transport",
      "Energy grid — minimize cost of power distribution"
    ]
  },
  "multi_commodity_flow": {
    "name": "Multi-Commodity Flow",
    "family": "flow", "complexity": "P (linear programming)",
    "topological_skeleton": "Directed graph with edge capacities shared across multiple commodities, each with own source-sink.",
    "canonical_description": "Route multiple distinct commodities through a shared capacitated network simultaneously without exceeding any edge capacity.",
    "core_objective": "maximize total flow across commodities or route all demands subject to shared capacities",
    "key_algorithms": ["Linear Programming", "Column Generation", "Approximation algorithms"],
    "slot_template": {
      "ENTITY_SET_A": {"type": "commodity_origins", "maps_to": "source_nodes_per_commodity"},
      "ENTITY_SET_B": {"type": "commodity_destinations", "maps_to": "sink_nodes_per_commodity"},
      "RELATION_C": {"type": "shared_paths", "maps_to": "edges"},
      "ATTRIBUTE_D": {"type": "path_capacity", "maps_to": "edge_capacities_shared"},
      "OBJECTIVE": "maximize total flow across all commodities"
    },
    "application_domains": [
      "Internet backbone — route multiple traffic types over shared links",
      "Freight rail — multiple cargo types on shared tracks",
      "Telecom wavelength routing — multiple signals on shared fiber"
    ]
  },

  # ===== MATCHING & ASSIGNMENT (8) =====
  "bipartite_matching": {
    "name": "Maximum Bipartite Matching",
    "family": "matching", "complexity": "P",
    "topological_skeleton": "Bipartite graph (two disjoint vertex sets A and B). Maximize number of disjoint edges.",
    "canonical_description": "Given a bipartite graph, find the maximum set of edges such that no two edges share a vertex.",
    "core_objective": "maximize number of disjoint pairings between two groups",
    "key_algorithms": ["Hopcroft-Karp O(E√V)", "Max Flow reduction O(VE)"],
    "slot_template": {
      "ENTITY_SET_A": {"type": "left_side_items", "maps_to": "left_partition"},
      "ENTITY_SET_B": {"type": "right_side_items", "maps_to": "right_partition"},
      "RELATION_C": {"type": "compatible_pairs", "maps_to": "allowed_edges"},
      "OBJECTIVE": "maximize number of one-to-one pairings"
    },
    "application_domains": [
      "Job matching — match workers to jobs they qualify for",
      "Dating app — match users with compatible partners",
      "School admissions — match students to schools",
      "Resource allocation — assign tasks to machines"
    ]
  },
  "assignment_problem": {
    "name": "Assignment Problem",
    "family": "matching", "complexity": "P",
    "topological_skeleton": "Complete bipartite graph with costs on edges. Assign each left vertex to exactly one right vertex.",
    "canonical_description": "Assign each agent to exactly one task to minimize total cost (or maximize total profit).",
    "core_objective": "minimize sum of assignment costs (one-to-one mapping)",
    "key_algorithms": ["Hungarian Algorithm O(n^3)", "Min-Cost Flow reduction"],
    "slot_template": {
      "ENTITY_SET_A": {"type": "agents_or_workers", "maps_to": "row_vertices"},
      "ENTITY_SET_B": {"type": "tasks_or_jobs", "maps_to": "column_vertices"},
      "ATTRIBUTE_D": {"type": "assignment_cost", "maps_to": "edge_costs"},
      "OBJECTIVE": "minimize total assignment cost (every agent assigned to one task)"
    },
    "application_domains": [
      "Workforce scheduling — assign workers to shifts",
      "Machine allocation — assign jobs to machines minimizing setup",
      "Ride-hailing — match drivers to riders minimizing wait time",
      "Sensor network — assign sensors to targets"
    ]
  },
  "stable_marriage": {
    "name": "Stable Marriage",
    "family": "matching", "complexity": "P",
    "topological_skeleton": "Two equal-size sets, each member has a ranked preference list over the other set.",
    "canonical_description": "Find a perfect matching between two equal-sized sets where no pair prefers each other over their current match.",
    "core_objective": "find a stable perfect matching (no blocking pairs)",
    "key_algorithms": ["Gale-Shapley O(n^2)"],
    "slot_template": {
      "ENTITY_SET_A": {"type": "proposers", "maps_to": "set_A_with_preferences"},
      "ENTITY_SET_B": {"type": "receivers", "maps_to": "set_B_with_preferences"},
      "RELATION_C": {"type": "preference_rankings", "maps_to": "ranked_edge_weights"},
      "OBJECTIVE": "find stable pairing where no two prefer each other over current match"
    },
    "application_domains": [
      "Medical residency matching (NRMP)",
      "School choice systems",
      "Organ donation matching",
      "Server-client pairing with quality preferences"
    ]
  },

  # ===== COVERING & PARTITIONING (8) =====
  "vertex_cover": {
    "name": "Minimum Vertex Cover",
    "family": "covering", "complexity": "NP-hard (P for bipartite)",
    "topological_skeleton": "Undirected graph. Select minimum set of vertices such that every edge is incident to at least one selected vertex.",
    "canonical_description": "Find the smallest set of vertices that touches every edge in the graph.",
    "core_objective": "minimize number of selected vertices covering all edges",
    "key_algorithms": ["2-approximation (maximal matching)", "ILP for optimal", "Kőnig's theorem for bipartite"],
    "slot_template": {
      "ENTITY_SET_A": {"type": "locations_to_guard", "maps_to": "vertices"},
      "RELATION_C": {"type": "connections_to_cover", "maps_to": "edges"},
      "OBJECTIVE": "minimize number of guarded locations covering all connections"
    },
    "application_domains": [
      "Security camera placement — cover all corridors",
      "Influencer selection — reach all social connections",
      "Chip testing — select minimum test points covering all circuits"
    ]
  },
  "set_cover": {
    "name": "Minimum Set Cover",
    "family": "covering", "complexity": "NP-hard",
    "topological_skeleton": "Universe of elements, collection of subsets. Select minimum number of subsets covering all elements.",
    "canonical_description": "Given a universe of elements and a collection of sets that cover subsets of elements, find the smallest subcollection covering all elements.",
    "core_objective": "minimize number of selected sets covering all elements",
    "key_algorithms": ["Greedy (ln n)-approximation", "ILP for optimal", "Primal-Dual"],
    "slot_template": {
      "ENTITY_SET_A": {"type": "elements_to_cover", "maps_to": "universe"},
      "ENTITY_SET_B": {"type": "covering_options", "maps_to": "family_of_sets"},
      "OBJECTIVE": "minimize number of selected options covering all elements"
    },
    "application_domains": [
      "Crew scheduling — cover all flights with minimum crews",
      "Sensor placement — cover all regions with minimum sensors",
      "Test selection — cover all faults with minimum test cases",
      "Document summarization — cover all key points with minimum sentences"
    ]
  },
  "graph_coloring": {
    "name": "Graph Coloring",
    "family": "covering", "complexity": "NP-hard",
    "topological_skeleton": "Undirected graph. Assign colors to vertices such that no adjacent vertices share a color. Minimize colors.",
    "canonical_description": "Color the vertices of a graph with the minimum number of colors such that no two adjacent vertices share the same color.",
    "core_objective": "minimize number of colors used (chromatic number)",
    "key_algorithms": ["Greedy coloring O(V+E)", "DSATUR", "Backtracking for optimal", "ILP"],
    "slot_template": {
      "ENTITY_SET_A": {"type": "items_to_schedule", "maps_to": "vertices"},
      "RELATION_C": {"type": "conflicts", "maps_to": "edges_mutual_exclusion"},
      "OBJECTIVE": "minimize number of time slots (colors) avoiding conflicts"
    },
    "application_domains": [
      "Exam scheduling — avoid time conflicts for shared students",
      "Register allocation — assign CPU registers to variables",
      "Frequency assignment — assign radio frequencies avoiding interference",
      "Meeting scheduling — schedule meetings with disjoint participants"
    ]
  },
  "maximum_clique": {
    "name": "Maximum Clique",
    "family": "covering", "complexity": "NP-hard",
    "topological_skeleton": "Undirected graph. Find the largest set of mutually adjacent vertices.",
    "canonical_description": "Find the largest complete subgraph (clique) in a given graph.",
    "core_objective": "maximize size of completely connected vertex subset",
    "key_algorithms": ["Bron–Kerbosch (exponential)", "Branch and Bound", "ILP"],
    "slot_template": {
      "ENTITY_SET_A": {"type": "entities", "maps_to": "vertices"},
      "RELATION_C": {"type": "mutual_compatibility", "maps_to": "edges"},
      "OBJECTIVE": "find largest group where everyone is mutually compatible"
    },
    "application_domains": [
      "Social network — find largest group of mutual friends",
      "Bioinformatics — find largest set of mutually similar proteins",
      "Computer vision — find largest set of mutually consistent feature matches"
    ]
  },
  "minimum_dominating_set": {
    "name": "Minimum Dominating Set",
    "family": "covering", "complexity": "NP-hard",
    "topological_skeleton": "Undirected graph. Select minimum vertices such that every vertex is either selected or adjacent to a selected vertex.",
    "canonical_description": "Find the smallest subset of vertices such that every vertex is either in the subset or adjacent to a vertex in the subset.",
    "core_objective": "minimize number of dominating vertices covering all vertices",
    "key_algorithms": ["Greedy (ln n+1)-approximation", "ILP for optimal"],
    "slot_template": {
      "ENTITY_SET_A": {"type": "locations_in_network", "maps_to": "vertices"},
      "RELATION_C": {"type": "reachability", "maps_to": "edges"},
      "OBJECTIVE": "minimize number of selected locations reaching all others in one hop"
    },
    "application_domains": [
      "Fire station placement — cover all neighborhoods within response range",
      "Router placement — cover all devices in wireless network",
      "Vaccination strategy — immunize key individuals to protect population"
    ]
  },
  "minimum_cut": {
    "name": "Minimum Cut",
    "family": "covering", "complexity": "P",
    "topological_skeleton": "Undirected weighted graph. Partition vertices into two sets minimizing total weight of crossing edges.",
    "canonical_description": "Partition the vertices of a weighted graph into two disjoint subsets minimizing the sum of weights of edges crossing between them.",
    "core_objective": "minimize total weight of edges between two vertex partitions",
    "key_algorithms": ["Stoer-Wagner O(V^3)", "Max Flow reduction for s-t cut"],
    "slot_template": {
      "ENTITY_SET_A": {"type": "items_to_separate", "maps_to": "vertex_set_left"},
      "ENTITY_SET_B": {"type": "items_to_separate", "maps_to": "vertex_set_right"},
      "RELATION_C": {"type": "connections_to_sever", "maps_to": "edges"},
      "ATTRIBUTE_D": {"type": "severance_cost", "maps_to": "edge_weights"},
      "OBJECTIVE": "minimize total cost of connections severed between two groups"
    },
    "application_domains": [
      "Image segmentation — separate foreground from background",
      "Community detection — split network into two communities",
      "Network reliability — find weakest link in network"
    ]
  },

  # ===== TOURING & ROUTING (8) =====
  "tsp": {
    "name": "Traveling Salesman Problem",
    "family": "touring", "complexity": "NP-hard",
    "topological_skeleton": "Complete weighted graph. Find minimum-weight Hamiltonian cycle.",
    "canonical_description": "Find the shortest possible route that visits each city exactly once and returns to the origin.",
    "core_objective": "minimize total tour length visiting all vertices exactly once",
    "key_algorithms": ["Held-Karp DP O(n^2 2^n)", "Christofides 1.5-approximation", "Lin-Kernighan heuristic", "Concorde (exact)"],
    "slot_template": {
      "ENTITY_SET_A": {"type": "locations_to_visit", "maps_to": "all_vertices"},
      "RELATION_C": {"type": "travel_connections", "maps_to": "complete_edges"},
      "ATTRIBUTE_D": {"type": "travel_cost_or_distance", "maps_to": "edge_weights"},
      "OBJECTIVE": "minimize total travel cost visiting all locations and returning"
    },
    "application_domains": [
      "Delivery route — optimize order of stops",
      "PCB drilling — minimize drill head travel time",
      "DNA sequencing — optimize probe order",
      "Tour planning — plan optimal sightseeing route"
    ]
  },
  "vrp": {
    "name": "Vehicle Routing Problem",
    "family": "touring", "complexity": "NP-hard",
    "topological_skeleton": "Complete weighted graph with depot vertex and customer vertices. Multiple vehicles with capacity constraints.",
    "canonical_description": "Determine optimal routes for a fleet of vehicles to deliver goods to customers, minimizing total distance while respecting vehicle capacities.",
    "core_objective": "minimize total route distance respecting vehicle capacity and depot constraints",
    "key_algorithms": ["Clarke-Wright savings", "Sweep algorithm", "Branch-and-Cut", "Metaheuristics (ALNS, GA)"],
    "slot_template": {
      "ENTITY_SET_A": {"type": "depot", "maps_to": "depot_vertex"},
      "ENTITY_SET_B": {"type": "customers", "maps_to": "customer_vertices"},
      "RELATION_C": {"type": "roads", "maps_to": "edges"},
      "ATTRIBUTE_D": {"type": "travel_distance", "maps_to": "edge_weights"},
      "ATTRIBUTE_E": {"type": "customer_demand", "maps_to": "vertex_demands"},
      "ATTRIBUTE_F": {"type": "vehicle_capacity", "maps_to": "global_capacity_constraint"},
      "OBJECTIVE": "minimize total fleet travel distance"
    },
    "application_domains": [
      "Last-mile delivery — optimize package delivery routes",
      "Waste collection — plan garbage truck routes",
      "School bus routing — pick up students efficiently",
      "Home healthcare — schedule nurse visits"
    ]
  }
}

from ontology_add1 import ADD1 as _A1
from ontology_add2 import ADD2 as _A2
from ontology_add3 import ADD3 as _A3
ONTOLOGY.update(_A1)
ONTOLOGY.update(_A2)
ONTOLOGY.update(_A3)


def get_all_problems():
    return list(ONTOLOGY.keys())

def get_problem(problem_id):
    return ONTOLOGY.get(problem_id, None)

def get_problems_by_family(family):
    return {k:v for k,v in ONTOLOGY.items() if v["family"] == family}

def get_family_counts():
    from collections import Counter
    return Counter(v["family"] for v in ONTOLOGY.values())

def generate_descriptions(problem_id, num_per_domain=3):
    """Generate sample problem descriptions for embedding training."""
    import random
    problem = ONTOLOGY[problem_id]
    templates = {
        "gps": "Find the {adj} route from {loc_a} to {loc_b} given the {attr} between them.",
        "network": "Route data packets from {loc_a} to {loc_b} through the network to {obj}.",
        "logistics": "A logistics company needs to transport goods from {loc_a} to {loc_b}. {attr} varies by route. {obj}.",
        "biology": "In the {adj} network, determine the optimal path from {loc_a} to {loc_b} to {obj}.",
        "finance": "Find the sequence of transactions from {loc_a} to {loc_b} that {obj} given {attr}.",
    }
    variations = []
    domains = problem.get("application_domains", [])
    for d in domains[:5]:
        for i in range(num_per_domain):
            t = random.choice(list(templates.values()))
            desc = t.format(
                adj=random.choice(["fastest", "shortest", "cheapest", "optimal"]),
                loc_a=random.choice(["Warehouse A", "Node Alpha", "Point X", "Origin"]),
                loc_b=random.choice(["Warehouse B", "Node Beta", "Point Y", "Destination"]),
                attr=random.choice(["travel time", "distance", "cost", "congestion"]),
                obj=problem["core_objective"]
            )
            variations.append({"description": desc, "domain": d, "problem_id": problem_id})
    return variations

def save_ontology(path=None):
    if path is None:
        path = os.path.join(ONTOLOGY_DIR, "results", "ontology.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(ONTOLOGY, f, indent=2)
    print(f"Ontology saved: {path} ({len(ONTOLOGY)} problems)")

if __name__ == "__main__":
    counts = get_family_counts()
    print("Ontology Summary:")
    for family, count in counts.items():
        print(f"  {family}: {count} problems")
    print(f"  Total: {len(ONTOLOGY)} problems")
    save_ontology()
