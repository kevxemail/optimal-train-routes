import heapq
from setup import id_name_conversion, junction_information

# Global dictionary (hash map) for the id to name conversions
name_id = dict() # Form of {name: id}
# Global data structure to see which city goes to which city for train routes.
junction_info = dict() # This will be of the form {city_id: [(distance, city), (distance, city), etc...]}

id_city  = list() # Get the list of strings of id to city information
with open("./files/rrNodeCity.txt") as f:
    id_city = [line.strip() for line in f]

junctions = list() # Get the list of strings that tells you which junction leads to which
with open("./files/rrEdges.txt") as f:
    junctions = [line.strip() for line in f]

city_locations = list() # Get the list of strings that tells you the longitude and latitude of each city
with open("./files/rrNodes.txt") as f:
    city_locations = [line.strip() for line in f]

name_id = id_name_conversion(id_city) # Initialize the global variables with methods from setup.py
junction_info = junction_information(junctions, city_locations)

"""
Calculates the shortest distance between two cities use Djikstra's algorithm. Like BFS, it checks closest nodes to farthest nodes. We use a minheap to grab the next closest city from the initial city1 and add that to the fringe to continue processing. We continue doing this until we get to city2. The set closed is used to make sure we don't go backwards to cities we've already checked. Basically, there's a chance we will add duplicate cities to the fringe with different distances depending how we got there. However, with the closed set we will first process the closest path to that city off the minheap, then add it to the closed set so future ones pulled off the minheap aren't processed
PARAMS:
city1: String for the name of city1
city2: String for the name of city2
RETURN:
Distance between the two cities
"""
def djikstra(city1, city2): # Basically A* without heuristics 
    city1_id = name_id[city1]
    city2_id = name_id[city2]
    goal = city2_id

    closed = set()
    start = (0, city1_id) # Starting node store as (distance from city1, city name)
    fringe = []
    heapq.heapify(fringe) # This is now a minheap so we can grab the closest city for djikstra's which is exhaustive

    closed.add(start)
    heapq.heappush(fringe, start)

    while (len(fringe) > 0):
        v = heapq.heappop(fringe) # Pop the closest citys
        if (v[1] == city2_id): # If it's the goal city then we're done
            return v
        if (v[1] not in closed): # Check if we've already found the shortest path for this particular node
            closed.add(v[1]) # We add items to the set closed after removing it from the fringe instead of when we add to guarantee we are getting the shortest path. Might add the goal city to the fringe multiple times but becaue of the heap we are popping the shortest distanced one guaranteed
            for child in junction_info[v[1]]: # Traverse through each city this is connected with
                if (child not in closed): # Don't want to go backwards to something we've already visited
                    distance, city_id = child # Unpack the tuple
                    depth = v[0] + distance # New calculated distance from city 1 
                    curr_node = (depth, city_id)
                    heapq.heappush(fringe, curr_node)
    return None

def main():

    print(djikstra("Albuquerque", "Atlanta"))

if __name__ == "__main__":
    main()