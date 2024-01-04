# Global dictionary (hash map) for the id to name conversions
id_name = dict()
# Global data structure

"""
Fill out the id_name data structure with id to city conversions
PARAMETERS:
id_city: List of strings with the format "xxxxxxx cityName" for each index
RETURN: void
"""
def id_name_conversion(id_city):
    for conversion in id_city:
        conversion = conversion.split() # Split the id and name into two seperate variables
        id, name = conversion[0], conversion[1]
        id_name[id] = name


def main():
    id_city  = list()
    with open("rrNodeCity.txt") as f:
        id_city = [line.strip() for line in f]
    id_name_conversion(id_city)
    print(id_name)
if __name__ == "__main__":
    main()