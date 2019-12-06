import csv
import sys


def read_input():
    list_rows = []
    with open('input.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
            list_rows.append(row[0])

    return list_rows


def main():
    input_list = read_input()
    dict_nodes_to_out_edges, dict_nodes_to_in_edges_count = {}, {}

    # problem: count paths using topological sort in a graph
    # track outgoing edges from each node and count of incoming edges
    set_nb_nodes = set()
    for edge in input_list:
        u, v = edge.split(')')
        if u not in dict_nodes_to_out_edges:
            dict_nodes_to_out_edges[u] = []
        dict_nodes_to_out_edges[u] = dict_nodes_to_out_edges[u] + [v]
        # incoming edge found for node v
        set_nb_nodes.add(v)
        if v in dict_nodes_to_in_edges_count:
            dict_nodes_to_in_edges_count[v] += 1
        else:
            dict_nodes_to_in_edges_count[v] = 1
    
    # set of nodes without incoming edge
    list_base_nodes = list(set(dict_nodes_to_out_edges.keys()).difference(set_nb_nodes))
    visited_nodes_to_depth = {n: 0 for n in list_base_nodes}
    
    ## PART-1
    # O(n + m) toplogical sort based counting
    count_total_paths = 0
    while list_base_nodes:
        # fifo queue
        n = list_base_nodes.pop(0)
        # recorded parent_depth
        parent_depth = visited_nodes_to_depth[n]
        if n not in dict_nodes_to_out_edges:
            continue
        for m in dict_nodes_to_out_edges[n]:
            dict_nodes_to_in_edges_count[m] -= 1
            # count all paths till edge
            count_total_paths += parent_depth + 1
            # if no incoming nodes then add to base
            if dict_nodes_to_in_edges_count[m] == 0:
                list_base_nodes.append(m)
                # record longest depth of node
                visited_nodes_to_depth[m] = parent_depth + 1
 
    # print(count_total_paths)
    
    ## PART-2 - BFS of shortest paths
    ## O(n + m) to reach YOU, then O(n + m) to reach SAN
    ## compute shortest distance between common_ancestor to YOU and common_ancestor to SAN
    # set of nodes without incoming edge

    # REINITIALIZE
    list_base_nodes = list(set(dict_nodes_to_out_edges.keys()).difference(set_nb_nodes))
    visited_nodes_to_depth = {n: 0 for n in list_base_nodes}
    shortest_path_parents = {n: 'ROOT' for n in list_base_nodes}

    while list_base_nodes:
        # fifo queue
        n = list_base_nodes.pop(0)
        # recorded shortest path parent_depth
        parent_depth = visited_nodes_to_depth[n]
        if n not in dict_nodes_to_out_edges:
            continue
        for m in dict_nodes_to_out_edges[n]:
            if m not in visited_nodes_to_depth:
                shortest_path_parents[m] = n
                # add to base
                list_base_nodes.append(m)
                # record shortest depth of node
                visited_nodes_to_depth[m] = parent_depth + 1

        # if target nodes found then break
        if ('YOU' in visited_nodes_to_depth) and ('SAN' in visited_nodes_to_depth):
            break

    # backtrack for node 'YOU'
    n = 'YOU'
    shortest_path_to_you = []
    while n != 'ROOT':
        pn = shortest_path_parents[n]
        shortest_path_to_you.append(pn)
        n = pn

    # backtrack for node 'SAN'
    n = 'SAN'
    shortest_path_to_san = []
    while n != 'ROOT':
        pn = shortest_path_parents[n]
        shortest_path_to_san.append(pn)
        n = pn

    # delete all common ancestors
    while shortest_path_to_san[-1] == shortest_path_to_you[-1]:
        shortest_path_to_san.pop()
        shortest_path_to_you.pop()
    
    print(len(shortest_path_to_san) + len(shortest_path_to_you))


if __name__ == "__main__":
    main()
