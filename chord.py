import threading
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



#The function for the user's query
def lookup_query(query_id,input_ed,input_aw,node_for_lookup):

    #Get the hash value for the given educational institution
    input_ed_hash = sha1_hash_function(input_ed)


    #Start the lookup from a specific node
    node = chord_ring.lookup(chord_ring.nodes[node_for_lookup], input_ed_hash)

    returned_scientists = []
    for scientist in node.keys_and_values:
        if((scientist[2] == input_ed) and (scientist[1] > int(input_aw))):
            returned_scientists.append(scientist)
    print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    print(f'Returned scientists for query ({query_id}): ')
    for s in returned_scientists:
        print(f'Surname: {s[0]}, Number of awards: {s[1]}, Education: {s[2]}')

    print(f'Data stored at node: {node.ID} ')

# Constructor to create a new node for the chord ring
class Chord_Node:

    def __init__(self, ID):
        self.ID = ID
        self.successor = None
        self.predecessor = None
        self.keys_and_values = []
        self.finger_table = []


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

        #The node checks its successor's keys and values to see if any of these should be assigned to it
        node_keys_and_values = []
        for obj in node.successor.keys_and_values:
            if (obj[3] <= node.ID):
                node_keys_and_values.append(obj)

        node.keys_and_values = node_keys_and_values

        #Update the successor's keys-values array
        temp = [obj for obj in node.successor.keys_and_values if obj not in node.keys_and_values]
        node.successor.keys_and_values = temp

        #Fix the finger tables
        chord_ring.fix_finger_tables()

        return node



    # This is the leave function. It is executed when a node leaves the chord ring
    def node_leave(self, ID):
        node = self.nodes[ID]
        #Assign the node's keys and values to its successor
        node.successor.keys_and_values.extend(node.keys_and_values)
        # The node notifies its predecessor
        node.predecessor.successor = node.successor
        # The node notifies its successor
        node.successor.predecessor = node.predecessor
        #The node leaves the chord ring
        del self.nodes[ID]
        # Fix the finger tables
        chord_ring.fix_finger_tables()


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


    # A function to insert a key in the chord ring
    def key_join(self,scientist):

        # Find the node where the key will be assigned to

        #Check if there is a node with the same identifier as the key
        hash_value = scientist[3]

        #If there is, we assign the key and the value to that node
        if(hash_value in chord_ring.nodes):
            node = chord_ring.nodes[hash_value]
            node.keys_and_values.append([scientist[0],scientist[1],scientist[2],hash_value])


        #If there is not, we search the chord ring to find the key's successor
        else:
          if (hash_value > max(chord_ring.nodes.keys())):
              pos = min(chord_ring.nodes.keys())
              node = chord_ring.nodes[pos]
              node.keys_and_values.append([scientist[0],scientist[1],scientist[2],hash_value])

          else:
              keys = sorted(chord_ring.nodes.keys())
              for k in keys:
                  if k > hash_value:
                      pos = k
                      break
              node = chord_ring.nodes[pos]
              node.keys_and_values.append([scientist[0],scientist[1],scientist[2],hash_value])




    #A function to fix the finger tables of the nodes that are part of the chord ring
    def fix_finger_tables(self):

        for node in chord_ring.nodes.values():
         val = node.ID
         temp_array = []

         for i in range(9):
            temp_array.append(chord_ring.find_node(val + 2**i))
         node.finger_table = temp_array




    #A function to find the node that has to be assigned to a finger table's position
    def find_node(self, val):

        if(val in chord_ring.nodes):
            node = chord_ring.nodes[val]
            return node


        else:
            if(val >= 512):
              node = chord_ring.find_node(val-512)
              return node

            elif((val > max(chord_ring.nodes.keys())) and (val < 512) ):
                pos = min(chord_ring.nodes.keys())
                node = chord_ring.nodes[pos]
                return node
            elif(val < max(chord_ring.nodes.keys())):
                keys = sorted(chord_ring.nodes.keys())
                for k in keys:
                    if k > val:
                        pos = k
                        break
                node = chord_ring.nodes[pos]
                return node


    #The function that executes the lookup operation
    def lookup(self,node,val):

        #Check if this node is the one we are looking for
        key_at_node = False
        for obj in node.keys_and_values:
               if (obj[3] == val):
                key_at_node = True
                break
        if(key_at_node):
            return node

        #If it is not, we keep on searching in the ring
        else:

        #We check if the key's id is between the node's id and its successor's id
         if(node.ID < val <= node.successor.ID):
             returned_node = chord_ring.lookup(node.successor,val)
             return returned_node

        #If it isn't, we use the node's finger table to find the node that is the closest to the key ID in the ring
         else:
             finger_table_IDs = []
             distance_values = []
             for n in node.finger_table:
                 finger_table_IDs.append(n.ID)
                 distance = chord_ring.calculate_distance(n.ID,val)
                 distance_values.append(distance)
             #Find the node with the minimum distance from the key ID
             idx = distance_values.index(min(distance_values))
             node_with_min_distance = finger_table_IDs[idx]

             #Execute the lookup from that node
             node1 = chord_ring.nodes[node_with_min_distance]
             returned_node = chord_ring.lookup(node1,val)
             return returned_node



    #This function is used to calculate the distance between two nodes of the chord ring
    def calculate_distance(self,node,key):
        clockwise_distance = (key - node) if key >= node else (512 - (node - key))
        return clockwise_distance


    def print_chord_ring(self):
        print('Chord Ring: ')
        for node in self.nodes.values():
            print(f'Node ID: {node.ID}, Node successor: {node.successor.ID}, Node predecessor: {node.predecessor.ID} ')
            print(f'\nKeys and values: {node.keys_and_values}')
            print(f'\nFinger table: ')
            for n in node.finger_table:
                print(n.ID)
            print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

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

    chord_ring = Chord_Ring()

    #Add 512 nodes in the chord ring
    for i in range(512):
        chord_ring.node_join(i)

    # We get the hash value of each educational institution (education field) for every scientist, and we insert the information in the chord ring with a key-value format
    for s in scientists:
        for uni in s[2]:
            hash_value = sha1_hash_function(uni)
            key_value = [s[0],s[1],uni,hash_value]
            chord_ring.key_join(key_value)


    chord_ring.print_chord_ring()

    #We ask the user to set the number of queries that he/she wants to be executed simultaneously
    num_of_queries = int(input("Give the number of queries that you want to make: "))


    ed_array = []
    aw_array = []
    node_for_lookup_array = []

    #Get the queries
    for x in range(num_of_queries):
     print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
     print(f'Scientists lookup query ({x})')
     input_ed = input('Please insert the educational institution: ')
     input_aw = input('Please insert the number of awards threshold: ')
     input_node_for_lookup = input('Please insert the node from which you want the lookup to start from: ')
     ed_array.append(input_ed)
     aw_array.append(input_aw)
     node_for_lookup_array.append(input_node_for_lookup)


    #Create the threads
    threads = []
    for i in range(num_of_queries):
        thread = threading.Thread(target=lookup_query, args=(i,ed_array[i],aw_array[i],int(node_for_lookup_array[i])))
        thread.start()
        threads.append(thread)

    #Wait for the threads to finish their execution
    for thread in threads:
        thread.join()
