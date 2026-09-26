# Chunk 3: TOURING (+9) additions
ADD3 = {
  "capacitated_vrp": {
    "name": "Capacitated VRP", "family": "touring", "complexity": "NP-hard",
    "topological_skeleton": "Depot plus customers with demands; vehicles with capacities; minimize total route length.",
    "canonical_description": "Serve all customers with a fleet of capacity-limited vehicles from a depot minimizing total travel.",
    "core_objective": "minimize total route length under vehicle capacities",
    "key_algorithms": ["Clarke-Wright savings", "Branch-and-cut", "ALNS metaheuristic"],
    "slot_template": {"ENTITY_SET_A": {"type": "customers", "maps_to": "vertices"}, "ENTITY_SET_B": {"type": "depot", "maps_to": "depot"}, "RELATION_C": {"type": "roads", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "demand_and_capacity", "maps_to": "vertex_and_vehicle_attributes"}, "OBJECTIVE": "minimize total route cost"},
    "application_domains": ["Beverage distribution", "Grocery delivery", "Waste collection routing"]
  },
  "prize_collecting_tsp": {
    "name": "Prize-Collecting TSP", "family": "touring", "complexity": "NP-hard",
    "topological_skeleton": "Complete metric graph with node prizes and penalties; visiting is optional.",
    "canonical_description": "Choose which cities to visit to balance collected prizes against travel cost and penalties.",
    "core_objective": "maximize prize minus travel cost minus penalties",
    "key_algorithms": ["Primal-dual approximation", "Iterative rounding"],
    "slot_template": {"ENTITY_SET_A": {"type": "optional_stops", "maps_to": "vertices"}, "RELATION_C": {"type": "routes", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "prize_and_cost", "maps_to": "vertex_prizes_edge_costs"}, "OBJECTIVE": "maximize net reward"},
    "application_domains": ["Sales territory planning", "Geocaching route design", "Inspection scheduling"]
  },
  "orienteering": {
    "name": "Orienteering", "family": "touring", "complexity": "NP-hard",
    "topological_skeleton": "Graph with node scores and a travel budget; select route within budget maximizing score.",
    "canonical_description": "Visit nodes to maximize collected score while keeping total travel within a time budget.",
    "core_objective": "maximize collected score under budget",
    "key_algorithms": ["DP on tree decomposition", "Greedy + ILP", "Iterative local search"],
    "slot_template": {"ENTITY_SET_A": {"type": "points_of_interest", "maps_to": "vertices"}, "RELATION_C": {"type": "paths", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "score_and_time", "maps_to": "vertex_scores_edge_times"}, "OBJECTIVE": "maximize score within budget"},
    "application_domains": ["Tourist itinerary planning", "Field data collection", "Drone survey planning"]
  },
  "dial_a_ride": {
    "name": "Dial-a-Ride", "family": "touring", "complexity": "NP-hard",
    "topological_skeleton": "Pickup and delivery requests with time windows; shared vehicles.",
    "canonical_description": "Schedule shared vehicle routes serving pickup-dropoff requests within time windows.",
    "core_objective": "minimize cost while satisfying time windows",
    "key_algorithms": ["ILP", "Column generation", "Adaptive large neighborhood search"],
    "slot_template": {"ENTITY_SET_A": {"type": "requests", "maps_to": "commodities"}, "RELATION_C": {"type": "trips", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "time_windows", "maps_to": "temporal_constraints"}, "OBJECTIVE": "minimize total travel time"},
    "application_domains": ["Paratransit services", "Airport shuttle pooling", "Hospital patient transport"]
  },
  "arc_routing": {
    "name": "Arc Routing", "family": "touring", "complexity": "NP-hard",
    "topological_skeleton": "Directed graph where required arcs must be traversed; start and end at depot.",
    "canonical_description": "Traverse all required directed arcs at minimum cost, starting and ending at a depot.",
    "core_objective": "minimize traversal cost covering required arcs",
    "key_algorithms": ["Directed rural postman reduction", "Branch-and-bound"],
    "slot_template": {"ENTITY_SET_A": {"type": "required_arcs", "maps_to": "required_edges"}, "ENTITY_SET_B": {"type": "depot", "maps_to": "depot"}, "RELATION_C": {"type": "segments", "maps_to": "arcs"}, "ATTRIBUTE_D": {"type": "traversal_cost", "maps_to": "arc_weights"}, "OBJECTIVE": "minimize total traversal cost"},
    "application_domains": ["Street inspection routing", "Meter reading tours", "Gritting one-way streets"]
  },
  "team_orienteering": {
    "name": "Team Orienteering", "family": "touring", "complexity": "NP-hard",
    "topological_skeleton": "Multiple agents start from depot; each has budget; maximize total collected scores.",
    "canonical_description": "Route multiple agents within individual budgets to maximize total score collected from nodes.",
    "core_objective": "maximize total team score under per-agent budgets",
    "key_algorithms": ["Iterated local search", "Ant colony optimization", "Matheuristics"],
    "slot_template": {"ENTITY_SET_A": {"type": "targets", "maps_to": "vertices"}, "ENTITY_SET_B": {"type": "agents", "maps_to": "routes"}, "RELATION_C": {"type": "paths", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "score_and_budget", "maps_to": "vertex_scores_edge_costs"}, "OBJECTIVE": "maximize total collected score"},
    "application_domains": ["Multi-drone inspection", "Tour group planning", "Disaster reconnaissance"]
  },
  "sequential_ordering": {
    "name": "Sequential Ordering", "family": "touring", "complexity": "NP-hard",
    "topological_skeleton": "Directed complete graph with precedence constraints between nodes.",
    "canonical_description": "Find the minimum-cost tour visiting all nodes while respecting precedence constraints.",
    "core_objective": "minimize tour length under precedence constraints",
    "key_algorithms": ["Branch-and-cut with precedence", "DP on partial orders"],
    "slot_template": {"ENTITY_SET_A": {"type": "tasks", "maps_to": "vertices"}, "RELATION_C": {"type": "precedence", "maps_to": "directed_edges"}, "ATTRIBUTE_D": {"type": "transition_cost", "maps_to": "edge_weights"}, "OBJECTIVE": "minimize total transition cost"},
    "application_domains": ["Assembly line sequencing", "Multi-stage production routing", "Protocol ordering"]
  },
  "pickup_and_delivery": {
    "name": "Pickup and Delivery", "family": "touring", "complexity": "NP-hard",
    "topological_skeleton": "Paired pickup and delivery locations; each pair served by same vehicle; pickup precedes delivery.",
    "canonical_description": "Route vehicles to serve paired pickup-delivery requests with precedence and capacity constraints.",
    "core_objective": "minimize routing cost for paired requests",
    "key_algorithms": ["Column generation", "Large neighborhood search", "Branch-and-price"],
    "slot_template": {"ENTITY_SET_A": {"type": "requests", "maps_to": "commodity_pairs"}, "RELATION_C": {"type": "trips", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "load_and_cost", "maps_to": "edge_attributes"}, "OBJECTIVE": "minimize total routing cost"},
    "application_domains": ["Courier services", "Freight forwarding", "Food delivery logistics"]
  },
  "green_vrp": {
    "name": "Green VRP", "family": "touring", "complexity": "NP-hard",
    "topological_skeleton": "VRP variant minimizing fuel/emissions dependent on load, speed, and distance.",
    "canonical_description": "Minimize fuel consumption or emissions of vehicle routes subject to load-dependent costs.",
    "core_objective": "minimize fuel or emission cost",
    "key_algorithms": ["Load-dependent routing models", "NSGA-II", "Adaptive heuristics"],
    "slot_template": {"ENTITY_SET_A": {"type": "customers", "maps_to": "vertices"}, "ENTITY_SET_B": {"type": "depot", "maps_to": "depot"}, "RELATION_C": {"type": "roads", "maps_to": "edges"}, "ATTRIBUTE_D": {"type": "emission_and_demand", "maps_to": "edge_and_vertex_attributes"}, "OBJECTIVE": "minimize total emissions"},
    "application_domains": ["Eco-friendly logistics", "Electric vehicle routing", "Carbon-aware fleet scheduling"]
  },
}
print("chunk3 done:", len(ADD3))
