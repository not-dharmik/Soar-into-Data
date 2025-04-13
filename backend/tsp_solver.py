from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import pandas as pd
import os
import math

EXCEL_PATH = os.path.join("data", "dataset.xlsx")
SCALING_FACTOR = 1000  # To preserve decimal precision for OR-Tools

def haversine(lat1, lon1, lat2, lon2):
    """Great-circle distance using haversine formula in miles."""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 3959 * c  # Earth radius in miles

def create_distance_matrix(coords):
    """Create scaled integer distance matrix from coordinates."""
    n = len(coords)
    matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist = haversine(coords[i][0], coords[i][1], coords[j][0], coords[j][1])
                matrix[i][j] = int(dist * SCALING_FACTOR)
    return matrix

def solve_tsp(distance_matrix, depot_index=0):
    n = len(distance_matrix)
    if n <= 1:
        return [0]

    manager = pywrapcp.RoutingIndexManager(n, 1, depot_index)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        return distance_matrix[manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]

    transit_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_index)

    # ✅ Remove this → routing.SetDepot(depot_index)

    params = pywrapcp.DefaultRoutingSearchParameters()
    params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    params.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    params.time_limit.seconds = 30

    solution = routing.SolveWithParameters(params)
    if not solution:
        return None

    index = routing.Start(0)
    route = []
    while not routing.IsEnd(index):
        route.append(manager.IndexToNode(index))
        index = solution.Value(routing.NextVar(index))
    route.append(manager.IndexToNode(index))  # Include return to depot
    return route


def get_static_route():
    """Return optimal static route starting/ending at UCI ISEB."""
    df = pd.read_excel(EXCEL_PATH)
    iseb_coord = [33.642963, -117.836463]
    iseb_address = "515 E Peltason Dr"

    coords = [iseb_coord] + df[["latitude", "longitude"]].values.tolist()
    addresses = [iseb_address] + df["Address"].tolist()

    dist_matrix = create_distance_matrix(coords)
    tsp_path = solve_tsp(dist_matrix, depot_index=0)

    ordered = [coords[i] for i in tsp_path]
    ordered_addresses = [addresses[i] for i in tsp_path]

    return [{"address": ordered_addresses[i], "lat": ordered[i][0], "lon": ordered[i][1]} for i in range(len(ordered))]

def get_dynamic_route(addresses, start_address):
    """Return optimal route for subset starting at `start_address`."""
    df = pd.read_excel(EXCEL_PATH)

    if start_address not in addresses:
        addresses.append(start_address)

    subset = df[df["Address"].isin(addresses)].copy()
    coords = subset[["latitude", "longitude"]].values.tolist()
    addr_list = subset["Address"].tolist()

    try:
        start_idx = addr_list.index(start_address)
    except ValueError:
        return []

    dist_matrix = create_distance_matrix(coords)
    tsp_path = solve_tsp(dist_matrix, depot_index=start_idx)

    ordered = [coords[i] for i in tsp_path]
    ordered_addresses = [addr_list[i] for i in tsp_path]

    return [{"address": ordered_addresses[i], "lat": ordered[i][0], "lon": ordered[i][1]} for i in range(len(ordered))]












# from ortools.constraint_solver import pywrapcp
# from ortools.constraint_solver import routing_enums_pb2
# import pandas as pd
# import os
# import math
# # Removed networkx import as it wasn't used

# EXCEL_PATH = os.path.join("data", "dataset.xlsx")
# SCALING_FACTOR = 1000 # Scale distances to preserve precision (e.g., 1000 = milli-miles)

# def haversine(lat1, lon1, lat2, lon2):
#     """Calculates the great-circle distance between two points on the Earth."""
#     # Convert to radians
#     lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
#     # Spherical Law of Cosines (3959 miles is approx Earth radius)
#     try:
#         # Use atan2 for better numerical stability with acos near 1 or -1
#         dlon = lon2 - lon1
#         dlat = lat2 - lat1
#         a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
#         c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#         distance = 3959 * c
#         return distance
#     except ValueError:
#         # Handle potential domain errors if points are identical or antipodal
#         if lat1 == lat2 and lon1 == lon2:
#             return 0.0
#         else:
#             # Fallback for potential numerical issues (less common with atan2)
#             return 3959 * math.acos(
#                 max(-1.0, min(1.0, # Clamp value to avoid domain error
#                     math.sin(lat1) * math.sin(lat2) +
#                     math.cos(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)
#                 ))
#             )


# def create_distance_matrix(coords):
#     """Creates a distance matrix using Haversine, scaled for OR-Tools."""
#     n = len(coords)
#     matrix = [[0] * n for _ in range(n)]
#     for i in range(n):
#         for j in range(n):
#             if i != j:
#                 distance = haversine(coords[i][0], coords[i][1], coords[j][0], coords[j][1])
#                 # Scale and convert to integer for OR-Tools
#                 matrix[i][j] = int(distance * SCALING_FACTOR)
#     return matrix

# def solve_tsp(distance_matrix, depot_index=0):
#     """Solves the TSP problem using OR-Tools."""
#     n = len(distance_matrix)
#     if n <= 1: # Handle trivial cases
#         return [0] if n == 1 else [], 0

#     # Create Routing Index Manager
#     # Args: num_nodes, num_vehicles, depot_node_index
#     manager = pywrapcp.RoutingIndexManager(n, 1, depot_index)
#     routing = pywrapcp.RoutingModel(manager)

#     # Create and register a transit callback.
#     def distance_callback(from_index, to_index):
#         """Returns the scaled distance between the two nodes."""
#         from_node = manager.IndexToNode(from_index)
#         to_node = manager.IndexToNode(to_index)
#         return distance_matrix[from_node][to_node]

#     transit_callback_index = routing.RegisterTransitCallback(distance_callback)

#     # Define cost of each arc.
#     routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

#     # Setting first solution heuristic.
#     search_parameters = pywrapcp.DefaultRoutingSearchParameters()
#     search_parameters.first_solution_strategy = (
#         routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
#     # Add local search
#     search_parameters.local_search_metaheuristic = (
#         routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
#     search_parameters.time_limit.seconds = 30 # max runtime

#     # Solve the problem.
#     solution = routing.SolveWithParameters(search_parameters)

#     # --- Extract solution ---
#     if not solution:
#         print("No solution found!")
#         return None, 0 # Return None for path, 0 for distance

#     # Get the route
#     route = []
#     total_distance_scaled = 0
#     index = routing.Start(0) # Start at the vehicle's start node
#     while not routing.IsEnd(index):
#         node_index = manager.IndexToNode(index)
#         route.append(node_index)
#         previous_index = index
#         index = solution.Value(routing.NextVar(index))
#         total_distance_scaled += routing.GetArcCostForVehicle(previous_index, index, 0)

#     # Add the end node (depot) to complete the loop
#     node_index = manager.IndexToNode(index)
#     route.append(node_index)

#     # Convert total distance back to original units (miles)
#     total_distance_miles = total_distance_scaled / SCALING_FACTOR

#     return route, total_distance_miles


# def get_static_route():
#     """Calculates the optimal route starting/ending at ISEB, visiting all other points."""
#     try:
#         df = pd.read_excel(EXCEL_PATH)
#     except FileNotFoundError:
#         print(f"Error: Excel file not found at {EXCEL_PATH}")
#         return None, 0.0

#     # Prepare coordinates and addresses
#     # Ensure ISEB is treated as point 0
#     iseb_coord = [33.6431, -117.8437]
#     other_coords = df[["latitude", "longitude"]].values.tolist()
#     all_coords = [iseb_coord] + other_coords # ISEB is index 0

#     iseb_address = "UCI ISEB"
#     other_addresses = df["Address"].tolist()
#     all_addresses = [iseb_address] + other_addresses # ISEB address is index 0

#     # Create the distance matrix
#     dist_matrix = create_distance_matrix(all_coords)

#     # Solve TSP (depot is 0 by default, which is ISEB)
#     tsp_path_indices, total_distance = solve_tsp(dist_matrix, depot_index=0)

#     if tsp_path_indices is None:
#         print("Failed to solve static TSP.")
#         return None, 0.0

#     # Reorder coordinates and addresses based on the solution path indices
#     # The path includes the return to the depot
#     ordered_coords = [all_coords[i] for i in tsp_path_indices]
#     ordered_addresses = [all_addresses[i] for i in tsp_path_indices]

#     # Format output
#     route_data = [{"address": ordered_addresses[i], "lat": ordered_coords[i][0], "lon": ordered_coords[i][1]}
#                   for i in range(len(ordered_coords))]

#     return route_data, total_distance

# def get_dynamic_route(target_addresses, start_address):
#     """
#     Calculates the optimal route for a subset of addresses,
#     starting and ending at start_address.
#     """
#     try:
#         df = pd.read_excel(EXCEL_PATH)
#     except FileNotFoundError:
#         print(f"Error: Excel file not found at {EXCEL_PATH}")
#         return None, 0.0

#     # Filter subset based on the given addresses
#     # Ensure start_address is included in the target addresses for a valid route
#     if start_address not in target_addresses:
#          target_addresses.append(start_address) # Or handle as an error depending on requirements

#     subset = df[df["Address"].isin(target_addresses)].copy()

#     if subset.empty:
#         print("Error: No matching addresses found in the dataset.")
#         return None, 0.0

#     # Get coordinates and addresses IN THE ORDER OF THE SUBSET DATAFRAME
#     coords = subset[["latitude", "longitude"]].values.tolist()
#     addresses_list = subset["Address"].tolist()

#     # Find the index of the start_address within the subset's lists
#     try:
#         start_idx = addresses_list.index(start_address)
#     except ValueError:
#         print(f"Error: Start address '{start_address}' not found in the filtered subset.")
#         # It should be found because we filtered by target_addresses which includes it,
#         # but this is a safeguard.
#         return None, 0.0

#     # Create the distance matrix for the subset
#     dist_matrix = create_distance_matrix(coords)

#     # Solve TSP, specifying the depot index corresponding to start_address
#     tsp_path_indices, total_distance = solve_tsp(dist_matrix, depot_index=start_idx)

#     if tsp_path_indices is None:
#         print("Failed to solve dynamic TSP.")
#         return None, 0.0

#     # Reorder coordinates and addresses based on the solution path indices
#     # The path includes the return to the depot (start_address)
#     ordered_coords = [coords[i] for i in tsp_path_indices]
#     ordered_addresses = [addresses_list[i] for i in tsp_path_indices]

#     # Format output
#     route_data = [{"address": ordered_addresses[i], "lat": ordered_coords[i][0], "lon": ordered_coords[i][1]}
#                   for i in range(len(ordered_coords))]

#     return route_data, total_distance

# # --- Example Usage (Requires data/dataset.xlsx to exist) ---
# if __name__ == "__main__":
#     # Create dummy data directory and Excel file if they don't exist
#     if not os.path.exists("data"):
#         os.makedirs("data")
#     if not os.path.exists(EXCEL_PATH):
#         print(f"Creating dummy data file at: {EXCEL_PATH}")
#         dummy_data = {
#             'Address': ['Location A', 'Location B', 'Location C', 'Location D'],
#             'latitude': [33.6500, 33.6450, 33.6400, 33.6350],
#             'longitude': [-117.8400, -117.8350, -117.8450, -117.8500]
#         }
#         dummy_df = pd.DataFrame(dummy_data)
#         dummy_df.to_excel(EXCEL_PATH, index=False)
#         print("Dummy data created.")
#     else:
#         print(f"Using existing data file: {EXCEL_PATH}")


#     print("\n--- Static Route Example (All points, start/end ISEB) ---")
#     static_route, static_dist = get_static_route()
#     if static_route:
#         print(f"Total Distance: {static_dist:.2f} miles")
#         print("Route:")
#         for point in static_route:
#             print(f"  - {point['address']} ({point['lat']:.4f}, {point['lon']:.4f})")
#     else:
#         print("Could not calculate static route.")


#     print("\n--- Dynamic Route Example (Subset, start/end Location B) ---")
#     dynamic_addresses = ["Location A", "Location B", "Location C"] # Subset to visit
#     start_point = "Location B"  # Where to start and end the route

#     dynamic_route, dynamic_dist = get_dynamic_route(dynamic_addresses, start_point)

#     if dynamic_route:
#         print(f"Total Distance: {dynamic_dist:.2f} miles")
#         print(f"Route (Starting/Ending at {start_point}):")
#         for point in dynamic_route:
#              print(f"  - {point['address']} ({point['lat']:.4f}, {point['lon']:.4f})")
#         # Verify start/end point
#         if dynamic_route[0]['address'] == start_point and dynamic_route[-1]['address'] == start_point:
#             print(f"Route correctly starts and ends at {start_point}.")
#         else:
#             print(f"Warning: Route does not correctly start/end at {start_point}!")
#             print(f"Starts at: {dynamic_route[0]['address']}, Ends at: {dynamic_route[-1]['address']}")

#     else:
#         print("Could not calculate dynamic route.")

#     print("\n--- Dynamic Route Example (Subset, start/end Location D - not in initial list) ---")
#     dynamic_addresses_2 = ["Location A", "Location C"] # Subset to visit
#     start_point_2 = "Location D"  # Where to start and end the route (will be added)

#     dynamic_route_2, dynamic_dist_2 = get_dynamic_route(dynamic_addresses_2, start_point_2)

#     if dynamic_route_2:
#         print(f"Total Distance: {dynamic_dist_2:.2f} miles")
#         print(f"Route (Starting/Ending at {start_point_2}):")
#         for point in dynamic_route_2:
#              print(f"  - {point['address']} ({point['lat']:.4f}, {point['lon']:.4f})")
#         # Verify start/end point
#         if dynamic_route_2[0]['address'] == start_point_2 and dynamic_route_2[-1]['address'] == start_point_2:
#             print(f"Route correctly starts and ends at {start_point_2}.")
#         else:
#             print(f"Warning: Route does not correctly start/end at {start_point_2}!")
#             print(f"Starts at: {dynamic_route_2[0]['address']}, Ends at: {dynamic_route_2[-1]['address']}")
#     else:
#         print("Could not calculate dynamic route.")











# from networkx.algorithms.approximation import greedy_tsp
# import pandas as pd
# import os
# import math
# import networkx as nx

# EXCEL_PATH = os.path.join("data", "dataset.xlsx")

# def haversine(lat1, lon1, lat2, lon2):
#     # Convert to radians
#     lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
#     # Spherical Law of Cosines
#     return 3959 * math.acos(
#         math.sin(lat1) * math.sin(lat2) +
#         math.cos(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)
#     )

# # Load the Excel file
# df = pd.read_excel(EXCEL_PATH)

# from networkx.algorithms.approximation import greedy_tsp

# def get_static_route():
#     iseb_point = ["UCI ISEB", 33.6431, -117.8437] 
#     # iseb_point = ["UCI", 33.6405, -117.8389]
#     coords = df[["Address", "latitude", "longitude"]].values.tolist()

#     coords.insert(0, iseb_point)

#     G = nx.complete_graph(len(coords))
#     for i in G.nodes:
#         for j in G.nodes:
#             if i != j:
#                 dist = haversine(coords[i][1], coords[i][2], coords[j][1], coords[j][2])
#                 G[i][j]["weight"] = dist

#     tsp_path = greedy_tsp(G, weight="weight", source=0)
#     ordered = [coords[i] for i in tsp_path]

#     return [{"address": r[0], "lat": r[1], "lon": r[2]} for r in ordered]



# def get_dynamic_route(addresses, start_address):
#     subset = df[df["Address"].isin(addresses)].copy()
#     coords = subset[["Address", "latitude", "longitude"]].values.tolist()

#     if start_address not in subset["Address"].values:
#         return []

#     start_idx = next(i for i, r in enumerate(coords) if r[0] == start_address)

#     G = nx.complete_graph(len(coords))
#     for i in G.nodes:
#         for j in G.nodes:
#             if i != j:
#                 dist = haversine(coords[i][1], coords[i][2], coords[j][1], coords[j][2])
#                 G[i][j]["weight"] = dist

#     tsp_path = greedy_tsp(G, weight="weight", source=start_idx)

#     ordered = [coords[i] for i in tsp_path]

#     return [{"address": r[0], "lat": r[1], "lon": r[2]} for r in ordered]

