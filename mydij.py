from flask import Flask
import scipy.io
import io

from scipy.io import loadmat

app = Flask(__name__)

def main_script():
    output = io.StringIO()
class PriorityQueue:
    def __init__(self):
        self.heap = []               
        self.node_to_index = {}     

    def isEmpty(self):             
        return len(self.heap) == 0  

    def insert(self, nodeName, priority): 
        node = (nodeName, priority)   
        self.heap.append(node)        
        self.node_to_index[nodeName] = len(self.heap)   
        self._swim(len(self.heap) - 1)  
       
    def extractMin(self):    
        if self.isEmpty():  
            return None
        min_node, min_priority = self.heap[0]  
        last_node, last_priority = self.heap.pop()  
        del self.node_to_index[min_node]  

        if self.heap:  # O(1)
            self.heap[0] = (last_node, last_priority)  
            self.node_to_index[last_node] = 0  
            self._sink(0)  

        return min_node  

    def decreaseKey(self, nodeName, newPriority):  
        if nodeName in self.node_to_index:  
            index = self.node_to_index[nodeName]  
            if newPriority < self.heap[index][1]: 
                self.heap[index] = (nodeName, newPriority) 
                self._swim(index)  

    def _swap(self, i, j):  
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i] 
        self.node_to_index[self.heap[i][0]] = i 
        self.node_to_index[self.heap[j][0]] = j  

    def _swim(self, index):  
        while index > 0: 
            parent_index = (index - 1) // 2  
            if self.heap[index][1] < self.heap[parent_index][1]: 
                self._swap(index, parent_index)  
                index = parent_index 
            else:
                break
     

    def _sink(self, index):  
        while True:  
            left_child_index = 2 * index + 1 
            right_child_index = 2 * index + 2  
            smallest = index 

            if (  
                left_child_index < len(self.heap)  
                and self.heap[left_child_index][1] < self.heap[smallest][1] 
            ):
                smallest = left_child_index 

            if (  # Check if the right child exists 
                right_child_index < len(self.heap) - 1 
                and self.heap[right_child_index][1] < self.heap[smallest][1] 
            ):
                smallest = right_child_index 

            if smallest != index: 
                self._swap(index, smallest)  
                index = smallest  
            else:
                break

def myDijkstra(adj_matrix, origin):
    num_nodes = len(adj_matrix)
    dist = [float('inf')] * num_nodes  # O(n) Initialize distance array with infinity for all nodes
    prev = [0] * num_nodes  # O(n) Initialize previous node array with zeros for all nodes
    dist[origin] = 0  # O(1) Set the distance to the origin node as 0
    pq = PriorityQueue()  # O(1) Create a priority queue to store nodes with distances
    pq.insert(origin, 0)  # O(log N) Insert the origin node with distance 0 into the priority queue

    while not all(dist[i] == float('inf') for i in range(num_nodes)):  # O(n) Input: Index; Output: node with the minimum distance from the priority queue
        current_node = pq.extractMin()  # O(log N)

        # Check if extractMin() returned None (i.e., the queue is empty)
        if current_node is None:  # O(1)
            break

        for neighbor in range(num_nodes):  #  O(n) Iterate through neighbors of the current node
            if adj_matrix[current_node][neighbor] > 0:  # O(1)  Check if there is an edge from the current node to the neighbor
                new_distance = dist[current_node] + adj_matrix[current_node][neighbor]  # O(1) Calculate the potential new distance to the neighbor
                if new_distance < dist[neighbor]:  # O(1)
                    dist[neighbor] = new_distance  # O(1)
                    prev[neighbor] = current_node + 1 # O(1) Find the smallest distance
                    pq.insert(neighbor, new_distance)  # Input: Neighbor, New Distance; O(log N)

    return dist, prev  # Output: Lists O(1)

    graph_files = ['graph1.mat', 'graph2.mat', 'graph3.mat', 'graph4.mat', 'graph5.mat', 'graph6.mat']

    # Iterate through each graph file
    for idx, graph_file in enumerate(graph_files):
        # Load the adjacency matrix from the current graph file
        mat_contents = scipy.io.loadmat(graph_file)
        # The variable name inside the .mat file is unknown, assuming it's the first key that's not '__globals__', '__header__', or '__version__'
        variable_names = [name for name in mat_contents if not name.startswith('__')]
        if variable_names:
            adj_matrix = mat_contents[variable_names[0]]
        else:
            continue  # If no valid variable names are found, skip to the next file

        # Specify the origin node (customizable as needed)
        origin = 0  

        # Call the my_dijkstra function to compute shortest distances
        dist, prev = my_dijkstra(adj_matrix, origin)

        # Write the results to the StringIO buffer
        output.write(f'Table {idx + 1}: {graph_file}\n')
        output.write('dist prev\n')
        for i in range(len(dist)):
            output.write(f'{dist[i]:<4} {prev[i]:<4}\n')
        output.write('\n')  

    
    return output.getvalue()

@app.route('/')
def run_script():
    # Call main_script and get the output
    result = main_script()
    # Return the result to the browser
    return f"<pre>{result}</pre>"  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
