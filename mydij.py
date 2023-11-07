from flask import Flask
import scipy.io
from scipy.io import loadmat
from io import StringIO

app = Flask(__name__)

class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.node_to_index = {}

    def isEmpty(self):
        return len(self.heap) == 0

    def insert(self, nodeName, priority):
        node = (nodeName, priority)
        self.heap.append(node)
        self.node_to_index[nodeName] = len(self.heap) - 1
        self._swim(len(self.heap) - 1)

    def extractMin(self):
        if self.isEmpty():
            return None
        min_node = self.heap[0][0]
        self._swap(0, len(self.heap) - 1)
        self.heap.pop()
        self.node_to_index.pop(min_node)
        if not self.isEmpty():
            self.node_to_index[self.heap[0][0]] = 0
            self._sink(0)
        return min_node

    def decreaseKey(self, nodeName, newPriority):
        if nodeName in self.node_to_index and newPriority < self.heap[self.node_to_index[nodeName]][1]:
            index = self.node_to_index[nodeName]
            self.heap[index] = (nodeName, newPriority)
            self._swim(index)

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.node_to_index[self.heap[i][0]] = i
        self.node_to_index[self.heap[j][0]] = j

    def _swim(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[index][1] < self.heap[parent][1]:
                self._swap(index, parent)
                index = parent
            else:
                break

    def _sink(self, index):
        while 2 * index + 1 < len(self.heap):
            j = 2 * index + 1
            if j < len(self.heap) - 1 and self.heap[j][1] > self.heap[j + 1][1]:
                j += 1
            if self.heap[index][1] <= self.heap[j][1]:
                break
            self._swap(index, j)
            index = j

def myDijkstra(adj_matrix, origin):
    num_nodes = len(adj_matrix)
    dist = [float('inf')] * num_nodes
    prev = [None] * num_nodes
    dist[origin] = 0
    pq = PriorityQueue()
    pq.insert(origin, 0)

    while not pq.isEmpty():
        current_node = pq.extractMin()

        for neighbor in range(num_nodes):
            if adj_matrix[current_node][neighbor] > 0:
                new_distance = dist[current_node] + adj_matrix[current_node][neighbor]
                if new_distance < dist[neighbor]:
                    dist[neighbor] = new_distance
                    prev[neighbor] = current_node
                    pq.decreaseKey(neighbor, new_distance)

    return dist, prev

def run_dijkstra_on_all_graphs(graph_files):
    output = StringIO()

    for idx, graph_file in enumerate(graph_files):
        mat_contents = loadmat(graph_file)
        variable_names = [name for name in mat_contents if not name.startswith('__')]
        if variable_names:
            adj_matrix = mat_contents[variable_names[0]]
            origin = 0
            distances, previous_nodes = myDijkstra(adj_matrix, origin)

            # Adjust prev array for 1-indexing for output and handling of unreachable nodes
            prev = ['None' if p is None else str(p + 1) for p in previous_nodes]

            output.write(f'Graph {idx + 1} results:\n')
            output.write("dist: " + " ".join(map(lambda d: 'Inf' if d == float('inf') else str(d), distances)) + "\n")
            output.write("prev: " + " ".join(prev) + "\n\n")
        else:
            output.write(f'Error reading {graph_file}: No valid variable names found.\n\n')

    return output.getvalue()


@app.route('/')
def run_script():
    graph_files = ['graph1.mat', 'graph2.mat', 'graph3.mat', 'graph4.mat', 'graph5.mat', 'graph6.mat']
    result = run_dijkstra_on_all_graphs(graph_files)
    return f"<pre>{result}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
