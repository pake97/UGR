wwwc2019_query = [
  {
      'constraint':"MATCH (a:Team)-[r:NAMED {deleted:false}]->(b:Squad)-[p:SYNTH {deleted:false}]->(c:Tournament) RETURN ID(a),ID(b),ID(c)",
      'create_constraint':"MATCH (a:Team)-[r:NAMED {deleted:false}]->(b:Squad)-[p:SYNTH {deleted:false}]->(c:Tournament) MERGE (a)-[:BELONGS]->(v1:Violation {solved:False, locked:false, nodes: ID(a)+','+ID(b)+','+ID(c)+','+ID(p)+','+ID(r),labels:'a,b,c,p,r', type:0})<-[:BELONGS]-(b) MERGE (v1)<-[:BELONGS]-(c)",
      'pattern': "MATCH (a:Team)-[r:NAMED {deleted:false}]->(b:Squad)-[p:FOR {deleted:false}]->(c:Tournament) RETURN ID(p)",
      'inject_errors':"MATCH (b:Squad)-[p:FOR {deleted:false}]->(c:Tournament) WHERE FILTRI MERGE (b)-[:SYNTH {deleted:false}]->(c)",
      'grr':"MATCH (a:Team)-[r:NAMED {deleted:false}]->(b:Squad)-[p:SYNTH {deleted:false}]->(c:Tournament) SET p.updated=True, p.deleted=True"
   },
  {
      'constraint':"MATCH (c:Squad)<-[p:COACH_FOR {deleted:false}]-(a:Person)-[r:REPRESENTS {deleted:false}]->(b:Team) WHERE b.synth1<c.synth1 RETURN ID(a),ID(b),ID(c)",
      'create_constraint':"MATCH (c:Squad)<-[p:COACH_FOR {deleted:false}]-(a:Person)-[r:REPRESENTS {deleted:false}]->(b:Team) WHERE b.synth1<c.synth1 MERGE (a)-[:BELONGS]->(v1:Violation {solved:False, locked:false, nodes: ID(a)+','+ID(b)+','+ID(c)+','+ID(p)+','+ID(r),labels:'a,b,c,p,r', type:1})<-[:BELONGS]-(b) MERGE (v1)<-[:BELONGS]-(c)",
      'pattern':"MATCH (c:Squad)<-[p:COACH_FOR {deleted:false}]-(a:Person)-[r:REPRESENTS {deleted:false}]->(b:Team) RETURN ID(b)",
      'inject_errors':"MATCH (b:Team) WHERE FILTRI SET b.synth1=0, b.injected=True",
      'grr':"MATCH (c:Squad)<-[p:COACH_FOR {deleted:false}]-(a:Person)-[r:REPRESENTS {deleted:false}]->(b:Team) WHERE b.synth1<c.synth1 SET c.updated=True, c.synth1=1, b.updated=True, b.synth1=1", 
  },
   {
  'constraint':"MATCH (a:Person)-[r:REPRESENTS {deleted:false}]->(b:Team)-[p:NAMED {deleted:false}]->(c:Squad)-[q:FOR {deleted:false}]->(d:Tournament) WHERE a.synth1<d.synth1 RETURN ID(a),ID(b),ID(c),ID(d)",
  'create_constraint':"MATCH (a:Person)-[r:REPRESENTS {deleted:false}]->(b:Team)-[p:NAMED {deleted:false}]->(c:Squad)-[q:FOR {deleted:false}]->(d:Tournament) WHERE a.synth1<d.synth1 MERGE (a)-[:BELONGS]->(v1:Violation {solved:False, locked:false, nodes: ID(a)+','+ID(b)+','+ID(c)+','+ID(d)+','+ID(p)+','+ID(r)+','+ID(q),labels:'a,b,c,d,p,r,q', type:2})<-[:BELONGS]-(b) MERGE (d)-[:BELONGS]->(v1)<-[:BELONGS]-(c)",
  'pattern':"MATCH (a:Person)-[r:REPRESENTS {deleted:false}]->(b:Team)-[p:NAMED {deleted:false}]->(c:Squad)-[q:FOR {deleted:false}]->(d:Tournament) RETURN ID(a)",
  'inject_errors':"MATCH (a:Person) WHERE FILTRI SET a.synth1=0, a.injected=True",
  'grr':"MATCH (a:Person)-[r:REPRESENTS {deleted:false}]->(b:Team)-[p:NAMED {deleted:false}]->(c:Squad)-[q:FOR {deleted:false}]->(d:Tournament) WHERE a.synth1<d.synth1 SET a.updated=True, a.synth1=1, d.updated=True, d.synth1=1",
  },
  { 
    'constraint':"MATCH (b:Match)<-[r:PLAYED_IN {deleted:false}]-(a1:Person)-[p:SCORED_GOAL {deleted:false}]->(c:Match), (a2:Person)-[q:COACH_FOR {deleted:false}]->(d:Squad) WHERE ID(a1)=ID(a2) AND b.synth1<>d.synth1 RETURN ID(a1),ID(b),ID(c),ID(d) ",
    'create_constraint':"MATCH (b:Match)<-[r:PLAYED_IN {deleted:false}]-(a1:Person)-[p:SCORED_GOAL {deleted:false}]->(c:Match), (a2:Person)-[q:COACH_FOR {deleted:false}]->(d:Squad) WHERE ID(a1)=ID(a2) AND b.synth1<>d.synth1 MERGE (a1)-[:BELONGS]->(v1:Violation {solved:False, locked:false, nodes: ID(a1)+','+ID(b)+','+ID(c)+','+ID(d)+','+ID(p)+','+ID(r)+','+ID(q),labels:'a1,b,c,d,p,r,q', type:3})<-[:BELONGS]-(b) MERGE (d)-[:BELONGS]->(v1)<-[:BELONGS]-(c)",
    'pattern':"MATCH (b:Match)<-[r:PLAYED_IN {deleted:false}]-(a1:Person)-[p:SCORED_GOAL {deleted:false}]->(c:Match), (a2:Person)-[q:COACH_FOR {deleted:false}]->(d:Squad) WHERE ID(a1)=ID(a2) RETURN ID(b)",
    'inject_errors':"MATCH (b:Match) WHERE FILTRI SET b.synth1=0, b.injected=True",
    'grr':"MATCH (b:Match)<-[r:PLAYED_IN {deleted:false}]-(a1:Person)-[p:SCORED_GOAL {deleted:false}]->(c:Match), (a2:Person)-[q:COACH_FOR {deleted:false}]->(d:Squad) WHERE ID(a1)=ID(a2) AND b.synth1<>d.synth1 SET b.updated=True, b.synth1=1, d.updated=True, d.synth1=1"
  },
  { 
    'constraint':"MATCH (b:Squad)<-[r:COACH_FOR {deleted:false}]-(a1:Person)-[p:PLAYED_IN {deleted:false}]->(c:Match), (a2:Person)-[q:SCORED_GOAL {deleted:false}]->(d:Match) WHERE ID(a1)=ID(a2) AND b.synth1<>d.synth1 RETURN ID(a1),ID(b),ID(c),ID(d) ",
    'create_constraint':"MATCH (b:Squad)<-[r:COACH_FOR {deleted:false}]-(a1:Person)-[p:PLAYED_IN {deleted:false}]->(c:Match), (a2:Person)-[q:SCORED_GOAL {deleted:false}]->(d:Match) WHERE ID(a1)=ID(a2) AND b.synth1<>d.synth1 MERGE (a1)-[:BELONGS]->(v1:Violation {solved:False, locked:false, nodes: ID(a1)+','+ID(b)+','+ID(c)+','+ID(d)+','+ID(p)+','+ID(r)+','+ID(q),labels:'a1,b,c,d,p,r,q', type:4})<-[:BELONGS]-(b) MERGE (d)-[:BELONGS]->(v1)<-[:BELONGS]-(c)",
    'pattern':"MATCH (b:Squad)<-[r:COACH_FOR {deleted:false}]-(a1:Person)-[p:PLAYED_IN {deleted:false}]->(c:Match), (a2:Person)-[q:SCORED_GOAL {deleted:false}]->(d:Match) WHERE ID(a1)=ID(a2) RETURN ID(b)",
    'inject_errors':"MATCH (b:Squad) WHERE FILTRI SET b.synth1=0, b.injected=True",
    'grr':"MATCH (b:Squad)<-[r:COACH_FOR {deleted:false}]-(a1:Person)-[p:PLAYED_IN {deleted:false}]->(c:Match), (a2:Person)-[q:SCORED_GOAL {deleted:false}]->(d:Match) WHERE ID(a1)=ID(a2) AND b.synth1<>d.synth1 SET b.updated=True, b.synth1=1, d.updated=True, d.synth1=1",
  }
 ]