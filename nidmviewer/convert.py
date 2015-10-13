"""
convert

Functions to convert nidm turtle to superior formats

"""

from nidmviewer.utils import read_file_lines
from rdflib.serializer import Serializer
from rdflib import Graph, plugin
import rdfextras
rdfextras.registerplugins()
plugin.register(
    'json-ld',
    Serializer,
    'rdflib_jsonld.serializer',
    'JsonLDSerializer')
import numpy
import json
import re

"""
Groups to look for in RDF

"""

def get_field_groups(ttl):
    num = re.compile("[0-9]")
    groups = []
    for entry in ttl:
        groups = groups + entry["@type"]
    # Main groups seem to have no numbers
    groups = numpy.unique(groups).tolist()
    groups = [g for g in groups if not num.search(g.split("#")[-1])]
    return groups


"""
Extract unique labels and ids from ttl file for dynamic lookup,
and also return all entires as a flat dictionary
returns the same as "get_fields" plus this flat version.

"""

def get_lookups(ttl):
    # First get keys from ttl, and flatten
    fields = get_fields(ttl)
    lookup = dict()
    for tag,entries in fields.iteritems():
        lookup.update(entries)
    return fields,lookup


"""
Extract unique labels and ids from ttl file for dynamic lookup
returns: dictionary with "keys" being different field groups
("eg, http://www.w3.org/ns/prov#Entity") and values being a dictionary
of {label:uri}

"""
def get_fields(ttl):
    groups = get_field_groups(ttl)
    label = "http://www.w3.org/2000/01/rdf-schema#label"
    lookup = dict()
    for entity in groups:
        keys = dict()
        for entry in ttl:
            # Entities with labels
            if label in entry:
                # if it's an entity
                if entity in entry["@type"]:
                    # This is hacky, but remove all numbers from string to get main labels
                    entity_id = [x for x in entry["@type"] if x not in [entity]][0]
                    entity_label = ''.join(i.lower() for i in entry[label][0]["@value"]
 if not i.isdigit())
                    entity_label = entity_label.split(":")[0].encode("utf-8").replace("'","")
                    entity_label = entity_label.replace("_","").strip()
                    keys[entity_id.encode("utf-8")] = entity_label
        lookup[entity] = keys 
    return lookup

"""
This was a first manual effort to get the right lookup keys, and then I
realized the files are different and wanted to :*(

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
       "coordinate":"http://purl.org/nidash/nidm#NIDM_0000015",
       "coordinateVector": "http://purl.org/nidash/nidm#NIDM_0000086",
       "atLocation":"http://www.w3.org/ns/prov#atLocation",
       "Location":"http://www.w3.org/ns/prov#Location",
       "value":"http://www.w3.org/ns/prov#value",
       "wasDerivedFrom":"http://www.w3.org/ns/prov#wasDerivedFrom",
       "wasGeneratedBy":"http://www.w3.org/ns/prov#wasGeneratedBy",
       "fileName":"http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#fileName"}
 

def getjson(nidm_file,format="n3"):
    g = Graph().parse(nidm_file, format=format)
    return json.loads(g.serialize(format='json-ld', indent=4))

def prettyjson(nidm_file,format="n3"):
    g = Graph().parse(nidm_file, format=format)
    return g.serialize(format='json-ld', indent=4)

