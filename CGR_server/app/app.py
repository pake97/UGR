from flask import Flask, request, jsonify, render_template, url_for, redirect
from neomodel import db, config, StructuredNode, RelationshipTo, RelationshipFrom
from config.sw_query import sw_query
from matplotlib.figure import Figure
from grdg.neo4j_connector import Neo4jConnector
from grdg.computeRepairs4 import computeRepairs
from grdg.checkSafety3 import checkSafety
import time
import json

config.DATABASE_URL = "YOUR AURADB CONNECTION STRING" 
# Create the app object
app = Flask(__name__)
neo4jConnector = Neo4jConnector(config.DATABASE_URL)
safetiness = False
violations_in_solving = []
interactions = 0
iterations = 0
waitings = 0
#
@app.route('/repair',methods=['POST'])
def repair():
    if(request.is_json):
        query = request.get_json()
        try:
            chosen_repair=query['repair']
            t=float(query['time'])
            violation_id=query['violationId']
            assigned_hypervertex = neo4jConnector.query("MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" RETURN v")
            assigned_hypervertex = assigned_hypervertex[0]
            print(chosen_repair)
            rep =neo4jConnector.query(chosen_repair+ ", v.timeToSolve="+str(time.time()-t)) 
            try:
                index = violations_in_solving.index(int(violation_id))
                violations_in_solving.pop(index)
            except:
                app.logger.info('Violation not found in solving list')
            
            app.logger.info('Interaction')

            properties = {}
            for l, v in assigned_hypervertex['v'].items():
                properties[l] = v 
            violation_nodes =properties['nodes'].split(",")                        
            violation_labels =properties['labels'].split(",")                
            neighbors=neo4jConnector.query("MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" CALL apoc.neighbors.athop(v, 'INTERSECT', 1) YIELD node RETURN ID(node) as id, node.nodes as nodes, node.labels as labels, node.type as type")
            for ngh in neighbors:
                ngh_id = ngh['id']
                print("NIGG",ngh_id)
                nodi=ngh['nodes'].split(",")
                labels=ngh['labels'].split(",")
                violation_type = ngh['type']
                filters =""
                for i in range(len(nodi)):
                    if(filters==""):
                        filters+="ID("+labels[i]+")="+nodi[i]
                    else:
                        filters+=" AND ID("+labels[i]+")="+nodi[i]
                query = sw_query[violation_type]['constraint']
                if("WHERE" in query):
                    query = query.replace("RETURN", "AND "+filters + " RETURN")
                else:
                    query = query.replace("RETURN", "WHERE "+filters + " RETURN")
                if(neo4jConnector.query(query)==[]):
                    print("SOLVED",ngh_id)
                    neo4jConnector.merge_query("MATCH (v:Violation) WHERE ID(v)= "+str(ngh_id)+" SET v.solved=True")
            for constraint in sw_query:
                allowed_nodes = constraint['ids']
                viols =[]
                for j in range(len(violation_nodes)):
                    if('ID('+violation_labels[j]+')' in allowed_nodes):
                        filters="ID("+violation_labels[j]+")="+violation_nodes[j]
                        vios=neo4jConnector.query(constraint['new_constraint'].replace("FILTRI",filters))   
                        viols.extend(vios)                            
                for viol in viols:
                    filters =""                                    
                    for nodes in viol.keys():
                        if(filters==""):
                            filters+=nodes + "="+str(viol[nodes])
                        else:
                            filters+=" AND "+nodes + "="+str(viol[nodes])
                    # query = self.constraints[violation_type]['constraint']
                    # if(self.neo4j_Connector.query(query.replace("RETURN", filters + " RETURN"))==[]):
                    if(len(neo4jConnector.query(constraint['check_new_violation'].replace("FILTRI",filters)))==0):
                        
                        new_violations = neo4jConnector.query(constraint['create_new_violation'].replace("FILTRI",filters))                                    
                        for v in new_violations:
                            id_v = v['v1'].element_id.split(":")[-1]
                            new_edges=neo4jConnector.merge_query("MATCH (v1:Violation {solved:False})<-[:BELONGS]-(a)-[:BELONGS]-(v2:Violation {solved:False}) WHERE ID(v1)="+str(id_v)+" AND ID(v2)<>"+str(id_v)+" AND NOT (v1)-[:INTERSECT]-(v2) MERGE (v1)-[:INTERSECT]-(v2)")

            if(len(neo4jConnector.query("MATCH (v:Violation {locked:false}) RETURN ID(v)"))==0 and len(violations_in_solving)==0):
                solvedViolations = neo4jConnector.query("MATCH (v:Violation {solved:true}) RETURN ID(v) as id")
                for v in solvedViolations:
                    neo4jConnector.query("MATCH (v:Violation) WHERE ID(v)="+str(v['id'])+" CALL apoc.refactor.rename.label('Violation', 'SolvedViolation', [v]) YIELD committedOperations RETURN committedOperations")
                neo4jConnector.merge_query("MATCH (sv:SolvedViolation)-[r]-() DELETE r")
                #neo4jConnector.merge_query("CALL gds.graph.drop('grdg') YIELD graphName;")
                neo4jConnector.merge_query("MATCH (v:Violation {solved:false}) SET v.locked=false")
                
                
                app.logger.info('Iteration')
            return jsonify({'msg': 'REPAIRED'}), 200
        except Exception as e:
            print(e)
            return jsonify({'msg': str(e)}), 500
    else:
        return jsonify({'msg': 'Invalid request body. Accepts only JSON body'}), 400
    

@app.route('/',methods=['GET'])
def assignRepair():
    if(len(neo4jConnector.query("MATCH (v:Violation {solved:false}) RETURN v"))==0):
        print("FINISH")
        response = jsonify({'message':'FINISH'}), 200 
        return response
    assigned_hypervertex = neo4jConnector.query("MATCH (v:Violation {locked : false}) RETURN v, rand() as r ORDER BY r LIMIT 1")
    if(len(assigned_hypervertex)==0):
        print("WAIT")
        app.logger.info('Waiting')
        response = jsonify({'message':'WAIT'}), 200
        return response
    print(assigned_hypervertex)
    assigned_hypervertex = assigned_hypervertex[0]
    violation_id=assigned_hypervertex['v'].element_id.split(":")[-1]     
    lock = neo4jConnector.merge_query("MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" SET v.locked = true") 
    #lock thr neighbors
    neo4jConnector.merge_query("MATCH (v:Violation) WHERE ID(v)="+str(violation_id)+" CALL apoc.neighbors.athop(v, 'INTERSECT', 1) YIELD node SET node.locked = true")
    violations_in_solving.append(int(violation_id))
    properties = {}
    for l, v in assigned_hypervertex['v'].items():
        properties[l] = v 
    violation_nodes =properties['nodes'].split(",")                        
    violation_labels =properties['labels'].split(",") 
    violation_type =properties['type'] 
    filters ="" 
    for i in range(len(violation_nodes)):
        if(filters==""):
            filters+="ID("+violation_labels[i]+")="+violation_nodes[i]
        else:
            filters+=" AND ID("+violation_labels[i]+")="+violation_nodes[i]                                   
    print(sw_query[violation_type]['violation'].replace("FILTRI",filters))
    pattern = neo4jConnector.query(sw_query[violation_type]['violation'].replace("FILTRI",filters))
    print(pattern)
    pattern_object = {}
    for k in list(pattern[0].keys()):
        id = pattern[0][k].element_id.split(":")[-1]
        pattern_object[k] = {'id':id}
        properties = {}
        for l, v in pattern[0][k].items():
            if(l in ["mass","height","name","model","vehicle_class","length","width","title","release_date","episode_id","average_height"]):
                properties[l] = v
        pattern_object[k]['properties']=properties
        if(k=='p' or k=='q' or k=='r'):
            nodes = pattern[0][k].nodes
            id1 = nodes[0].element_id.split(":")[-1]
            id2 = nodes[1].element_id.split(":")[-1]
            pattern_object[k]['nodes'] = [id1,id2]
            types= pattern[0][k].type
            pattern_object[k]['type'] = types
        else:
            pattern_object[k]['label'] = list(pattern[0][k].labels)[0]
            pattern_object[k]['nodes'] = []

    #print("assigned",assigned_hypervertex)
    repairs = computeRepairs(assigned_hypervertex, sw_query)['possible_repairs']
    explanation = sw_query[violation_type]['explanation']
    #response = jsonify({'repairs':repairs, 'violationId': violation_id, 'pattern':pattern_object, 'explanation':explanation}), 200
    return render_template('index.html', repairs=repairs, violationId=violation_id, pattern=json.dumps(pattern_object), explanation=explanation, t = time.time() )
    #return response


if __name__ == "__main__":
    app.run(port=5000,debug=True)
    
