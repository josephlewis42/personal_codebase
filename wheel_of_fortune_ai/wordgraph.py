
import collections

class NgramGraph:
	graph = None
	
	def __init__(self):
		self.graph = collections.defaultdict(list)
	
	def add_edge(from_node, to_node, score):
		graph[from_node].append((score, to_node))
		graph[from_node] = sorted(graph[from_node], reverse=True)
	
	def dfs(self, start_node, depth, match_function):
		
		
