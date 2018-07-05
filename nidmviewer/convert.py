"""
convert
Functions to convert/parse output from nidm sparql queries

Copyright (c) 2014-2018, Vanessa Sochat
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
        else:
            coordinate_df.loc[count] = [None,None,None]
        count+=1
    return coordinate_df

def getjson(nidm_file,format="n3"):
    g = Graph().parse(nidm_file, format=format)
    return json.loads(g.serialize(format='json-ld', indent=4))

def prettyjson(nidm_file,format="n3"):
    g = Graph().parse(nidm_file, format=format)
    return g.serialize(format='json-ld', indent=4)

