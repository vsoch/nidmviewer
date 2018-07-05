'''
sparql.py: part of the nidmviewer package
Sparql queries

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

'''

import rdflib
import rdfextras
rdfextras.registerplugins()
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
from pandas import DataFrame

def do_query(ttl_file,query,rdf_format="turtle",serialize_format="csv",output_df=True):
    g = rdflib.Graph()
    g.parse(ttl_file,format=rdf_format)
    result = g.query(query)   
    if result is None:
        print("No results matching query.")
    else:
        print("Found results matching query.")
        result = result.serialize(format=serialize_format)    
        if output_df == True:
            if isinstance(result, bytes):
                result = result.decode('utf-8')
            result = StringIO(result)
            return DataFrame.from_csv(result,sep=",")
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
            prefix nidm_ExcursionSetMap: <http://purl.org/nidash/nidm#NIDM_0000025>
            SELECT DISTINCT ?statmap ?excsetmap_location ?statmap_type ?z_score 
            ?pvalue_uncorrected ?coordinate_id ?coord_name ?coordinate ?exc_set
            WHERE {
            ?statmap a statistic_map: ;
                statistic_type: ?statmap_type .
            ?exc_set a nidm_ExcursionSetMap: ;
                prov:wasGeneratedBy/prov:used ?statmap ;
                prov:atLocation ?excsetmap_location .
            OPTIONAL {
            ?peak prov:wasDerivedFrom/prov:wasDerivedFrom/prov:wasGeneratedBy/prov:used ?statmap ;
                prov:atLocation ?coord ;
                equivalent_zstatistic: ?z_score ;
                pvalue_uncorrected: ?pvalue_uncorrected ;
                prov:atLocation ?coordinate_id .
            ?coordinate_id rdfs:label ?coord_name ;
                coordinate: ?coordinate .
                }
            }
            """
    return do_query(ttl_file,query)
