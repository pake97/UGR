rules={"rules":["?a  COMMENTED  ?g  ?g  COMMENTED_ON  ?b   => ?a  ASKED  ?b",
"?a  PROVIDED  ?h  ?h  hasSynth  ?b   => ?a  hasSynth  ?b",
"?a  COMMENTED  ?h  ?h  hasSynth  ?b   => ?a  hasSynth  ?b",
"?a  ASKED  ?h  ?h  hasSynth  ?b   => ?a  hasSynth  ?b",
"?a  ASKED  ?h  ?b  COMMENTED_ON  ?h   => ?a  COMMENTED  ?b",
"?g  ASKED  ?b  ?g  COMMENTED  ?a   => ?a  COMMENTED_ON  ?b",
"?a  COMMENTED_ON  ?h  ?h  hasSynth  ?b   => ?a  hasSynth  ?b",
"?g  PROVIDED  ?a  ?g  hasSynth  ?b   => ?a  hasSynth  ?b",
"?a  ANSWERED  ?h  ?h  hasSynth  ?b   => ?a  hasSynth  ?b",
"?g  COMMENTED_ON  ?a  ?g  hasSynth  ?b   => ?a  hasSynth  ?b",
"?g  ANSWERED  ?a  ?g  hasSynth  ?b   => ?a  hasSynth  ?b",
"?g  ASKED  ?b  ?g  PROVIDED  ?a   => ?a  ANSWERED  ?b",
"?g  TAGGED  ?a  ?g  hasSynth  ?b   => ?a  hasSynth  ?b",
"?g  COMMENTED  ?a  ?g  hasSynth  ?b   => ?a  hasSynth  ?b",
"?g  ASKED  ?a  ?g  hasSynth  ?b   => ?a  hasSynth  ?b",
"?a  TAGGED  ?h  ?h  hasSynth  ?b   => ?a  hasSynth  ?b"],
"queries":["MATCH (a)-[:COMMENTED]->(g)-[:COMMENTED_ON]->(b) MERGE (a)-[:ASKED {added:True}]->(b)",
"MATCH (a)-[:PROVIDED]-(h) SET a.synth1 = h.synth1, a.updated = True",
"MATCH (a)-[:COMMENTED]-(h) SET a.synth1 = h.synth1, a.updated = True",
"MATCH (a)-[:ASKED]-(h) SET a.synth1 = h.synth1, a.updated = True",
"MATCH (a)-[:ASKED]-(h)-[:COMMENTED_ON]->(b) MERGE (a)-[:COMMENTED {added:True}]->(b)",
"MATCH (g)-[:ASKED]-(b)-[:COMMENTED]->(a) MERGE (a)-[:COMMENTED_ON {added:True}]->(b)",
"MATCH (a)-[:COMMENTED_ON]-(h) SET a.synth1 = h.synth1, a.updated = True",
"MATCH (g)-[:PROVIDED]-(a) SET a.synth1 = g.synth1, a.updated = True",
"MATCH (a)-[:ANSWERED]-(h) SET a.synth1 = h.synth1, a.updated = True",
"MATCH (g)-[:COMMENTED_ON]-(a) SET a.synth1 = g.synth1, a.updated = True",
"MATCH (g)-[:ANSWERED]-(a) SET a.synth1 = g.synth1, a.updated = True",
"MATCH (g)-[:ASKED]-(b)-[:PROVIDED]->(a) MERGE (a)-[:ANSWERED {added:True}]->(b)",
"MATCH (g)-[:TAGGED]-(a) SET a.synth1 = g.synth1, a.updated = True",
"MATCH (g)-[:COMMENTED]-(a) SET a.synth1 = g.synth1",
"MATCH (g)-[:ASKED]-(a) SET a.synth1 = g.synth1, a.updated = True",
"MATCH (a)-[:TAGGED]-(h) SET a.synth1 = h.synth1, a.updated = True",
"MATCH (a)-[r:SYNTH]-(b) set r.deleted=True"]}