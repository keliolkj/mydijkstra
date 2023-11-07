from flask import Flask
import scipy.io
import io

app = Flask(__name__)
class PriorityQueue:
    def __init__(self):
        self.heap = []               # O(1) Create a list to store nodes with priorities in the priority queue. Initialized as an empty list.
        self.node_to_index = {}      # O(1) Create a dictionary to maintain the mapping of node names to their indices in the heap

    def isEmpty(self):              # Checking the length of a list 
        return len(self.heap) == 0  # O(1)

    def insert(self, nodeName, priority): # Inserts a new element into the heap (the name of the node and the priority) into the PQ to maintain the heap property
        node = (nodeName, priority)   # Input: Node name, priority; O(1) 
        self.heap.append(node)        # O(1) Appends new node
        self.node_to_index[nodeName] = len(self.heap)   # O(1) Store the index of the new node
        self._swim(len(self.heap) - 1)  # Input: Index; Output: None. O(log N)
        #Calls the _swim() method to move the new node up in the heap if necessary to maintain the heap property

    def extractMin(self):    #takes no explicit input and returns the name of the node with the minimum priority value in the PQ, then removes the node from the queue.
        if self.isEmpty():   # O(1)
            return None
        min_node, min_priority = self.heap[0]  # Input: None; Output: Node name, priority. O(1)
        last_node, last_priority = self.heap.pop()  # Input: None; Output: Node name, priority. O(1)
        del self.node_to_index[min_node]  # O(1) update the dictionary by delete the min_node

        if self.heap:  # O(1)
            self.heap[0] = (last_node, last_priority)  # O(1) if heap is not empty, update the root with the values of the last node
            self.node_to_index[last_node] = 0  # O(1)
            self._sink(0)  # Input: Index； Output: None. O(log N) ensure the root element satisfies the heap property

        return min_node  # O(1) return node with minimum priority value

    def decreaseKey(self, nodeName, newPriority):  # It takes two inputs, nodeName and newPriority, and updates the priority of the specified node in the Priority Queue. It does not return any value.
        if nodeName in self.node_to_index:  # O(1) Input: Node name. Output: Boolean. Check if node exists in node_to_index
            index = self.node_to_index[nodeName]  # O(1)
            if newPriority < self.heap[index][1]:  # O(1)
                self.heap[index] = (nodeName, newPriority)  # O(1) If the new priority is less than current priority, updates the priority in self.heap
                self._swim(index)  # Input: Index. Output: None. O(log N)

    def _swap(self, i, j):  # It takes two indices, i and j, and swaps the elements at these positions in the PQ
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]  # Input: Indices. Output: None. O(1)
        self.node_to_index[self.heap[i][0]] = i  # O(1) updates indices for swapped elements
        self.node_to_index[self.heap[j][0]] = j  # O(1)

    def _swim(self, index):  # It takes the index of an element in the heap and moves it up the heap if necessary to maintain the heap property
        while index > 0:  # O(log N) The loop is executed to check and potentially fix the heap property violations by moving the element up the heap
            parent_index = (index - 1) // 2  # O(1) Input: Index. Output; Parent index. Calculate the parent index
            if self.heap[index][1] < self.heap[parent_index][1]:  # O(1) Compare the priority of element with the priority of its parent
                self._swap(index, parent_index)  # O(1) If the comparison is true (i.e., the element has a higher priority than its parent), swap the element with its parent
                index = parent_index  # O(1) Upadte index
            else:
                break
        #time complexity is determined by the number of iterations in the loop, which depends on the height of the binary heap. In a binary heap with N elements, the height is logN.

    def _sink(self, index):  # Input: the index of an element in the heap and moves it down the heap if necessary to maintain the heap property
        while True:  # O(log N) Execute loop and fix the heap property violations by moving the element down the heap
            left_child_index = 2 * index + 1  # Input: Index; Output: Left child index. O(1)
            right_child_index = 2 * index + 2  # Input: Index; Output: Right child index. O(1)
            smallest = index  # O(1) Initialize smallest with current index

            if (  # Check if the left child exists by check if it is within the bounds of the heap ans well as if its priority is smaller than the current smallest
                left_child_index < len(self.heap)  # O(1)
                and self.heap[left_child_index][1] < self.heap[smallest][1]  # O(1)
            ):
                smallest = left_child_index  # O(1) upadte the index of the left child

            if (  # Check if the right child exists 
                right_child_index < len(self.heap) - 1 # Input: None. Output: Boolean O(1)
                and self.heap[right_child_index][1] < self.heap[smallest][1]  # O(1)
            ):
                smallest = right_child_index  # O(1)

            if smallest != index:  # O(1)  Check if the smallest index is still the same as the original index to see if heap property is satisfied
                self._swap(index, smallest)  # O(1)
                index = smallest  # O(1)
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

from scipy.io import loadmat

def main_script():
    output = io.StringIO()
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
        origin = 0  # Python uses 0-indexing

        # Call the my_dijkstra function to compute shortest distances
        dist, prev = my_dijkstra(adj_matrix, origin)

        # Write the results to the StringIO buffer
        output.write(f'Table {idx + 1}: {graph_file}\n')
        output.write('dist prev\n')
        for i in range(len(dist)):
            # Check if prev[i] is None and handle it
            prev_node = 'None' if prev[i] is None else prev[i]
            output.write(f'{dist[i]:<5} {prev_node:<5}\n')
        output.write('\n')  # Separate results of different graphs with an empty line

    # Return the entire buffer contents as a string
    return output.getvalue()

@app.route('/')
def run_script():
    # Call main_script and get the output
    result = main_script()
    # Return the result to the browser
    return f"<pre>{result}</pre>"  # Use <pre> tags to format text like in a terminal

if __name__ == '__main__':
    # Run the Flask app on all available interfaces on port 80
    app.run(host='0.0.0.0', port=80)
