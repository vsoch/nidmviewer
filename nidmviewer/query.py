'''
query.py: part of the nidmviewer package

'''

from nidmviewer.convert import get_lookups, get_nidm_keys, get_field_groups
from nidmviewer.utils import strip_url, get_extension
import pandas

"""
result should be a json object (python dictionary) converted from a
nidm.ttl file with nidmviewer.convert getjson() function

"""

def get_peaks_and_maps(ttl,identifier="peak"):

    fields,lookup = get_lookups(ttl)
    df = get_table(ttl,fields,lookup)
    # Brainmaps are the fields with files
    brainmaps = df[df.fileName.isnull()==False]
    brainmaps = brainmaps[["fileName","atLocation"]]
    # Get unique maps, only nifti files
    maps = dict()
    for row in brainmaps.iterrows():
        # Don't care about maps without files
        if str(row[1].atLocation)!="nan":
            ext = get_extension(str(row[1].atLocation))
            if ext in ["nii.gz","nii"]:
                maps[row[1].fileName] = row[1].atLocation
    # Remove brainmaps from rest
    df = df.loc[df.index.isin(brainmaps.index)==False,:]
    df = df.drop("fileName",axis=1)
    # Filter down to those with defined coordinates
    coordinates = df.loc[df.coordinateVector.isnull()==False,"coordinateVector"]
    # Find peaky things
    peaks = lookup.keys()[lookup.values().index(identifier)]
    peakdf = df[df.type==peaks]
    # Append a coordinate to each peak
    peaks_with_coords = peakdf.index[peakdf.atLocation.isin(coordinates.index)]
    peakdf = peakdf.loc[peaks_with_coords]
    coords = coordinates.loc[peakdf.atLocation.tolist()].tolist()
    coords = [coord.replace("[","").replace("]","").strip() for coord in coords]
    coords = [coord.split(",") for coord in coords]
    peakdf["x"] = [coord[0].strip() for coord in coords]
    peakdf["y"] = [coord[1].strip() for coord in coords]
    peakdf["z"] = [coord[2].strip() for coord in coords]
    return peakdf,maps

def get_table(ttl,fields,lookup):    

    # Get fields that are not available in the ttl [frown face >:!]
    # This includes relationships "wasDerivedFrom" and "atLocation" which are important
    groups = get_field_groups(ttl)
    manual_fields = get_nidm_keys()
    for name,uri in manual_fields.iteritems():
        if uri not in lookup:
            lookup[uri] = name

    df = pandas.DataFrame()

    # PARSE THE BEAST
    for result in ttl:
        rgroup = [x for x in result["@type"] if x in groups][0] 
        rtype = [x for x in result["@type"] if x != rgroup]
        if len(rtype)>0:
            rtype = rtype[0]
            if rtype in lookup.keys():
                result_id = result["@id"]
                label = lookup[rtype]
                # Find things we know about
                data = [x for x in result.keys() if x in lookup.keys()]
                data_labels = [lookup[d] for d in data]
                for d in range(len(data)):
                    datum = data[d]
                    human_label = data_labels[d]
                    df.loc[result_id,"type"] = rtype.encode("utf-8")
                    if "@id" in result[datum][0]:
                        df.loc[result_id,human_label] = result[datum][0]["@id"].encode("utf-8")
                    # Value overwrites ID
                    if "@value" in result[datum][0]:
                        df.loc[result_id,human_label] = result[datum][0]["@value"].encode("utf-8")

    return df
