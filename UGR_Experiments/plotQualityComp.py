import json
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
rcParams['axes.titlepad'] = 20 
fig=plt.figure(figsize=(50, 8))
columns = 5
rows =  1  

directory = os.getcwd()

for filename in os.listdir(directory):
    
    if filename.endswith(".json") and "Wwc19Output" in filename and "random" not in filename:        
    
        f = open(filename, "r")
        
       
        dataListF1S = []
        dataListF1U = []
       

        data = json.load(f) 
        
        for exp in data:
            
            waitings = exp['f1']
            if(exp['safetiness'] == 'True'):
                for w in waitings:
                    dataListF1S.append([exp['answer'],w,'cQAR-safe',exp['assignement']])
            else:
                for w in waitings:
                    dataListF1U.append([exp['answer'],w,'cQAR-unsafe',exp['assignement']])
        f.close()

        
        dfF1S = pd.DataFrame(dataListF1S, columns=['answer','f1', 'safetiness','assignement'])
        dfF1U = pd.DataFrame(dataListF1U, columns=['answer','f1', 'safetiness','assignement'])

        
         
        fig.add_subplot(rows, columns, 3)
        sns.pointplot(
            data=dfF1S, x="answer", y="f1", hue="assignement", 
            capsize=.01, errorbar="sd",legend=None,
            palette=sns.color_palette([ '#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d','#91918c','#329da8'])).set(title='F1 Score for Wwc19 with safe repair')
        
        plt.title('F1 Score for Wwc19 with safe repair', fontsize=25)
        plt.xlabel("Answer", fontsize=25)
        plt.ylabel("F1", fontsize=25)        
        plt.yticks(fontsize=15)
        plt.xticks(fontsize=15) 
        
        # sns.pointplot(
        #     data=dfF1U, x="answer", y="f1", hue="assignement", 
        #     capsize=.01, errorbar="sd",
        #     palette=sns.color_palette([ '#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d','#91918c','#329da8'])).set(title='F1 Score for Wwc19 with unsafe repair')
        # plt.legend(loc="upper center",bbox_to_anchor=(.5, -0.1), ncol=3, title=None, frameon=True)
        # plt.title('F1 Score for Wwc19 with unsafe repair', fontsize=25)
        # plt.margins(x=0)
        # plt.margins(y=0)
        # plt.xlabel("Answer", fontsize=25)
        # plt.ylabel("F1", fontsize=25)        
        # plt.yticks(fontsize=15)
        # plt.xticks(fontsize=15) 
        

directory = os.getcwd()

for filename in os.listdir(directory):
    if filename.endswith(".json") and "StackOutput" in filename:        
    
        f = open(filename, "r")
        
        dataListF1S = []
        dataListF1U = []

        data = json.load(f) 
        
        for exp in data:
            
            waitings = exp['f1']
            if(exp['safetiness'] == 'True'):
                for w in waitings:
                    dataListF1S.append([exp['answer'],w,'cQAR-safe',exp['assignement']])
            else:
                for w in waitings:
                    dataListF1U.append([exp['answer'],w,'cQAR-unsafe',exp['assignement']])
        f.close()



        

        dfF1S = pd.DataFrame(dataListF1S, columns=['answer','f1', 'safetiness','assignement'])
        dfF1U = pd.DataFrame(dataListF1U, columns=['answer','f1', 'safetiness','assignement'])

        fig.add_subplot(rows, columns, 2)
        sns.pointplot(
            data=dfF1S, x="answer", y="f1", hue="assignement", 
            capsize=.01, errorbar="sd",legend=None,
            palette=sns.color_palette([ '#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d','#91918c','#329da8'])).set(title='F1 Score for Stackoverflow with safe repair')
        
        plt.title('F1 Score for Stackoverflow with safe repair', fontsize=25)
        
        plt.xlabel("Answer", fontsize=25)
        plt.ylabel("F1", fontsize=25)        
        plt.yticks(fontsize=15)
        plt.xticks(fontsize=15) 
        
        # sns.pointplot(
        #     data=dfF1U, x="answer", y="f1", hue="assignement", 
        #     capsize=.01, errorbar="sd",
        #     palette=sns.color_palette([ '#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d','#91918c','#329da8'])).set(title='F1 Score for Stackoverflow with unsafe repair')
        # plt.legend(loc="upper center",bbox_to_anchor=(.5, -0.1), ncol=3, title=None, frameon=True)
        # plt.title('F1 Score for Stackoverflow with unsafe repair', fontsize=25)
        # plt.margins(x=0)
        # plt.margins(y=0)
        # plt.xlabel("Answer", fontsize=25)
        # plt.ylabel("F1", fontsize=25)        
        # plt.yticks(fontsize=15)
        # plt.xticks(fontsize=15) 



directory = os.getcwd()

for filename in os.listdir(directory):
    if filename.endswith(".json") and "SyntheaOutput" in filename:        
    
        f = open(filename, "r")
        
        
       
        dataListF1S = []
        dataListF1U = []
       
        data = json.load(f) 
        
        for exp in data:
            
            waitings = exp['f1']
            if(exp['safetiness'] == 'True'):
                for w in waitings:
                    dataListF1S.append([exp['answer'],w,'cQAR-safe',exp['assignement']])
            else:
                for w in waitings:
                    dataListF1U.append([exp['answer'],w,'cQAR-unsafe',exp['assignement']])
        f.close()



        

        dfF1S = pd.DataFrame(dataListF1S, columns=['answer','f1', 'safetiness','assignement'])
        dfF1U = pd.DataFrame(dataListF1U, columns=['answer','f1', 'safetiness','assignement'])

        
        fig.add_subplot(rows, columns, 4)
        sns.pointplot(
            data=dfF1S, x="answer", y="f1", hue="assignement", 
            capsize=.01, errorbar="sd",legend=None,
            palette=sns.color_palette([ '#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d','#91918c','#329da8'])).set(title='F1 Score for Synthea with safe repair')
        
        plt.title('F1 Score for Synthea with safe repair', fontsize=25)
        
        plt.xlabel("Answer", fontsize=25)
        plt.ylabel("F1", fontsize=25)        
        plt.yticks(fontsize=15)
        plt.xticks(fontsize=15) 
        
        # sns.pointplot(
        #     data=dfF1U, x="answer", y="f1", hue="assignement", 
        #     capsize=.01, errorbar="sd",
        #     palette=sns.color_palette([ '#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d','#91918c','#329da8'])).set(title='F1 Score for Synthea with unsafe repair')
        # plt.legend(loc="upper center",bbox_to_anchor=(.5, -0.1), ncol=3, title=None, frameon=True)
        # plt.title('F1 Score for Synthea with unsafe repair', fontsize=25)
        # plt.margins(x=0)
        # plt.margins(y=0)
        # plt.xlabel("Answer", fontsize=25)
        # plt.ylabel("F1", fontsize=25)        
        # plt.yticks(fontsize=15)
        # plt.xticks(fontsize=15) 
        




directory = os.getcwd()

for filename in os.listdir(directory):
    if filename.endswith(".json") and "FincenOutput" in filename:        
    
        f = open(filename, "r")
        
        
       
        dataListF1S = []
        dataListF1U = []
    


        data = json.load(f) 
        
        for exp in data:
            
            waitings = exp['f1']
            if(exp['safetiness'] == 'True'):
                for w in waitings:
                    dataListF1S.append([exp['answer'],w,'cQAR-safe',exp['assignement']])
            else:
                for w in waitings:
                    dataListF1U.append([exp['answer'],w,'cQAR-unsafe',exp['assignement']])
        f.close()

        

        dfF1S = pd.DataFrame(dataListF1S, columns=['answer','f1', 'safetiness','assignement'])
        dfF1U = pd.DataFrame(dataListF1U, columns=['answer','f1', 'safetiness','assignement'])

        
        fig.add_subplot(rows, columns, 5)
        sns.pointplot(
            data=dfF1S, x="answer", y="f1", hue="assignement", 
            capsize=.01, errorbar="sd",legend=None,
            palette=sns.color_palette([ '#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d','#91918c','#329da8'])).set(title='F1 Score for Fincen with safe repair')
        
        plt.title('F1 Score for Fincen with safe repair', fontsize=25)
       
        plt.xlabel("Answer", fontsize=25)
        plt.ylabel("F1", fontsize=25)        
        plt.yticks(fontsize=15)
        plt.xticks(fontsize=15) 
        
        # sns.pointplot(
        #     data=dfF1U, x="answer", y="f1", hue="assignement", 
        #     capsize=.01, errorbar="sd",
        #     palette=sns.color_palette([ '#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d','#91918c','#329da8'])).set(title='F1 Score for Fincen with unsafe repair')
        # plt.legend(loc="upper center",bbox_to_anchor=(.5, -0.1), ncol=3, title=None, frameon=True)
        # plt.title('F1 Score for Fincen with unsafe repair', fontsize=25)
        # plt.margins(x=0)
        # plt.margins(y=0)
        # plt.xlabel("Answer", fontsize=25)
        # plt.ylabel("F1", fontsize=25)        
        # plt.yticks(fontsize=15)
        # plt.xticks(fontsize=15) 


directory = os.getcwd()

for filename in os.listdir(directory):
    if filename.endswith(".json") and "SWOutput" in filename:        
    
        f = open(filename, "r")
        
       
        dataListF1S = []
        dataListF1U = []
        

        data = json.load(f) 
        
        for exp in data:
            
            waitings = exp['f1']
            if(exp['safetiness'] == 'True'):
                for w in waitings:
                    dataListF1S.append([exp['answer'],w,'cQAR-safe',exp['assignement']])
            else:
                for w in waitings:
                    dataListF1U.append([exp['answer'],w,'cQAR-unsafe',exp['assignement']])
        f.close()


        

        dfF1S = pd.DataFrame(dataListF1S, columns=['answer','f1', 'safetiness','assignement'])
        dfF1U = pd.DataFrame(dataListF1U, columns=['answer','f1', 'safetiness','assignement'])

        
        fig.add_subplot(rows, columns, 1)
        sns.pointplot(
            data=dfF1S, x="answer", y="f1", hue="assignement", 
            capsize=.01, errorbar="sd",
            palette=sns.color_palette([ '#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d','#91918c','#329da8'])).set(title='F1 Score for StarWars with safe repair')
        plt.title('F1 Score for StarWars with safe repair', fontsize=25)
        
        plt.xlabel("Answer", fontsize=25)
        plt.ylabel("F1", fontsize=25)        
        plt.yticks(fontsize=15)
        plt.xticks(fontsize=15) 
        
        # sns.pointplot(
        #     data=dfF1U, x="answer", y="f1", hue="assignement", 
        #     capsize=.01, errorbar="sd",
        #     palette=sns.color_palette([ '#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d','#91918c','#329da8'])).set(title='F1 Score for StarWars with unsafe repair')
        # plt.legend(loc="upper center",bbox_to_anchor=(.5, -0.1), ncol=3, title=None, frameon=True)
        # plt.title('F1 Score for StarWars with unsafe repair', fontsize=25)
        # plt.margins(x=0)
        # plt.margins(y=0)
        # plt.xlabel("Answer", fontsize=25)
        # plt.ylabel("F1", fontsize=25)        
        # plt.yticks(fontsize=15)
        # plt.xticks(fontsize=15) 
        
plt.legend(loc="upper center",bbox_to_anchor=(2.85, -0.1), fontsize="25",ncol=7, title=None, frameon=True)
plt.savefig("plots/quality/comparison.png",bbox_inches='tight')