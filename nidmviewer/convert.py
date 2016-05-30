"""
convert

Functions to convert/parse output from nidm sparql queries

"""

from nidmviewer.utils import read_file_lines
from numpy import isnan, float64
import pandas 

def parse_coordinates(coordinates):
    '''parse_coordinates
    convert a list of xyz strings in format '[x,y,z]' to separate variables
    This is what we get from the sparql query
    Parameters
    ==========
    coordinates: list
        a list of xyz coordinate strings, each a list in a string '[x,y,z]'
    Returns
    =======
    coordinate_df: pandas dataframe
    columns are x,y,z
    '''
    count=0
    coordinate_df = pandas.DataFrame(columns=["x","y","z"])
    for coordinate in coordinates:
        if isinstance(coordinate, str):
            coordinate_df.loc[count] = [x.strip() for x in coordinate.strip("]").strip("[").split(",")]
        # This happens when there are no coordinates
        elif isinstance(coordinate, float64) and isnan(coordinate):
            coordinate_df.loc[count] = [None, None, None]
        count+=1
    return coordinate_df

def getjson(nidm_file,format="n3"):
    g = Graph().parse(nidm_file, format=format)
    return json.loads(g.serialize(format='json-ld', indent=4))

def prettyjson(nidm_file,format="n3"):
    g = Graph().parse(nidm_file, format=format)
    return g.serialize(format='json-ld', indent=4)

