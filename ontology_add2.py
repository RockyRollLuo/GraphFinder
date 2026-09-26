# Chunk 2: MATCHING (+7) and COVERING (+8) additions
ADD2 = {
  "max_weighted_matching": {
    "name": "Maximum Weighted Matching", "family": "matching", "complexity": "P",
    "topological_skeleton": "Undirected weighted graph; select disjoint edges maximizing total weight.",
    "canonical_description": "Select a set of vertex-disjoint edges maximizing the sum of their weights.",
    "core_objective": "maximize total weight of disjoint edges",
    "key_algorithms": ["Edmonds' Blossom O(V^3)", "Primal-dual O(VE log V)"],
    "slot_template": {"ENTITY_SET_A": {"type": "left_entities", "maps_to": "vertices"}, "ENTITY_SET_B": {"type": "right_entities", "maps_to": "vertices"}, "RELATION_C": {"type": "compatibility", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "benefit", "maps_to": "edge_weights"}, "OBJECTIVE": "maximize total matching weight"},
    "application_domains": ["Ride-sharing pairing", "Protein docking", "Ad-auction winner selection"]
  },
  "perfect_matching": {
    "name": "Perfect Matching", "family": "matching", "complexity": "P",
    "topological_skeleton": "Undirected graph; partition all vertices into disjoint pairs.",
    "canonical_description": "Pair every vertex with exactly one partner using graph edges; find minimum-cost such pairing.",
    "core_objective": "pair all vertices at minimum cost",
    "key_algorithms": ["Edmonds' Blossom", "ILP for weighted variants"],
    "slot_template": {"ENTITY_SET_A": {"type": "items", "maps_to": "vertices"}, "RELATION_C": {"type": "compatibility", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "pairing_cost", "maps_to": "edge_weights"}, "OBJECTIVE": "minimize total pairing cost"},
    "application_domains": ["Roommate assignment", "Drone task pairing", "Circuit pin matching"]
  },
  "generalized_assignment": {
    "name": "Generalized Assignment", "family": "matching", "complexity": "NP-hard",
    "topological_skeleton": "Bipartite graph of items to bins; each assignment consumes bin capacity with a cost.",
    "canonical_description": "Assign each item to at most one bin respecting bin capacities while minimizing total cost.",
    "core_objective": "minimize assignment cost under capacities",
    "key_algorithms": ["Lagrangian relaxation", "Branch-and-bound"],
    "slot_template": {"ENTITY_SET_A": {"type": "items", "maps_to": "left_vertices"}, "ENTITY_SET_B": {"type": "bins", "maps_to": "right_vertices"}, "RELATION_C": {"type": "possible_assignments", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "cost_and_size", "maps_to": "edge_attributes"}, "OBJECTIVE": "minimize total assignment cost"},
    "application_domains": ["Machine job scheduling", "Warehouse slotting", "Cloud VM placement"]
  },
  "bottleneck_assignment": {
    "name": "Bottleneck Assignment", "family": "matching", "complexity": "P",
    "topological_skeleton": "Bipartite graph with edge costs; minimize the maximum cost of any matched edge.",
    "canonical_description": "Assign every left vertex to a distinct right vertex minimizing the largest assignment cost.",
    "core_objective": "minimize maximum edge cost in perfect matching",
    "key_algorithms": ["Threshold + matching O(V^2.5 log V)"],
    "slot_template": {"ENTITY_SET_A": {"type": "workers", "maps_to": "left_vertices"}, "ENTITY_SET_B": {"type": "tasks", "maps_to": "right_vertices"}, "RELATION_C": {"type": "eligibility", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "completion_time", "maps_to": "edge_costs"}, "OBJECTIVE": "minimize worst-case cost"},
    "application_domains": ["Emergency task dispatch", "Minimize makespan assignments", "Minimax team formation"]
  },
  "min_cost_perfect_matching": {
    "name": "Minimum-Cost Perfect Matching", "family": "matching", "complexity": "P",
    "topological_skeleton": "Undirected weighted graph; perfect matching of minimum total weight.",
    "canonical_description": "Find the perfect matching minimizing total edge weight in an undirected graph.",
    "core_objective": "minimize total weight of perfect matching",
    "key_algorithms": ["Edmonds' weighted Blossom O(V^3)", "T-join reduction"],
    "slot_template": {"ENTITY_SET_A": {"type": "entities", "maps_to": "vertices"}, "RELATION_C": {"type": "pairings", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "cost", "maps_to": "edge_weights"}, "OBJECTIVE": "minimize total pairing cost"},
    "application_domains": ["Carpool formation", "Sensor pairing", "Peer review assignment"]
  },
  "capacitated_assignment": {
    "name": "Capacitated Assignment", "family": "matching", "complexity": "NP-hard",
    "topological_skeleton": "Bipartite graph where right vertices have capacities on matched degree.",
    "canonical_description": "Assign items to capacitated bins so each bin takes at most its capacity, minimizing cost.",
    "core_objective": "minimize cost under vertex capacities",
    "key_algorithms": ["Min-cost flow on bipartite graph", "ILP"],
    "slot_template": {"ENTITY_SET_A": {"type": "items", "maps_to": "left_vertices"}, "ENTITY_SET_B": {"type": "slots", "maps_to": "right_vertices"}, "RELATION_C": {"type": "assignments", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "cost_and_capacity", "maps_to": "edge_attributes"}, "OBJECTIVE": "minimize total cost"},
    "application_domains": ["Classroom seating", "Cloud resource allocation", "Staff shift assignment"]
  },
  "online_bipartite_matching": {
    "name": "Online Bipartite Matching", "family": "matching", "complexity": "NP-hard",
    "topological_skeleton": "Right vertices arrive sequentially; match irrevocably upon arrival.",
    "canonical_description": "Match arriving items to limited-capacity servers online without knowing future arrivals.",
    "core_objective": "maximize total online matched value",
    "key_algorithms": ["Greedy (1/2-competitive)", "Ranking (1-1/e)-competitive"],
    "slot_template": {"ENTITY_SET_A": {"type": "arriving_items", "maps_to": "online_vertices"}, "ENTITY_SET_B": {"type": "servers", "maps_to": "offline_vertices"}, "RELATION_C": {"type": "eligibility", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "value", "maps_to": "edge_weights"}, "OBJECTIVE": "maximize online matching value"},
    "application_domains": ["Ride-hailing dispatch", "Ad impression allocation", "Online kidney exchange"]
  },
  "edge_coloring": {
    "name": "Edge Coloring", "family": "covering", "complexity": "NP-hard",
    "topological_skeleton": "Undirected graph; color edges so incident edges differ; minimize colors.",
    "canonical_description": "Assign colors to edges such that no two adjacent edges share a color, using the minimum number of colors.",
    "core_objective": "minimize number of edge colors",
    "key_algorithms": ["Vizing approximation Delta+1", "ILP"],
    "slot_template": {"ENTITY_SET_A": {"type": "edges", "maps_to": "edges"}, "RELATION_C": {"type": "incidence", "maps_to": "adjacency"}, "ATTRIBUTE_D": {"type": "color", "maps_to": "edge_colors"}, "OBJECTIVE": "minimize color count"},
    "application_domains": ["Exam timetable scheduling", "Wavelength assignment in optics", "Sports round scheduling"]
  },
  "maximum_independent_set": {
    "name": "Maximum Independent Set", "family": "covering", "complexity": "NP-hard",
    "topological_skeleton": "Undirected graph; largest set of mutually non-adjacent vertices.",
    "canonical_description": "Select the maximum number of vertices such that no two selected vertices share an edge.",
    "core_objective": "maximize size of pairwise non-adjacent set",
    "key_algorithms": ["Branch-and-bound", "SDP relaxation", "Kernelization + FPT"],
    "slot_template": {"ENTITY_SET_A": {"type": "items", "maps_to": "vertices"}, "RELATION_C": {"type": "conflicts", "maps_to": "edges"}, "OBJECTIVE": "maximize selected non-conflicting items"},
    "application_domains": ["Frequency assignment avoiding interference", "Protein side-chain packing", "Scheduling non-conflicting jobs"]
  },
  "minimum_edge_dominating_set": {
    "name": "Minimum Edge Dominating Set", "family": "covering", "complexity": "NP-hard",
    "topological_skeleton": "Undirected graph; smallest edge set whose adjacent edges cover all edges.",
    "canonical_description": "Select the minimum number of edges such that every edge shares an endpoint with a selected edge.",
    "core_objective": "minimize size of edge dominating set",
    "key_algorithms": ["Reduction to edge cover", "ILP"],
    "slot_template": {"ENTITY_SET_A": {"type": "edges", "maps_to": "edges"}, "RELATION_C": {"type": "adjacency", "maps_to": "edge_adjacency"}, "OBJECTIVE": "minimize selected edge count"},
    "application_domains": ["Sensor placement on links", "Network monitoring point selection"]
  },
  "feedback_vertex_set": {
    "name": "Feedback Vertex Set", "family": "covering", "complexity": "NP-hard",
    "topological_skeleton": "Directed or undirected graph; remove minimum vertices to eliminate all cycles.",
    "canonical_description": "Delete the minimum number of vertices so the remaining graph is acyclic.",
    "core_objective": "minimize removed vertices to break all cycles",
    "key_algorithms": ["FPT O(2^k n)", "Iterative compression", "2-approximation"],
    "slot_template": {"ENTITY_SET_A": {"type": "nodes", "maps_to": "vertices"}, "RELATION_C": {"type": "dependencies", "maps_to": "edges"}, "OBJECTIVE": "minimize deletions for acyclicity"},
    "application_domains": ["Deadlock resolution in OS", "Feedback loop elimination in circuits", "Dependency cycle breaking"]
  },
  "min_st_cut": {
    "name": "Minimum s-t Cut", "family": "covering", "complexity": "P",
    "topological_skeleton": "Directed weighted graph; partition separating source from sink minimizing cut capacity.",
    "canonical_description": "Remove edges of minimum total capacity so that no path remains from source to sink.",
    "core_objective": "minimize capacity of s-t separating cut",
    "key_algorithms": ["Max-flow min-cut O(V^2 E)"],
    "slot_template": {"ENTITY_SET_A": {"type": "protected_source", "maps_to": "source"}, "ENTITY_SET_B": {"type": "blocked_sink", "maps_to": "sink"}, "RELATION_C": {"type": "links", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "capacity", "maps_to": "edge_capacities"}, "OBJECTIVE": "minimize cut capacity"},
    "application_domains": ["Network security isolation", "Image segmentation (graph cuts)", "Supply chain disruption analysis"]
  },
  "multiway_cut": {
    "name": "Multiway Cut", "family": "covering", "complexity": "NP-hard",
    "topological_skeleton": "Graph with k terminal vertices; separate all terminals from each other.",
    "canonical_description": "Remove minimum-weight edges so that no path connects any pair of distinguished terminals.",
    "core_objective": "minimize weight of edges separating all terminals",
    "key_algorithms": ["2-2/k approximation", "Isolation heuristic", "SDP relaxation"],
    "slot_template": {"ENTITY_SET_A": {"type": "terminals", "maps_to": "terminal_vertices"}, "RELATION_C": {"type": "links", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "removal_cost", "maps_to": "edge_weights"}, "OBJECTIVE": "minimize separation cost"},
    "application_domains": ["Multi-class image segmentation", "Firewall placement between zones", "Contraband interdiction"]
  },
  "minimum_bisection": {
    "name": "Minimum Bisection", "family": "covering", "complexity": "NP-hard",
    "topological_skeleton": "Undirected graph; split into two equal-sized halves minimizing crossing edges.",
    "canonical_description": "Partition vertices into two sets of equal size minimizing the number of edges between them.",
    "core_objective": "minimize crossing edges under balanced partition",
    "key_algorithms": ["Spectral partitioning", "Multilevel Kernighan-Lin", "SDP approximation"],
    "slot_template": {"ENTITY_SET_A": {"type": "vertices", "maps_to": "vertices"}, "RELATION_C": {"type": "links", "maps_to": "edges"}, "OBJECTIVE": "minimize cross-partition edges"},
    "application_domains": ["Parallel workload partitioning", "VLSI layout", "Community detection"]
  },
  "sparsest_cut": {
    "name": "Sparsest Cut", "family": "covering", "complexity": "NP-hard",
    "topological_skeleton": "Undirected graph; find cut minimizing edge-weight to separated-vertex ratio.",
    "canonical_description": "Find the cut minimizing the ratio of cut weight to the product of separated side sizes.",
    "core_objective": "minimize cut sparsity ratio",
    "key_algorithms": ["SDP rounding O(sqrt(log n))", "Spectral heuristics"],
    "slot_template": {"ENTITY_SET_A": {"type": "vertices", "maps_to": "vertices"}, "RELATION_C": {"type": "links", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "edge_cost", "maps_to": "edge_weights"}, "OBJECTIVE": "minimize sparsity ratio"},
    "application_domains": ["Bottleneck identification in networks", "Graph clustering", "Load balancing"]
  },
}
print("chunk2 done:", len(ADD2))
