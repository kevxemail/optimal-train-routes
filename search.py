import collections
import heapq
import sys
from setup import name_id, junction_info, city_loc_processed
from animation import create_map
import tkinter as tk
from great_circle_distance import calcd
from time import perf_counter


"""
Calculates the shortest distance between two cities use Djikstra's algorithm. Like BFS, it checks closest nodes to farthest nodes. We use a minheap to grab the next closest city from the initial city1 and add that to the fringe to continue processing. We continue doing this until we get to city2. The set closed is used to make sure we don't go backwards to cities we've already checked. Basically, there's a chance we will add duplicate cities to the fringe with different distances depending how we got there. However, with the closed set we will first process the closest path to that city off the minheap, then add it to the closed set so future ones pulled off the minheap aren't processed
PARAMS:
city1: String for the name of city1
city2: String for the name of city2
lines: The stored lines we drew for the train routes for the United States
r: Root to update the tkinter GUI
c: Canvas to change line colors as we search and find the correct path
RETURN:
Distance between the two cities
"""
def djikstra(city1, city2, lines, r, c): # Basically A* without heuristics 
    city1_id = name_id[city1]
    city2_id = name_id[city2]
    closed = set()
    start = (0, city1_id) # Starting node store as (distance from city1, city name, parent)
    fringe = []
    heapq.heapify(fringe) # This is now a minheap so we can grab the closest city for djikstra's which is exhaustive

    parents = dict() # Use to keep track of the parent so we can go back at the end with the correct path

    closed.add(start)
    heapq.heappush(fringe, start)

    loop_count = 0 # Use this to determine when we should update the root (r).
    while (len(fringe) > 0):
        if loop_count == 600:
            r.update()
            loop_count = 0
        v = heapq.heappop(fringe) # Pop the closest citys
        if (v[1] == city2_id): # If it's the goal city then we're done
            curr = v
            loop_count = 0
            while (curr in parents): # Keep going until we reach the start node again
                c1 = parents[curr][1]
                c2 = curr[1]
                line = lines[c1, c2]
                c.itemconfig(line, fill="blue")
                curr = parents[curr]
                loop_count += 1
            r.update() # Update the GUI one last time before returning
            return v
        if (v[1] not in closed): # Check if we've already found the shortest path for this particular node
            closed.add(v[1]) # We add items to the set closed after removing it from the fringe instead of when we add to guarantee we are getting the shortest path. Might add the goal city to the fringe multiple times but becaue of the heap we are popping the shortest distanced one guaranteed
            for child in junction_info[v[1]]: # Traverse through each city this is connected with
                if (child not in closed): # Don't want to go backwards to something we've already visited
                    distance, city_id = child # Unpack the tuple
                    depth = v[0] + distance # New calculated distance from city 1 
                    curr_node = (depth, city_id)
                    line = lines[v[1], city_id] # Color the explored line red
                    c.itemconfig(line, fill="red")
                    parents[curr_node] = v # Create a way to backtrack to find the parent
                    heapq.heappush(fringe, curr_node)
        loop_count += 1
    r.update()   
    return None

"""
Calculates the shortest distance between two cities use Bidirectional Djikstra's algorithm. One starts from the beginning and one starts from the end
PARAMS:
city1: String for the name of city1
city2: String for the name of city2
lines: The stored lines we drew for the train routes for the United States
r: Root to update the tkinter GUI
c: Canvas to change line colors as we search and find the correct path
RETURN:
Distance between the two cities
"""
def BidirectionalDjikstra(city1, city2, lines, r, c): # Basically A* without heuristics 
    city1_id = name_id[city1]
    city2_id = name_id[city2]
    closed = set()
    start = (0, city1_id) # Starting node store as (distance from city1, city name, parent)
    fringe = []
    heapq.heapify(fringe) # This is now a minheap so we can grab the closest city for djikstra's which is exhaustive
    parents = dict() # Use to keep track of the parent so we can go back at the end with the correct path
    closed.add(start)
    heapq.heappush(fringe, start)

    closed2 = set()
    start2 = (0, city2_id)
    fringe2 = []
    heapq.heapify(fringe2)
    parents = dict()
    closed2.add(start2)
    heapq.heappush(fringe2, start2)

    loop_count = 0 # Use this to determine when we should update the root (r).
    while (len(fringe) > 0):
        if loop_count == 600:
            r.update()
            loop_count = 0
        v = heapq.heappop(fringe) # Pop the closest citys
        if (v[1] == city2_id): # If it's the goal city then we're done
            curr = v
            loop_count = 0
            while (curr in parents): # Keep going until we reach the start node again
                c1 = parents[curr][1]
                c2 = curr[1]
                line = lines[c1, c2]
                c.itemconfig(line, fill="blue")
                curr = parents[curr]
                loop_count += 1
            r.update() # Update the GUI one last time before returning
            return v
        if (v[1] not in closed): # Check if we've already found the shortest path for this particular node
            closed.add(v[1]) # We add items to the set closed after removing it from the fringe instead of when we add to guarantee we are getting the shortest path. Might add the goal city to the fringe multiple times but becaue of the heap we are popping the shortest distanced one guaranteed
            for child in junction_info[v[1]]: # Traverse through each city this is connected with
                if (child not in closed): # Don't want to go backwards to something we've already visited
                    distance, city_id = child # Unpack the tuple
                    depth = v[0] + distance # New calculated distance from city 1 
                    curr_node = (depth, city_id)
                    line = lines[v[1], city_id] # Color the explored line red
                    c.itemconfig(line, fill="red")
                    parents[curr_node] = v # Create a way to backtrack to find the parent
                    heapq.heappush(fringe, curr_node)
        loop_count += 1
    r.update()   
    return None

"""
Heuristic which estimates the distance from city1 to city2 pretending that there is a straight shot between them. This is guaranteed to underestimate or be equal to the actual distance which is good.
PARAMETERS:
city1_id: id for city1
city2_id: id for city2
RETURN:
The distance between the two cities as if it were a straight shot
"""
def circle_heuristic(city1_id, city2_id):
    return calcd(city_loc_processed[city1_id], city_loc_processed[city2_id])

"""
Finds the shortest path with A* search. Similar logic to code above but with a heuristic
PARAMS:
city1: String for the name of city1
city2: String for the name of city2
lines: The stored lines we drew for the train routes for the United States
r: Root to update the tkinter GUI
c: Canvas to change line colors as we search and find the correct path
RETURN:
Distance between the two cities
"""
def AStar(city1, city2, lines, r, c): # Same algo as above but we add a heuristic

    city1_id = name_id[city1]
    city2_id = name_id[city2]

    closed = set()
    heuristic = circle_heuristic(city1_id, city2_id)
    start = (heuristic, 0, city1_id) # Starting node store as (distance from city1, city name)
    fringe = []
    heapq.heapify(fringe) # This is now a minheap so we can grab the closest city for djikstra's which is exhaustive

    parents = dict() # Use to keep track of the parent so we can go back at the end with the correct path

    closed.add(start)
    heapq.heappush(fringe, start)
    loop_count = 0 # Use this to determine when we should update the root (r).
    while (len(fringe) > 0):
        if loop_count == 600:
            r.update()
            loop_count = 0
        v = heapq.heappop(fringe) # Pop the closest citys
        if (v[2] == city2_id): # If it's the goal city then we're done
            curr = v
            while (curr in parents): # Keep going until we reach the start node again
                c1 = parents[curr][2]
                c2 = curr[2]
                line = lines[c1, c2]
                c.itemconfig(line, fill="blue")
                curr = parents[curr]
            r.update() # Update the GUI one last time before returning
            return v
        if (v[2] not in closed): # Check if we've already found the shortest path for this particular node
            closed.add(v[2]) # We add items to the set closed after removing it from the fringe instead of when we add to guarantee we are getting the shortest path. Might add the goal city to the fringe multiple times but becaue of the heap we are popping the shortest distanced one guaranteed
            for child in junction_info[v[2]]: # Traverse through each city this is connected with
                if (child not in closed): # Don't want to go backwards to something we've already visited
                    distance, city_id = child # Unpack the tuple
                    heuristic = circle_heuristic(city_id, city2_id) # Heuristic calculation
                    depth = v[1] + distance # New calculated distance from city 1, taking into account the new distance from the parent to this child
                    line = lines[v[2], city_id] # Color the explored line red
                    c.itemconfig(line, fill="red")
                    curr_node = (heuristic + depth, depth, city_id) # Create new node to put on fringe
                    parents[curr_node] = v
                    heapq.heappush(fringe, curr_node)
                    loop_count += 1
                    if loop_count == 600: # Unlike djikstra's I'm also having the GUI update here because A* is too fast to observe otherwise
                        r.update()
                        loop_count = 0
    return None


"""
Reverse A*. It performs as bad as it sounds. Use a maxheap instead of a minheap
PARAMS:
city1: String for the name of city1
city2: String for the name of city2
lines: The stored lines we drew for the train routes for the United States
r: Root to update the tkinter GUI
c: Canvas to change line colors as we search and find the correct path
RETURN:
Distance between the two cities
"""
def ReverseAStar(city1, city2, lines, r, c): # Same algo as above but we add a heuristic

    city1_id = name_id[city1]
    city2_id = name_id[city2]

    closed = set()
    heuristic = circle_heuristic(city1_id, city2_id)
    start = (-1 * heuristic, 0, city1_id) # Starting node store as (distance from city1, city name)
    fringe = []
    heapq.heapify(fringe) # This is now a minheap so we can grab the closest city for djikstra's which is exhaustive

    parents = dict() # Use to keep track of the parent so we can go back at the end with the correct path

    closed.add(start)
    heapq.heappush(fringe, start)
    loop_count = 0 # Use this to determine when we should update the root (r).
    while (len(fringe) > 0):
        if loop_count == 600:
            r.update()
            loop_count = 0
        v = heapq.heappop(fringe) # Pop the closest citys
        if (v[2] == city2_id): # If it's the goal city then we're done
            curr = v
            while (curr in parents): # Keep going until we reach the start node again
                c1 = parents[curr][2]
                c2 = curr[2]
                line = lines[c1, c2]
                c.itemconfig(line, fill="blue")
                curr = parents[curr]
            r.update() # Update the GUI one last time before returning
            return v
        if (v[2] not in closed): # Check if we've already found the shortest path for this particular node
            closed.add(v[2]) # We add items to the set closed after removing it from the fringe instead of when we add to guarantee we are getting the shortest path. Might add the goal city to the fringe multiple times but becaue of the heap we are popping the shortest distanced one guaranteed
            for child in junction_info[v[2]]: # Traverse through each city this is connected with
                if (child not in closed): # Don't want to go backwards to something we've already visited
                    distance, city_id = child # Unpack the tuple
                    heuristic = circle_heuristic(city_id, city2_id) # Heuristic calculation
                    depth = v[1] + distance # New calculated distance from city 1, taking into account the new distance from the parent to this child
                    line = lines[v[2], city_id] # Color the explored line red
                    c.itemconfig(line, fill="red")
                    curr_node = (-1 * (heuristic + depth), depth, city_id) # Create new node to put on fringe
                    parents[curr_node] = v
                    heapq.heappush(fringe, curr_node)
                    loop_count += 1
                    if loop_count == 600: # Unlike djikstra's I'm also having the GUI update here because A* is too fast to observe otherwise
                        r.update()
                        loop_count = 0
    return None

"""
Finds a path with BFS. Not guaranteed to be shortest.
PARAMS:
city1: String for the name of city1
city2: String for the name of city2
lines: The stored lines we drew for the train routes for the United States
r: Root to update the tkinter GUI
c: Canvas to change line colors as we search and find the correct path
RETURN:
Distance between the two cities
"""
def BFS(city1, city2, lines, r, c):

    city1_id = name_id[city1]
    city2_id = name_id[city2]

    visited = set()

    fringe = collections.deque()

    parents = dict() # Use to keep track of the parent so we can go back at the end with the correct path

    visited.add(city1_id)
    fringe.append(city1_id)
    loop_count = 0 # Use this to determine when we should update the root (r).
    while (len(fringe) > 0):
        if loop_count == 600:
            r.update()
            loop_count = 0
        v = fringe.popleft()
        if (v == city2_id): # If it's the goal city then we're done
            curr = v
            while (curr in parents): # Keep going until we reach the start node again
                c1 = parents[curr]
                c2 = curr
                line = lines[c1, c2]
                c.itemconfig(line, fill="blue")
                curr = parents[curr]
            r.update() # Update the GUI one last time before returning
            return v
        for child in junction_info[v]:
            distance, city_id = child
            if (city_id not in visited):
                visited.add(city_id)
                fringe.append(city_id)
                parents[city_id] = v
                line = lines[v, city_id] # Color the explored line red
                c.itemconfig(line, fill="red")
        loop_count += 1
    return None

"""
Finds a path with DFS. Not guaranteed to be shortest.
PARAMS:
city1: String for the name of city1
city2: String for the name of city2
lines: The stored lines we drew for the train routes for the United States
r: Root to update the tkinter GUI
c: Canvas to change line colors as we search and find the correct path
RETURN:
Distance between the two cities
"""
def DFS(city1, city2, lines, r, c):

    city1_id = name_id[city1]
    city2_id = name_id[city2]

    visited = set()

    fringe = collections.deque()

    parents = dict() # Use to keep track of the parent so we can go back at the end with the correct path

    visited.add(city1_id)
    fringe.append(city1_id)
    loop_count = 0 # Use this to determine when we should update the root (r).
    while (len(fringe) > 0):
        if loop_count == 600:
            r.update()
            loop_count = 0
        v = fringe.pop()
        if (v == city2_id): # If it's the goal city then we're done
            curr = v
            while (curr in parents): # Keep going until we reach the start node again
                c1 = parents[curr]
                c2 = curr
                line = lines[c1, c2]
                c.itemconfig(line, fill="blue")
                curr = parents[curr]
            r.update() # Update the GUI one last time before returning
            return v
        for child in junction_info[v]:
            distance, city_id = child
            if (city_id not in visited):
                visited.add(city_id)
                fringe.append(city_id)
                parents[city_id] = v
                line = lines[v, city_id] # Color the explored line red
                c.itemconfig(line, fill="red")
        loop_count += 1
    return None
"""
Actual searching algo for ID-DFS
"""
def k_DFS(city1_id, city2_id, lines, r, c, k):

    visited = set()

    fringe = collections.deque()

    parents = dict() # Use to keep track of the parent so we can go back at the end with the correct path

    visited.add(city1_id)
    fringe.append((city1_id, 0))
    loop_count = 0 # Use this to determine when we should update the root (r).
    while (len(fringe) > 0):
        if loop_count == 600:
            r.update()
            loop_count = 0
        v = fringe.pop()
        if (v[0] == city2_id): # If it's the goal city then we're done
            curr = v
            while (curr in parents): # Keep going until we reach the start node again
                c1 = parents[curr][0]
                c2 = curr[0]
                line = lines[c1, c2]
                c.itemconfig(line, fill="blue")
                curr = parents[curr]
            r.update() # Update the GUI one last time before returning
            return v
        if (v[1] > k):
            return None
        for child in junction_info[v[0]]:
            distance, city_id = child
            if (city_id not in visited):
                temp = (city_id, distance + v[1])
                visited.add(city_id)
                fringe.append(temp)
                parents[temp] = v
                line = lines[v[0], city_id] # Color the explored line red
                c.itemconfig(line, fill="red")
        loop_count += 1
    return None

"""
Finds a path with ID-DFS. Not guaranteed to be shortest.
PARAMS:
city1: String for the name of city1
city2: String for the name of city2
lines: The stored lines we drew for the train routes for the United States
r: Root to update the tkinter GUI
c: Canvas to change line colors as we search and find the correct path
RETURN:
Distance between the two cities
"""
def ID_DFS(city1, city2, lines, r, c): 
    city1_id = name_id[city1]
    city2_id = name_id[city2]
    temp = circle_heuristic(city1_id, city2_id)
    max_depth = temp
    result = None
    while (result is None):
        result = k_DFS(city1_id, city2_id, lines, r, c, max_depth)
        max_depth = max_depth + temp
    return result

def main():
    city1 = sys.argv[1]
    city2 = sys.argv[2]

    root = tk.Tk() #creates the frame
    canvas = tk.Canvas(root, height=1000, width=1000, bg='white') #creates a canvas widget, which can be used for drawing lines and shapes
    lines = create_map(root, canvas)
    canvas.pack(expand=True) #packing widgets places them on the board

    algo = ""
    while (algo != "BFS" and algo != "DFS" and algo != "djikstra" and algo != "a-star" and algo != "ID-DFS" and algo != "Reverse AStar"):
        print("Type the algorithm you would like to use:")
        print("'a-star' for A* Search")
        print("'djikstra' for Djikstra's Algorithm")
        print("'BFS' for BFS search")
        print("'DFS' for DFS Search")
        print("'ID-DFS' for Iterative Deepening DFS search")
        print("'Reverse AStar' for Reverse A* Search")
        algo = input()
    print("Click enter to begin searching")
    input()
    if (algo == "BFS"):
        print(BFS(city1, city2, lines, root, canvas))
    if (algo == "DFS"):
        print(DFS(city1, city2, lines, root, canvas))
    if (algo == "a-star"):
        print(AStar(city1, city2, lines, root, canvas))
    if (algo == "djikstra"):
        print(djikstra(city1, city2, lines, root, canvas))
    if (algo == "ID-DFS"):
        print(ID_DFS(city1, city2, lines, root, canvas))
    if (algo == "Reverse AStar"):
        print(ReverseAStar(city1, city2, lines, root, canvas))
    root.mainloop()

    """
    Commented code below is if you want to test the run time of each algorithm individually without animation.
    """
    # start = perf_counter()
    # res1 = djikstra(city1, city2, {})
    # end = perf_counter()
    # time1 = end-start

    # start = perf_counter()
    # res2 = AStar(city1, city2, {})
    # end = perf_counter()
    # time2 = end-start

    # print(city1, "to", city2, "with Djikstra:", res1[0], "in", time1, "seconds")
    # print(city1, "to", city2, "with A*:", res2[1], "in", time2, "seconds")

if __name__ == "__main__":
    main()