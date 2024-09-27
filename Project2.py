import time
import math
import statistics
import random
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

class Graph:

    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])

    def find(self, parent, i):
        if parent[i] != i:
            parent[i] = self.find(parent, parent[i])
        return parent[i]

    def union(self, parent, rank, x, y):
        if rank[x] < rank[y]:
            parent[x] = y
        elif rank[x] > rank[y]:
            parent[y] = x
        else:
            parent[y] = x
            rank[x] += 1

    def KruskalMST(self):
        result = []
        edge_count = 0
        i = 0
        self.graph.sort(key=lambda edge: edge[2])
        parent = list(range(self.V))
        rank = [0] * self.V  # Initialize rank array
        start_time = time.perf_counter_ns()
        while edge_count < self.V - 1 and i < len(self.graph):
            u, v, weight = self.graph[i]
            i += 1
            root_u = self.find(parent, u)
            root_v = self.find(parent, v)
            if root_u != root_v:
                edge_count += 1
                result.append([u, v, weight])
                self.union(parent, rank, root_u, root_v)
        end_time = time.perf_counter_ns()
        experimental_time = end_time - start_time
        E = len(self.graph)
        V = self.V
        theoretical_time = E * math.log2(V)
        return experimental_time, theoretical_time, E, V


if __name__ == '__main__':
    test_cases = []
    random.seed(42)

    def generate_large_graph(vertices, edges):
        g = Graph(vertices)
        added_edges = set()
        while len(g.graph) < edges:
            u = random.randint(0, vertices - 1)
            v = random.randint(0, vertices - 1)
            if u != v and (u, v) not in added_edges and (v, u) not in added_edges:
                weight = random.randint(1, 10000)  # Random weight between 1 and 10,000
                g.addEdge(u, v, weight)
                added_edges.add((u, v))
        return g

    # Test case 1: 5000 vertices, 20000 edges
    g1 = generate_large_graph(5000, 20000)
    test_cases.append(g1.KruskalMST())

    # Test case 2: 7500 vertices, 30000 edges
    g2 = generate_large_graph(7500, 30000)
    test_cases.append(g2.KruskalMST())

    # Test case 3: 10000 vertices, 45000 edges
    g3 = generate_large_graph(10000, 45000)
    test_cases.append(g3.KruskalMST())

    # Test case 4: 15000 vertices, 70000 edges
    g4 = generate_large_graph(15000, 70000)
    test_cases.append(g4.KruskalMST())

    # Test case 5: 20000 vertices, 100000 edges
    g5 = generate_large_graph(20000, 100000)
    test_cases.append(g5.KruskalMST())

    theoretical_times = []
    experimental_times = []
    vertices = []
    edges = []
    adjusted_th = []

    for idx, (experimental, theoretical, E, V) in enumerate(test_cases, 1):
        theoretical_times.append(theoretical)
        experimental_times.append(experimental)
        vertices.append(V)
        edges.append(E)

    # Compute average scaling constant from all cases
    avg_experimental = statistics.mean(experimental_times)
    avg_theoretical = statistics.mean(theoretical_times)
    avg_scaling = avg_experimental / avg_theoretical


    for i in range(len(theoretical_times)):
        adjusted_th.append(theoretical_times[i] *avg_scaling)

    print(f"  Avg_ex = {avg_experimental} ns")
    print(f"  Avg_th = {avg_theoretical} ns")
    print(f"  Avg_scaling = {avg_scaling} ns\n")

    # Print the results
    for i in range(len(edges)):
        print(f"Test-{i + 1}:")
        print(f"  Vertices= {vertices[i]}, Edges= {edges[i]}")
        print(f"  Experimental Time = {experimental_times[i]} ns")
        print(f"  Theoretical Time = {theoretical_times[i]} operations")
        print(f"  Adjusted Theoretical Time = {adjusted_th[i]} operations\n")

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(vertices, adjusted_th, label="Adjusted Theoretical Time", marker='o')
    plt.plot(vertices, experimental_times, label="Experimental Time", marker='x')
    plt.xscale('linear')
    plt.yscale('linear')
    plt.gca().xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0f}'))
    plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0f}'))
    plt.xlabel("Vertices")
    plt.ylabel("Time (ns)")
    plt.title("Comparison of Adjusted Theoretical and Experimental Time Complexity")
    plt.legend()
    plt.show()