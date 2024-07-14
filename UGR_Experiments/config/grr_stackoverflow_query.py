stackoverflow_query = [
  {
      'constraint':"MATCH (a:User)-[r:ASKED {deleted:false}]->(b:Question)-[p:SYNTH {deleted:false}]->(c:Tag) ",
      'create_constraint':"MATCH (a:User)-[r:ASKED {deleted:false}]->(b:Question)-[p:SYNTH {deleted:false}]->(c:Tag) MERGE (a)-[:BELONGS]->(v1:Violation {solved:False, locked:false, nodes: ID(a)+','+ID(b)+','+ID(c)+','+ID(p)+','+ID(r),labels:'a,b,c,p,r', type:0})<-[:BELONGS]-(b) MERGE (v1)<-[:BELONGS]-(c)",
      'pattern': "MATCH (a:User)-[r:ASKED {deleted:false}]->(b:Question)-[p:TAGGED {deleted:false}]->(c:Tag) RETURN ID(p)",
      'inject_errors':"MATCH (b:Question)-[p:TAGGED {deleted:false}]->(c:Tag) WHERE FILTRI MERGE (b)-[:SYNTH {deleted:false}]->(c)",
      'grr':"MATCH (a:User)-[r:ASKED {deleted:false}]->(b:Question)-[p:SYNTH {deleted:false}]->(c:Tag) SET p.updated=True, p.deleted=True"
   },
  {
      'constraint':"MATCH (c:Comment)<-[p:COMMENTED {deleted:false}]-(a:User)-[r:PROVIDED {deleted:false}]->(b:Answer) WHERE c.synth1<>b.synth1 RETURN ID(a),ID(b),ID(c)",
      'create_constraint':"MATCH (c:Comment)<-[p:COMMENTED {deleted:false}]-(a:User)-[r:PROVIDED {deleted:false}]->(b:Answer) WHERE c.synth1<>b.synth1 MERGE (a)-[:BELONGS]->(v1:Violation {solved:False, locked:false, nodes: ID(a)+','+ID(b)+','+ID(c)+','+ID(p)+','+ID(r),labels:'a,b,c,p,r', type:1})<-[:BELONGS]-(b) MERGE (v1)<-[:BELONGS]-(c)",
      'pattern':"MATCH (c:Comment)<-[p:COMMENTED {deleted:false}]-(a:User)-[r:PROVIDED {deleted:false}]->(b:Answer) RETURN ID(c)",
      'inject_errors':"MATCH (c:Comment) WHERE FILTRI SET c.synth1=0, c.injected=True",
      'grr':"MATCH (c:Comment)<-[p:COMMENTED {deleted:false}]-(a:User)-[r:PROVIDED {deleted:false}]->(b:Answer) WHERE c.synth1<>b.synth1 SET c.updated=True, c.synth1=1, b.updated=True, b.synth1=1"
  },
  {
    'constraint':"MATCH (a:User)-[r:COMMENTED {deleted:false}]->(b:Comment)-[p:COMMENTED_ON {deleted:false}]->(c:Question)-[q:TAGGED {deleted:false}]->(d:Tag) WHERE a.synth1<d.synth1 RETURN ID(a),ID(b),ID(c),ID(d)",
    'create_constraint':"MATCH (a:User)-[r:COMMENTED {deleted:false}]->(b:Comment)-[p:COMMENTED_ON {deleted:false}]->(c:Question)-[q:TAGGED {deleted:false}]->(d:Tag) WHERE a.synth1<d.synth1 MERGE (a)-[:BELONGS]->(v1:Violation {solved:False, locked:false, nodes: ID(a)+','+ID(b)+','+ID(c)+','+ID(d)+','+ID(p)+','+ID(r)+','+ID(q),labels:'a,b,c,d,p,r,q', type:2})<-[:BELONGS]-(b) MERGE (d)-[:BELONGS]->(v1)<-[:BELONGS]-(c)",
    'pattern':"MATCH (a:User)-[r:COMMENTED {deleted:false}]->(b:Comment)-[p:COMMENTED_ON {deleted:false}]->(c:Question)-[q:TAGGED {deleted:false}]->(d:Tag) RETURN ID(a)",
    'inject_errors':"MATCH (a:User) WHERE FILTRI SET a.synth1=0, a.injected=True",
    'grr':"MATCH (a:User)-[r:COMMENTED {deleted:false}]->(b:Comment)-[p:COMMENTED_ON {deleted:false}]->(c:Question)-[q:TAGGED {deleted:false}]->(d:Tag) WHERE a.synth1<d.synth1 SET a.updated=True, a.synth1=1, d.updated=True, d.synth1=1"
  },
  { 
    'constraint':"MATCH (b:Question)<-[r:ASKED {deleted:false}]-(a1:User)-[p:ASKED {deleted:false}]->(c:Question), (a2:User)-[q:PROVIDED {deleted:false}]->(d:Answer) WHERE ID(a1)=ID(a2) AND b.synth1<>d.synth1 RETURN ID(a1),ID(b),ID(c),ID(d) ",
    'create_constraint':"MATCH (b:Question)<-[r:ASKED {deleted:false}]-(a1:User)-[p:ASKED {deleted:false}]->(c:Question), (a2:User)-[q:PROVIDED {deleted:false}]->(d:Answer) WHERE ID(a1)=ID(a2) AND b.synth1<>d.synth1 MERGE (a1)-[:BELONGS]->(v1:Violation {solved:False, locked:false, nodes: ID(a1)+','+ID(b)+','+ID(c)+','+ID(d)+','+ID(p)+','+ID(r)+','+ID(q),labels:'a1,b,c,d,p,r,q', type:3})<-[:BELONGS]-(b) MERGE (d)-[:BELONGS]->(v1)<-[:BELONGS]-(c)",
    'pattern':"MATCH (b:Question)<-[r:ASKED {deleted:false}]-(a1:User)-[p:ASKED {deleted:false}]->(c:Question), (a2:User)-[q:PROVIDED {deleted:false}]->(d:Answer) WHERE ID(a1)=ID(a2) RETURN ID(b)",
    'inject_errors':"MATCH (b:Question) WHERE FILTRI SET b.synth1=0, b.injected=True",
    'grr':"MATCH (b:Question)<-[r:ASKED {deleted:false}]-(a1:User)-[p:ASKED {deleted:false}]->(c:Question), (a2:User)-[q:PROVIDED {deleted:false}]->(d:Answer) WHERE ID(a1)=ID(a2) AND b.synth1<>d.synth1 SET b.updated=True, b.synth1=1, d.updated=True, d.synth1=1",
  }
 ]