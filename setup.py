from heuristic import calcd # Get the method we need for distances between cities
# Global dictionary (hash map) for the id to name conversions
id_name = dict() # Form of {id: name}
# Global data structure to see which city goes to which city for train routes.
junction_info = dict() # This will be of the form {city_id: [(distance, city), (distance, city), etc...]}

"""
Fill out a dictionary with id to city conversions in the form of {id: name}
PARAMETERS:
id_city: List of strings with the format "xxxxxxx cityName" for each index
RETURN: void
"""
def id_name_conversion(id_city):
    id_name = dict()
    for conversion in id_city:
        conversion = conversion.split() # Split the id and name into two seperate variables
        id, name = conversion[0], conversion[1]
        id_name[id] = name
    return id_name

"""
AFTER the id_name dictionary is correctly filled out, utilize this method to fill out junctions so that
each city (the key) refers to a list of which cities it directly leads to (the value). This will be stored as a list of tuples because we also want to store the distance
PARAMETERS:
junctions: list of strings which contains information about which cities are connected
city_locations: list of strings which contains information about the longitude/latitude of eachc ity
"""
def junction_information(junctions, city_locations):
    city_loc_processed = dict() # Make a dict of city_id:(latitude, longitude) for less of a headache
    junction_info = dict() # This will be of the form city: [(distance, city), (distance, city), etc...]

    for i in city_locations: # Process the city locations into a dictionary to make it less annoying
        curr = i.split()
        city_id, latitude, longitude = curr
        latitude = float(latitude) # Convert from a string to a float
        longitude = float(longitude)
        city_loc_processed[city_id] = (latitude, longitude)

    for i in junctions:
        curr = i.split()
        city_id1, city_id2 = curr # Get the city ids

        coordinates1 = city_loc_processed[city_id1] # Get the coordinates for the cities
        coordinates2 = city_loc_processed[city_id2]
        distance = calcd(coordinates1, coordinates2) # Get their distance with the heuristic function

        if city_id1 not in junction_info:
            junction_info[city_id1] = list()

        junction_info[city_id1].append((distance, city_id2)) # Append the tuple as (distance, other city id)
            
        if city_id2 not in junction_info:
            junction_info[city_id2] = list()
        junction_info[city_id2].append((distance, city_id1)) # Trains can go both ways

    return junction_info

def main():
    id_city  = list() # Get the list of strings of id to city information
    with open("./files/rrNodeCity.txt") as f:
        id_city = [line.strip() for line in f]

    junctions = list() # Get the list of strings that tells you which junction leads to which
    with open("./files/rrEdges.txt") as f:
        junctions = [line.strip() for line in f]

    city_locations = list() # Get the list of strings that tells you the longitude and latitude of each city
    with open("./files/rrNodes.txt") as f:
        city_locations = [line.strip() for line in f]
    
    id_name = id_name_conversion(id_city)
    junction_info = junction_information(junctions, city_locations)

if __name__ == "__main__":
    main()