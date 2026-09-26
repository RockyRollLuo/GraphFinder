# Chunk 1: PATH (+4) and FLOW (+6) additions
ADD1 = {
  "rural_postman": {
    "name": "Rural Postman", "family": "path", "complexity": "NP-hard",
    "topological_skeleton": "Undirected weighted graph; only a required subset of edges must be traversed; may duplicate other edges.",
    "canonical_description": "Traverse all required edges of a weighted graph at minimum total cost, optionally traversing additional edges to connect components.",
    "core_objective": "minimize total traversal cost covering a required edge subset",
    "key_algorithms": ["ILP", "T-join reduction", "branch-and-cut"],
    "slot_template": {"ENTITY_SET_A": {"type": "mandatory_segments", "maps_to": "required_edges"}, "RELATION_C": {"type": "connections", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "traversal_cost", "maps_to": "edge_weights"}, "OBJECTIVE": "minimize total traversal cost"},
    "application_domains": ["Street sweeping covering specified streets", "Mail delivery on selected routes", "Snow plowing of priority roads"]
  },
  "k_shortest_paths": {
    "name": "K Shortest Paths", "family": "path", "complexity": "P",
    "topological_skeleton": "Weighted directed graph; single source, single target; enumerate k shortest simple paths.",
    "canonical_description": "Find the k shortest simple paths from a source to a target in a weighted graph, ordered by total weight.",
    "core_objective": "enumerate k paths minimizing total weight in order",
    "key_algorithms": ["Yen's algorithm O(kV(E+V log V))", "Eppstein O(E+V log V+k)"],
    "slot_template": {"ENTITY_SET_A": {"type": "origin", "maps_to": "source"}, "ENTITY_SET_B": {"type": "destination", "maps_to": "target"}, "RELATION_C": {"type": "transitions", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "cost", "maps_to": "edge_weights"}, "OBJECTIVE": "minimize path costs for top-k"},
    "application_domains": ["Backup routes in transportation", "Alternative itineraries in navigation", "Risk-diversified network routing"]
  },
  "widest_path": {
    "name": "Widest Path", "family": "path", "complexity": "P",
    "topological_skeleton": "Graph with edge capacities (bottleneck weights); single source, single target.",
    "canonical_description": "Find the path between two vertices that maximizes the minimum edge capacity along the path.",
    "core_objective": "maximize the minimum edge weight along a path",
    "key_algorithms": ["Modified Dijkstra O(E log V)", "Max spanning tree path"],
    "slot_template": {"ENTITY_SET_A": {"type": "sender", "maps_to": "source"}, "ENTITY_SET_B": {"type": "receiver", "maps_to": "target"}, "RELATION_C": {"type": "channels", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "bandwidth", "maps_to": "edge_capacities"}, "OBJECTIVE": "maximize bottleneck capacity"},
    "application_domains": ["Maximum-bandwidth internet routing", "Heavy-load truck routing", "Pipeline throughput maximization"]
  },
  "all_pairs_shortest_paths": {
    "name": "All-Pairs Shortest Paths", "family": "path", "complexity": "P",
    "topological_skeleton": "Weighted directed graph; shortest paths between every ordered pair of vertices.",
    "canonical_description": "Compute the shortest path distances between every pair of vertices in a weighted graph.",
    "core_objective": "minimize path weight for all vertex pairs",
    "key_algorithms": ["Floyd-Warshall O(V^3)", "Johnson O(VE+V^2 log V)"],
    "slot_template": {"ENTITY_SET_A": {"type": "all_nodes", "maps_to": "all_vertices"}, "RELATION_C": {"type": "links", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "distance", "maps_to": "edge_weights"}, "OBJECTIVE": "minimize all pairwise distances"},
    "application_domains": ["Road network distance tables", "Airline hub connectivity analysis", "Social network closeness computation"]
  },
  "circulation": {
    "name": "Circulation", "family": "flow", "complexity": "P",
    "topological_skeleton": "Directed graph with lower and upper bounds per edge; flow conservation at every vertex.",
    "canonical_description": "Find a feasible flow assignment satisfying edge lower and upper bounds with conservation at every node.",
    "core_objective": "find feasible flow respecting bounds",
    "key_algorithms": ["Reduction to max flow O(VE log V)", "Cycle cancellation"],
    "slot_template": {"ENTITY_SET_A": {"type": "nodes", "maps_to": "vertices"}, "RELATION_C": {"type": "channels", "maps_to": "directed_edges"}, "ATTRIBUTE_D": {"type": "min_max_bounds", "maps_to": "edge_bounds"}, "OBJECTIVE": "feasibility of bounded flow"},
    "application_domains": ["Production planning with quotas", "Network load balancing", "Staff scheduling with constraints"]
  },
  "max_bipartite_flow": {
    "name": "Maximum Bipartite Flow", "family": "flow", "complexity": "P",
    "topological_skeleton": "Bipartite directed network from left partition through right partition to sink with edge capacities.",
    "canonical_description": "Maximize total flow in a bipartite network where edges only connect the two partitions.",
    "core_objective": "maximize total flow in bipartite network",
    "key_algorithms": ["Ford-Fulkerson O(VE)", "Hopcroft-Karp specialization O(E sqrt(V))"],
    "slot_template": {"ENTITY_SET_A": {"type": "suppliers", "maps_to": "left_partition"}, "ENTITY_SET_B": {"type": "consumers", "maps_to": "right_partition"}, "RELATION_C": {"type": "channels", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "capacity", "maps_to": "edge_capacities"}, "OBJECTIVE": "maximize total flow"},
    "application_domains": ["Ad-server allocation", "Sensor-to-processor data assignment", "Two-sided market matching"]
  },
  "min_cost_max_flow": {
    "name": "Minimum-Cost Maximum Flow", "family": "flow", "complexity": "P",
    "topological_skeleton": "Directed graph with capacities and costs per edge; send maximum possible flow at minimum cost.",
    "canonical_description": "Among all maximum flows, find the one minimizing total edge cost.",
    "core_objective": "minimize cost among maximum flows",
    "key_algorithms": ["Successive shortest path", "Cost-scaling O(V^2 E log VC)"],
    "slot_template": {"ENTITY_SET_A": {"type": "sources", "maps_to": "source"}, "ENTITY_SET_B": {"type": "destinations", "maps_to": "sink"}, "RELATION_C": {"type": "routes", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "cost_and_capacity", "maps_to": "edge_attributes"}, "OBJECTIVE": "minimize cost at max throughput"},
    "application_domains": ["Telecom bandwidth allocation", "Evacuation planning", "Logistics at full utilization"]
  },
  "generalized_flow": {
    "name": "Generalized Flow", "family": "flow", "complexity": "NP-hard",
    "topological_skeleton": "Directed graph where each edge has a gain/loss multiplier applied to flow traversing it.",
    "canonical_description": "Maximize flow from source to sink where each edge multiplies flow by a gain factor.",
    "core_objective": "maximize flow with multiplicative edge gains",
    "key_algorithms": ["Linear programming", "Approximation via gain cycles"],
    "slot_template": {"ENTITY_SET_A": {"type": "source", "maps_to": "source"}, "ENTITY_SET_B": {"type": "sink", "maps_to": "sink"}, "RELATION_C": {"type": "transfers", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "gain_factor", "maps_to": "edge_multipliers"}, "OBJECTIVE": "maximize surviving flow"},
    "application_domains": ["Currency conversion arbitrage", "Water distribution with leakage", "Energy transmission loss"]
  },
  "dynamic_flow": {
    "name": "Dynamic Flow", "family": "flow", "complexity": "NP-hard",
    "topological_skeleton": "Network with edge transit times; flow evolves over a time horizon.",
    "canonical_description": "Maximize flow delivered to the sink within a time horizon given edge transit times.",
    "core_objective": "maximize flow over time window",
    "key_algorithms": ["Time-expanded network", "Temporally repeated flows"],
    "slot_template": {"ENTITY_SET_A": {"type": "origin", "maps_to": "source"}, "ENTITY_SET_B": {"type": "destination", "maps_to": "sink"}, "RELATION_C": {"type": "links", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "capacity_and_transit_time", "maps_to": "edge_attributes"}, "OBJECTIVE": "maximize time-bounded flow"},
    "application_domains": ["Evacuation over time", "Traffic flow forecasting", "Supply delivery scheduling"]
  },
  "unsplittable_flow": {
    "name": "Unsplittable Flow", "family": "flow", "complexity": "NP-hard",
    "topological_skeleton": "Commodity demands must be routed along single paths without splitting.",
    "canonical_description": "Route indivisible commodity demands through a capacitated network to maximize throughput.",
    "core_objective": "maximize routed unsplittable demand",
    "key_algorithms": ["LP rounding", "Greedy + randomized rounding"],
    "slot_template": {"ENTITY_SET_A": {"type": "demand_pairs", "maps_to": "commodities"}, "RELATION_C": {"type": "links", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "capacity_and_demand", "maps_to": "edge_attributes"}, "OBJECTIVE": "maximize satisfied demand"},
    "application_domains": ["VPN tunnel routing", "Dedicated circuit provisioning", "Bulk data transfer scheduling"]
  },
}
print("chunk1 done:", len(ADD1))
