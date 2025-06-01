import matplotlib.pyplot as plt
import numpy as np
import topo

# Same setup for Jellyfish and fat-tree
num_servers = 686
num_switches = 245
num_ports = 14

# Function to convert tuples to dictionary
def tuplegraph(tuples):
     graph = {}
     for edge in tuples:
          n1 , n2 = edge
          if n1 not in graph:
               graph[n1] = []
          if n2 not in graph:
               graph[n2] = []
          graph[n1].append(n2)
          graph[n2].append(n1)
     return graph

# Dijkstra Algorithm to find the shortest path's distance
def dijkstraalg(graph, source, destinaton ):
     # Initialize distances to all nodes as infinity
     distances = {node: float('inf') for node in graph}
     # Distance from the source node to itself is 0
     distances[source] = 0
     # Set to keep track of visited nodes
     visited = set()

     while len(visited) < len(graph):
          # Find the node with the smallest tentative distance among unvisited nodes
          current_node = min((node for node in graph if node not in visited), key=lambda x: distances[x])
          visited.add(current_node)

          if current_node == destinaton:
               return distances[destinaton]

          # Explore neighbors of the current node
          for neighbor in graph[current_node]:
               distance = distances[current_node] + 1  # Assuming unit weight for all edges
               # If the new distance is smaller than the recorded distance, update it
               if distance < distances[neighbor]:
                    distances[neighbor] = distance

     return None

# Run Fattree Topology
print("Fattree Started")
ft_topo = topo.Fattree(num_ports)
attr_ft = ft_topo.get_attributes() # Gettting output attributes from fattree topology

tuples = attr_ft[0]
servers = attr_ft[1]

graph = tuplegraph(tuples)
list_serverpairs=[]
dict_serverpairs={"2":0,"3":0,"4":0,"5":0,"6":0} # Dictionary to store the number of occurance of paths lengths

for a,i in enumerate(servers):
     shortest_distance=dijkstraalg(graph,'h000',i.id)  # Calling Dijkstra algorithm to get the shortest path length
     list_serverpairs.append(shortest_distance) # Appending the shortest path length to a list

for num in list_serverpairs:
     if num > 1:
          dict_serverpairs[str(num)] += 1 # Adding the number of occurance of path lengths to dictionary

print("Dictionary of occurance of paths lengths created")         
print("Dictionary: ",dict_serverpairs)

# Generating the graph axis
x1 = list(dict_serverpairs.keys())
y1 = list(dict_serverpairs.values())
y1 = [n/1000 for n in y1] # Convert to fraction of server pairs
print("Fattree Completed")


# Plot the figure 1(c)---------------------------------------

labels=x1 # X-axis labels
x = np.arange(len(x1))  # create a range of x-coordinates for the bars

# create the bar plots
width = 0.35
fig, ax = plt.subplots()
ax.bar(x + 0.5*width, y1, width, color='red', label='Fattree')

# add labels and title
ax.set_xticks(x)
ax.set_xticklabels(labels)

# set y-axis limit
ax.set_ylim([0, 1])

# set y-axis ticks
num_ticks = 10  # specify the number of ticks on the y-axis
ticks = np.linspace(0, 1, num_ticks)  # calculate y-axis tick values
tick_labels = ['{:.1f}'.format(tick) for tick in ticks]  # format tick labels as string
ax.set_yticks(ticks)  # apply y-axis tick values
ax.set_yticklabels(tick_labels)  # apply y-axis tick labels

# Adding labels
plt.xlabel('Path Length')
plt.ylabel('Fraction of Server Pairs')
plt.title('Reproducing figure 1(c) in jellyfish paper')

# add legend
plt.legend()

# display the plot
print("Displaying the graph")
plt.show()
