from flask import Flask, jsonify, request

app = Flask(__name__)

# Here you would paste the full implementation of your PriorityQueue class and any other necessary classes or functions.
class PriorityQueue:
    # ... (include all the methods of the PriorityQueue class)

def myDijkstra(adj_matrix, origin):
    # ... (implement the Dijkstra's algorithm)

@app.route('/shortest-path')
def shortest_path():
    # Extract origin and destination from the URL parameters
    origin = request.args.get('origin', default=None, type=int)
    destination = request.args.get('destination', default=None, type=int)

    # Validate the input
    if origin is None or destination is None:
        return jsonify({"error": "Origin and destination must be provided."}), 400

    # Here, you would need to define or load your graph's adjacency matrix
    adj_matrix = # ... (define or load your adjacency matrix here)

    # Call your Dijkstra's algorithm function
    dist, prev = myDijkstra(adj_matrix, origin)

    # Reconstruct the path from origin to destination
    path = []
    current_node = destination
    while current_node != origin:
        if current_node is None or prev[current_node] is None:
            return jsonify({"error": "Path not found."}), 404
        path.insert(0, current_node)
        current_node = prev[current_node]
    path.insert(0, origin)

    # Return the path as a JSON response
    return jsonify({"shortest_path": path})

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False for production
