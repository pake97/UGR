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
index=1
directory = os.getcwd()

for filename in os.listdir(directory):
    
    if filename.endswith(".json") and "Wwc19Output" in filename and "random" not in filename:        
    
        f = open(filename, "r")
        
        
        f1PreferredDeleteS = [
      0.005157962604771116, 0.008037508372404556, 0.006049606775559589,
      0.006972690296339337, 0.006277463904582549, 0.005509641873278237,
      0.008130081300813009, 0.008484848484848484, 0.005594405594405594,
      0.005287508261731659
    ]
        f1PreferredUpdateS = [
      0.5869311551925321, 0.6263672999424295, 0.8954183266932271,
      0.07248520710059171, 0.29295426452410384, 0.16421895861148197,
      0.897308075772682, 0.12364130434782608, 0.6896180742334589,
      0.12756909992912827
    ]
        
        f1PreferredNumberS = [
      0.0048543689320388345, 0.00804289544235925, 0.0060716454159077116,
      0.006976744186046511, 0.006246096189881324, 0.005513439007580979,
      0.008135593220338983, 0.008489993935718618, 0.005714285714285715,
      0.005312084993359894
    ]
        f1PreferredSchemaS = [
      0.16416938110749185, 0.869248291571754, 0.1087248322147651,
      0.18793650793650793, 0.7058237929318069, 0.6204039357845675,
      0.8796680497925311, 0.6349367088607596, 0.643714136671883,
      0.895482728077945
    ]
        f1PreferredSchemaU = [
      0.2874141876430206, 0.17877679038159958, 0.3275109170305677,
      0.37099316868102994, 0.3390065995137201, 0.5441783649876136,
      0.2512333965844402, 0.3650793650793651, 0.3271130625686059,
      0.3818090954522739
    ]
   
        f1PreferredDeleteU =  [
      0.005003126954346467, 0.007787151200519143, 0.005896226415094338,
      0.007259528130671506, 0.006093845216331505, 0.005215123859191656,
      0.007874015748031496, 0.008244994110718492, 0.005521048999309868,
      0.005144694533762058
    ]
        f1PreferredUpdateU = [
      0.4047856430707876, 0.2392604676454595, 0.17780661907852044,
      0.31678486997635935, 0.5895691609977324, 0.3900497512437811,
      0.5236768802228412, 0.39143426294820716, 0.25375, 0.22886716503737778
    ]
        f1PreferredNumberU =[
      0.005085823267641449, 0.008264462809917356, 0.006093845216331506,
      0.007915567282321899, 0.00649772579597141, 0.005333333333333334,
      0.007766990291262135, 0.008454106280193238, 0.005759539236861051,
      0.005263157894736842
    ]

        dataListF1S0 = []
        dataListF1S025 = []
        dataListF1S05 = []
        dataListF1S075 = []
        dataListF1S1 = []
        dataListF1U0 = []
        dataListF1U025 = []
        dataListF1U05 = []
        dataListF1U075 = []
        dataListF1U1 = []
        
        data = json.load(f) 
        
        for exp in data:
            if(exp['assignement'] == 'random'):
                waitings = exp['f1']
                if(exp['safetiness'] == 'True'):
                    if(exp['answer'] == '0'):
                        for w in waitings:
                            dataListF1S0.append(w)
                    if(exp['answer'] == '0.25'):
                        for w in waitings:
                            dataListF1S025.append(w)
                    if(exp['answer'] == '0.5'):
                        for w in waitings:
                            dataListF1S05.append(w)
                    if(exp['answer'] == '0.75'):
                        for w in waitings:
                            dataListF1S075.append(w)
                    if(exp['answer'] == '1'):
                        for w in waitings:
                            dataListF1S1.append(w)
                else:
                    if(exp['answer'] == '0'):
                        for w in waitings:
                            dataListF1U0.append(w)
                    if(exp['answer'] == '0.25'):
                        for w in waitings:
                            dataListF1U025.append(w)
                    if(exp['answer'] == '0.5'):
                        for w in waitings:
                            dataListF1U05.append(w)
                    if(exp['answer'] == '0.75'):
                        for w in waitings:
                            dataListF1U075.append(w)
                    if(exp['answer'] == '1'):
                        for w in waitings:
                            dataListF1U1.append(w)
        f.close()
            
        fig.add_subplot(rows, columns, 3)        
        x=[0,0.25,0.5,0.75,1]
        colors=['#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d']
        plt.plot(x,[np.mean(dataListF1S0),np.mean(dataListF1S025),np.mean(dataListF1S05),np.mean(dataListF1S075),np.mean(dataListF1S1)],label='cQAR-safe',color=colors[0], marker='o', linewidth=3)
        plt.plot(x,[np.mean(f1PreferredDeleteS),np.mean(f1PreferredDeleteS),np.mean(f1PreferredDeleteS),np.mean(f1PreferredDeleteS),np.mean(f1PreferredDeleteS)],label='D-pref-safe',color=colors[1], marker='o', linewidth=3)
        plt.plot(x,[np.mean(f1PreferredUpdateS),np.mean(f1PreferredUpdateS),np.mean(f1PreferredUpdateS),np.mean(f1PreferredUpdateS),np.mean(f1PreferredUpdateS)],label='U-pref-safe',color=colors[2], marker='o', linewidth=3)
        plt.plot(x,[np.mean(f1PreferredNumberS),np.mean(f1PreferredNumberS),np.mean(f1PreferredNumberS),np.mean(f1PreferredNumberS),np.mean(f1PreferredNumberS)],label='N-pref-safe',color=colors[3], marker='o', linewidth=3)
        plt.plot(x,[np.mean(f1PreferredSchemaS),np.mean(f1PreferredSchemaS),np.mean(f1PreferredSchemaS),np.mean(f1PreferredSchemaS),np.mean(f1PreferredSchemaS)],label='L-pref-safe',color=colors[4], marker='o', linewidth=3)
        plt.title('F1 Score for Wwc19 with safe repair', fontsize=25)
        plt.margins(x=0)
        plt.margins(y=0)
        plt.xlabel("Answer", fontsize=25)
        plt.ylabel("F1", fontsize=25)        
        plt.yticks(fontsize=15)
        plt.xticks(fontsize=15)    
        
        # plt.plot(x,[np.mean(dataListF1U0),np.mean(dataListF1U025),np.mean(dataListF1U05),np.mean(dataListF1U075),np.mean(dataListF1U1)],label='cQAR-unsafe',color=colors[0], marker='o', linewidth=3)
        # plt.plot(x,[np.mean(f1PreferredDeleteU),np.mean(f1PreferredDeleteU),np.mean(f1PreferredDeleteU),np.mean(f1PreferredDeleteU),np.mean(f1PreferredDeleteU)],label='D-pref-unsafe',color=colors[1], marker='o', linewidth=3)
        # plt.plot(x,[np.mean(f1PreferredUpdateU),np.mean(f1PreferredUpdateU),np.mean(f1PreferredUpdateU),np.mean(f1PreferredUpdateU),np.mean(f1PreferredUpdateU)],label='U-pref-unsafe',color=colors[2], marker='o', linewidth=3)
        # plt.plot(x,[np.mean(f1PreferredNumberU),np.mean(f1PreferredNumberU),np.mean(f1PreferredNumberU),np.mean(f1PreferredNumberU),np.mean(f1PreferredNumberU)],label='N-pref-unsafe',color=colors[3], marker='o', linewidth=3)
        # plt.plot(x,[np.mean(f1PreferredSchemaU),np.mean(f1PreferredSchemaU),np.mean(f1PreferredSchemaU),np.mean(f1PreferredSchemaU),np.mean(f1PreferredSchemaU)],label='L-pref-unsafe',color=colors[4], marker='o', linewidth=3)
        # plt.title('F1 Score for Wwc19 with unsafe repair', fontsize=25)
        # plt.margins(x=0)
        # plt.margins(y=0)
        # plt.xlabel("Answer", fontsize=25)
        # plt.ylabel("F1", fontsize=25)        
        # plt.yticks(fontsize=15)
        # plt.xticks(fontsize=15)    

        index+=1


directory = os.getcwd()

for filename in os.listdir(directory):
    if filename.endswith(".json") and "StackOutput" in filename:        
    
        f = open(filename, "r")
        
        
        f1PreferredDeleteS = [
      0.0017921146953405018, 0.00196078431372549, 0.0019550342130987292,
      0.0018501387604070304, 0, 0.001956947162426615, 0, 0.0017391304347826085,
      0, 0.0018993352326685659
    ]
        f1PreferredUpdateS =  [
      0.2087604846225536, 0.25547445255474455, 0.2170686456400742,
      0.2310536044362292, 0.9937040923399789, 0.27289048473967686,
      0.9841605068637803, 0.9863013698630136, 0.29359430604982206,
      0.22181146025878004
    ]
     
        f1PreferredNumberS = [
      0.0017921146953405018, 0.00196078431372549, 0.0019550342130987292,
      0.0018501387604070304, 0, 0.001956947162426615, 0, 0.0017391304347826085,
      0, 0.0018993352326685659
    ]

        f1PreferredDeleteU = [
      0.0017921146953405018, 0.00196078431372549, 0.0019550342130987292,
      0.0018501387604070304, 0, 0.001956947162426615, 0, 0.0017391304347826085,
      0, 0.0018993352326685659
    ]
        f1PreferredUpdateU = [
      0.20289855072463767, 0.25724637681159424, 0.21389396709323583,
      0.23084025854108955, 0.3795130142737196, 0.2635658914728682,
      0.38143459915611816, 0.4542536115569823, 0.3248299319727891,
      0.2137809187279152
    ]
      
        f1PreferredNumberU = [
      0.0006369426751592356, 0.0006261740763932373, 0.0006385696040868455,
      0.0006195786864931846, 0, 0.0006389776357827475, 0, 0.0006293266205160479,
      0, 0.0006261740763932373
    ]
        
        f1PreferredSchemaS = [
      0.20837209302325582, 0.2581818181818182, 0.21666666666666665,
      0.23062730627306272, 0.9937106918238994, 0.2754919499105546,
      0.9841772151898734, 0.9863301787592008, 0.2978723404255319,
      0.2246777163904236
    ]
        f1PreferredSchemaU = [
      0.20456621004566206, 0.2449355432780847, 0.21566820276497697,
      0.23277467411545621, 0.3840947546531303, 0.25196850393700787,
      0.38605442176870747, 0.4462540716612378, 0.3160621761658031,
      0.20107719928186712
    ]
        dataListF1S0 = []
        dataListF1S025 = []
        dataListF1S05 = []
        dataListF1S075 = []
        dataListF1S1 = []
        dataListF1U0 = []
        dataListF1U025 = []
        dataListF1U05 = []
        dataListF1U075 = []
        dataListF1U1 = []
        
        data = json.load(f) 
        
        for exp in data:
            if(exp['assignement'] == 'random'):
                waitings = exp['f1']
                if(exp['safetiness'] == 'True'):
                    if(exp['answer'] == '0'):
                        for w in waitings:
                            dataListF1S0.append(w)
                    if(exp['answer'] == '0.25'):
                        for w in waitings:
                            dataListF1S025.append(w)
                    if(exp['answer'] == '0.5'):
                        for w in waitings:
                            dataListF1S05.append(w)
                    if(exp['answer'] == '0.75'):
                        for w in waitings:
                            dataListF1S075.append(w)
                    if(exp['answer'] == '1'):
                        for w in waitings:
                            dataListF1S1.append(w)
                else:
                    if(exp['answer'] == '0'):
                        for w in waitings:
                            dataListF1U0.append(w)
                    if(exp['answer'] == '0.25'):
                        for w in waitings:
                            dataListF1U025.append(w)
                    if(exp['answer'] == '0.5'):
                        for w in waitings:
                            dataListF1U05.append(w)
                    if(exp['answer'] == '0.75'):
                        for w in waitings:
                            dataListF1U075.append(w)
                    if(exp['answer'] == '1'):
                        for w in waitings:
                            dataListF1U1.append(w)
        f.close()
            
        fig.add_subplot(rows, columns, 2)                
        x=[0,0.25,0.5,0.75,1]
        colors=['#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d']
        plt.plot(x,[np.mean(dataListF1S0),np.mean(dataListF1S025),np.mean(dataListF1S05),np.mean(dataListF1S075),np.mean(dataListF1S1)],label='cQAR-safe',color=colors[0], marker='o', linewidth=3)
        plt.plot(x,[np.mean(f1PreferredDeleteS),np.mean(f1PreferredDeleteS),np.mean(f1PreferredDeleteS),np.mean(f1PreferredDeleteS),np.mean(f1PreferredDeleteS)],label='D-pref-safe',color=colors[1], marker='o', linewidth=3)
        plt.plot(x,[np.mean(f1PreferredUpdateS),np.mean(f1PreferredUpdateS),np.mean(f1PreferredUpdateS),np.mean(f1PreferredUpdateS),np.mean(f1PreferredUpdateS)],label='U-pref-safe',color=colors[2], marker='o', linewidth=3)
        plt.plot(x,[np.mean(f1PreferredNumberS),np.mean(f1PreferredNumberS),np.mean(f1PreferredNumberS),np.mean(f1PreferredNumberS),np.mean(f1PreferredNumberS)],label='N-pref-safe',color=colors[3], marker='o', linewidth=3)
        plt.plot(x,[np.mean(f1PreferredSchemaS),np.mean(f1PreferredSchemaS),np.mean(f1PreferredSchemaS),np.mean(f1PreferredSchemaS),np.mean(f1PreferredSchemaS)],label='L-pref-safe',color=colors[4], marker='o', linewidth=3)
        plt.title('F1 Score for Stackoverflow with safe repair', fontsize=25)
        plt.margins(x=0)
        plt.margins(y=0)
        plt.xlabel("Answer", fontsize=25)
        plt.ylabel("F1", fontsize=25)        
        plt.yticks(fontsize=15)
        plt.xticks(fontsize=15)    
        
        
        
        # plt.plot(x,[np.mean(dataListF1U0),np.mean(dataListF1U025),np.mean(dataListF1U05),np.mean(dataListF1U075),np.mean(dataListF1U1)],label='cQAR-unsafe',color=colors[0], marker='o', linewidth=3)
        # plt.plot(x,[np.mean(f1PreferredDeleteU),np.mean(f1PreferredDeleteU),np.mean(f1PreferredDeleteU),np.mean(f1PreferredDeleteU),np.mean(f1PreferredDeleteU)],label='D-pref-unsafe',color=colors[1], marker='o', linewidth=3)
        # plt.plot(x,[np.mean(f1PreferredUpdateU),np.mean(f1PreferredUpdateU),np.mean(f1PreferredUpdateU),np.mean(f1PreferredUpdateU),np.mean(f1PreferredUpdateU)],label='U-pref-unsafe',color=colors[2], marker='o', linewidth=3)
        # plt.plot(x,[np.mean(f1PreferredNumberU),np.mean(f1PreferredNumberU),np.mean(f1PreferredNumberU),np.mean(f1PreferredNumberU),np.mean(f1PreferredNumberU)],label='N-pref-unsafe',color=colors[3], marker='o', linewidth=3)
        # plt.plot(x,[np.mean(f1PreferredSchemaU),np.mean(f1PreferredSchemaU),np.mean(f1PreferredSchemaU),np.mean(f1PreferredSchemaU),np.mean(f1PreferredSchemaU)],label='L-pref-unsafe',color=colors[4], marker='o', linewidth=3)
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
        
        
        f1PreferredDeleteS = [
      0.0006369426751592356, 0.0006402048655569781, 0.0006319115323854661,
      0.000630715862503942, 0, 0.0006383657835939993, 0, 0.0006317119393556539,
      0, 0.0006248047485160887
    ]
        f1PreferredUpdateS =  [
      0.4217573221757322, 0.4236343366778149, 0.5675949367088607,
      0.6101694915254238, 0.5943536404160477, 0.48122317596566533,
      0.6942909760589319, 0.469316031359827, 0.6190128859713105,
      0.5304957176226317
    ]
       
        f1PreferredNumberS =  [
      0.0006369426751592356, 0.0006261740763932373, 0.0006385696040868455,
      0.0006195786864931846, 0, 0.0006389776357827475, 0, 0.0006293266205160479,
      0, 0.0006261740763932373
    ]


        f1PreferredDeleteU = [
      0.000643707756678468, 0.0006408202499198974, 0.0006323110970597534,
      0.0006321112515802781, 0, 0.0006414368184733803, 0, 0.0006303183107469273,
      0, 0.0006339144215530902
    ]
        f1PreferredUpdateU = [
      0.5387396694214877, 0.3886039886039886, 0.5907845579078457,
      0.5918367346938775, 0.5995558845299779, 0.5622143219908583,
      0.6836853098166628, 0.5485772878749039, 0.6315028901734104,
      0.5673076923076923
    ]
        f1PreferredNumberU = [
      0.000634517766497462, 0.0006447453255963894, 0.0006251953735542357,
      0.0006222775357809583, 0, 0.0006422607578676943, 0, 0.0006339144215530902,
      0, 0.0006347191367819739
    ]
        
        f1PreferredSchemaS = [
      0.42825361512791993, 0.40755355129650506, 0.46953696181965876,
      0.6221355436372501, 0.6130456105934282, 0.4721772015126959,
      0.6676096181046676, 0.45633187772925765, 0.6296924194720271,
      0.4435883324160705
    ]
        f1PreferredSchemaU = [
      0.41580274586718974, 0.35122520420070014, 0.5952795031055901,
      0.6342995169082126, 0.6438159156279961, 0.5488586817132598,
      0.702020202020202, 0.6402307137707282, 0.6348287506029908,
      0.465002712967987
    ]
     
        dataListF1S0 = []
        dataListF1S025 = []
        dataListF1S05 = []
        dataListF1S075 = []
        dataListF1S1 = []
        dataListF1U0 = []
        dataListF1U025 = []
        dataListF1U05 = []
        dataListF1U075 = []
        dataListF1U1 = []
        
        data = json.load(f) 
        
        for exp in data:
            if(exp['assignement'] == 'random'):
                waitings = exp['f1']
                if(exp['safetiness'] == 'True'):
                    if(exp['answer'] == '0'):
                        for w in waitings:
                            dataListF1S0.append(w)
                    if(exp['answer'] == '0.25'):
                        for w in waitings:
                            dataListF1S025.append(w)
                    if(exp['answer'] == '0.5'):
                        for w in waitings:
                            dataListF1S05.append(w)
                    if(exp['answer'] == '0.75'):
                        for w in waitings:
                            dataListF1S075.append(w)
                    if(exp['answer'] == '1'):
                        for w in waitings:
                            dataListF1S1.append(w)
                else:
                    if(exp['answer'] == '0'):
                        for w in waitings:
                            dataListF1U0.append(w)
                    if(exp['answer'] == '0.25'):
                        for w in waitings:
                            dataListF1U025.append(w)
                    if(exp['answer'] == '0.5'):
                        for w in waitings:
                            dataListF1U05.append(w)
                    if(exp['answer'] == '0.75'):
                        for w in waitings:
                            dataListF1U075.append(w)
                    if(exp['answer'] == '1'):
                        for w in waitings:
                            dataListF1U1.append(w)
        f.close()
            
        fig.add_subplot(rows, columns, 4)       
        x=[0,0.25,0.5,0.75,1]
        colors=['#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d']
        plt.plot(x,[np.mean(dataListF1S0),np.mean(dataListF1S025),np.mean(dataListF1S05),np.mean(dataListF1S075),np.mean(dataListF1S1)],label='cQAR-safe',color=colors[0], marker='o', linewidth=3)
        plt.plot(x,[np.mean(f1PreferredDeleteS),np.mean(f1PreferredDeleteS),np.mean(f1PreferredDeleteS),np.mean(f1PreferredDeleteS),np.mean(f1PreferredDeleteS)],label='D-pref-safe',color=colors[1], marker='o', linewidth=3)
        plt.plot(x,[np.mean(f1PreferredUpdateS),np.mean(f1PreferredUpdateS),np.mean(f1PreferredUpdateS),np.mean(f1PreferredUpdateS),np.mean(f1PreferredUpdateS)],label='U-pref-safe',color=colors[2], marker='o', linewidth=3)
        plt.plot(x,[np.mean(f1PreferredNumberS),np.mean(f1PreferredNumberS),np.mean(f1PreferredNumberS),np.mean(f1PreferredNumberS),np.mean(f1PreferredNumberS)],label='N-pref-safe',color=colors[3], marker='o', linewidth=3)
        plt.plot(x,[np.mean(f1PreferredSchemaS),np.mean(f1PreferredSchemaS),np.mean(f1PreferredSchemaS),np.mean(f1PreferredSchemaS),np.mean(f1PreferredSchemaS)],label='L-pref-safe',color=colors[4], marker='o', linewidth=3)
        plt.title('F1 Score for Synthea with safe repair', fontsize=25)
        plt.margins(x=0)
        plt.margins(y=0)
        plt.xlabel("Answer", fontsize=25)
        plt.ylabel("F1", fontsize=25)        
        plt.yticks(fontsize=15)
        plt.xticks(fontsize=15)    
        
        # fig2.add_subplot(rows, columns, index)        
        # x=[0,0.25,0.5,0.75,1]
        # colors=['#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d']
        # plt.plot(x,[np.mean(dataListF1U0),np.mean(dataListF1U025),np.mean(dataListF1U05),np.mean(dataListF1U075),np.mean(dataListF1U1)],label='cQAR-unsafe',color=colors[0], marker='o', linewidth=3)
        # plt.plot(x,[np.mean(f1PreferredDeleteU),np.mean(f1PreferredDeleteU),np.mean(f1PreferredDeleteU),np.mean(f1PreferredDeleteU),np.mean(f1PreferredDeleteU)],label='D-pref-unsafe',color=colors[1], marker='o', linewidth=3)
        # plt.plot(x,[np.mean(f1PreferredUpdateU),np.mean(f1PreferredUpdateU),np.mean(f1PreferredUpdateU),np.mean(f1PreferredUpdateU),np.mean(f1PreferredUpdateU)],label='U-pref-unsafe',color=colors[2], marker='o', linewidth=3)
        # plt.plot(x,[np.mean(f1PreferredNumberU),np.mean(f1PreferredNumberU),np.mean(f1PreferredNumberU),np.mean(f1PreferredNumberU),np.mean(f1PreferredNumberU)],label='N-pref-unsafe',color=colors[3], marker='o', linewidth=3)
        # plt.plot(x,[np.mean(f1PreferredSchemaU),np.mean(f1PreferredSchemaU),np.mean(f1PreferredSchemaU),np.mean(f1PreferredSchemaU),np.mean(f1PreferredSchemaU)],label='L-pref-unsafe',color=colors[4], marker='o', linewidth=3)
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
        
        
        f1PreferredDeleteS = [
      0.37882892269222757, 0.35253549695740366, 0.2835913312693499,
      0.36787669843845067, 0.3407682775712515, 0.3176285826462505,
      0.36619718309859156, 0.3624322697170379, 0.4009168576786831,
      0.31239259117815543
    ]
        f1PreferredUpdateS = [
      0.6203835790141068, 0.5046424499104089, 0.24492834543085798,
      0.3128784159711995, 0.6427152317880795, 0.5203448797458781,
      0.6065265675721851, 0.6522797338958299, 0.6753841124550507,
      0.5325328573746552
    ]
       
        f1PreferredNumberS =[
      0.3411332430864436, 0.377992440151197, 0.26354627872654435,
      0.3872039883672621, 0.40211873758552197, 0.30295810998610284,
      0.3750255049989798, 0.3884449907805778, 0.3952022768855459,
      0.2671621357324467
    ]

        f1PreferredDeleteU = [
      0.3723747980613893, 0.3201522520617467, 0.2653696498054474,
      0.37288135593220334, 0.4024127531236536, 0.2819646052893219,
      0.297104323681079, 0.3818913480885312, 0.41433752933646256,
      0.37175792507204614
    ]
        f1PreferredUpdateU = [
      0.20289855072463767, 0.25724637681159424, 0.21389396709323583,
      0.23084025854108955, 0.3795130142737196, 0.2635658914728682,
      0.38143459915611816, 0.4542536115569823, 0.3248299319727891,
      0.2137809187279152
    ]
        f1PreferredNumberU =[
      0.3766101001840115, 0.33340439138776384, 0.3667359667359667,
      0.3782246597603088, 0.39430724152365004, 0.2845468053491828,
      0.3962425277540564, 0.3838509316770186, 0.4580152671755725,
      0.3627714581178904
    ]
        
        f1PreferredSchemaS =  [
      0.6893926857521098, 0.8110821866865006, 0.8113242689513875,
      0.7727489280609813, 0.8110821866865006, 0.8147375738616613,
      0.8856724074752655, 0.7836298932384341, 0.81496953872933,
      0.8860482103725346
    ]
        f1PreferredSchemaU = [
      0.9225137278828553, 0.8980971011915349, 0.8874551971326167,
      0.7711565585331452, 0.8980971011915349, 0.8882110174053471,
      0.9225137278828553, 0.9225137278828553, 0.7453040432983126,
      0.9225137278828553
    ]
        dataListF1S0 = []
        dataListF1S025 = []
        dataListF1S05 = []
        dataListF1S075 = []
        dataListF1S1 = []
        dataListF1U0 = []
        dataListF1U025 = []
        dataListF1U05 = []
        dataListF1U075 = []
        dataListF1U1 = []
        
        data = json.load(f) 
        
        for exp in data:
            if(exp['assignement'] == 'random'):
                waitings = exp['f1']
                if(exp['safetiness'] == 'True'):
                    if(exp['answer'] == '0'):
                        for w in waitings:
                            dataListF1S0.append(w)
                    if(exp['answer'] == '0.25'):
                        for w in waitings:
                            dataListF1S025.append(w)
                    if(exp['answer'] == '0.5'):
                        for w in waitings:
                            dataListF1S05.append(w)
                    if(exp['answer'] == '0.75'):
                        for w in waitings:
                            dataListF1S075.append(w)
                    if(exp['answer'] == '1'):
                        for w in waitings:
                            dataListF1S1.append(w)
                else:
                    if(exp['answer'] == '0'):
                        for w in waitings:
                            dataListF1U0.append(w)
                    if(exp['answer'] == '0.25'):
                        for w in waitings:
                            dataListF1U025.append(w)
                    if(exp['answer'] == '0.5'):
                        for w in waitings:
                            dataListF1U05.append(w)
                    if(exp['answer'] == '0.75'):
                        for w in waitings:
                            dataListF1U075.append(w)
                    if(exp['answer'] == '1'):
                        for w in waitings:
                            dataListF1U1.append(w)
        f.close()
            
        fig.add_subplot(rows, columns, 5)        
        x=[0,0.25,0.5,0.75,1]
        colors=['#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d']
        plt.plot(x,[np.mean(dataListF1S0),np.mean(dataListF1S025),np.mean(dataListF1S05),np.mean(dataListF1S075),np.mean(dataListF1S1)],label='cQAR-safe',color=colors[0], marker='o', linewidth=3)
        plt.plot(x,[np.mean(f1PreferredDeleteS),np.mean(f1PreferredDeleteS),np.mean(f1PreferredDeleteS),np.mean(f1PreferredDeleteS),np.mean(f1PreferredDeleteS)],label='D-pref-safe',color=colors[1], marker='o', linewidth=3)
        plt.plot(x,[np.mean(f1PreferredUpdateS),np.mean(f1PreferredUpdateS),np.mean(f1PreferredUpdateS),np.mean(f1PreferredUpdateS),np.mean(f1PreferredUpdateS)],label='U-pref-safe',color=colors[2], marker='o', linewidth=3)
        plt.plot(x,[np.mean(f1PreferredNumberS),np.mean(f1PreferredNumberS),np.mean(f1PreferredNumberS),np.mean(f1PreferredNumberS),np.mean(f1PreferredNumberS)],label='N-pref-safe',color=colors[3], marker='o', linewidth=3)
        plt.plot(x,[np.mean(f1PreferredSchemaS),np.mean(f1PreferredSchemaS),np.mean(f1PreferredSchemaS),np.mean(f1PreferredSchemaS),np.mean(f1PreferredSchemaS)],label='L-pref-safe',color=colors[4], marker='o', linewidth=3)
        plt.title('F1 Score for Fincen with safe repair', fontsize=25)
        plt.margins(x=0)
        plt.margins(y=0)
        plt.ylim(0,1)
        plt.xlabel("Answer", fontsize=25)
        plt.ylabel("F1", fontsize=25)        
        plt.yticks(fontsize=15)
        plt.xticks(fontsize=15)    
        
        # fig2.add_subplot(rows, columns, index)        
        # x=[0,0.25,0.5,0.75,1]
        # colors=['#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d']
        # plt.plot(x,[np.mean(dataListF1U0),np.mean(dataListF1U025),np.mean(dataListF1U05),np.mean(dataListF1U075),np.mean(dataListF1U1)],label='cQAR-unsafe',color=colors[0], marker='o', linewidth=3)
        # plt.plot(x,[np.mean(f1PreferredDeleteU),np.mean(f1PreferredDeleteU),np.mean(f1PreferredDeleteU),np.mean(f1PreferredDeleteU),np.mean(f1PreferredDeleteU)],label='D-pref-unsafe',color=colors[1], marker='o', linewidth=3)
        # plt.plot(x,[np.mean(f1PreferredUpdateU),np.mean(f1PreferredUpdateU),np.mean(f1PreferredUpdateU),np.mean(f1PreferredUpdateU),np.mean(f1PreferredUpdateU)],label='U-pref-unsafe',color=colors[2], marker='o', linewidth=3)
        # plt.plot(x,[np.mean(f1PreferredNumberU),np.mean(f1PreferredNumberU),np.mean(f1PreferredNumberU),np.mean(f1PreferredNumberU),np.mean(f1PreferredNumberU)],label='N-pref-unsafe',color=colors[3], marker='o', linewidth=3)
        # plt.plot(x,[np.mean(f1PreferredSchemaU),np.mean(f1PreferredSchemaU),np.mean(f1PreferredSchemaU),np.mean(f1PreferredSchemaU),np.mean(f1PreferredSchemaU)],label='L-pref-unsafe',color=colors[4], marker='o', linewidth=3)
        # plt.title('F1 Score for Fincen with unsafe repair', fontsize=25)
        # plt.margins(x=0)
        # plt.margins(y=0)
        # plt.ylim(0,1)
        # plt.xlabel("Answer", fontsize=25)
        # plt.ylabel("F1", fontsize=25)        
        # plt.yticks(fontsize=15)
        # plt.xticks(fontsize=15)    

        index+=1


directory = os.getcwd()

for filename in os.listdir(directory):
    if filename.endswith(".json") and "SWOutput" in filename:        
    
        f = open(filename, "r")
        
        
        f1PreferredDeleteS = [
      0.025, 0.03550295857988166, 0.023529411764705885, 0.02484472049689441,
      0.012903225806451611, 0.011976047904191617, 0.011764705882352943,
      0.01234567901234568, 0, 0.011695906432748539
    ]
        f1PreferredUpdateS = [
      0.6368159203980099, 0.28717948717948716, 0.3431372549019608,
      0.15384615384615383, 0.3888888888888889, 0.6842105263157894,
      0.811965811965812, 0.8095238095238095, 0.6782608695652173,
      0.6666666666666667
    ]
     
        f1PreferredNumberS =[
      0.025, 0.03550295857988166, 0.023529411764705885, 0.024539877300613494,
      0.012903225806451611, 0.012121212121212121, 0.011764705882352943,
      0.01234567901234568, 0, 0.011834319526627219
    ]

        f1PreferredDeleteU = [
      0.023391812865497078, 0.037267080745341616, 0.02469135802469136,
      0.02484472049689441, 0.012903225806451611, 0.011976047904191617,
      0.012195121951219513, 0.01234567901234568, 0, 0.011695906432748539
    ]
        f1PreferredUpdateU = [
      0.6368159203980099, 0.16410256410256407, 0.8227848101265822,
      0.8275862068965517, 0.7728813559322034, 0.7188940092165897,
      0.7755102040816327, 0.8319327731092436, 0.6782608695652173,
      0.7009345794392522
    ]
        
        f1PreferredNumberU=[
      0.025, 0.03680981595092024, 0.023529411764705885, 0.02484472049689441,
      0.012903225806451611, 0.011976047904191617, 0.012195121951219513,
      0.01234567901234568, 0, 0.011695906432748539
    ]
        f1PreferredSchemaS = [
      0.6499999999999999, 0.28717948717948716, 0.35467980295566504,
      0.17486338797814208, 0.4784688995215311, 0.7441860465116279,
      0.8362068965517242, 0.8559322033898306, 0.75, 0.7264150943396227
    ]
        f1PreferredSchemaU =  [
      0.6499999999999999, 0.16410256410256407, 0.828752642706131,
      0.8322368421052633, 0.8226950354609929, 0.7441860465116279,
      0.8362068965517242, 0.8559322033898306, 0.75, 0.7264150943396227
    ]
        
        dataListF1S0 = []
        dataListF1S025 = []
        dataListF1S05 = []
        dataListF1S075 = []
        dataListF1S1 = []
        dataListF1U0 = []
        dataListF1U025 = []
        dataListF1U05 = []
        dataListF1U075 = []
        dataListF1U1 = []
        
        data = json.load(f) 
        
        for exp in data:
            if(exp['assignement'] == 'random'):
                waitings = exp['f1']
                if(exp['safetiness'] == 'True'):
                    if(exp['answer'] == '0'):
                        for w in waitings:
                            dataListF1S0.append(w)
                    if(exp['answer'] == '0.25'):
                        for w in waitings:
                            dataListF1S025.append(w)
                    if(exp['answer'] == '0.5'):
                        for w in waitings:
                            dataListF1S05.append(w)
                    if(exp['answer'] == '0.75'):
                        for w in waitings:
                            dataListF1S075.append(w)
                    if(exp['answer'] == '1'):
                        for w in waitings:
                            dataListF1S1.append(w)
                else:
                    if(exp['answer'] == '0'):
                        for w in waitings:
                            dataListF1U0.append(w)
                    if(exp['answer'] == '0.25'):
                        for w in waitings:
                            dataListF1U025.append(w)
                    if(exp['answer'] == '0.5'):
                        for w in waitings:
                            dataListF1U05.append(w)
                    if(exp['answer'] == '0.75'):
                        for w in waitings:
                            dataListF1U075.append(w)
                    if(exp['answer'] == '1'):
                        for w in waitings:
                            dataListF1U1.append(w)
        f.close()
            
        fig.add_subplot(rows, columns, 1)        
        x=[0,0.25,0.5,0.75,1]
        colors=['#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d']
        plt.plot(x,[np.mean(dataListF1S0),np.mean(dataListF1S025),np.mean(dataListF1S05),np.mean(dataListF1S075),np.mean(dataListF1S1)],label='cQAR-safe',color=colors[0], marker='o', linewidth=3)
        plt.plot(x,[np.mean(f1PreferredDeleteS),np.mean(f1PreferredDeleteS),np.mean(f1PreferredDeleteS),np.mean(f1PreferredDeleteS),np.mean(f1PreferredDeleteS)],label='D-pref-safe',color=colors[1], marker='o', linewidth=3)
        plt.plot(x,[np.mean(f1PreferredUpdateS),np.mean(f1PreferredUpdateS),np.mean(f1PreferredUpdateS),np.mean(f1PreferredUpdateS),np.mean(f1PreferredUpdateS)],label='U-pref-safe',color=colors[2], marker='o', linewidth=3)
        plt.plot(x,[np.mean(f1PreferredNumberS),np.mean(f1PreferredNumberS),np.mean(f1PreferredNumberS),np.mean(f1PreferredNumberS),np.mean(f1PreferredNumberS)],label='N-pref-safe',color=colors[3], marker='o', linewidth=3)
        plt.plot(x,[np.mean(f1PreferredSchemaS),np.mean(f1PreferredSchemaS),np.mean(f1PreferredSchemaS),np.mean(f1PreferredSchemaS),np.mean(f1PreferredSchemaS)],label='L-pref-safe',color=colors[4], marker='o', linewidth=3)
        plt.title('F1 Score for StarWars with safe repair', fontsize=25)
        plt.margins(x=0)
        plt.margins(y=0)
        plt.xlabel("Answer", fontsize=25)
        plt.ylabel("F1", fontsize=25)        
        plt.yticks(fontsize=15)
        plt.xticks(fontsize=15)    
        
        # fig2.add_subplot(rows, columns, index)        
        # x=[0,0.25,0.5,0.75,1]
        # colors=['#d48428', '#298360','#1469a5','#bb73ae','#e9dc2d']
        # plt.plot(x,[np.mean(dataListF1U0),np.mean(dataListF1U025),np.mean(dataListF1U05),np.mean(dataListF1U075),np.mean(dataListF1U1)],label='cQAR-unsafe',color=colors[0], marker='o', linewidth=3)
        # plt.plot(x,[np.mean(f1PreferredDeleteU),np.mean(f1PreferredDeleteU),np.mean(f1PreferredDeleteU),np.mean(f1PreferredDeleteU),np.mean(f1PreferredDeleteU)],label='D-pref-unsafe',color=colors[1], marker='o', linewidth=3)
        # plt.plot(x,[np.mean(f1PreferredUpdateU),np.mean(f1PreferredUpdateU),np.mean(f1PreferredUpdateU),np.mean(f1PreferredUpdateU),np.mean(f1PreferredUpdateU)],label='U-pref-unsafe',color=colors[2], marker='o', linewidth=3)
        # plt.plot(x,[np.mean(f1PreferredNumberU),np.mean(f1PreferredNumberU),np.mean(f1PreferredNumberU),np.mean(f1PreferredNumberU),np.mean(f1PreferredNumberU)],label='N-pref-unsafe',color=colors[3], marker='o', linewidth=3)
        # plt.plot(x,[np.mean(f1PreferredSchemaU),np.mean(f1PreferredSchemaU),np.mean(f1PreferredSchemaU),np.mean(f1PreferredSchemaU),np.mean(f1PreferredSchemaU)],label='L-pref-unsafe',color=colors[4], marker='o', linewidth=3)
        # plt.title('F1 Score for StarWars with unsafe repair', fontsize=25)
        # plt.margins(x=0)
        # plt.margins(y=0)
        # plt.xlabel("Answer", fontsize=25)
        # plt.ylabel("F1", fontsize=25)        
        # plt.yticks(fontsize=15)
        # plt.xticks(fontsize=15)    

        index+=1


plt.legend(loc="upper center",bbox_to_anchor=(2.9, -0.1), fontsize="25",ncol=5, title=None, frameon=True)
plt.savefig("plots/quality/quality.png",bbox_inches='tight')