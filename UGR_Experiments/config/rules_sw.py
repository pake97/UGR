rules={"rules":["?g  OF  ?a  ?g  hasSynth  ?b   => ?a  hasSynth  ?b",
"?a  PILOT  ?h  ?h  hasSynth  ?b   => ?a  hasSynth  ?b",
"?g  PILOT  ?a  ?g  hasSynth  ?b   => ?a  hasSynth  ?b",
"?g  HOMEWORLD  ?a  ?g  hasSynth  ?b   => ?a  hasSynth  ?b",
"?g  APPEARED_IN  ?b  ?g  OF  ?a   => ?a  APPEARED_IN  ?b",
"?g  APPEARED_IN  ?b  ?g  PILOT  ?a   => ?a  APPEARED_IN  ?b",
"?h  APPEARED_IN  ?b  ?a  PILOT  ?h   => ?a  APPEARED_IN  ?b",
"?g  HOMEWORLD  ?b  ?g  OF  ?a   => ?a  HOMEWORLD  ?b",
"?a  OF  ?h  ?h  hasSynth  ?b   => ?a  hasSynth  ?b",
"?h  APPEARED_IN  ?b  ?a  HOMEWORLD  ?h   => ?a  APPEARED_IN  ?b",
"?h  HOMEWORLD  ?b  ?a  OF  ?h   => ?a  HOMEWORLD  ?b",
"?a  HOMEWORLD  ?h  ?h  hasSynth  ?b   => ?a  hasSynth  ?b",
"?g  APPEARED_IN  ?b  ?g  HOMEWORLD  ?a   => ?a  APPEARED_IN  ?b",
"?g  APPEARED_IN  ?a  ?g  hasSynth  ?b   => ?a  hasSynth  ?b",
"?h  APPEARED_IN  ?b  ?a  OF  ?h   => ?a  APPEARED_IN  ?b",
"?a  APPEARED_IN  ?h  ?h  hasSynth  ?b   => ?a  hasSynth  ?b"],
"queries":["MATCH (g)-[:OF]->(a) SET a.synth1 = g.synth1, a.updated = True",
"MATCH (a)-[:PILOT]->(h) SET a.synth1 = h.synth1, a.updated = True",
"MATCH (g)-[:PILOT]->(a) SET a.synth1 = g.synth1, a.updated = True",
"MATCH (g)-[:HOMEWORLD]->(a) SET a.synth1 = g.synth1, a.updated = True",
"MATCH (a)-[:OF]-(g)-[:APPEARED_IN]->(b) MERGE (a)-[:APPEARED_IN {added:True}]->(b)",
"MATCH (a)-[:PILOT]-(g)-[:APPEARED_IN]->(b) MERGE (a)-[:APPEARED_IN {added:True}]->(b)",
"MATCH (a)-[:PILOT]-(h)-[:APPEARED_IN]->(b) MERGE (a)-[:APPEARED_IN {added:True}]->(b)",
"MATCH (g)-[:OF]-(b)-[:HOMEWORLD]->(a) MERGE (a)-[:HOMEWORLD {added:True}]->(b)",
"MATCH (a)-[:OF]->(h) SET a.synth1 = h.synth1, a.updated = True",
"MATCH (a)-[:HOMEWORLD]-(h)-[:APPEARED_IN]->(b) MERGE (a)-[:APPEARED_IN {added:True}]->(b)",
"MATCH (a)-[:HOMEWORLD]-(b)-[:OF]->(h) MERGE (a)-[:HOMEWORLD {added:True}]->(b)",
"MATCH (a)-[:HOMEWORLD]-(h) SET a.synth1 = h.synth1, a.updated = True",
"MATCH (g)-[:APPEARED_IN]->(b)-[:OF]->(a) MERGE (a)-[:APPEARED_IN {added:True}]->(b)",
"MATCH (g)-[:APPEARED_IN]->(a) SET a.synth1 = g.synth1, a.updated = True",
"MATCH (a)-[:APPEARED_IN]-(h)-[:OF]->(b) MERGE (a)-[:APPEARED_IN {added:True}]->(b)",
"MATCH (a)-[:APPEARED_IN]-(h) SET a.synth1 = h.synth1, a.updated = True",
"MATCH (a)-[r:SYNTH]-(b) set r.deleted=True"
]}