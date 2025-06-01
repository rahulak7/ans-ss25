"""
 Copyright 2024 Computer Networks Group @ UPB

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 """

# Class for an edge in the graph
class Edge:
	def __init__(self):
		self.lnode = None
		self.rnode = None
		self.weight = None
	
	def remove(self):
		self.lnode.edges.remove(self)
		self.rnode.edges.remove(self)
		self.lnode = None
		self.rnode = None

# Class for a node in the graph
class Node:
	def __init__(self, id, type):
		self.edges = []
		self.id = id
		self.type = type

	# Add an edge connected to another node
	def add_edge(self, node):
		edge = Edge()
		edge.lnode = self
		edge.rnode = node
		self.edges.append(edge)
		node.edges.append(edge)
		return edge

	# Remove an edge from the node
	def remove_edge(self, edge):
		self.edges.remove(edge)

	# Decide if another node is a neighbor
	def is_neighbor(self, node):
		for edge in self.edges:
			if edge.lnode == node or edge.rnode == node:
				return True
		return False
		
class Fattree:

	def __init__(self, num_ports):
		self.servers = []
		self.switches = []
		self.adj = []
		self.adj_ft = self.generate(num_ports)
		
	def generate(self, num_ports):
		# TODO: code for generating the fat-tree topology
		if num_ports % 2 != 0:
			raise ValueError("k must be even.")
		
		# Number of pods
		pods = num_ports
			# Number of core switches
		coreSwitchCount = (num_ports // 2) ** 2
			# Number of aggregation switches per pod
		aggSwitchCount = num_ports // 2
			# Number of edge switches per pod
		edgeSwitchCount = num_ports // 2
			# Number of hosts per edge switch
		hostsPerEdgeSwitch = num_ports // 2

		# Create core switches
		coreSwitches = []
		coreswitchIPs = []
		for i in range(1, num_ports // 2 + 1):
			for j in range(1, num_ports // 2 + 1):
				switchName = f'cs{i}{j}'
				coreswitchIP = f'10.{num_ports}.{j}.{i}'
				switch = Node(switchName,'switch')
				self.switches.append(switch)
				coreswitchIPs.append(coreswitchIP)
				coreSwitches.append(switch)
		print("Core switches created")
		# Create pods
		for pod in range(pods):
			aggSwitches = []
			edgeSwitches = []
			aggswitchIPs = []
			edgeswitchIPs = []
			# Create aggregation switches in the pod
			for i in range(num_ports//2,num_ports):
				switchName = f'as{pod}{i}'
				aggswitchIP = f'10.{pod}.{i}.1'
				switch = Node(switchName,'switch')
				self.switches.append(switch)
				aggswitchIPs.append(aggswitchIP)
				aggSwitches.append(switch)

			# Create edge switches and hosts in the pod
			for i in range(edgeSwitchCount):
				switchName = f'es{pod}{i}'
				edgeswitchIP = f'10.{pod}.{i}.1'
				edgeswitchIPs.append(edgeswitchIP)
				switch = Node(switchName,'switch')
				self.switches.append(switch)
				edgeSwitches.append(switch)
				
				# Create and connect hosts
				for hostID in range(hostsPerEdgeSwitch):
					hostName = f'h{pod}{i}{hostID}'
					hostIP = f'10.{pod}.{i}.{hostID}'
					server = Node(hostName,'server')
					self.servers.append(server)
					h = server.add_edge(switch)
					self.adj.append((hostName,switch.id))

			# Connect edge switches to aggregation switches
			for edgeSwitch in edgeSwitches:
				for aggSwitch in aggSwitches:
					aggSwitch.add_edge(edgeSwitch)
					self.adj.append((aggSwitch.id,edgeSwitch.id))

			# Connect aggregation switches to core switches
			for i,coreSwitch in enumerate(coreSwitches):
				for idx, aggSwitch in enumerate(aggSwitches):
					if ( i < coreSwitchCount//2 ):
						if( idx % 2 == 0):
							aggSwitch.add_edge(coreSwitch)
							self.adj.append((aggSwitch.id,coreSwitch.id))
					else :
						if( idx % 2 != 0):
							aggSwitch.add_edge(coreSwitch)
							self.adj.append((aggSwitch.id,coreSwitch.id))
		print("All connections are done")
		return self.adj

	def get_attributes(self):
		print("Returned attributes")
		return self.adj_ft, self.servers