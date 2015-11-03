import rdflib
import rdfextras
rdfextras.registerplugins()
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
from pandas import DataFrame

'''
sparql.py: part of the nidmviewer package
Sparwl queries

'''

def do_query(ttl_file,query,rdf_format="turtle",serialize_format="csv",output_df=True):
    g = rdflib.Graph()
    g.parse(ttl_file,format=rdf_format)
    result = g.query(query)   
    result = result.serialize(format=serialize_format)    
    if output_df == True:
        result = StringIO(result)
        return DataFrame.from_csv(result,sep=",")
    else:
        return result

def get_coordinates(ttl_file):
    query = """
    SELECT DISTINCT ?name ?coordinate ?z_score ?peak_name ?pvalue_uncorrected
    WHERE {?coord a nidm:NIDM_0000015 ;
           rdfs:label ?name ;
           nidm:NIDM_0000086 ?coordinate .
       ?peak prov:atLocation ?coord ;
           nidm:NIDM_0000092 ?z_score ;
           rdfs:label ?peak_name ;
           nidm:NIDM_0000116 ?pvalue_uncorrected .}
     ORDER BY ?name
    """
    return do_query(ttl_file,query)


def get_brainmaps(ttl_file):
    query = """
            PREFIX nidm: <http://purl.org/nidash/nidm#> 
            PREFIX prov: <http://www.w3.org/ns/prov#> 
            prefix nfo: <http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#>
            SELECT ?filename ?location WHERE 
            { ?file prov:atLocation ?location . 
            ?file nfo:fileName ?filename .
            FILTER regex(?filename, "TS*")
            }
            """
    return do_query(ttl_file,query)

def get_coordinates_and_maps(ttl_file):
    query = """
            PREFIX nidm: <http://purl.org/nidash/nidm#>
            PREFIX prov: <http://www.w3.org/ns/prov#>
            prefix nfo: <http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#>
            prefix spm: <http://purl.org/nidash/spm#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix peak: <http://purl.org/nidash/nidm#NIDM_0000062>
            prefix significant_cluster: <http://purl.org/nidash/nidm#NIDM_0000070>
            prefix coordinate: <http://purl.org/nidash/nidm#NIDM_0000086>
            prefix equivalent_zstatistic: <http://purl.org/nidash/nidm#NIDM_0000092>
            prefix pvalue_fwer: <http://purl.org/nidash/nidm#NIDM_0000115>
            prefix pvalue_uncorrected: <http://purl.org/nidash/nidm#NIDM_0000116>
            prefix statistic_map: <http://purl.org/nidash/nidm#NIDM_0000076>
            prefix statistic_type: <http://purl.org/nidash/nidm#NIDM_0000123>
            SELECT DISTINCT ?statmap ?statmap_location ?statmap_type ?z_score ?pvalue_uncorrected ?coordinate_id ?coord_name ?coordinate
            WHERE {
            ?statmap a statistic_map: ;
                statistic_type: ?statmap_type ;
                prov:atLocation ?statmap_location .
            ?peak prov:wasDerivedFrom/prov:wasDerivedFrom/prov:wasGeneratedBy/prov:used ?statmap ;
                prov:atLocation ?coord ;
                equivalent_zstatistic: ?z_score ;
                pvalue_uncorrected: ?pvalue_uncorrected ;
                prov:atLocation ?coordinate_id .
            ?coordinate_id rdfs:label ?coord_name ;
                coordinate: ?coordinate .
            }
            """
    return do_query(ttl_file,query)
