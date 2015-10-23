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
    SELECT DISTINCT ?name ?coordinate ?z ?peak_name ?pvalue_uncorrected
    WHERE {?coord a nidm:NIDM_0000015 ;
           rdfs:label ?name ;
           nidm:NIDM_0000086 ?coordinate .
       ?peak prov:atLocation ?coord ;
           nidm:NIDM_0000092 ?z ;
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
