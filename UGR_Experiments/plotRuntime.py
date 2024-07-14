import json
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

directory = os.getcwd()
dataListF1 = []
from matplotlib import rcParams
rcParams['axes.titlepad'] = 20 

def getName(dataset):
    if dataset==1:
        return 'StarWars'
    if dataset==2:
        return 'Stackoverflow'
    if dataset==3:
        return 'wwc2019'
    if dataset==4:
        return 'Synthea'
    if dataset==5:
        return 'Fincen'
    
        
fig=plt.figure(figsize=(50, 8))
columns = 5
rows =  1       
index=1
for filename in ['SWOutput.json','StackOutput.json','Wwc19Output.json','SyntheaOutput.json', 'FincenOutput.json' ]:
    
    f = open(filename, "r")        
    data = json.load(f) 
    for exp in data:
        if(exp['answer']=='1' and exp['safetiness']=='True' and exp['assignement']=='random'):
            dataListF1T = []
            dataListF1U = []
            dataListF1D = []
            idx=0
            timesGrdg = exp['buildGrdg']
            timesDiramation = exp['diramation']
            timesUpdate = exp['update']
            timesDelete = exp['delete']
            maxLen = len(timesDiramation[0])
            timeouts = exp['timeouts']
            for count,sol in enumerate(timesDiramation):
                if len(sol) < maxLen and len(sol) > 0 and not timeouts[count]:
                    maxLen = len(sol)
                    idx = count
            
            shortestDiramation= timesDiramation[idx]
            shortestGrdg = timesGrdg[idx]
            print(shortestGrdg)
            shortestUpdate = timesUpdate[idx]
            shortestDelete = timesDelete[idx]
            shortestUpdate.append(0)
            dataListF1T.append(shortestGrdg)
            dataListF1D.append(0)
            dataListF1U.append(0)



            for i in range(len(shortestDiramation)):
                
                dataListF1D.append(shortestDiramation[i])
                dataListF1U.append(shortestUpdate[i])
                #dataListF1.append([i+1,shortestDiramation[i]+shortestUpdate[i]+shortestDelete[i],"Total time"])                
                dataListF1T.append(shortestDiramation[i]+shortestUpdate[i])                

            #dfF1 = pd.DataFrame(dataListF1, columns=['Iteration','Time', 'Measure'])

            fig.add_subplot(rows, columns, index)
            
            x=np.arange(0,len(dataListF1T),1)
            plt.plot(x,dataListF1T,label='Total time',color='blue')
            plt.plot(x,dataListF1U,label='Update time',color='green')
            plt.plot(x,dataListF1D,label='Diramation time',color='red')
            plt.title('Runtime for '+getName(index),fontsize = 25)
            plt.margins(x=0)
            plt.margins(y=0)
            plt.xlabel("Iteration", fontsize=25)
            plt.ylabel("Time (Seconds)", fontsize=25)        
            plt.yticks(fontsize=15)
            plt.xticks(fontsize=15)    
            index+=1
f.close()
plt.legend(loc="upper center",bbox_to_anchor=(-1.9, -0.1), fontsize="25",ncol=3, title=None, frameon=True)
plt.savefig("plots/runtime/runtime.png",bbox_inches='tight')