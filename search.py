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

def djikstra(city1id, city2id):
    goal = city2id
    
    closed = set()
    heuristic = taxicabHeuristic(board, size, positionTracker)
    start = (heuristic, 0, board) # Starting node, storing in tuples like (f(x) = g(x) + h(x) which is initially just h(x), depth, board)
    fringe = []
    heapq.heapify(fringe) # This is now a minheap

    closed.add(start)
    heapq.heappush(fringe, start)

    while (len(fringe) > 0):
        v = heapq.heappop(fringe) # Pop the minimum off of the board
        if (v[2] == goalBoard): # If it's the goal board then we're done
            return v
        if (v[2] not in closed): # Check if we've already found the shortest path for this particular node
            closed.add(v[2]) # We add items to the set closed after removing it from the fringe instead of when we add 
            for child in get_children(v[2], size):
                if (child not in closed):
                    depth = v[1] + 1 # It is one more depth than its parent, g(x)
                    heuristic = taxicabHeuristic(v[2], size, positionTracker) # Get the heuristic value, h(x)
                    temp = (heuristic + depth, depth, child)
                    heapq.heappush(fringe, temp)
    return None

def main():



    name_id = id_name_conversion(id_city) 
    junction_info = junction_information(junctions, city_locations)

if __name__ == "__main__":
    main()