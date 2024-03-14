#version 2

import json
import hashlib



#The hash function used to produce the IDs
def sha1_hash_function(input):
    #Calculate the hash value, returned by the SHA-1 hash function, in hexadecimal format
    hash_value = hashlib.sha1(input.encode()).hexdigest()
    #We transform the hex hash value into a decimal value, and we keep only the first 9 bits of its binary format (the value remains in decimal format)
    hash_dec = int(hash_value, 16) >> (160 - 9)
    #By this way, the hash function returns decimal hash values between 0 and 511, which is what we want since we choose to have 512 identifiers
    return hash_dec



# Constructor to create a new node for the chord ring
class Chord_Node:

    def __init__(self, ID):
        self.ID = ID
        self.successor = None
        self.predecessor = None



# Constructor to create the chord ring and add the nodes in it
class Chord_Ring:
    def __init__(self):
        # The nodes that the chord ring contains
        self.nodes = {}

    # This is the join function. It is executed when a node joins the chord ring
    def node_join(self,ID):
        #Create the node
        node = Chord_Node(ID)
        #Add the node to the ring
        self.nodes[ID] = node
        #Find the node's successor
        node.successor = chord_ring.find_successor(ID)
        #The node notifies its successor
        node.successor.predecessor = node
        #Find the node's predecessor
        node.predecessor = chord_ring.find_predecessor(ID)
        # The node notifies its predecessor
        node.predecessor.successor = node
        return node


    # This is the leave function. It is executed when a node leaves the chord ring
    def node_leave(self, ID):
        node = self.nodes[ID]
        # The node notifies its predecessor
        node.predecessor.successor = node.successor
        # The node notifies its successor
        node.successor.predecessor = node.predecessor
        #The node leaves the chord ring
        del self.nodes[ID]


    # A function to find the successor of a node that joins the chord ring
    def find_successor(self, node_ID):
        # Get the list of the nodes' IDs
        node_IDs = list(self.nodes.keys())
        # Sort the list
        node_IDs.sort()
        # Find the index of the given node ID
        index = node_IDs.index(node_ID)
        # If the given node ID is the last in the list, return the first node ID
        if index == len(node_IDs) - 1:
            return self.nodes[node_IDs[0]]
        # Otherwise, return the successor
        return self.nodes[node_IDs[index + 1]]

    # A function to find the predecessor of a node that joins the chord ring
    def find_predecessor(self, node_ID):
        # Get the list of the nodes' IDs
        node_IDs = list(self.nodes.keys())
        # Sort the list
        node_IDs.sort()
        # Find the index of the given node ID
        index = node_IDs.index(node_ID)
        # If the given node ID is the first in the list, return the last node ID
        if index == 0:
            return self.nodes[node_IDs[-1]]
        # Otherwise, return the predecessor
        return self.nodes[node_IDs[index - 1]]

    def print_chord_ring(self):
        for node in self.nodes.values():
            print(f'Node ID: {node.ID}, Node successor: {node.successor.ID}, Node predecessor: {node.predecessor.ID} ')






# Main function
if __name__ == '__main__':

    # Get the data from the JSON file
    with open('scientist_info.json', 'r', encoding="utf-8") as file:
        data = json.load(file)

    # fetch the surnames
    surnames = [scientist['surname'] for scientist in data]


    # fetch the number of awards
    awards = [scientist['awards'] for scientist in data]
    awards_int = [int(aw) for aw in awards]

    # fetch the education
    education = [scientist['education'] for scientist in data]

    counter = 0;  # counter used for the attributes insertion in the attributes_array.
    attributes_array = []

    for s in surnames:
        temp_list = [surnames[counter], awards_int[counter], education[counter]]
        attributes_array.append(temp_list)
        counter = counter + 1


    # Example usage:
    chord_ring = Chord_Ring()
    node1 = chord_ring.node_join(1)

    node2 = chord_ring.node_join(3)

    node3 = chord_ring.node_join(2)

    node4 = chord_ring.node_join(4)

    node5 = chord_ring.node_join(0)



    chord_ring.print_chord_ring()

    print('\nNode leave (2)')
    chord_ring.node_leave(2)
    chord_ring.print_chord_ring()

    print('\nNode leave (0)')
    chord_ring.node_leave(0)
    chord_ring.print_chord_ring()

    print('\nNode join (2)')
    chord_ring.node_join(2)
    chord_ring.print_chord_ring()

    print('\nNode join (5)')
    chord_ring.node_join(5)
    chord_ring.print_chord_ring()








