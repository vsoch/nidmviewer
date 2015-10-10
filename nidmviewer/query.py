'''
query.py: part of the nidmviewer package

'''

from nidmviewer.convert import get_nidm_keys
from nidmviewer.utils import strip_url
import pandas

"""
result should be a json object (python dictionary) converted from a
nidm.ttl file with nidmviewer.convert getjson() function

"""

def get_peaks_and_maps(results):

    # Here are the rdf keys we care about for a peak
    keys = ["atLocation","value","pvalue_fwer","wasDerivedFrom"]
    lookup = get_nidm_keys()
    peak = lookup["peak"]
    df = pandas.DataFrame(columns=keys)

    # We will save a list of coordinates to match to peaks as we go
    coordinates = dict()
    brainmaps = dict()
    brainmaps_lookup = ["statistic_map","residual_mean_squares_map","contrast_standard_error_map",
                        "resels_per_voxel_map","mask","contrast_map","grand_mean_map","excursion_set_map",
                        "cluster_label_map","beta_map"]

    # PARSE THE BEAST
    for result in results:
        # Is it a peak?
        if peak in result["@type"]:
            peakid = strip_url(result["@id"])
            for key in keys:
                if lookup[key] in result:
                    if "@value" in result[lookup[key]][0]:    
                        df.loc[peakid,key] = result[lookup[key]][0]["@value"].encode("utf-8")
                    if "@id" in result[lookup[key]][0]:
                        df.loc[peakid,key] = result[lookup[key]][0]["@id"].encode("utf-8")
        
        # Is it a coordinate?
        if lookup["Location"] in result["@type"]:
            coord = result[lookup["coordinateVector"]][0]["@value"].encode("utf-8")
            coordinates[result["@id"]] = coord.strip("[").strip("]").split(",")

        # Is it a brain map?
        for brainmap in brainmaps_lookup:  
            if lookup[brainmap] in result["@type"]:
                if lookup["atLocation"] in result:
                    brainmaps[result["@id"].encode("utf-8")] = result[lookup["atLocation"]][0]["@value"].encode("utf-8")

    # Match coordinateVectors to peaks
    df["x"] = [int(coordinates[x][0]) for x in df["atLocation"].tolist()]
    df["y"] = [int(coordinates[x][1]) for x in df["atLocation"].tolist()]
    df["z"] = [int(coordinates[x][2]) for x in df["atLocation"].tolist()]
    return df,brainmaps


