def computeRepairs(assigned_hypervertex,properties,chosen_repair):
    
    violation_id = assigned_hypervertex['v'].element_id.split(":")[-1]
    nodes_ids =str(properties['nodes']).split(",")
    node_labels =properties['labels'].split(",")
    violation_type =int(properties['type'])    
    possible_repairs=[]
    best_repair=""

    
    
    if(violation_type==0):
        if(chosen_repair=="MATCH (a) WHERE ID(a)=FILTRI SET a.updated=True, a.status='Inactive'"):
            return "MATCH (a) WHERE ID(a)="+str(nodes_ids[0])+" SET a.updated=True, a.status='Inactive' UNION MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" SET v.solved=True"
        else:
            return "MATCH (a) WHERE ID(a)="+str(nodes_ids[0])+" SET a.updated=True, a.inactivation_date='' UNION MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" SET v.solved=True"
    if(violation_type==1):
        if(chosen_repair=="MATCH (a:Other)-[p:same_name_as {deleted:false}]-(b:Entity) where FILTRI SET a.updated=True, a.name=b.name"):
            return "MATCH (a:Other)-[p:same_name_as ]-(b:Entity) where ID(a)="+str(nodes_ids[0])+" and ID(b)="+str(nodes_ids[1])+" and ID(p)="+str(nodes_ids[2])+" SET a.updated=True, a.name=b.name UNION MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" SET v.solved=True"
        if(chosen_repair=="MATCH (a:Other)-[p:same_name_as {deleted:false}]-(b:Entity) where FILTRI SET a.updated=True, b.name=a.name"):
            return "MATCH (a:Other)-[p:same_name_as ]-(b:Entity) where ID(a)="+str(nodes_ids[0])+" and ID(b)="+str(nodes_ids[1])+" and ID(p)="+str(nodes_ids[2])+" SET b.updated=True, b.name=a.name UNION MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" SET v.solved=True"
        if(chosen_repair=="MATCH (a:Other)-[p:same_name_as {deleted:false}]-(b:Entity) where FILTRI SET p.updated=True, p.deleted=True"):
            return "MATCH (a:Other)-[p:same_name_as ]-(b:Entity) where ID(a)="+str(nodes_ids[0])+" and ID(b)="+str(nodes_ids[1])+" and ID(p)="+str(nodes_ids[2])+" SET p.updated=True, p.deleted=True UNION MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" SET v.solved=True"
        if(chosen_repair=="MATCH (a:Other)-[p:same_name_as {deleted:false}]-(b:Entity) where FILTRI SET a.updated=True, a.name=b.name, p.updated=True, p.deleted=True"):
            return "MATCH (a:Other)-[p:same_name_as ]-(b:Entity) where ID(a)="+str(nodes_ids[0])+" and ID(b)="+str(nodes_ids[1])+" and ID(p)="+str(nodes_ids[2])+" SET a.updated=True, a.name=b.name, p.updated=True, p.deleted=True UNION MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" SET v.solved=True"
        if(chosen_repair=="MATCH (a:Other)-[p:same_name_as {deleted:false}]-(b:Entity) where FILTRI SET a.updated=True, b.name=a.name, p.updated=True, p.deleted=True"):
            return "MATCH (a:Other)-[p:same_name_as ]-(b:Entity) where ID(a)="+str(nodes_ids[0])+" and ID(b)="+str(nodes_ids[1])+" and ID(p)="+str(nodes_ids[2])+" SET b.updated=True, b.name=a.name, p.updated=True, p.deleted=True UNION MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" SET v.solved=True"
        
    if(violation_type==2):
        if(chosen_repair=="MATCH (a:Address)-[p {deleted:false}]-(b) where FILTRI SET b.updated=True, b.country_codes=apoc.text.join([a.country_codes,b.country_codes],',')"):
            return "MATCH (a:Address)-[p ]-(b) where ID(a)="+str(nodes_ids[0])+" and ID(b)="+str(nodes_ids[1])+" and ID(p)="+str(nodes_ids[2])+" SET b.updated=True, b.country_codes=apoc.text.join([a.country_codes,b.country_codes],',')  UNION MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" SET v.solved=True"
        if(chosen_repair=="MATCH (a:Address)-[p {deleted:false}]-(b) where FILTRI SET p.updated=True, p.deleted=True"):
            return "MATCH (a:Address)-[p ]-(b) where ID(a)="+str(nodes_ids[0])+" and ID(b)="+str(nodes_ids[1])+" and ID(p)="+str(nodes_ids[2])+" SET p.updated=True, p.deleted=True UNION MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" SET v.solved=True"
        if(chosen_repair=="MATCH (a:Address)-[p {deleted:false}]-(b) where FILTRI SET b.updated=True, b.country_codes=apoc.text.join([a.country_codes,b.country_codes],','), p.updated=True, p.deleted=True"):
            return "MATCH (a:Address)-[p ]-(b) where ID(a)="+str(nodes_ids[0])+" and ID(b)="+str(nodes_ids[1])+" and ID(p)="+str(nodes_ids[2])+" SET b.updated=True, b.country_codes=apoc.text.join([a.country_codes,b.country_codes],','), p.updated=True, p.deleted=True UNION MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" SET v.solved=True"
    if(violation_type==3):
        if(chosen_repair=="MATCH (a)-[p:officer_of {deleted:false}]->(b) WHERE ID(p)=FILTRI SET p.updated=True, p.deleted=True"):
            return "MATCH (a)-[p:officer_of ]->(b) WHERE ID(p)="+str(nodes_ids[2])+" SET p.updated=True, p.deleted=True UNION MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" SET v.solved=True"
        if(chosen_repair=="MATCH (a)-[r:officer_of {deleted:false}]->(b) WHERE ID(r)=FILTRI SET r.updated=True, r.deleted=True"):
            return "MATCH (a)-[r:officer_of ]->(b) WHERE ID(r)="+str(nodes_ids[3])+" SET r.updated=True, r.deleted=True UNION MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" SET v.solved=True"
        if(chosen_repair=="MATCH (a)-[r:officer_of {deleted:false}]->(b)<-[p:officer_of {deleted:false}]-(a) WHERE ID(r)=FILTRI SET r.updated=True, r.deleted=True,p.updated=True, p.deleted=True"):
            return "MATCH (b)<-[r:officer_of ]-(a)-[p:officer_of ]->(b) WHERE ID(p)="+str(nodes_ids[2])+" and ID(r)="+str(nodes_ids[3])+" SET r.updated=True, r.deleted=True,p.updated=True, p.deleted=True UNION MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" SET v.solved=True "
        if(chosen_repair=="MATCH (a)-[p:officer_of {deleted:false}]->(b) WHERE ID(p)=FILTRI SET p.updated=True, p.link=apoc.coll.randomItem(apoc.coll.remove(['owner of','member of','shareholder of','power of attorney of','director of'], apoc.coll.indexOf(['owner of','member of','shareholder of','power of attorney of','director of'], p.link), 1))"):
            return "MATCH (a)-[p:officer_of ]->(b) WHERE ID(p)="+str(nodes_ids[2])+" SET p.updated=True, p.link=apoc.coll.randomItem(apoc.coll.remove(['owner of','member of','shareholder of','power of attorney of','director of'], apoc.coll.indexOf(['owner of','member of','shareholder of','power of attorney of','director of'], p.link), 1)) UNION MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" SET v.solved=True"
        if(chosen_repair=="MATCH (a)-[p:officer_of {deleted:false}]->(b) WHERE ID(p)=FILTRI SET r.updated=True, r.link=apoc.coll.randomItem(apoc.coll.remove(['owner of','member of','shareholder of','power of attorney of','director of'], apoc.coll.indexOf(['owner of','member of','shareholder of','power of attorney of','director of'], r.link), 1))"):
            return "MATCH (a)-[r:officer_of ]->(b) WHERE ID(r)="+str(nodes_ids[3])+" SET r.updated=True, r.link=apoc.coll.randomItem(apoc.coll.remove(['owner of','member of','shareholder of','power of attorney of','director of'], apoc.coll.indexOf(['owner of','member of','shareholder of','power of attorney of','director of'], r.link), 1)) UNION MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" SET v.solved=True"
        if(chosen_repair=="MATCH (b:Entity)<-[r:officer_of {deleted:false}]-(a)-[p:officer_of {deleted:false}]->(b) where FILTRI SET p.updated=True, p.link=apoc.coll.randomItem(apoc.coll.remove(['owner of','member of','shareholder of','power of attorney of','director of'], apoc.coll.indexOf(['owner of','member of','shareholder of','power of attorney of','director of'], p.link), 1)), r.updated=True, r.deleted=True"):
            return "MATCH (b:Entity)<-[r:officer_of ]-(a)-[p:officer_of ]->(b) where ID(a)="+str(nodes_ids[0])+" and ID(b)="+str(nodes_ids[1])+" and ID(p)="+str(nodes_ids[2])+" and id(r)="+str(nodes_ids[3])+" SET p.updated=True, p.link=apoc.coll.randomItem(apoc.coll.remove(['owner of','member of','shareholder of','power of attorney of','director of'], apoc.coll.indexOf(['owner of','member of','shareholder of','power of attorney of','director of'], p.link), 1)), r.updated=True, r.deleted=True"
        if(chosen_repair=="MATCH (b:Entity)<-[r:officer_of {deleted:false}]-(a)-[p:officer_of {deleted:false}]->(b) where FILTRI SET r.updated=True, r.link=apoc.coll.randomItem(apoc.coll.remove(['owner of','member of','shareholder of','power of attorney of','director of'], apoc.coll.indexOf(['owner of','member of','shareholder of','power of attorney of','director of'], r.link), 1)), p.updated=True, p.deleted=True"):
            return "MATCH (b:Entity)<-[r:officer_of ]-(a)-[p:officer_of ]->(b) where ID(a)="+str(nodes_ids[0])+" and ID(b)="+str(nodes_ids[1])+" and ID(p)="+str(nodes_ids[2])+" and id(r)="+str(nodes_ids[3])+" SET r.updated=True, r.link=apoc.coll.randomItem(apoc.coll.remove(['owner of','member of','shareholder of','power of attorney of','director of'], apoc.coll.indexOf(['owner of','member of','shareholder of','power of attorney of','director of'], r.link), 1)), p.updated=True, p.deleted=True"
        
    
        
    
    