#!/usr/bin/python
from math import ceil
import scipy.optimize

def compute(V, init = 10):
	if len(V) <= 1:
		return
	def h(x):
		return sum([x**(-v) for v in V])-1
	return scipy.optimize.brenth(h,1,init)

def choose(L, k, n = None):
	if n == None:
		n = len(L)
	if k == 0:
		return [[]]
	if k == 1:
		return [[L[i]] for i in range(n)]
	R = []
	for i in range(k-1,n):
		for S in choose(L, k-1, i):
			R.append(S+[L[i]])
	return R

def make_graph(E):
	n = 1 +max([max(x) for x in E])
	G = [[] for x in range(n)]
	for e in E:
		G[e[0]].append(e[1])
		G[e[1]].append(e[0])
	return G

def find_P4(G):
	for v1 in range(len(G)):
		for v2 in G[v1]:
			for v3 in G[v2]:
				if v3 == v1: continue
				if v3 in G[v1]: continue
				for v4 in G[v3]:
					if v4 in [v1,v2]: continue
					if v4 in G[v1] or v4 in G[v2]: continue
					return True
	return False

# Check if D is a subset of a set in L
def check(L, D):
	D = set(D)
	for X in L:
		if X.issubset(D):
			return True
	return False

def minimal_deletion_sets(E):
	if not find_P4(make_graph(E)):
		return [],[]

	E = [(min(x),max(x)) for x in E]

	L = []
	for k in range(1,len(E)+1):
		for Del in choose(E, k):
			if check(L, Del):
				continue
			E2 = [x for x in E if x not in Del]
			G = make_graph(E2)
			if not find_P4(G):
				L.append(set(Del))
	return L

def minimal_editing_sets(E, colors):
	if not find_P4(make_graph(E)):
		return [],[]

	E = [(min(x),max(x)) for x in E]

	n = max([max(x) for x in E])+1
	E_comp = [] # The complement of E
	for j in range(n):
		for i in range(j):
			if colors[i] != colors[j] and (i,j) not in E:
				E_comp.append((i,j))
	L = []
	for k in range(1,len(E)+len(E_comp)+1):
		for k1 in range(0, k+1):
			if k1 > len(E): continue
			k2 = k-k1
			if k2 > len(E_comp): continue
			for Del in choose(E, k1):
				for Add in choose(E_comp, k2):
					if check(L, Del+Add):
						continue
					E2 = [x for x in E if x not in Del]+Add
					G = make_graph(E2)
					if not find_P4(G):
						L.append(set(Del+Add))
	return L

def process(E, Rule, Edges, colors = [0,1]*4):
	print "Rule ("+str(Rule)+")","additional edges:",Edges
	if Rule == 9:
		L = minimal_deletion_sets(E)
	else:
		L = minimal_editing_sets(E, colors)
	for i,X in enumerate(L):
		if Rule == 8:
			print "$\{"+",".join(["u_%d u_%d" % (x[0]+1,x[1]+1) for x in list(X)])+"\}$"+("," if i < len(L)-1 else "")
		else:
			print "$\{"+",".join(["v_%d v_%d" % (x[0],x[1]) for x in list(X)])+"\}$"+("," if i < len(L)-1 else "")
	V = [len(X) for X in L]
	print "Branching vector",V
	x = compute(V)
	print "Branching number",ceil(x*1000)/1000
	print

E0 = [(0,1),(1,2),(2,3),(3,4),(4,5)]

process(E0+[(0,3),(5,2)],5,"")
process(E0+[(0,3),(5,2),(0,5)],5,"v_0v_5")

process(E0+[(0,3),(0,5)],6,"")

process(E0+[(0,3),(6,5)],7,"")
process(E0+[(0,3),(6,5),(6,1)],7,"v_1v_6")
process(E0+[(0,3),(6,5),(6,3)],7,"v_3v_6")
process(E0+[(0,3),(6,5),(6,1),(6,3)],7,"v_1v_6,v_3v_6")

process(E0+[(0,5),(0,6),(6,7),(3,7)],8,"",[0,1]*3+[1,0])

process(E0,9,"")
process(E0+[(0,5)],9,"v_0v_5")
