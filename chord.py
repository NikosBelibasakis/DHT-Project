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
        self.keys = {}



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

    #Fetch the data from the JSON file
    with open('scientist_info.json', 'r', encoding="utf-8") as file:
        data = json.load(file)

    scientists = []

    for item in data:
        surname = item['surname']
        awards = item['awards']
        education = item['education']

        #Check if the scientist has studied in more than one educational institutions
        if ', ' in education:
            education = education.split(', ')
        else:
            education = [education]

        scientist = [surname, awards, education]
        scientists.append(scientist)



    for s in scientists:
        print(s)




    chord_ring = Chord_Ring()



    #Add 512 nodes in the chord ring
    for i in range(512):
        chord_ring.node_join(i)


    #!!TEMP COMMENT!!
   # print('Chord ring: ')
   # chord_ring.print_chord_ring()

















