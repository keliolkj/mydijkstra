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
        self._sink(0)
        return min_node

    def decreaseKey(self, nodeName, newPriority):
        if nodeName in self.node_to_index:
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
            if self.heap[parent][1] > self.heap[index][1]:
                self._swap(parent, index)
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

def my_dijkstra(adj_matrix, origin):
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

def load_graphs(graph_files):
    results = []
    for graph_file in graph_files:
        mat_contents = loadmat(graph_file)
        variable_names = [name for name in mat_contents if not name.startswith('__')]
        if variable_names:
            adj_matrix = mat_contents[variable_names[0]]
            origin = 0  # Assuming the origin is always node 0
            dist, prev = my_dijkstra(adj_matrix, origin)
            results.append((dist, prev))
        else:
            results.append(([], []))  # No valid variable names found
    return results

@app.route('/')
def run_script():
    graph_files = ['graph1.mat', 'graph2.mat', 'graph3.mat', 'graph4.mat', 'graph5.mat', 'graph6.mat']
    graphs_results = load_graphs(graph_files)
    
    output = StringIO()
    for idx, (dist, prev) in enumerate(graphs_results):
        output.write(f'Table {idx + 1}:\n')
        output.write('dist prev\n')
        for i in range(len(dist)):
            output.write(f'{dist[i]:<5} {prev[i]:<5}\n')
        output.write('\n')
    
    return f"<pre>{output.getvalue()}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
