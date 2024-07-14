# import required module
import os
import json
directory = os.getcwd()

for filename in ['preferredFincen','preferredSynthea','preferredWwc19','preferredStack','preferredSw']:
    
    # checking if it is a file
    if True:
    
    
        contents = []

        with open(filename) as f:
            contents = f.readlines()

        exps = []


        for i in range(len(contents)):
            line=contents[i].strip("\n")
            timedOut=False
            if("Running" in line):
                exps.append({'tp':0,'fp':0,'fn':0})
                params = line.split(' ')
                safetiness = params[2]
                mode = params[3]
                exps[-1]['mode'] = mode
                exps[-1]['safetiness'] = safetiness
                exps[-1]['timeout'] = 0
                exps[-1]['count'] = [[]]
                exps[-1]['precision'] = []
                exps[-1]['recall'] = []
                exps[-1]['f1'] = []
                exps[-1]['solved'] =[[]]
                exps[-1]['added'] =[[]]
                exps[-1]['iteration'] =[]
                
                
            if("[{'count':" in line):
                exps[-1]['count'][-1].append(float(line.split(":")[-1].strip("}]")))                
            if("Solved" in line):
                exps[-1]['solved'][-1].append(float(line.split(":")[-1]))
            if("Introduced" in line):
                exps[-1]['added'][-1].append(float(line.split(":")[-1]))
            if("iteration count" in line):
                exps[-1]['iteration'].append(float(line.split(":")[-1]))
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
                exps[-1]['solved'].append([])
                exps[-1]['added'].append([])
                exps[-1]['count'].append([])
            if("timed" in line):
                exps[-1]['timeout'] += 1


        with open(filename+".json", "w") as fp:
            json.dump(exps, fp)
    """ except Exception as e:
        print(e)
        print("Error in file: "+filename)
        continue  """