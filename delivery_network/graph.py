from time import perf_counter
import math
class Graph:
    def _init_(self, nodes=[]):
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
    


    def _str_(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
    
    def add_edge(self, node1, node2, power, dist=1):
        k = self.graph.keys()
        if node1 not in k:
            self.graph[node1] = [(node2, power, dist)]
        else : 
            self.graph[node1].append((node2, power, dist))

        if node2 not in k:
            self.graph[node2] = [(node1, power, dist)]
        else : 
            self.graph[node2].append((node1, power, dist))

 # Question 2
    def neig(self, node):
        return [j[0] for j in self.graph.get(node)]  

    def deep_parcour(self,node,l):
        if node not in l:
            l.append(node)
            for w in self.neig(node):
                self.deep_parcour(w, l)
        return l 

    def connected_components(self):
        visited = [False] * self.nb_nodes
        component = []
        for i in range(self.nb_nodes):
            if not visited[i] : 
                component.append(self.deep_parcour(i+1, l=[]))
                for j in self.deep_parcour(i+1, l = []):
                    visited[j-1] = True 
        return component
# fin Q2

    def connected_components_set(self):
        return set(map(frozenset, self.connected_components()))
    
# Question3
    def get_path_with_power(self, src, dest, power):
        def arret(l, dest):
            for i in l:
                if i[-1] is not dest : 
                    return False
            return True 
        c = []
        for l in self.connected_components():
            if src in l:
                c = l
        if dest not in c:
            return None
                
        chem = [[src]]
        while not arret(chem, dest):
            q = []
            for p in chem:
                u = p[-1]
                if u == dest:
                    q.append(p)
                else:
                    for t in self.graph[u]:
                        if not (t[0] in p) and power>= t[1]:
                            v = [i for i in p]
                            v.append(t[0])
                            q.append(v)
            chem= q
        if len(chem) == 0:
            return None
        else:
            return chem[0]
# Fin Q3

#On construit une fonction qui nous permet de déterminer tous les chemis liant un point de départ à un point d'arrivée.
    def get_all_path_with_power(self, src, dest, power):
        def arret(l, dest):
            for i in l:
                if i[-1] is not dest : 
                    return False
            return True 
        c = []
        for l in self.connected_components():
            if src in l:
                c = l
        if dest not in c:
            return None
                
        chem = [[src]]
        while not arret(chem, dest):
            q = []
            for p in chem:
                u = p[-1]
                if u == dest:
                    q.append(p)
                else:
                    for t in self.graph[u]:
                        if not (t[0] in p) and power>= t[1]:
                            v = [i for i in p]
                            v.append(t[0])
                            q.append(v)
            chem= q
        if len(chem) == 0:
            return None
        else:
            return chem()

#Cette fonction nous permet de trouver la puissance minimale nécessaire 
    def min_power(self, src, dest):
        """
        Computes the minimum power necessary to go from src to dest and returns the path and the minimum power.
        """
        #D'abord, on essaye de chercher un chemin, car s'il n'y a pas de chemin : pas besoin de s'embêter à trouver le chemin le plus court! 
        path = self.get_path_with_power(src, dest, float("inf"))
        if path is None : 
            raise ValueError(f"No path found between {src} and {dest}")
        else : 
            # If a path exists, do a binary search for the minimum power
            left, right = 0, 100000000 #poser la question au prof de la valeur maximale pour commencer: on pourrait récupérer la valeur annoncée quand on fait le get_path_with_power
            while left < right:
                mid = (left + right) // 2
                if self.get_path_with_power(src, dest, mid): #Ca vaut dire qu'il existe ENCORE un chemin, mais cette fois ci avec une puissance qui est inférieure ou égale à mid
                    right = mid # donc on rétrécit l'intervalle entre left et right
                else:
                    left = mid + 1 # Pas de chemin en dessous de la puissance mid (la fonction self.get_path_with_power(src, dest, mid) return None) DONC on cherche au dessus de mid. 
        return path, left




# Question 1 et 4
def graph_from_file(filename):
    with open(filename, "r") as file:
        n, m = map(int, file.readline().split())
        g = Graph(range(1, n+1))
        for _ in range(m):
            edge = list(map(int, file.readline().split()))
            if len(edge) == 3:
                node1, node2, power_min = edge
                g.add_edge(node1, node2, power_min) # will add dist=1 by default
            elif len(edge) == 4:
                node1, node2, power_min, dist = edge
                g.add_edge(node1, node2, power_min, dist)
            else:
                raise Exception("Format incorrect")
    return g



