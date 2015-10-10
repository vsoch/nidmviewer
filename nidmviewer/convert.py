"""
convert

Functions to convert nidm turtle to superior formats

"""

from rdflib import Graph, plugin
from rdflib.serializer import Serializer
import json

"""
Here is how we look up things like coodinates, pvalues, etc.
"""
def get_nidm_keys():
    return {
       "nidm":"http://purl.org/nidash/nidm#",
       "prov":"http://www.w3.org/ns/prov#",
       "peak":"http://purl.org/nidash/nidm#NIDM_0000062",
       "inference":"http://purl.org/nidash/nidm#NIDM_0000049",
       "beta_map":"http://purl.org/nidash/nidm#NIDM_0000061",
       "mask":"http://purl.org/nidash/nidm#NIDM_0000054",
       "search_space_mask":"http://purl.org/nidash/nidm#NIDM_0000068",
       "grand_mean_map":"http://purl.org/nidash/nidm#NIDM_0000033",
       "residual_mean_squares_map":"http://purl.org/nidash/nidm#NIDM_0000066",
       "excursion_set_map":"http://purl.org/nidash/nidm#NIDM_0000025",
       "cluster_label_map":"http://purl.org/nidash/nidm#NIDM_0000008",
       "resels_per_voxel_map":"http://purl.org/nidash/nidm#NIDM_0000144",
       "contrast_standard_error_map":"http://purl.org/nidash/nidm#NIDM_0000013",
       "nfo":"http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#",
       "significant_cluster":"http://purl.org/nidash/nidm#NIDM_0000070",
       "equivalent_zstatistic":"http://purl.org/nidash/nidm#NIDM_0000092",
       "pvalue_fwer": "http://purl.org/nidash/nidm#NIDM_0000115",
       "pvalue_uncorrected": "http://purl.org/nidash/nidm#NIDM_0000116",
       "statistic_map": "http://purl.org/nidash/nidm#NIDM_0000076",
       "contrast_map":"http://purl.org/nidash/nidm#NIDM_0000002",
       "statistic_type": "http://purl.org/nidash/nidm#NIDM_0000123",
       "coordinateVector": "http://purl.org/nidash/nidm#NIDM_0000086",
       "atLocation":"http://www.w3.org/ns/prov#atLocation",
       "Location":"http://www.w3.org/ns/prov#Location",
       "value":"http://www.w3.org/ns/prov#value",
       "wasDerivedFrom":"http://www.w3.org/ns/prov#wasDerivedFrom"}
 

def getjson(nidm_file):
    g = Graph().parse(nidm_file, format='n3')
    return json.loads(g.serialize(format='json-ld', indent=4))

def prettyjson(nidm_file):
    g = Graph().parse(nidm_file, format='n3')
    return g.serialize(format='json-ld', indent=4)

