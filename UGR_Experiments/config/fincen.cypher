CREATE INDEX FOR (n:Filing) ON (n.icij_sar_id);
CREATE INDEX FOR (n:Entity) ON (n.name);
CREATE INDEX FOR (n:Filing) ON (n.begin);
CREATE INDEX FOR (n:Filing) ON (n.end);
CREATE INDEX FOR (n:Filing) ON (n.amount);
CREATE INDEX FOR (n:Country) ON (n.name);
CREATE INDEX FOR (n:Filing) ON (n.synth1);
CREATE INDEX FOR (n:Country) ON (n.synth1);
CREATE INDEX FOR (n:Entity) ON (n.synth1);

load csv with headers from "file:////download_transactions_map.csv" as value
merge (s:Filing {id:value.id}) set s += value;

load csv with headers from "file:////download_bank_connections.csv" as value
match (f:Filing {icij_sar_id:value.icij_sar_id})
merge (filer:Entity {id:value.filer_org_name_id}) on create set filer.name = value.filer_org_name, 
filer.location = point({latitude:toFloat(value.filer_org_lat),longitude:toFloat(value.filer_org_lng)})
merge (other:Entity {id:value.entity_b_id}) on create set other.name = value.entity_b, 
other.location = point({latitude:toFloat(value.entity_b_lat),longitude:toFloat(value.entity_b_lng)}),
other.country = value.entity_b_iso_code
merge (c:Country {code:value.entity_b_iso_code}) on create set c.name = value.entity_b_country
merge (f)<-[:FILED]-(filer)
merge (f)-[:CONCERNS]->(other)
merge (other)-[:COUNTRY]->(c);

match (f:Filing)
set f.transactions = toInteger(f.number_transactions)
set f.amount = toFloat(f.amount_transactions)
set f.end=f.end_date
set f.begin=f.begin_date

merge (ben:Entity {id:f.beneficiary_bank_id})
on create set ben.name = f.beneficiary_bank, ben.location = point({latitude:toFloat(f.beneficiary_lat), longitude:toFloat(f.beneficiary_lng)})
merge (cben:Country {code:f.beneficiary_iso})
merge (ben)-[:COUNTRY]->(cben)
merge (f)-[:BENEFITS]->(ben)

merge (filer:Entity {id:f.filer_org_name_id})
on create set filer.name = f.filer_org_name, filer.location = point({latitude:toFloat(f.filer_org_lat), longitude:toFloat(f.filer_org_lng)})
merge (f)<-[:FILED]-(filer)

merge (org:Entity {id:f.originator_bank_id})
on create set org.name = f.originator_bank, org.location = point({latitude:toFloat(f.origin_lat), longitude:toFloat(f.origin_lng)})
merge (corg:Country {code:f.originator_iso})
merge (org)-[:COUNTRY]->(corg)
merge (f)-[:ORIGINATOR]->(org)
;

