infinity = float("inf")
processed = []
graph = {}
costs = {}
parents = {}
 
def test_example():
    graph["start"] = {}
    graph["start"]["a"] = 6
    graph["start"]["b"] = 2
    graph["a"] = {}
    graph["a"]["fin"]  = 1
    graph["b"] = {}
    graph["b"]["a"] = 3
    graph["b"]["fin"]  = 5
    graph["fin"] = {}

    costs["a"] = 6
    costs["b"] = 2
    costs["fin"] = infinity

    parents["a"] = "start"
    parents["b"] = "start"
    parents["fin"] = None

def dz71():
    # задание 7.1
    graph["start"] = {}
    graph["start"]["a"] = 5
    graph["start"]["b"] = 2
    graph["a"] = {}
    graph["a"]["c"]  = 4
    graph["a"]["d"]  = 2
    graph["b"] = {}
    graph["b"]["a"] = 8
    graph["b"]["d"]  = 7
    graph["c"] = {}
    graph["c"]["d"] = 6
    graph["c"]["fin"] = 3
    graph["d"] = {}
    graph["d"]["fin"] = 1
    graph["fin"] = {}

    costs["a"] = 5
    costs["b"] = 2
    costs["c"] = infinity
    costs["d"] = infinity
    costs["fin"] = infinity
    
    parents["a"] = "start"
    parents["b"] = "start"
    parents["c"] = None
    parents["d"] = None
    parents["fin"] = None

def dz72():
    # задание 7.2
    graph["start"] = {}
    graph["start"]["a"] = 10
    graph["a"] = {}
    graph["a"]["c"]  = 20
    graph["b"] = {}
    graph["b"]["a"] = 1
    graph["c"] = {}
    graph["c"]["b"] = 1
    graph["c"]["fin"] = 30
    graph["fin"] = {}

    costs["a"] = 10
    costs["b"] = infinity
    costs["c"] = infinity
    costs["fin"] = infinity
    
    parents["a"] = "start"
    parents["b"] = None
    parents["c"] = None
    parents["fin"] = None

def find_lowest_code_node(costs):
    lowest_cost = float("inf")
    lowest_cost_node = None
    for node in costs:
        cost = costs[node]
        if cost < lowest_cost and node not in processed:
            lowest_cost = cost
            lowest_cost_node = node
    return lowest_cost_node

dz72()
node = find_lowest_code_node(costs)
while node is not None:
    cost = costs[node]
    neighbors = graph[node]
    for n in neighbors.keys():
        new_cost = cost + neighbors[n]
        if costs[n] > new_cost:
            costs[n] = new_cost
            parents[n] = node
    processed.append(node)
    node = find_lowest_code_node(costs)

print(costs)
print(parents)
print(processed)
