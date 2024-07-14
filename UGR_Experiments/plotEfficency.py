import json
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


directory = os.getcwd()
from matplotlib import rcParams
rcParams['axes.titlepad'] = 20 
fig=plt.figure(figsize=(50, 8))
columns = 5
rows =  1  


for filename in os.listdir(directory):
    if filename.endswith(".json") and "FincenOutput" in filename:        
        dataListInteractionsS = []
        dataListWaitingsS = []
        dataListIterationS = []
        dataListInteractionsU = []
        dataListWaitingsU = []
        dataListIterationU = []
        dataListEfficencyS = []
        dataListEfficencyU = []
        
        f = open(filename, "r")
        
        data = json.load(f)
        
        for exp in data:
            iterations = exp['iteration']
            interactions = exp['interactions']
            waitings = exp['waitings']
            timeouts = exp['timeouts']
            users = int(exp['users'])
            eff=[]
            for count,vals in enumerate(waitings):
                if(not timeouts[count]):
                    
                    eff.append(1- waitings[count]/(users*iterations[count]))
            if(exp['safetiness']=='True'):
                for count,w in enumerate(waitings):
                    if(not timeouts[count]):
                        dataListWaitingsS.append([exp['users'],w,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                for count,i in enumerate(interactions):
                    if(not timeouts[count]):
                        dataListInteractionsS.append([exp['users'],i,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                for count,it in enumerate(iterations):
                    if(not timeouts[count]):
                        dataListIterationS.append([exp['users'],it,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                for count,ef in enumerate(eff):
                    if(not timeouts[count]):
                        dataListEfficencyS.append([exp['users'],ef,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
            else:
                for count,w in enumerate(waitings):
                    if(not timeouts[count]):
                        dataListWaitingsU.append([exp['users'],w,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                for count,i in enumerate(interactions):
                    if(not timeouts[count]):
                        dataListInteractionsU.append([exp['users'],i,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                for count,it in enumerate(iterations):
                    if(not timeouts[count]):
                        dataListIterationU.append([exp['users'],it,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                for count,ef in enumerate(eff):
                    if(not timeouts[count]):
                        dataListEfficencyU.append([exp['users'],ef,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
            

        f.close()

        
        dfIterationsS = pd.DataFrame(dataListIterationS, columns=['users','iterations', 'repair','assignement'])
        dfWaitingsS = pd.DataFrame(dataListWaitingsS, columns=['users','waitings', 'repair','assignement'])
        dfInteractionsS = pd.DataFrame(dataListInteractionsS, columns=['users','interactions', 'repair','assignement'])
        dfIterationsU = pd.DataFrame(dataListIterationU, columns=['users','iterations', 'repair','assignement'])
        dfWaitingsU = pd.DataFrame(dataListWaitingsU, columns=['users','waitings', 'repair','assignement'])
        dfInteractionsU = pd.DataFrame(dataListInteractionsU, columns=['users','interactions', 'repair','assignement'])
        dfEfficencyS = pd.DataFrame(dataListEfficencyS, columns=['users','efficency', 'repair','assignement'])
        dfEfficencyU = pd.DataFrame(dataListEfficencyU, columns=['users','efficency', 'repair','assignement'])
        
        fig.add_subplot(rows, columns, 5)
        sns.barplot(
            data=dfWaitingsS, x="users", y="waitings", hue="assignement", legend=None,
            errorbar="sd", 
            palette=sns.color_palette([ '#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d','#91918c','#329da8']))
          
        
        # sns.barplot(
        #     data=dfInteractionsS, x="users", y="interactions", hue="assignement", 
        #     errorbar="sd", legend=None,
        #     palette=sns.color_palette([ '#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d','#91918c','#329da8'])).set(title='Interactions for Fincen with safe repair')
        plt.title('Waitings for Fincen with safe repair', fontsize=25)
        plt.margins(x=0)
        plt.margins(y=0)
        plt.xlabel("Users", fontsize=25)
        plt.ylabel("#wait", fontsize=25)        
        plt.yticks(fontsize=15)
        plt.xticks(fontsize=15) 

    if filename.endswith(".json") and "StackoverflowOutput" in filename:        
            dataListInteractionsS = []
            dataListWaitingsS = []
            dataListIterationS = []
            dataListInteractionsU = []
            dataListWaitingsU = []
            dataListIterationU = []
            dataListEfficencyS = []
            dataListEfficencyU = []
            
            f = open(filename, "r")
            
            data = json.load(f)
            
            for exp in data:
                iterations = exp['iteration']
                interactions = exp['interactions']
                waitings = exp['waitings']
                timeouts = exp['timeouts']
                users = int(exp['users'])
                eff=[]
                for count,vals in enumerate(waitings):
                    if(not timeouts[count]):
                        
                        eff.append(1- waitings[count]/(users*iterations[count]))
                if(exp['safetiness']=='True'):
                    for count,w in enumerate(waitings):
                        if(not timeouts[count]):
                            dataListWaitingsS.append([exp['users'],w,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,i in enumerate(interactions):
                        if(not timeouts[count]):
                            dataListInteractionsS.append([exp['users'],i,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,it in enumerate(iterations):
                        if(not timeouts[count]):
                            dataListIterationS.append([exp['users'],it,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,ef in enumerate(eff):
                        if(not timeouts[count]):
                            dataListEfficencyS.append([exp['users'],ef,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                else:
                    for count,w in enumerate(waitings):
                        if(not timeouts[count]):
                            dataListWaitingsU.append([exp['users'],w,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,i in enumerate(interactions):
                        if(not timeouts[count]):
                            dataListInteractionsU.append([exp['users'],i,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,it in enumerate(iterations):
                        if(not timeouts[count]):
                            dataListIterationU.append([exp['users'],it,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,ef in enumerate(eff):
                        if(not timeouts[count]):
                            dataListEfficencyU.append([exp['users'],ef,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                

            f.close()
            

            
            dfIterationsS = pd.DataFrame(dataListIterationS, columns=['users','iterations', 'repair','assignement'])
            dfWaitingsS = pd.DataFrame(dataListWaitingsS, columns=['users','waitings', 'repair','assignement'])
            dfInteractionsS = pd.DataFrame(dataListInteractionsS, columns=['users','interactions', 'repair','assignement'])
            dfIterationsU = pd.DataFrame(dataListIterationU, columns=['users','iterations', 'repair','assignement'])
            dfWaitingsU = pd.DataFrame(dataListWaitingsU, columns=['users','waitings', 'repair','assignement'])
            dfInteractionsU = pd.DataFrame(dataListInteractionsU, columns=['users','interactions', 'repair','assignement'])
            dfEfficencyS = pd.DataFrame(dataListEfficencyS, columns=['users','efficency', 'repair','assignement'])
            dfEfficencyU = pd.DataFrame(dataListEfficencyU, columns=['users','efficency', 'repair','assignement'])
            
            fig.add_subplot(rows, columns, 2)
            sns.barplot(
                data=dfWaitingsS, x="users", y="waitings", hue="assignement", legend=None,
                errorbar="sd", 
                palette=sns.color_palette([ '#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d','#91918c','#329da8'])).set(title='Waitings for Fincen with safe repair')
            
            # sns.barplot(
            #     data=dfInteractionsS, x="users", y="interactions", hue="assignement", 
            #     errorbar="sd", legend=None,
            #     palette=sns.color_palette([ '#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d','#91918c','#329da8'])).set(title='Interactions for Fincen with safe repair')
            plt.title('Waitings for Stackoverflow with safe repair', fontsize=25)
            plt.margins(x=0)
            plt.margins(y=0)
            plt.xlabel("Users", fontsize=25)
            plt.ylabel("#wait", fontsize=25)        
            plt.yticks(fontsize=15)
            plt.xticks(fontsize=15) 

    if filename.endswith(".json") and "Wwc19Output" in filename:        
            dataListInteractionsS = []
            dataListWaitingsS = []
            dataListIterationS = []
            dataListInteractionsU = []
            dataListWaitingsU = []
            dataListIterationU = []
            dataListEfficencyS = []
            dataListEfficencyU = []
            
            f = open(filename, "r")
            
            data = json.load(f)
            
            for exp in data:
                iterations = exp['iteration']
                interactions = exp['interactions']
                waitings = exp['waitings']
                timeouts = exp['timeouts']
                users = int(exp['users'])
                eff=[]
                for count,vals in enumerate(waitings):
                    if(not timeouts[count]):
                        
                        eff.append(1- waitings[count]/(users*iterations[count]))
                if(exp['safetiness']=='True'):
                    for count,w in enumerate(waitings):
                        if(not timeouts[count]):
                            dataListWaitingsS.append([exp['users'],w,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,i in enumerate(interactions):
                        if(not timeouts[count]):
                            dataListInteractionsS.append([exp['users'],i,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,it in enumerate(iterations):
                        if(not timeouts[count]):
                            dataListIterationS.append([exp['users'],it,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,ef in enumerate(eff):
                        if(not timeouts[count]):
                            dataListEfficencyS.append([exp['users'],ef,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                else:
                    for count,w in enumerate(waitings):
                        if(not timeouts[count]):
                            dataListWaitingsU.append([exp['users'],w,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,i in enumerate(interactions):
                        if(not timeouts[count]):
                            dataListInteractionsU.append([exp['users'],i,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,it in enumerate(iterations):
                        if(not timeouts[count]):
                            dataListIterationU.append([exp['users'],it,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,ef in enumerate(eff):
                        if(not timeouts[count]):
                            dataListEfficencyU.append([exp['users'],ef,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                

            f.close()
            
            
            dfIterationsS = pd.DataFrame(dataListIterationS, columns=['users','iterations', 'repair','assignement'])
            dfWaitingsS = pd.DataFrame(dataListWaitingsS, columns=['users','waitings', 'repair','assignement'])
            dfInteractionsS = pd.DataFrame(dataListInteractionsS, columns=['users','interactions', 'repair','assignement'])
            dfIterationsU = pd.DataFrame(dataListIterationU, columns=['users','iterations', 'repair','assignement'])
            dfWaitingsU = pd.DataFrame(dataListWaitingsU, columns=['users','waitings', 'repair','assignement'])
            dfInteractionsU = pd.DataFrame(dataListInteractionsU, columns=['users','interactions', 'repair','assignement'])
            dfEfficencyS = pd.DataFrame(dataListEfficencyS, columns=['users','efficency', 'repair','assignement'])
            dfEfficencyU = pd.DataFrame(dataListEfficencyU, columns=['users','efficency', 'repair','assignement'])
            
            fig.add_subplot(rows, columns, 3)
            sns.barplot(
                data=dfWaitingsS, x="users", y="waitings", hue="assignement", legend=None,
                errorbar="sd", 
                palette=sns.color_palette([ '#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d','#91918c','#329da8'])).set(title='Waitings for Fincen with safe repair')
            
            # sns.barplot(
            #     data=dfInteractionsS, x="users", y="interactions", hue="assignement", 
            #     errorbar="sd", legend=None,
            #     palette=sns.color_palette([ '#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d','#91918c','#329da8'])).set(title='Interactions for Fincen with safe repair')
            plt.title('Waitings for wwc2019 with safe repair', fontsize=25)
            plt.margins(x=0)
            plt.margins(y=0)
            plt.xlabel("Users", fontsize=25)
            plt.ylabel("#wait", fontsize=25)        
            plt.yticks(fontsize=15)
            plt.xticks(fontsize=15) 

    if filename.endswith(".json") and "SyntheaOutput" in filename:        
            dataListInteractionsS = []
            dataListWaitingsS = []
            dataListIterationS = []
            dataListInteractionsU = []
            dataListWaitingsU = []
            dataListIterationU = []
            dataListEfficencyS = []
            dataListEfficencyU = []
            
            f = open(filename, "r")
            
            data = json.load(f)
            
            for exp in data:
                iterations = exp['iteration']
                interactions = exp['interactions']
                waitings = exp['waitings']
                timeouts = exp['timeouts']
                users = int(exp['users'])
                eff=[]
                for count,vals in enumerate(waitings):
                    if(not timeouts[count]):
                        
                        eff.append(1- waitings[count]/(users*iterations[count]))
                if(exp['safetiness']=='True'):
                    for count,w in enumerate(waitings):
                        if(not timeouts[count]):
                            dataListWaitingsS.append([exp['users'],w,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,i in enumerate(interactions):
                        if(not timeouts[count]):
                            dataListInteractionsS.append([exp['users'],i,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,it in enumerate(iterations):
                        if(not timeouts[count]):
                            dataListIterationS.append([exp['users'],it,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,ef in enumerate(eff):
                        if(not timeouts[count]):
                            dataListEfficencyS.append([exp['users'],ef,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                else:
                    for count,w in enumerate(waitings):
                        if(not timeouts[count]):
                            dataListWaitingsU.append([exp['users'],w,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,i in enumerate(interactions):
                        if(not timeouts[count]):
                            dataListInteractionsU.append([exp['users'],i,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,it in enumerate(iterations):
                        if(not timeouts[count]):
                            dataListIterationU.append([exp['users'],it,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,ef in enumerate(eff):
                        if(not timeouts[count]):
                            dataListEfficencyU.append([exp['users'],ef,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                

            f.close()
           
            
            dfIterationsS = pd.DataFrame(dataListIterationS, columns=['users','iterations', 'repair','assignement'])
            dfWaitingsS = pd.DataFrame(dataListWaitingsS, columns=['users','waitings', 'repair','assignement'])
            dfInteractionsS = pd.DataFrame(dataListInteractionsS, columns=['users','interactions', 'repair','assignement'])
            dfIterationsU = pd.DataFrame(dataListIterationU, columns=['users','iterations', 'repair','assignement'])
            dfWaitingsU = pd.DataFrame(dataListWaitingsU, columns=['users','waitings', 'repair','assignement'])
            dfInteractionsU = pd.DataFrame(dataListInteractionsU, columns=['users','interactions', 'repair','assignement'])
            dfEfficencyS = pd.DataFrame(dataListEfficencyS, columns=['users','efficency', 'repair','assignement'])
            dfEfficencyU = pd.DataFrame(dataListEfficencyU, columns=['users','efficency', 'repair','assignement'])
            
            fig.add_subplot(rows, columns, 4)
            sns.barplot(
                data=dfWaitingsS, x="users", y="waitings", hue="assignement", legend=None,
                errorbar="sd", 
                palette=sns.color_palette([ '#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d','#91918c','#329da8'])).set(title='Waitings for Fincen with safe repair')
            
            # sns.barplot(
            #     data=dfInteractionsS, x="users", y="interactions", hue="assignement", 
            #     errorbar="sd", legend=None,
            #     palette=sns.color_palette([ '#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d','#91918c','#329da8'])).set(title='Interactions for Fincen with safe repair')

            plt.title('Waitings for Synthea with safe repair', fontsize=25)
            plt.margins(x=0)
            plt.margins(y=0)
            plt.xlabel("Users", fontsize=25)
            plt.ylabel("#wait", fontsize=25)        
            plt.yticks(fontsize=15)
            plt.xticks(fontsize=15) 
    if filename.endswith(".json") and "SwOutput" in filename:        
            dataListInteractionsS = []
            dataListWaitingsS = []
            dataListIterationS = []
            dataListInteractionsU = []
            dataListWaitingsU = []
            dataListIterationU = []
            dataListEfficencyS = []
            dataListEfficencyU = []
            
            f = open(filename, "r")
            
            data = json.load(f)
            
            for exp in data:
                iterations = exp['iteration']
                interactions = exp['interactions']
                waitings = exp['waitings']
                timeouts = exp['timeouts']
                users = int(exp['users'])
                eff=[]
                for count,vals in enumerate(waitings):
                    if(not timeouts[count]):
                        
                        eff.append(1- waitings[count]/(users*iterations[count]))
                if(exp['safetiness']=='True'):
                    for count,w in enumerate(waitings):
                        if(not timeouts[count]):
                            dataListWaitingsS.append([exp['users'],w,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,i in enumerate(interactions):
                        if(not timeouts[count]):
                            dataListInteractionsS.append([exp['users'],i,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,it in enumerate(iterations):
                        if(not timeouts[count]):
                            dataListIterationS.append([exp['users'],it,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,ef in enumerate(eff):
                        if(not timeouts[count]):
                            dataListEfficencyS.append([exp['users'],ef,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                else:
                    for count,w in enumerate(waitings):
                        if(not timeouts[count]):
                            dataListWaitingsU.append([exp['users'],w,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,i in enumerate(interactions):
                        if(not timeouts[count]):
                            dataListInteractionsU.append([exp['users'],i,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,it in enumerate(iterations):
                        if(not timeouts[count]):
                            dataListIterationU.append([exp['users'],it,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                    for count,ef in enumerate(eff):
                        if(not timeouts[count]):
                            dataListEfficencyU.append([exp['users'],ef,'safe' if exp['safetiness']=='True' else 'unsafe',exp['assignement']])
                

            f.close()
            
            
            dfIterationsS = pd.DataFrame(dataListIterationS, columns=['users','iterations', 'repair','assignement'])
            dfWaitingsS = pd.DataFrame(dataListWaitingsS, columns=['users','waitings', 'repair','assignement'])
            dfInteractionsS = pd.DataFrame(dataListInteractionsS, columns=['users','interactions', 'repair','assignement'])
            dfIterationsU = pd.DataFrame(dataListIterationU, columns=['users','iterations', 'repair','assignement'])
            dfWaitingsU = pd.DataFrame(dataListWaitingsU, columns=['users','waitings', 'repair','assignement'])
            dfInteractionsU = pd.DataFrame(dataListInteractionsU, columns=['users','interactions', 'repair','assignement'])
            dfEfficencyS = pd.DataFrame(dataListEfficencyS, columns=['users','efficency', 'repair','assignement'])
            dfEfficencyU = pd.DataFrame(dataListEfficencyU, columns=['users','efficency', 'repair','assignement'])
            
            fig.add_subplot(rows, columns, 1)
            sns.barplot(
                data=dfWaitingsS, x="users", y="waitings", hue="assignement", 
                errorbar="sd", 
                palette=sns.color_palette([ '#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d','#91918c','#329da8'])).set(title='Waitings for Fincen with safe repair')
            # sns.barplot(
            #     data=dfInteractionsS, x="users", y="interactions", hue="assignement", 
            #     errorbar="sd", legend=None,
            #     palette=sns.color_palette([ '#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d','#91918c','#329da8'])).set(title='Interactions for Fincen with safe repair')        
            plt.title('Waitings for StarWars with safe repair', fontsize=25)
            plt.margins(x=0)
            plt.margins(y=0)
            plt.xlabel("Users", fontsize=25)
            plt.ylabel("#wait", fontsize=25)        
            plt.yticks(fontsize=15)
            plt.xticks(fontsize=15) 
plt.legend(
        
        loc="upper center",
        bbox_to_anchor=(1.5, -0.1), ncol=7, title=None, frameon=True, fontsize=25
    )

plt.savefig("plots/efficency/Wait.png",bbox_inches='tight')
    