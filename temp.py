import networkx as nx
import math
import matplotlib.pyplot as plt

def dijkstra(zones, levels):

    G = nx.Graph()
    # szerokosc 5, dlugosc 10
    pos_adj_per_level = 0
    for level in levels:
        G.add_node(f'Entr{level}', pos = (5 + pos_adj_per_level, 22.5))
        G.add_node(f'Lvl{level}', pos=(25 + pos_adj_per_level, 22.5))
        if level % 2 != 0:
            #D
            G.add_node(f'{level}D1', pos=(5 + pos_adj_per_level, 26.25))
            G.add_node(f'{level}D2', pos=(5 + pos_adj_per_level, 28.75))
            G.add_node(f'{level}D3', pos=(5 + pos_adj_per_level, 31.25))
            G.add_node(f'{level}D4', pos=(5 + pos_adj_per_level, 33.75))
            G.add_node(f'{level}D5', pos=(5 + pos_adj_per_level, 36.25))
            G.add_node(f'{level}D6', pos=(5 + pos_adj_per_level, 38.75))
            G.add_node(f'{level}D7', pos=(6.25 + pos_adj_per_level, 40))
            G.add_node(f'{level}D8', pos=(8.75 + pos_adj_per_level, 40))
            G.add_node(f'{level}D9', pos=(11.25 + pos_adj_per_level, 40))
            G.add_node(f'{level}D10', pos=(13.75 + pos_adj_per_level, 40))
            G.add_node(f'{level}D11', pos=(10 + pos_adj_per_level, 33.75))
            G.add_node(f'{level}D12', pos=(10 + pos_adj_per_level, 31.25))
            G.add_node(f'{level}D13', pos=(10 + pos_adj_per_level, 28.75))
            G.add_node(f'{level}D14', pos=(10 + pos_adj_per_level, 26.25))
            #C
            G.add_node(f'{level}C1', pos=(5 + pos_adj_per_level, 18.75))
            G.add_node(f'{level}C2', pos=(5 + pos_adj_per_level, 16.25))
            G.add_node(f'{level}C3', pos=(5 + pos_adj_per_level, 13.75))
            G.add_node(f'{level}C4', pos=(5 + pos_adj_per_level, 11.25))
            G.add_node(f'{level}C5', pos=(5 + pos_adj_per_level, 8.75))
            G.add_node(f'{level}C6', pos=(5 + pos_adj_per_level, 6.25))
            G.add_node(f'{level}C7', pos=(6.25 + pos_adj_per_level, 5))
            G.add_node(f'{level}C8', pos=(8.75 + pos_adj_per_level, 5))
            G.add_node(f'{level}C9', pos=(11.25 + pos_adj_per_level, 5))
            G.add_node(f'{level}C10', pos=(13.75 + pos_adj_per_level, 5))
            G.add_node(f'{level}C11', pos=(10 + pos_adj_per_level, 11.25))
            G.add_node(f'{level}C12', pos=(10 + pos_adj_per_level, 13.75))
            G.add_node(f'{level}C13', pos=(10 + pos_adj_per_level, 16.25))
            G.add_node(f'{level}C14', pos=(10 + pos_adj_per_level, 18.75))
            #A
            G.add_node(f'{level}A1', pos=(25 + pos_adj_per_level, 26.25))
            G.add_node(f'{level}A2', pos=(25 + pos_adj_per_level, 28.75))
            G.add_node(f'{level}A3', pos=(25 + pos_adj_per_level, 31.25))
            G.add_node(f'{level}A4', pos=(25 + pos_adj_per_level, 33.75))
            G.add_node(f'{level}A5', pos=(25 + pos_adj_per_level, 36.25))
            G.add_node(f'{level}A6', pos=(25 + pos_adj_per_level, 38.75))
            G.add_node(f'{level}A7', pos=(23.75 + pos_adj_per_level, 40))
            G.add_node(f'{level}A8', pos=(21.25 + pos_adj_per_level, 40))
            G.add_node(f'{level}A9', pos=(18.75 + pos_adj_per_level, 40))
            G.add_node(f'{level}A10', pos=(16.25 + pos_adj_per_level, 40))
            G.add_node(f'{level}A11', pos=(20 + pos_adj_per_level, 33.75))
            G.add_node(f'{level}A12', pos=(20 + pos_adj_per_level, 31.25))
            G.add_node(f'{level}A13', pos=(20 + pos_adj_per_level, 28.75))
            G.add_node(f'{level}A14', pos=(20 + pos_adj_per_level, 26.25))
            #B
            G.add_node(f'{level}B1', pos=(25 + pos_adj_per_level, 18.75))
            G.add_node(f'{level}B2', pos=(25 + pos_adj_per_level, 16.25))
            G.add_node(f'{level}B3', pos=(25 + pos_adj_per_level, 13.75))
            G.add_node(f'{level}B4', pos=(25 + pos_adj_per_level, 11.25))
            G.add_node(f'{level}B5', pos=(25 + pos_adj_per_level, 8.75))
            G.add_node(f'{level}B6', pos=(25 + pos_adj_per_level, 6.25))
            G.add_node(f'{level}B7', pos=(23.75 + pos_adj_per_level, 5))
            G.add_node(f'{level}B8', pos=(21.25 + pos_adj_per_level, 5))
            G.add_node(f'{level}B9', pos=(18.75 + pos_adj_per_level, 5))
            G.add_node(f'{level}B10', pos=(16.25 + pos_adj_per_level, 5))
            G.add_node(f'{level}B11', pos=(20 + pos_adj_per_level, 11.25))
            G.add_node(f'{level}B12', pos=(20 + pos_adj_per_level, 13.75))
            G.add_node(f'{level}B13', pos=(20 + pos_adj_per_level, 16.25))
            G.add_node(f'{level}B14', pos=(20 + pos_adj_per_level, 18.75))
        else:
            #A
            G.add_node(f'{level}A1', pos=(5 + pos_adj_per_level, 26.25))
            G.add_node(f'{level}A2', pos=(5 + pos_adj_per_level, 28.75))
            G.add_node(f'{level}A3', pos=(5 + pos_adj_per_level, 31.25))
            G.add_node(f'{level}A4', pos=(5 + pos_adj_per_level, 33.75))
            G.add_node(f'{level}A5', pos=(5 + pos_adj_per_level, 36.25))
            G.add_node(f'{level}A6', pos=(5 + pos_adj_per_level, 38.75))
            G.add_node(f'{level}A7', pos=(6.25 + pos_adj_per_level, 40))
            G.add_node(f'{level}A8', pos=(8.75 + pos_adj_per_level, 40))
            G.add_node(f'{level}A9', pos=(11.25 + pos_adj_per_level, 40))
            G.add_node(f'{level}A10', pos=(13.75 + pos_adj_per_level, 40))
            G.add_node(f'{level}A11', pos=(10 + pos_adj_per_level, 33.75))
            G.add_node(f'{level}A12', pos=(10 + pos_adj_per_level, 31.25))
            G.add_node(f'{level}A13', pos=(10 + pos_adj_per_level, 28.75))
            G.add_node(f'{level}A14', pos=(10 + pos_adj_per_level, 26.25))
            #B
            G.add_node(f'{level}B1', pos=(5 + pos_adj_per_level, 18.75))
            G.add_node(f'{level}B2', pos=(5 + pos_adj_per_level, 16.25))
            G.add_node(f'{level}B3', pos=(5 + pos_adj_per_level, 13.75))
            G.add_node(f'{level}B4', pos=(5 + pos_adj_per_level, 11.25))
            G.add_node(f'{level}B5', pos=(5 + pos_adj_per_level, 8.75))
            G.add_node(f'{level}B6', pos=(5 + pos_adj_per_level, 6.25))
            G.add_node(f'{level}B7', pos=(6.25 + pos_adj_per_level, 5))
            G.add_node(f'{level}B8', pos=(8.75 + pos_adj_per_level, 5))
            G.add_node(f'{level}B9', pos=(11.25 + pos_adj_per_level, 5))
            G.add_node(f'{level}B10', pos=(13.75 + pos_adj_per_level, 5))
            G.add_node(f'{level}B11', pos=(10 + pos_adj_per_level, 11.25))
            G.add_node(f'{level}B12', pos=(10 + pos_adj_per_level, 13.75))
            G.add_node(f'{level}B13', pos=(10 + pos_adj_per_level, 16.25))
            G.add_node(f'{level}B14', pos=(10 + pos_adj_per_level, 18.75))
            #D
            G.add_node(f'{level}D1', pos=(25 + pos_adj_per_level, 26.25))
            G.add_node(f'{level}D2', pos=(25 + pos_adj_per_level, 28.75))
            G.add_node(f'{level}D3', pos=(25 + pos_adj_per_level, 31.25))
            G.add_node(f'{level}D4', pos=(25 + pos_adj_per_level, 33.75))
            G.add_node(f'{level}D5', pos=(25 + pos_adj_per_level, 36.25))
            G.add_node(f'{level}D6', pos=(25 + pos_adj_per_level, 38.75))
            G.add_node(f'{level}D7', pos=(23.75 + pos_adj_per_level, 40))
            G.add_node(f'{level}D8', pos=(21.25 + pos_adj_per_level, 40))
            G.add_node(f'{level}D9', pos=(18.75 + pos_adj_per_level, 40))
            G.add_node(f'{level}D10', pos=(16.25 + pos_adj_per_level, 40))
            G.add_node(f'{level}D11', pos=(20 + pos_adj_per_level, 33.75))
            G.add_node(f'{level}D12', pos=(20 + pos_adj_per_level, 31.25))
            G.add_node(f'{level}D13', pos=(20 + pos_adj_per_level, 28.75))
            G.add_node(f'{level}D14', pos=(20 + pos_adj_per_level, 26.25))
            #C
            G.add_node(f'{level}C1', pos=(25 + pos_adj_per_level, 18.75))
            G.add_node(f'{level}C2', pos=(25 + pos_adj_per_level, 16.25))
            G.add_node(f'{level}C3', pos=(25 + pos_adj_per_level, 13.75))
            G.add_node(f'{level}C4', pos=(25 + pos_adj_per_level, 11.25))
            G.add_node(f'{level}C5', pos=(25 + pos_adj_per_level, 8.75))
            G.add_node(f'{level}C6', pos=(25 + pos_adj_per_level, 6.25))
            G.add_node(f'{level}C7', pos=(23.75 + pos_adj_per_level, 5))
            G.add_node(f'{level}C8', pos=(21.25 + pos_adj_per_level, 5))
            G.add_node(f'{level}C9', pos=(18.75 + pos_adj_per_level, 5))
            G.add_node(f'{level}C10', pos=(16.25 + pos_adj_per_level, 5))
            G.add_node(f'{level}C11', pos=(20 + pos_adj_per_level, 11.25))
            G.add_node(f'{level}C12', pos=(20 + pos_adj_per_level, 13.75))
            G.add_node(f'{level}C13', pos=(20 + pos_adj_per_level, 16.25))
            G.add_node(f'{level}C14', pos=(20 + pos_adj_per_level, 18.75))
        
        #edges
        #entrance to next level
        dist = distance(G, f'Entr{level}', f'Lvl{level}')
        G.add_edge(f'Entr{level}', f'Lvl{level}', weight=dist)

        for zone in zones:
            #entrance to 1
            dist = distance(G, f'Entr{level}', f'{level}{zone}1')
            G.add_edge(f'Entr{level}', f'{level}{zone}1', weight=dist)

            #entrance to 14
            dist = distance(G, f'Entr{level}', f'{level}{zone}14')
            G.add_edge(f'Entr{level}', f'{level}{zone}14', weight=dist)

            # side spots
            for spot in [1,2,3,4,5,6,7,8,9]:
                dist = distance(G, f'{level}A{spot}', f'{level}A{spot + 1}')
                G.add_edge(f'{level}{zone}{spot}', f'{level}{zone}{spot + 1}', weight=dist)
            
            # mid spots
            for spot in [14,13,12]:
                dist = distance(G, f'{level}A{spot}', f'{level}A{spot - 1}')
                G.add_edge(f'{level}{zone}{spot}', f'{level}{zone}{spot - 1}', weight=dist)
        
        # A11/10 - D11/10
        dist = distance(G, f'{level}A11', f'{level}D11')
        G.add_edge(f'{level}A11', f'{level}D11', weight=dist)
        dist = distance(G, f'{level}A10', f'{level}D10')
        G.add_edge(f'{level}A10', f'{level}D10', weight=dist)
        # B11/10 - C11/10
        dist = distance(G, f'{level}B11', f'{level}C11')
        G.add_edge(f'{level}B11', f'{level}C11', weight=dist)
        dist = distance(G, f'{level}B10', f'{level}C10')
        G.add_edge(f'{level}B10', f'{level}C10', weight=dist)

        pos_adj_per_level += 30
    # from exit to next entrance
    for level in levels:
        if G.nodes.__contains__(f'Entr{level+1}'):
            dist = distance(G, f'Entr{level+1}', f'Lvl{level}')
            G.add_edge(f'Entr{level+1}', f'Lvl{level}', weight=dist)


    nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, node_size=50)
    pos=nx.get_node_attributes(G,'pos')
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    print(nx.dijkstra_predecessor_and_distance(G, f'Entr1')[1])
    plt.show()

def distance(G, first_node, second_node):
    first_node_pos = G.nodes[first_node]['pos']
    second_node_pos =  G.nodes[second_node]['pos']
    dist = math.sqrt((first_node_pos[0]-second_node_pos[0])**2 + (first_node_pos[1]-second_node_pos[1])**2)
    return round(dist,2)

dijkstra(['A', 'B', 'C', 'D'], [1,2,3])