import socket
import sys
import pickle
import math
import os

# Helper functions for sockets

def create_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock

def create_server_side(ip, port, number_of_nodes):
    sock = create_socket()
    sock.bind((ip, int(port)))
    sock.listen(int(number_of_nodes))
    return sock

def create_client_side(ip, port):
    sock = create_socket()
    sock.connect((ip, int(port)))
    return sock

# Helper function for parsing costs file

def read_costs_file(port_number):
    neigh = []
    dis_vec = {}
    costs_file_name = f"{port_number}.costs"
    with open(costs_file_name, 'r') as cost_file:
        number_of_nodes = int(cost_file.readline())
        # print("number of nodes: ", number_of_nodes)

        for line in cost_file.readlines():
            neigh_node, cost = map(int, line.strip().split())
            neigh.append(neigh_node)
            dis_vec[neigh_node] = cost

    return neigh, dis_vec, number_of_nodes

# initialize the distance vector

def init_dis_vec_for_bf_algo(number_of_nodes, dist_vec):
    for i in range(3000, 3000 + int(number_of_nodes)):
        dist_vec.setdefault(i, math.inf)

# bellman ford algorithm implementation

def bellman_ford(dist_vec, counter, rcv_data, flag):
    for key in rcv_data.keys():
        if key in dist_vec.keys():
            if dist_vec[key] > rcv_data[key] + dist_vec[counter]:
                dist_vec[key] = rcv_data[key] + dist_vec[counter]
                flag = True
        else:
            dist_vec[key] = rcv_data[key] + dist_vec[counter]
            flag = True
    return flag, dist_vec


def main():
    
    localhost = '127.0.0.1'
    port_number = sys.argv[1]  # get port number from terminal
    neigh = []  # list of neighbors nodes
    dis_vec = {}  # dict of distance vector
    con = None
    
    neigh, dis_vec, number_of_nodes = read_costs_file(
        port_number)  # read costs file
    dis_vec[int(port_number)] = 0  # 0 cost for itself

    # prepare initialize distance vector
    init_dis_vec_for_bf_algo(number_of_nodes, dis_vec)

    ## debug print
    # print("port_number", port_number)
    # print("neyybirrrsss: ", neigh)
    # print("distinsss: ", dis_vec)

    #create server side socket
    server_side = create_server_side(
        localhost, int(port_number), number_of_nodes)
    server_side.settimeout(5)

    for ne in neigh:
        try:
            client_side = create_client_side(localhost, ne)
            client_side.sendall(pickle.dumps(dis_vec))
            client_side.close()
        except:
            # print("debug vovovovov1")
            pass

    try:
        while 1:
            flag = False

            for n in neigh:
                con, addr = server_side.accept()
                rcv_data = con.recv(3444)
                rcv_data = pickle.loads(rcv_data)
                con.close()

                nc = 0
                for key in rcv_data:
                    if rcv_data[key] == 0:
                        nc = key
                        break
     
                flag, dis_vec = bellman_ford(dis_vec, nc, rcv_data, flag)

            if flag:
                flag = False

                for ne in neigh:
                    try:
                        client_side = create_client_side(
                            localhost, ne)
                        client_side.sendall(pickle.dumps(dis_vec))
                        client_side.close()
                    except:
                        pass  # print("debug vovovovov2")

    except socket.timeout:
        con.close()
        server_side.close()
        # sorted_disc_vec = sorted(dis_vec.items(), key=lambda x: x[1])
        # print(dis_vec)
        for key in sorted(dis_vec):
            print(port_number, "-", key, "|", dis_vec[key])
        print("\n")
            


if __name__ == '__main__':
    main()
