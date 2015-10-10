'''
sparql.py: part of the nidmviewer package
These functions don't actually serve any purpose but to store rdf queries
that have been useful to (someone) in the past. If someone else wants to 
write functions to query using sparql, this script is here.
I will not be using them. :)

'''

def get_peaks():
    return """PREFIX nidm: <http://purl.org/nidash/nidm#>
       PREFIX prov: <http://www.w3.org/ns/prov#>
       prefix peak: <http://purl.org/nidash/nidm#NIDM_0000062>
       prefix significant_cluster: <http://purl.org/nidash/nidm#NIDM_0000070>
       prefix coordinate: <http://purl.org/nidash/nidm#NIDM_0000086>
       prefix equivalent_zstatistic: <http://purl.org/nidash/nidm#NIDM_0000092>
       prefix pvalue_fwer: <http://purl.org/nidash/nidm#NIDM_0000115>
       prefix pvalue_uncorrected: <http://purl.org/nidash/nidm#NIDM_0000116>
       prefix statistic_map: <http://purl.org/nidash/nidm#NIDM_0000076>
       prefix statistic_type: <http://purl.org/nidash/nidm#NIDM_0000123>
       prefix coordinateVector: <http://purl.org/nidash/nidm#NIDM_0000086>
       SELECT DISTINCT ?cluster ?peak ?x ?equiv_z ?pval_fwer ?stat WHERE
       { ?peak a peak: .
         ?cluster a significant_cluster: .
         ?peak prov:wasDerivedFrom ?cluster .
         ?peak prov:atLocation ?coordinate .
         ?coordinate coordinateVector: ?x .
         ?peak equivalent_zstatistic: ?equiv_z .
         ?peak pvalue_fwer: ?pval_fwer .
         ?cluster prov:wasDerivedFrom/prov:wasGeneratedBy/prov:used ?statmap .
         ?statmap a statistic_map: .
         ?statmap statistic_type: ?stat .
       }
       ORDER BY ?cluster ?peak}"""

def get_filesnames():
    return """PREFIX nidm: <http://purl.org/nidash/nidm#> 
              PREFIX prov: <http://www.w3.org/ns/prov#> 
              prefix nfo: <http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#>
              SELECT ?filename ?location WHERE 
              { ?file prov:atLocation ?location . 
              ?file nfo:fileName ?filename .
              FILTER regex(?filename, "TS*")
            }"""
