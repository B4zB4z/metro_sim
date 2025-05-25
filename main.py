from graph import Graph
from process_stations import process_stations, build_station_vertices
from travel_time import connect_sequential_stations, connect_transfer_stations

def build_graph():
    features = process_stations()

    graph = Graph()
    metro = build_station_vertices(features)
    for code, vertex in metro.items():
        graph.vertices[code] = vertex

    connect_sequential_stations(graph, features)
    connect_transfer_stations(graph, features)

    return graph, features

def find_code_by_name(features, name):
    matches = features[features['name'].str.lower() == name.lower()]
    if len(matches) == 0:
        return None
    elif len(matches) == 1:
        return matches.iloc[0]['code']
    else:
        print(f"Multiple lines found for {name}:")
        print(matches[['code', 'line', 'num']])
        return matches.iloc[0]['code']

def print_path(vertex):
    if vertex.parent is not None:
        print_path(vertex.parent)
    print(vertex.data, end=' -> ')

def shortest_path(graph, start_code, end_code):
    print("\n--- Shortest Path (Least Stops) ---")
    graph.bfs(start_code)
    if end_code in graph.vertices:
        dest = graph.vertices[end_code]
        if dest.parent:
            print_path(dest)
            print("END")
            print(f"Stops: {dest.distance}")
        else:
            print("No path found.")
    else:
        print("Destination station code not found.")

def fastest_path(graph, start_code, end_code):
    print("\n--- Fastest Path (Least Travel Time) ---")
    graph.dijkstra(start_code)
    if end_code in graph.vertices:
        dest = graph.vertices[end_code]
        if dest.parent:
            print_path(dest)
            print("END")
            print(f"Total Travel Time: {dest.distance} minutes")
        else:
            print("No path found.")
    else:
        print("Destination station code not found.")

if __name__ == "__main__":
    graph, features = build_graph()

    start_name = input("Enter start station name: ")
    end_name = input("Enter destination station name: ")

    start_code = find_code_by_name(features, start_name)
    end_code = find_code_by_name(features, end_name)

    if start_code and end_code:
        shortest_path(graph, start_code, end_code)
        fastest_path(graph, start_code, end_code)
    else:
        print("Could not resolve both station names to valid codes.")
