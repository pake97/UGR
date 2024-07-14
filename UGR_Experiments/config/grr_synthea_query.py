synthea_query = [
  {
      'constraint':"MATCH (a:Encounter)-[r:NEXT {deleted:false}]->(b:Encounter)-[p:SYNTH {deleted:false}]->(c:Allergy) RETURN ID(a),ID(b),ID(c)",
      'create_constraint':"MATCH (a:Encounter)-[r:NEXT {deleted:false}]->(b:Encounter)-[p:SYNTH {deleted:false}]->(c:Allergy) MERGE (a)-[:BELONGS]->(v1:Violation {solved:false, locked:false, nodes: ID(a)+','+ID(b)+','+ID(c)+','+ID(p)+','+ID(r),labels:'a,b,c,p,r', type:0})<-[:BELONGS]-(b) MERGE (v1)<-[:BELONGS]-(c)",
      'pattern': "MATCH (a:Encounter)-[r:NEXT {deleted:false}]->(b:Encounter)-[p:HAS_ALLERGY {deleted:false}]->(c:Allergy) RETURN ID(p)",
      'inject_errors':"MATCH (b:Encounter)-[p:HAS_ALLERGY {deleted:false}]->(c:Allergy) WHERE FILTRI MERGE (b)-[:SYNTH {deleted:false}]->(c)",
      'grr':"MATCH (a:Encounter)-[r:NEXT {deleted:false}]->(b:Encounter)-[p:SYNTH {deleted:false}]->(c:Allergy) SET p.updated=True, p.deleted=True",
   },
  {
      'constraint':"MATCH (c:Allergy)<-[p:HAS_ALLERGY {deleted:false}]-(a:Encounter)-[r:HAS_PROVIDER {deleted:false}]->(b:Organization) WHERE b.synth1<c.synth1 RETURN ID(a),ID(b),ID(c)",
      'create_constraint':"MATCH (c:Allergy)<-[p:HAS_ALLERGY {deleted:false}]-(a:Encounter)-[r:HAS_PROVIDER {deleted:false}]->(b:Organization) WHERE b.synth1<c.synth1 MERGE (a)-[:BELONGS]->(v1:Violation {solved:false, locked:false, nodes: ID(a)+','+ID(b)+','+ID(c)+','+ID(p)+','+ID(r),labels:'a,b,c,p,r', type:1})<-[:BELONGS]-(b) MERGE (v1)<-[:BELONGS]-(c)",
      'pattern':"MATCH (c:Allergy)<-[p:HAS_ALLERGY {deleted:false}]-(a:Encounter)-[r:HAS_PROVIDER {deleted:false}]->(b:Organization) RETURN ID(b)",
      'inject_errors':"MATCH (b:Organization) WHERE FILTRI SET b.synth1=0, b.injected=True",
      'grr':"MATCH (c:Allergy)<-[p:HAS_ALLERGY {deleted:false}]-(a:Encounter)-[r:HAS_PROVIDER {deleted:false}]->(b:Organization) WHERE b.synth1<c.synth1 SET c.updated=True, c.synth1=1, b.updated=True, b.synth1=1",
  },
   {
  'constraint':"MATCH (a:Patient)-[r:HAS_ENCOUNTER {deleted:false}]->(b:Encounter)-[p:NEXT {deleted:false}]->(c:Encounter)-[q:HAS_ALLERGY {deleted:false}]->(d:Allergy) WHERE a.synth1<d.synth1 RETURN ID(a),ID(b),ID(c),ID(d)",
  'create_constraint':"MATCH (a:Patient)-[r:HAS_ENCOUNTER {deleted:false}]->(b:Encounter)-[p:NEXT {deleted:false}]->(c:Encounter)-[q:HAS_ALLERGY {deleted:false}]->(d:Allergy) WHERE a.synth1<d.synth1 MERGE (a)-[:BELONGS]->(v1:Violation {solved:false, locked:false, nodes: ID(a)+','+ID(b)+','+ID(c)+','+ID(d)+','+ID(p)+','+ID(r)+','+ID(q),labels:'a,b,c,d,p,r,q', type:2})<-[:BELONGS]-(b) MERGE (d)-[:BELONGS]->(v1)<-[:BELONGS]-(c)",
  'pattern':"MATCH (a:Patient)-[r:HAS_ENCOUNTER {deleted:false}]->(b:Encounter)-[p:NEXT {deleted:false}]->(c:Encounter)-[q:HAS_ALLERGY {deleted:false}]->(d:Allergy) RETURN ID(a)",
  'inject_errors':"MATCH (a:Patient) WHERE FILTRI SET a.synth1=0, a.injected=True",
  'grr':"MATCH (a:Patient)-[r:HAS_ENCOUNTER {deleted:false}]->(b:Encounter)-[p:NEXT {deleted:false}]->(c:Encounter)-[q:HAS_ALLERGY {deleted:false}]->(d:Allergy) WHERE a.synth1<d.synth1 SET a.updated=True, a.synth1=1, d.updated=True, d.synth1=1",
  },
  { 
    'constraint':"MATCH (b:Drug)<-[r:HAS_DRUG {deleted:false}]-(a1:Encounter)-[p:HAS_CONDITION {deleted:false}]->(c:Condition), (a2:Encounter)-[q:HAS_PAYER {deleted:false}]->(d:Payer) WHERE ID(a1)=ID(a2) AND b.synth1<>d.synth1 RETURN ID(a1),ID(b),ID(c),ID(d) ",
    'create_constraint':"MATCH (b:Drug)<-[r:HAS_DRUG {deleted:false}]-(a1:Encounter)-[p:HAS_CONDITION {deleted:false}]->(c:Condition), (a2:Encounter)-[q:HAS_PAYER {deleted:false}]->(d:Payer) WHERE ID(a1)=ID(a2) AND b.synth1<>d.synth1 MERGE (a1)-[:BELONGS]->(v1:Violation {solved:false, locked:false, nodes: ID(a1)+','+ID(b)+','+ID(c)+','+ID(d)+','+ID(p)+','+ID(r)+','+ID(q),labels:'a1,b,c,d,p,r,q', type:3})<-[:BELONGS]-(b) MERGE (d)-[:BELONGS]->(v1)<-[:BELONGS]-(c)",
    'pattern':"MATCH (b:Drug)<-[r:HAS_DRUG {deleted:false}]-(a1:Encounter)-[p:HAS_CONDITION {deleted:false}]->(c:Condition), (a2:Encounter)-[q:HAS_PAYER {deleted:false}]->(d:Payer) WHERE ID(a1)=ID(a2) RETURN ID(b)",
    'inject_errors':"MATCH (b:Drug) WHERE FILTRI SET b.synth1=0, b.injected=True",
    'grr':"MATCH (b:Drug)<-[r:HAS_DRUG {deleted:false}]-(a1:Encounter)-[p:HAS_CONDITION {deleted:false}]->(c:Condition), (a2:Encounter)-[q:HAS_PAYER {deleted:false}]->(d:Payer) WHERE ID(a1)=ID(a2) AND b.synth1<>d.synth1 SET b.updated=True, b.synth1=1, d.updated=True, d.synth1=1",
  },
  { 
    'constraint':"MATCH (b:Condition)<-[r:HAS_CONDITION {deleted:false}]-(a1:Encounter)-[p:NEXT {deleted:false}]->(c:Encounter)-[q:HAS_END {deleted:false}]->(a1) WHERE b.synth1<>c.synth1 RETURN ID(a1),ID(b),ID(c) ",
    'create_constraint':"MATCH (b:Condition)<-[r:HAS_CONDITION {deleted:false}]-(a1:Encounter)-[p:NEXT {deleted:false}]->(c:Encounter)-[q:HAS_END {deleted:false}]->(a1) WHERE b.synth1<>c.synth1 MERGE (a1)-[:BELONGS]->(v1:Violation {solved:false, locked:false, nodes: ID(a1)+','+ID(b)+','+ID(c)+','+ID(p)+','+ID(r)+','+ID(q),labels:'a1,b,c,p,r,q', type:4})<-[:BELONGS]-(b) MERGE (v1)<-[:BELONGS]-(c)",
    'pattern':"MATCH (b:Condition)<-[r:HAS_CONDITION {deleted:false}]-(a1:Encounter)-[p:NEXT {deleted:false}]->(c:Encounter)-[q:HAS_END {deleted:false}]->(a1) RETURN ID(b)",
    'inject_errors':"MATCH (b:Condition) WHERE FILTRI SET b.synth1=0, b.injected=True",
    'grr':"MATCH (b:Condition)<-[r:HAS_CONDITION {deleted:false}]-(a1:Encounter)-[p:NEXT {deleted:false}]->(c:Encounter)-[q:HAS_END {deleted:false}]->(a1) WHERE b.synth1<>c.synth1 SET b.updated=True, b.synth1=1, c.updated=True, c.synth1=1",
  },
  { 
    'constraint':"MATCH (b:Encounter)-[r:NEXT {deleted:false}]->(a1:Encounter)-[p:NEXT {deleted:false}]->(c:Encounter)-[q:HAS_END {deleted:false}]->(b) WHERE b.synth1<>c.synth1 RETURN ID(a1),ID(b),ID(c) ",
    'create_constraint':"MATCH (b:Encounter)-[r:NEXT {deleted:false}]->(a1:Encounter)-[p:NEXT {deleted:false}]->(c:Encounter)-[q:HAS_END {deleted:false}]->(b) WHERE b.synth1<>c.synth1 MERGE (a1)-[:BELONGS]->(v1:Violation {solved:false, locked:false, nodes: ID(a1)+','+ID(b)+','+ID(c)+','+ID(p)+','+ID(r)+','+ID(q),labels:'a1,b,c,p,r,q', type:5})<-[:BELONGS]-(b) MERGE (v1)<-[:BELONGS]-(c)",
    'pattern':"MATCH (b:Encounter)-[r:NEXT {deleted:false}]->(a1:Encounter)-[p:NEXT {deleted:false}]->(c:Encounter)-[q:HAS_END {deleted:false}]->(b) RETURN ID(b)",
    'inject_errors':"MATCH (b:Encounter) WHERE FILTRI SET b.synth1=0, b.injected=True",
    'grr':"MATCH (b:Encounter)-[r:NEXT {deleted:false}]->(a1:Encounter)-[p:NEXT {deleted:false}]->(c:Encounter)-[q:HAS_END {deleted:false}]->(b) WHERE b.synth1<>c.synth1 SET b.updated=True, b.synth1=1, c.updated=True, c.synth1=1",
  }
 ]