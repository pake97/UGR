import math
import random 
import time
def injectInconsistencies(neo4j_Connector,constraints,error_distribution,SEED):
    random.seed(SEED)
    to_inject = []
    partialSum = 0
    for idx,constraint in enumerate(constraints):
        
        final_results = []
        pattern = constraint['pattern']
        
        inject_errors = constraint['inject_errors']
        

        try:
             
            t0 = time.time()
            results, meta = neo4j_Connector.query_id(pattern+" LIMIT "+str(error_distribution[idx]))
            t1=time.time()
            #print("Query time: ",t1-t0)
            resul = [x[0] for x in results]
            final_results = list(set(resul))
            partialSum += len(final_results)
            
            # while True:
            #     t0 = time.time()
            #     results, meta = neo4j_Connector.query_id(pattern+" SKIP "+str(i*100)+" LIMIT 100")
            #     t1=time.time()
            #     #print("Query time: ",t1-t0)
            #     resul = [x[0] for x in results]
            #     final_results = list(set(resul).union(set(final_results)))
            #     if(len(final_results)>=error_distribution[idx] or i>1000):
            #         while(len(final_results)>error_distribution[idx]):
            #             final_results.pop()
            #         break
            #     i+=1
            # print(len(final_results))
            #to_inject = random.choices(final_results,k=math.floor(num_inconsitencies*error_distribution[idx]))
           
            for res in final_results:
                result = neo4j_Connector.query(inject_errors.replace("FILTRI",meta[0]+"="+str(res)))
           
            to_inject.append({'meta':meta[0],'ids':final_results})
            #print("Injected inconsistencies in ",t3-t2," seconds")
        except Exception as e:
            print("INJECT Error executing query: ", pattern)
            print(e)
            continue
    #print(partialSum)
    return to_inject