fincen_queries = [
  {
      'constraint':"MATCH (c:Country)<-[r:COUNTRY {deleted:false}]-(a:Entity)-[p:SYNTH {deleted:false}]->(b:Country) RETURN ID(a),ID(b),ID(c)",
      'create_constraint':"MATCH (c:Country)<-[r:COUNTRY {deleted:false}]-(a:Entity)-[p:SYNTH {deleted:false}]->(b:Country) MERGE (a)-[:BELONGS]->(v1:Violation {solved:False, locked:false, nodes: ID(a)+','+ID(b)+','+ID(c)+','+ID(p)+','+ID(r),labels:'a,b,c,p,r', type:0})<-[:BELONGS]-(b) MERGE (v1)<-[:BELONGS]-(c)",
      'pattern': "MATCH (c:Country)<-[r:COUNTRY {deleted:false}]-(a:Entity)-[p:COUNTRY {deleted:false}]->(b:Country) RETURN ID(p)",
      'inject_errors':"MATCH (a:Entity)-[p:COUNTRY {deleted:false}]->(b:Country) WHERE FILTRI MERGE (a)-[:SYNTH {deleted:false}]->(b)",
      'grr':"MATCH (c:Country)<-[r:COUNTRY {deleted:false}]-(a:Entity)-[p:SYNTH {deleted:false}]->(b:Country) SET p.updated=True, p.deleted=True",
   },
   {
  'constraint':"MATCH (a:Entity)-[r:SYNTH {deleted:false}]->(b:Filing)-[p:ORIGINATOR {deleted:false}]->(c:Entity)-[q:COUNTRY {deleted:false}]->(d:Country) RETURN ID(a),ID(b),ID(c),ID(d)",
  'create_constraint':"MATCH (a:Entity)-[r:SYNTH {deleted:false}]->(b:Filing)-[p:ORIGINATOR {deleted:false}]->(c:Entity)-[q:COUNTRY {deleted:false}]->(d:Country) MERGE (a)-[:BELONGS]->(v1:Violation {solved:False, locked:false, nodes: ID(a)+','+ID(b)+','+ID(c)+','+ID(d)+','+ID(p)+','+ID(r)+','+ID(q),labels:'a,b,c,d,p,r,q', type:1})<-[:BELONGS]-(b) MERGE (d)-[:BELONGS]->(v1)<-[:BELONGS]-(c)",
  'pattern':"MATCH (a:Entity)-[r:FILED {deleted:false}]->(b:Filing)-[p:ORIGINATOR {deleted:false}]->(c:Entity)-[q:COUNTRY {deleted:false}]->(d:Country) RETURN ID(r)",
  'inject_errors':"MATCH (a:Entity)-[r:FILED {deleted:false}]->(b:Filing) WHERE FILTRI MERGE (a)-[:SYNTH {deleted:false}]->(b)",
  'grr':"MATCH (a:Entity)-[r:SYNTH {deleted:false}]->(b:Filing)-[p:ORIGINATOR {deleted:false}]->(c:Entity)-[q:COUNTRY {deleted:false}]->(d:Country) SET r.updated=True, r.deleted=True",
  },
  { 
    'constraint':"MATCH (b:Country)<-[r:COUNTRY {deleted:false}]-(a1:Entity)-[p:COUNTRY {deleted:false}]->(c:Country), (a2:Entity)-[q:COUNTRY {deleted:false}]->(d:Country) WHERE ID(a1)=ID(a2) AND b.synth1<>d.synth1 RETURN ID(a1),ID(b),ID(c),ID(d) ",
    'create_constraint':"MATCH (b:Country)<-[r:COUNTRY {deleted:false}]-(a1:Entity)-[p:COUNTRY {deleted:false}]->(c:Country), (a2:Entity)-[q:COUNTRY {deleted:false}]->(d:Country) WHERE ID(a1)=ID(a2) AND b.synth1<>d.synth1 MERGE (a1)-[:BELONGS]->(v1:Violation {solved:False, locked:false, nodes: ID(a1)+','+ID(b)+','+ID(c)+','+ID(d)+','+ID(p)+','+ID(r)+','+ID(q),labels:'a1,b,c,d,p,r,q', type:2})<-[:BELONGS]-(b) MERGE (d)-[:BELONGS]->(v1)<-[:BELONGS]-(c)",
    'pattern':"MATCH (b:Country)<-[r:COUNTRY {deleted:false}]-(a1:Entity)-[p:COUNTRY {deleted:false}]->(c:Country), (a2:Entity)-[q:COUNTRY {deleted:false}]->(d:Country) WHERE ID(a1)=ID(a2) RETURN ID(b)",
    'inject_errors':"MATCH (b:Country) WHERE FILTRI SET b.synth1=0, b.injected=True",
    'grr':"MATCH (b:Country)<-[r:COUNTRY {deleted:false}]-(a1:Entity)-[p:COUNTRY {deleted:false}]->(c:Country), (a2:Entity)-[q:COUNTRY {deleted:false}]->(d:Country) WHERE ID(a1)=ID(a2) AND b.synth1<>d.synth1 SET b.updated=True, b.synth1=1, d.updated=True, d.synth1=1",
  },
  { 
    'constraint':"MATCH (b:Entity)<-[r:CONCERNS {deleted:false}]-(a1:Filing)-[p:ORIGINATOR {deleted:false}]->(c:Entity)-[q:FILED {deleted:false}]->(a2:Filing) WHERE ID(a1)=ID(a2) AND a1.synth1<>c.synth1 RETURN ID(a1),ID(b),ID(c)",
    'create_constraint':"MATCH (b:Entity)<-[r:CONCERNS {deleted:false}]-(a1:Filing)-[p:ORIGINATOR {deleted:false}]->(c:Entity)-[q:FILED {deleted:false}]->(a2:Filing) WHERE ID(a1)=ID(a2) AND a1.synth1<>c.synth1 MERGE (a1)-[:BELONGS]->(v1:Violation {solved:False, locked:false, nodes: ID(a1)+','+ID(b)+','+ID(c)+','+ID(p)+','+ID(r)+','+ID(q),labels:'a1,b,c,p,r,q', type:3})<-[:BELONGS]-(b) MERGE (v1)<-[:BELONGS]-(c)",
    'pattern':"MATCH (b:Entity)<-[r:CONCERNS {deleted:false}]-(a1:Filing)-[p:ORIGINATOR {deleted:false}]->(c:Entity)-[q:FILED {deleted:false}]->(a2:Filing) WHERE ID(a1)=ID(a2) RETURN ID(a1)",
    'inject_errors':"MATCH (a1:Filing) WHERE FILTRI SET a1.synth1=0, a1.injected=True",
    'grr':"MATCH (b:Entity)<-[r:CONCERNS {deleted:false}]-(a1:Filing)-[p:ORIGINATOR {deleted:false}]->(c:Entity)-[q:FILED {deleted:false}]->(a2:Filing) WHERE ID(a1)=ID(a2) AND a1.synth1<>c.synth1 SET b.updated=True, b.synth1=1, c.updated=True, c.synth1=1",
  },
  { 
    
    'constraint':"MATCH (b:Country)<-[r:COUNTRY {deleted:false}]-(a1:Entity)-[p:COUNTRY {deleted:false}]->(c:Country), (a2:Entity)-[q:SYNTH {deleted:false}]->(d:Country) WHERE ID(a1)=ID(a2) RETURN ID(a1),ID(b),ID(c),ID(d) ",
    'create_constraint':"MATCH (b:Country)<-[r:COUNTRY {deleted:false}]-(a1:Entity)-[p:COUNTRY {deleted:false}]->(c:Country), (a2:Entity)-[q:SYNTH {deleted:false}]->(d:Country) WHERE ID(a1)=ID(a2) MERGE (a1)-[:BELONGS]->(v1:Violation {solved:False, locked:false, nodes: ID(a1)+','+ID(b)+','+ID(c)+','+ID(d)+','+ID(p)+','+ID(r)+','+ID(q),labels:'a1,b,c,d,p,r,q', type:4})<-[:BELONGS]-(b) MERGE (d)-[:BELONGS]->(v1)<-[:BELONGS]-(c)",
    'pattern':"MATCH (b:Country)<-[r:COUNTRY {deleted:false}]-(a1:Entity)-[p:COUNTRY {deleted:false}]->(c:Country), (a2:Entity)-[q:COUNTRY {deleted:false}]->(d:Country) WHERE ID(a1)=ID(a2) RETURN ID(q)",
    'inject_errors':"MATCH (a2:Entity)-[q:COUNTRY {deleted:false}]->(d:Country) WHERE FILTRI MERGE (a1)-[:SYNTH {deleted:false}]->(d)",
    'grr':"MATCH (b:Country)<-[r:COUNTRY {deleted:false}]-(a1:Entity)-[p:COUNTRY {deleted:false}]->(c:Country), (a2:Entity)-[q:SYNTH {deleted:false}]->(d:Country) WHERE ID(a1)=ID(a2) SET b.updated=True, b.synth1=1, d.updated=True, d.synth1=1",
  },
 ]

