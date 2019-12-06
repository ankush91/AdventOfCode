import csv


def read_input():
    list_rows = []
    with open('input.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
            list_rows.append(row)

    return list_rows


def main():
    input_list = read_input()
    dict_nodes_to_edges, dict_incoming_edges_count = {}, {}

    # problem: count paths using topological sort in a graph
    # track outgoing edges from each node and count of incoming edges
    for edge in input_list:
        u, v = edge.split(')')
        if u not in dict_nodes_to_edges:
            dict_nodes_to_edges[u] = []
        dict_nodes_to_edges[u] = dict_nodes_to_edges[u] + [v]
        dict_incoming_edges_count[v] += 1
    
    # sort nodes as per incoming edges
    queue_no_incoming = sorted(dict_incoming_edges_count.items(), key=lambda x: x[1])
    
    queue_no_incoming = []
    dict_path_counts = {}
    while sorted_nodes:
        n, in_count = sorted_nodes[0][1]
        # if no incoming nodes then add to queue
        if in_count == 0:
            queue_no_incoming.append(n)
        else:
            break        
       

if __name__ == "__main__":
    main()
