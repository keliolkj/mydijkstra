from flask import Flask, jsonify, request

app = Flask(__name__)

# Insert your PriorityQueue class definition here
class PriorityQueue:
    # Constructor and other methods with proper indentation
    # ...

# Insert your myDijkstra function here, with proper indentation
def myDijkstra(adj_matrix, origin):
    # Your Dijkstra's algorithm implementation
    # ...

@app.route('/shortest-path')
def shortest_path():
    origin = request.args.get('origin', type=int)
    destination = request.args.get('destination', type=int)

    if origin is None or destination is None:
        return jsonify({"error": "Origin and destination parameters are required."}), 400

    # Assuming adj_matrix is globally defined or you have a way to get it based on origin and destination
    adj_matrix = # ... (your code to generate or get the adjacency matrix)

    # Get the shortest path from the Dijkstra's algorithm
    dist, prev = myDijkstra(adj_matrix, origin)
    
    # Reconstruct the path from the destination to the origin
    path = []
    current_node = destination
    while current_node is not None and current_node != origin:
        path.insert(0, current_node)
        current_node = prev[current_node]
    if current_node is None:
        return jsonify({"error": "No path found from origin to destination"}), 404
    path.insert(0, origin)
    
    return jsonify({"shortest_path": path})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=70, debug=True)  # Running on all interfaces on port 80, not recommended for production
