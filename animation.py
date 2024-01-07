from setup import name_id, junction_info, city_loc_processed
import tkinter as tk

"""
Transforms the Y coordinates to be standardized for tkinter
PARAMETERS: 
Coordinate - the coordinate to transform
RETURN:
The transformed coordinate
"""
def transform_coordinate_y(coordinate): # Fiddled with these until it looked good
    coordinate = 14 * coordinate 
    return coordinate

"""
Transforms the X coordinates to be standardized for tkinter
PARAMETERS: 
Coordinate - the coordinate to transform
RETURN:
The transformed coordinate
"""
def transform_coordinate_x(coordinate):
    coordinate = 13 * coordinate
    coordinate = coordinate * -1
    return coordinate

"""
Initializes the tkinter map of train routes in the United States
PARAMETERS: 
r: root for tkinter to update the graphic once the map has been generated
c: tkinter canvas to draw the lines
RETURN:
Dictionary mapping two city ids in a tuple to a line
"""
def create_map(r, c): # Create empty map of the united states
    lines = dict()
    for city_id in junction_info:
        for element in junction_info[city_id]:
            distance, other_city_id = element

            coordinates1 = city_loc_processed[city_id]
            coordinates2 = city_loc_processed[other_city_id]
            y1 = transform_coordinate_y(coordinates1[0])
            y2 = transform_coordinate_y(coordinates2[0])

            x1 = transform_coordinate_x(coordinates1[1])
            x2 = transform_coordinate_x(coordinates2[1])

            x1 = 1750 - x1 # Need to flip them because tkinter is oriented top left to bottom right
            x2 = 1750 - x2 # Basically just fiddled until they looked good
            y1 = 950 - y1
            y2 = 950 - y2
            line = c.create_line([(x1, y1), (x2, y2)], tag='grid_line')
            c.itemconfig(line, fill="black")
            lines[(city_id, other_city_id)] = line
            lines[(other_city_id, city_id)] = line
        r.update()
    return lines