# import required module
import os
import json
directory = os.getcwd()

#list output files to parse
for filename in []:
    
    # checking if it is a file
    if True:
        try:
        
            contents = []

            with open(filename) as f:
                contents = f.readlines()

            exps = []


            for i in range(len(contents)):
                line=contents[i].strip("\n")
                timedOut=False
                if("Running" in line):
                    exps.append({'tp':0,'fp':0,'fn':0,'iteration':[],'interactions':[],'waitings':[]})
                    params = line.split(' ')
                    dataset = params[1]
                    safetiness = params[2]
                    assignement = params[3]
                    users = params[4]
                    asnwer = params[5]
                    exps[-1]['dataset'] = dataset
                    exps[-1]['users'] = users
                    exps[-1]['safetiness'] = safetiness
                    exps[-1]['assignement'] = assignement
                    exps[-1]['answer'] = asnwer 
                    exps[-1]['timeout'] = 0
                    exps[-1]['timeouts'] = []
                    exps[-1]['buildGrdg'] = []
                    exps[-1]['computeBtw'] = []
                    exps[-1]['densityGrdg'] = []
                    exps[-1]['delete'] = []
                    exps[-1]['update'] = []
                    exps[-1]['count'] = []
                    exps[-1]['diramation'] = []
                    exps[-1]['minBtw'] = 0
                    exps[-1]['maxBtw'] = 0
                    exps[-1]['meanBtw'] = 0
                    exps[-1]['precision'] = []
                    exps[-1]['recall'] = []
                    exps[-1]['f1'] = []
                    exps[-1]['chosen'] =[]
                    exps[-1]['solved'] =[]
                    exps[-1]['added'] =[]

                if("build grdg" in line):
                    exps[-1]['buildGrdg'].append(float(line.split(":")[-1]))
                    exps[-1]['computeBtw'].append([])
                    exps[-1]['delete'].append([])
                    exps[-1]['update'].append([])
                    exps[-1]['diramation'].append([])
                    exps[-1]['solved'].append([])
                    exps[-1]['chosen'].append([])
                    exps[-1]['added'].append([])
                    exps[-1]['count'].append([])
                    exps[-1]['timeouts'].append(False)
                if("[{'count':" in line):
                    exps[-1]['count'][-1].append(float(line.split(":")[-1].strip("}]")))                
                if("compute btw" in line):
                    exps[-1]['computeBtw'][-1].append(float(line.split(":")[-1]))
                if("Density" in line):
                    exps[-1]['densityGrdg'] = float(line.split(":")[-1])
                if("delete" in line):
                    exps[-1]['delete'][-1].append(float(line.split(":")[-1]))
                if("update" in line):
                    exps[-1]['update'][-1].append(float(line.split(":")[-1]))
                if("diramation" in line):
                    exps[-1]['diramation'][-1].append(float(line.split(":")[-1]))
                if("Chosen" in line):
                    exps[-1]['chosen'][-1].append(float(line.split(":")[-1]))
                if("Solved" in line):
                    exps[-1]['solved'][-1].append(float(line.split(":")[-1]))
                if("Added" in line):
                    exps[-1]['added'][-1].append(float(line.split(":")[-1]))
                if("iteration count" in line):
                    exps[-1]['iteration'].append(float(line.split(":")[-1]))
                if("interaction count" in line):
                    exps[-1]['interactions'].append(float(line.split(":")[-1]))
                if("wait count" in line):
                    exps[-1]['waitings'].append(float(line.split(":")[-1]))
                if("minimumScore" in line):
                    params = line.split(',')
                    exps[-1]['minBtw'] = float(params[0].split(":")[-1])
                    exps[-1]['meanBtw'] = float(params[1].split(":")[-1])
                    exps[-1]['maxBtw'] = float(params[2].split(":")[-1].strip("}]"))
                if("True positives" in line):
                    exps[-1]['tp'] += int(line.split(":")[-1])
                if("False positives" in line):
                    exps[-1]['fp'] += int(line.split(":")[-1])
                if("False negatives" in line):
                    exps[-1]['fn'] += int(line.split(":")[-1])
                    if(exps[-1]['tp']+exps[-1]['fp'] == 0):
                        exps[-1]['precision'].append(0)
                    else:
                        exps[-1]['precision'].append(exps[-1]['tp']/(exps[-1]['tp']+exps[-1]['fp']))
                    if(exps[-1]['tp']+exps[-1]['fn'] == 0):
                        exps[-1]['recall'].append(0)
                    else:
                        exps[-1]['recall'].append(exps[-1]['tp']/(exps[-1]['tp']+exps[-1]['fn']))
                    if(exps[-1]['precision'][-1]+exps[-1]['recall'][-1] == 0):
                        exps[-1]['f1'].append(0)
                    else:
                        exps[-1]['f1'].append(2*(exps[-1]['precision'][-1]*exps[-1]['recall'][-1])/(exps[-1]['precision'][-1]+exps[-1]['recall'][-1]))
                    exps[-1]['tp'] = 0
                    exps[-1]['fp'] = 0
                    exps[-1]['fn'] = 0
                """ if("iteration" in line):
                    exps[-1]['iteration'] = float(line.split(":")[-1])
                if("interactions" in line):
                    exps[-1]['interactions'] = float(line.split(":")[-1])
                if("waitings" in line):
                    exps[-1]['waitings'] = float(line.split(":")[-1]) """
                if("timed" in line):
                    exps[-1]['timeout'] += 1
                    exps[-1]['timeouts'][-1] = True


            with open(filename+".json", "w") as fp:
                json.dump(exps, fp)
        except Exception as e:
            print(e)
            print("Error in file: "+filename)
            continue 