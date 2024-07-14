def injectSyntheticData(neo4j_connector):
    res = neo4j_connector.query("MATCH (a) SET a.synth1=1, a.updated=False")
    #res = neo4j_connector.query("MATCH (a) SET a.synth2=1")
    #res = neo4j_connector.query("MATCH (a) SET a.synth3=1")
    res = neo4j_connector.query("MATCH (a)-[r]-(b) SET r.deleted=false, r.updated=False")
    