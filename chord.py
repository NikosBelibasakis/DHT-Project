#version 1
import json

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


