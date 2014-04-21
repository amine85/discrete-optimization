#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import sys
Item = namedtuple("Item", ['index', 'value', 'weight'])

# define node class for branch and bound 
class Node:
	def __init__(self, value=0, room=0, estimate=0, x_i=0, x_v=0):
		self.value = value
		self.room = room
		self.estimate = estimate
		self.x_i = x_i
		self.path = []

def dfs_branch_bound(items,capacity,est):
	
	num_levels = len(items)-1
	# first let us initiate the root node
	root = Node()
	root.value = 0
	root.room = capacity
	root.estimate = est
	root.x_i = -1
	
	# use stack to do a depth first search
	node_stack = []	
	node_stack.append(root)
	
	# best estimated value
	best_value = -sys.float_info.max
	solution = []
	
	while node_stack:
		node = node_stack.pop()
		if  len(node.path) == len(items): 
			if node.value > best_value:
				best_value = node.value
				solution = node.path
			continue
		
		# create branch node 1: select item
		node1 = Node()		
		node1.x_i = node.x_i + 1
		node1.path = node.path + [1]
		node1.value = node.value + items[node1.x_i].value
		node1.room = node.room - items[node1.x_i].weight
		node1.estimate = node.estimate
		
		# create branch node 2: do not select item
		node2 = Node()
		node2.x_i = node.x_i + 1
		node2.path = node.path + [0]
		node2.value = node.value
		node2.room = node.room
		node2.estimate = node.estimate - items[node2.x_i].value
		
		if node1.room >= 0:
			node_stack.append(node1)

		if node2.estimate >= best_value:
			node_stack.append(node2)
			
	return solution
	
	
def get_linear_relax_est(items,capacity):
	
	# compute & sort densities:
	densities = [float(it.value)/float(it.weight) for it in items]
	indx_list = [densities.index(x) for x in sorted(densities, reverse=True)]
	
	# compute estimated value:
	est_value = 0
	est_weight = 0 
	last_index = 0
	for i in range(0,len(indx_list)):
		if est_weight + items[indx_list[i]].weight <= capacity:
			est_weight += items[indx_list[i]].weight
			est_value += items[indx_list[i]].value
			last_index = i
	
	if last_index < (len(indx_list)-1) and est_weight < capacity:
		est_value += float(capacity-est_weight)*densities[indx_list[last_index]]
	
	return est_value

def check_solution(items,capacity,taken):
	
	weight = 0
	print len(taken)
	print len(items)
	for i in range(0,len(items)):
		if taken[i] == 1:
			weight+=items[i].weight
	if weight > capacity:
		return False
	else:
		return True
	
	