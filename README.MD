# Distance-Vector Routing Protocol

This repository contains the implementation of a distance-vector routing protocol. The protocol is implemented in Python and allows nodes in a network to communicate asynchronously using TCP sockets. The algorithm terminates when there are no more updates to be made in any of the distance vectors of the nodes.

## Implementation Details

The implementation consists of a single `Node.py` file that is run separately for each node in the network. The nodes communicate with each other by sending and receiving distance vector updates.

## Creating the Nodes and Initializing Costs

- Each node reads its assigned `<port>.costs` file from the disk to populate its initial distance vector.
- The initial distances for nodes that are not immediate neighbors of the current node are set to infinite.
- Every node starts listening on its assigned port number on `localhost` (127.0.0.1) to receive distance vector updates from neighboring nodes.

## Sending Distance Vector Updates

- Each node sends its initial distance vector to its immediate neighboring nodes.
- When a node receives a distance vector update, it checks each node in the entire network.
- For each node y, the distance to node y is updated based on the formula: `distx(y) = min {dist(x, v) + dist(v, y)}` for every v ∈ immediate neighbors of x. (Bellman-Ford Algorithm)
- If this update causes any change in the distance vector, the node advertises its new distance vector to its immediate neighbors.
- This distributed and asynchronous communication continues until there are no more updates on any of the nodes of the network.
The algorithm terminates after 5 seconds of inactivity, indicating no further updates.

## Overall Stages
- Read the neighborhood information from the `.costs` file.
- Send the node's distance vector to every immediate neighbor.
- Listen for updates from the neighbors.
- Attempt to update the distance vector by using received distance vectors.
- If no update happens for 5 seconds, close all connections and print the distance vector.

## Usage
1. Clone the repository: 
```
git clone https://github.com/ramazantokay/Distance-Vector-Routing-Protocol.git
```
2. Navigate to the repository: 
```
cd Distance-Vector-Routing-Protocol
```
3. Run the `Node.py` script for each node in the network, providing the appropriate arguments (e.g., port number, .costs file).
4. The nodes will start communicating and updating their distance vectors.
5. Once the algorithm terminates, the nodes will close their connections and print out their final distance vectors.
6. Additionally, you can test your implementation by running the "runner.sh" in the test_inputs folder. This script will run the nodes with the given inputs.

## Acknowledgements
This project is based on the Go-Back-N protocol described in the textbook "Computer Networking: A Top-Down Approach" by James F. Kurose and Keith W. Ross.