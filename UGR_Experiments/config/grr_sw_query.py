sw_queries = [
  {
      'constraint':"MATCH (a:Species)-[r:HOMEWORLD {deleted:false}]->(b:Planet)-[p:SYNTH {deleted:false}]->(c:Film) RETURN ID(a),ID(b),ID(c)",
      'create_constraint':"MATCH (a:Species)-[r:HOMEWORLD {deleted:false}]->(b:Planet)-[p:SYNTH {deleted:false}]->(c:Film) MERGE (a)-[:BELONGS]->(v1:Violation {solved:False, locked:false, nodes: ID(a)+','+ID(b)+','+ID(c)+','+ID(p)+','+ID(r),labels:'a,b,c,p,r', type:0})<-[:BELONGS]-(b) MERGE (v1)<-[:BELONGS]-(c)",
      'pattern': "MATCH (a:Species)-[r:HOMEWORLD {deleted:false}]->(b:Planet)-[p:APPEARED_IN {deleted:false}]->(c:Film) RETURN ID(p)",
      'inject_errors':"MATCH (b:Planet)-[p:APPEARED_IN {deleted:false}]->(c:Film) WHERE FILTRI MERGE (b)-[:SYNTH {deleted:false}]->(c)",
      'grr':"MATCH (a:Species)-[r:HOMEWORLD {deleted:false}]->(b:Planet)-[p:SYNTH {deleted:false}]->(c:Film) SET p.updated=True, p.deleted=True",
   },
  {
      'constraint':"MATCH (c:Vehicle)<-[p:PILOT{deleted:false}]-(a:Character)-[r:OF {deleted:false}]->(b:Species) WHERE c.synth1<>b.synth1 RETURN ID(a),ID(b),ID(c)",
      'create_constraint':"MATCH (c:Vehicle)<-[p:PILOT{deleted:false}]-(a:Character)-[r:OF {deleted:false}]->(b:Species) WHERE c.synth1<>b.synth1 MERGE (a)-[:BELONGS]->(v1:Violation {solved:False, locked:false, nodes: ID(a)+','+ID(b)+','+ID(c)+','+ID(p)+','+ID(r),labels:'a,b,c,p,r', type:1})<-[:BELONGS]-(b) MERGE (v1)<-[:BELONGS]-(c)",
      'pattern':"MATCH (c:Vehicle)<-[p:PILOT{deleted:false}]-(a:Character)-[r:OF {deleted:false}]->(b:Species) RETURN ID(b)",
      'inject_errors':"MATCH (b:Species) WHERE FILTRI SET b.synth1=0, b.injected=True",
      'grr':"MATCH (c:Vehicle)<-[p:PILOT{deleted:false}]-(a:Character)-[r:OF {deleted:false}]->(b:Species) WHERE c.synth1<>b.synth1 SET c.updated=True, c.synth1=1, b.updated=True, b.synth1=1",
  },
   {
      'constraint':"MATCH (a:Character)-[r:OF]->(b:Species)-[p:HOMEWORLD]->(c:Planet)-[q:APPEARED_IN]->(d:Film) WHERE a.synth1<d.synth1 RETURN ID(a),ID(b),ID(c),ID(d)",
      'create_constraint':"MATCH (a:Character)-[r:OF]->(b:Species)-[p:HOMEWORLD]->(c:Planet)-[q:APPEARED_IN]->(d:Film) WHERE a.synth1<d.synth1 MERGE (a)-[:BELONGS]->(v1:Violation {solved:False, locked:false, nodes: ID(a)+','+ID(b)+','+ID(c)+','+ID(d)+','+ID(p)+','+ID(r)+','+ID(q),labels:'a,b,c,d,p,r,q', type:2})<-[:BELONGS]-(b) MERGE (d)-[:BELONGS]->(v1)<-[:BELONGS]-(c)",
      'pattern':"MATCH (a:Character)-[r:OF]->(b:Species)-[p:HOMEWORLD]->(c:Planet)-[q:APPEARED_IN]->(d:Film) RETURN ID(a)",
      'inject_errors':"MATCH (a:Character) WHERE FILTRI SET a.synth1=0, a.injected=True",
      'grr':"MATCH (a:Character)-[r:OF]->(b:Species)-[p:HOMEWORLD]->(c:Planet)-[q:APPEARED_IN]->(d:Film) WHERE a.synth1<d.synth1 SET a.updated=True, a.synth1=1, d.updated=True, d.synth1=1",
  },
  { 
    'constraint':"MATCH (b:Species)<-[r:OF {deleted:false}]-(a1:Character)-[p:APPEARED_IN {deleted:false}]->(c:Film), (a2:Character)-[q:PILOT {deleted:false}]->(d:Vehicle) WHERE ID(a1)=ID(a2) AND b.synth1<>d.synth1 RETURN ID(a1),ID(b),ID(c),ID(d) ",
    'create_constraint':"MATCH (b:Species)<-[r:OF {deleted:false}]-(a1:Character)-[p:APPEARED_IN {deleted:false}]->(c:Film), (a2:Character)-[q:PILOT {deleted:false}]->(d:Vehicle) WHERE ID(a1)=ID(a2) AND b.synth1<>d.synth1 MERGE (a1)-[:BELONGS]->(v1:Violation {solved:False, locked:false, nodes: ID(a1)+','+ID(b)+','+ID(c)+','+ID(d)+','+ID(p)+','+ID(r)+','+ID(q),labels:'a1,b,c,d,p,r,q', type:3})<-[:BELONGS]-(b) MERGE (d)-[:BELONGS]->(v1)<-[:BELONGS]-(c)",
    'pattern':"MATCH (b:Species)<-[r:OF {deleted:false}]-(a1:Character)-[p:APPEARED_IN {deleted:false}]->(c:Film), (a2:Character)-[q:PILOT {deleted:false}]->(d:Vehicle) WHERE ID(a1)=ID(a2) RETURN ID(b)",
    'inject_errors':"MATCH (b:Species) WHERE FILTRI SET b.synth1=0, b.injected=True",
    'grr':"MATCH (b:Species)<-[r:OF {deleted:false}]-(a1:Character)-[p:APPEARED_IN {deleted:false}]->(c:Film), (a2:Character)-[q:PILOT {deleted:false}]->(d:Vehicle) WHERE ID(a1)=ID(a2) AND b.synth1<>d.synth1 SET b.updated=True, b.synth1=1, d.updated=True, d.synth1=1"
  }
 ]