import json
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import numpy as np
from scipy.stats import ranksums,kruskal
directory = os.getcwd()
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

for filename in os.listdir(directory):
    
    if filename.endswith(".json") and "Wwc19Quality" in filename and "random" not in filename:        
        print(filename)
        f = open(filename, "r")
        data = json.load(f) 
        
        
    
        
        
        for exp in data:
            
            f1 = exp['f1']
            if(exp['safetiness'] == 'True'):
                if(exp['answer'] == '0'):
                    dataListF1S0.append(f1)
                elif(exp['answer'] == '0.25'):
                    dataListF1S025.append(f1)
                elif(exp['answer'] == '0.5'):
                    dataListF1S05.append(f1)
                elif(exp['answer'] == '0.75'):
                    dataListF1S075.append(f1)
                elif(exp['answer'] == '1'):
                    dataListF1S1.append(f1)
            else:
                if(exp['answer'] == '0'):
                    dataListF1U0.append(f1)
                elif(exp['answer'] == '0.25'):
                    dataListF1U025.append(f1)
                elif(exp['answer'] == '0.5'):
                    dataListF1U05.append(f1)
                elif(exp['answer'] == '0.75'):
                    dataListF1U075.append(f1)
                elif(exp['answer'] == '1'):
                    dataListF1U1.append(f1)
                
        f.close()


# Assuming you have 7 arrays of 10 results each
# Replace these with your actual data

# Perform t-tests between each pair of arrays
print("S0")
alpha = 0.05
n_arrays = len(dataListF1S0)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S0[i], dataListF1S0[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S0)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S0[i], dataListF1S0[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:

    statistic, p_value = kruskal(*dataListF1U1)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("S025")
alpha = 0.05
n_arrays = len(dataListF1S025)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S025[i], dataListF1S025[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S025)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S025[i], dataListF1S025[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1S025)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("S05")
alpha = 0.05
n_arrays = len(dataListF1S05)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S05[i], dataListF1S05[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S05)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S05[i], dataListF1S05[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1S05)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("S075")
alpha = 0.05
n_arrays = len(dataListF1S075)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S075[i], dataListF1S075[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')

# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S075)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S075[i], dataListF1S075[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1S075)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("S1")
alpha = 0.05
n_arrays = len(dataListF1S1)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S1[i], dataListF1S1[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S1)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S1[i], dataListF1S1[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1S1)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("U0")
alpha = 0.05
n_arrays = len(dataListF1U0)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U0[i], dataListF1U0[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')

# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U0)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U0[i], dataListF1U0[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U0)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)


print("U025")
alpha = 0.05
n_arrays = len(dataListF1U025)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U025[i], dataListF1U025[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')

# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U025)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U025[i], dataListF1U025[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U025)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("U05")
alpha = 0.05
n_arrays = len(dataListF1U05)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U05[i], dataListF1U05[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U05)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U05[i], dataListF1U05[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U05)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("U075")
alpha = 0.05
n_arrays = len(dataListF1U075)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U075[i], dataListF1U075[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')

# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U075)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U075[i], dataListF1U075[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U075)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)


print("U1")
alpha = 0.05
n_arrays = len(dataListF1U1)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U1[i], dataListF1U1[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U1)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U1[i], dataListF1U1[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U1)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)


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


directory = os.getcwd()

for filename in os.listdir(directory):
    if filename.endswith(".json") and "StackQuality" in filename:        
        print(filename)
        f = open(filename, "r")
        data = json.load(f) 
    
        
        for exp in data:
            
            f1 = exp['f1']
            if(exp['safetiness'] == 'True'):
                if(exp['answer'] == '0'):
                    dataListF1S0.append(f1)
                elif(exp['answer'] == '0.25'):
                    dataListF1S025.append(f1)
                elif(exp['answer'] == '0.5'):
                    dataListF1S05.append(f1)
                elif(exp['answer'] == '0.75'):
                    dataListF1S075.append(f1)
                elif(exp['answer'] == '1'):
                    dataListF1S1.append(f1)
            else:
                if(exp['answer'] == '0'):
                    dataListF1U0.append(f1)
                elif(exp['answer'] == '0.25'):
                    dataListF1U025.append(f1)
                elif(exp['answer'] == '0.5'):
                    dataListF1U05.append(f1)
                elif(exp['answer'] == '0.75'):
                    dataListF1U075.append(f1)
                elif(exp['answer'] == '1'):
                    dataListF1U1.append(f1)
                
        f.close()

# Assuming you have 7 arrays of 10 results each
# Replace these with your actual data

# Perform t-tests between each pair of arrays
print("S0")
alpha = 0.05
n_arrays = len(dataListF1S0)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S0[i], dataListF1S0[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S0)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S0[i], dataListF1S0[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:

    statistic, p_value = kruskal(*dataListF1U1)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("S025")
alpha = 0.05
n_arrays = len(dataListF1S025)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S025[i], dataListF1S025[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S025)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S025[i], dataListF1S025[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1S025)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("S05")
alpha = 0.05
n_arrays = len(dataListF1S05)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S05[i], dataListF1S05[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S05)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S05[i], dataListF1S05[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1S05)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("S075")
alpha = 0.05
n_arrays = len(dataListF1S075)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S075[i], dataListF1S075[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')

# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S075)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S075[i], dataListF1S075[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1S075)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("S1")
alpha = 0.05
n_arrays = len(dataListF1S1)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S1[i], dataListF1S1[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S1)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S1[i], dataListF1S1[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1S1)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("U0")
alpha = 0.05
n_arrays = len(dataListF1U0)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U0[i], dataListF1U0[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')

# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U0)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U0[i], dataListF1U0[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U0)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)


print("U025")
alpha = 0.05
n_arrays = len(dataListF1U025)
p_values = np.zeros((n_arrays, n_arrays))

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         t_statistic, p_value = stats.ttest_ind(dataListF1U025[i], dataListF1U025[j])
#         p_values[i][j] = p_value

# # Apply Bonferroni correction
# bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# # Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')

# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U025)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U025[i], dataListF1U025[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U025)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("U05")
alpha = 0.05
n_arrays = len(dataListF1U05)
p_values = np.zeros((n_arrays, n_arrays))

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         t_statistic, p_value = stats.ttest_ind(dataListF1U05[i], dataListF1U05[j])
#         p_values[i][j] = p_value

# # Apply Bonferroni correction
# bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# # Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U05)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U05[i], dataListF1U05[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U05)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("U075")
alpha = 0.05
n_arrays = len(dataListF1U075)
p_values = np.zeros((n_arrays, n_arrays))

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         t_statistic, p_value = stats.ttest_ind(dataListF1U075[i], dataListF1U075[j])
#         p_values[i][j] = p_value

# # Apply Bonferroni correction
# bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# # Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')

# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U075)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U075[i], dataListF1U075[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U075)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)


print("U1")
alpha = 0.05
n_arrays = len(dataListF1U1)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U1[i], dataListF1U1[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U1)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U1[i], dataListF1U1[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U1)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

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


directory = os.getcwd()

for filename in os.listdir(directory):
    if filename.endswith(".json") and "SyntheaQuality" in filename:        
        print(filename)
        f = open(filename, "r")
        data = json.load(f) 
    
        
        for exp in data:
            
            f1 = exp['f1']
            if(exp['safetiness'] == 'True'):
                if(exp['answer'] == '0'):
                    dataListF1S0.append(f1)
                elif(exp['answer'] == '0.25'):
                    dataListF1S025.append(f1)
                elif(exp['answer'] == '0.5'):
                    dataListF1S05.append(f1)
                elif(exp['answer'] == '0.75'):
                    dataListF1S075.append(f1)
                elif(exp['answer'] == '1'):
                    dataListF1S1.append(f1)
            else:
                if(exp['answer'] == '0'):
                    dataListF1U0.append(f1)
                elif(exp['answer'] == '0.25'):
                    dataListF1U025.append(f1)
                elif(exp['answer'] == '0.5'):
                    dataListF1U05.append(f1)
                elif(exp['answer'] == '0.75'):
                    dataListF1U075.append(f1)
                elif(exp['answer'] == '1'):
                    dataListF1U1.append(f1)
                
        f.close()



# Assuming you have 7 arrays of 10 results each
# Replace these with your actual data

# Perform t-tests between each pair of arrays
print("S0")
alpha = 0.05
n_arrays = len(dataListF1S0)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S0[i], dataListF1S0[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S0)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S0[i], dataListF1S0[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:

    statistic, p_value = kruskal(*dataListF1U1)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("S025")
alpha = 0.05
n_arrays = len(dataListF1S025)
p_values = np.zeros((n_arrays, n_arrays))

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         t_statistic, p_value = stats.ttest_ind(dataListF1S025[i], dataListF1S025[j])
#         p_values[i][j] = p_value

# # Apply Bonferroni correction
# bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# # Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S025)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S025[i], dataListF1S025[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1S025)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("S05")
alpha = 0.05
n_arrays = len(dataListF1S05)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S05[i], dataListF1S05[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S05)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S05[i], dataListF1S05[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1S05)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("S075")
alpha = 0.05
n_arrays = len(dataListF1S075)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S075[i], dataListF1S075[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')

# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S075)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S075[i], dataListF1S075[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1S075)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("S1")
alpha = 0.05
n_arrays = len(dataListF1S1)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S1[i], dataListF1S1[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S1)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S1[i], dataListF1S1[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1S1)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("U0")
alpha = 0.05
n_arrays = len(dataListF1U0)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U0[i], dataListF1U0[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')

# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U0)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U0[i], dataListF1U0[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U0)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)


print("U025")
alpha = 0.05
n_arrays = len(dataListF1U025)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U025[i], dataListF1U025[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')

# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U025)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U025[i], dataListF1U025[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U025)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("U05")
alpha = 0.05
n_arrays = len(dataListF1U05)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U05[i], dataListF1U05[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U05)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U05[i], dataListF1U05[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U05)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("U075")
alpha = 0.05
n_arrays = len(dataListF1U075)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U075[i], dataListF1U075[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')

# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U075)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U075[i], dataListF1U075[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U075)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)


print("U1")
alpha = 0.05
n_arrays = len(dataListF1U1)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U1[i], dataListF1U1[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U1)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U1[i], dataListF1U1[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U1)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

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

directory = os.getcwd()

for filename in os.listdir(directory):
    if filename.endswith(".json") and "FincenQuality" in filename:        
        print(filename)
        f = open(filename, "r")
        data = json.load(f) 
    
        
        for exp in data:
            
            f1 = exp['f1']
            if(exp['safetiness'] == 'True'):
                if(exp['answer'] == '0'):
                    dataListF1S0.append(f1)
                elif(exp['answer'] == '0.25'):
                    dataListF1S025.append(f1)
                elif(exp['answer'] == '0.5'):
                    dataListF1S05.append(f1)
                elif(exp['answer'] == '0.75'):
                    dataListF1S075.append(f1)
                elif(exp['answer'] == '1'):
                    dataListF1S1.append(f1)
            else:
                if(exp['answer'] == '0'):
                    dataListF1U0.append(f1)
                elif(exp['answer'] == '0.25'):
                    dataListF1U025.append(f1)
                elif(exp['answer'] == '0.5'):
                    dataListF1U05.append(f1)
                elif(exp['answer'] == '0.75'):
                    dataListF1U075.append(f1)
                elif(exp['answer'] == '1'):
                    dataListF1U1.append(f1)
                
        f.close()

# Assuming you have 7 arrays of 10 results each
# Replace these with your actual data

# Perform t-tests between each pair of arrays
print("S0")
alpha = 0.05
n_arrays = len(dataListF1S0)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S0[i], dataListF1S0[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S0)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S0[i], dataListF1S0[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:

    statistic, p_value = kruskal(*dataListF1U1)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("S025")
alpha = 0.05
n_arrays = len(dataListF1S025)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S025[i], dataListF1S025[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S025)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S025[i], dataListF1S025[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1S025)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("S05")
alpha = 0.05
n_arrays = len(dataListF1S05)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S05[i], dataListF1S05[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S05)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S05[i], dataListF1S05[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1S05)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("S075")
alpha = 0.05
n_arrays = len(dataListF1S075)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S075[i], dataListF1S075[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')

# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S075)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S075[i], dataListF1S075[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1S075)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("S1")
alpha = 0.05
n_arrays = len(dataListF1S1)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S1[i], dataListF1S1[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S1)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S1[i], dataListF1S1[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1S1)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("U0")
alpha = 0.05
n_arrays = len(dataListF1U0)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U0[i], dataListF1U0[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')

# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U0)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U0[i], dataListF1U0[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U0)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)


print("U025")
alpha = 0.05
n_arrays = len(dataListF1U025)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U025[i], dataListF1U025[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')

# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U025)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U025[i], dataListF1U025[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U025)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("U05")
alpha = 0.05
n_arrays = len(dataListF1U05)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U05[i], dataListF1U05[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U05)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U05[i], dataListF1U05[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U05)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("U075")
alpha = 0.05
n_arrays = len(dataListF1U075)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U075[i], dataListF1U075[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')

# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U075)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U075[i], dataListF1U075[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U075)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)


print("U1")
alpha = 0.05
n_arrays = len(dataListF1U1)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U1[i], dataListF1U1[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U1)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U1[i], dataListF1U1[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U1)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

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

directory = os.getcwd()

for filename in os.listdir(directory):
    if filename.endswith(".json") and "SWQuality" in filename:        
        print(filename)
        f = open(filename, "r")
        data = json.load(f) 
    
        
        for exp in data:
            
            f1 = exp['f1']
            if(exp['safetiness'] == 'True'):
                if(exp['answer'] == '0'):
                    dataListF1S0.append(f1)
                elif(exp['answer'] == '0.25'):
                    dataListF1S025.append(f1)
                elif(exp['answer'] == '0.5'):
                    dataListF1S05.append(f1)
                elif(exp['answer'] == '0.75'):
                    dataListF1S075.append(f1)
                elif(exp['answer'] == '1'):
                    dataListF1S1.append(f1)
            else:
                if(exp['answer'] == '0'):
                    dataListF1U0.append(f1)
                elif(exp['answer'] == '0.25'):
                    dataListF1U025.append(f1)
                elif(exp['answer'] == '0.5'):
                    dataListF1U05.append(f1)
                elif(exp['answer'] == '0.75'):
                    dataListF1U075.append(f1)
                elif(exp['answer'] == '1'):
                    dataListF1U1.append(f1)
                
        f.close()


# Assuming you have 7 arrays of 10 results each
# Replace these with your actual data

# Perform t-tests between each pair of arrays
print("S0")
alpha = 0.05
n_arrays = len(dataListF1S0)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S0[i], dataListF1S0[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S0)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S0[i], dataListF1S0[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:

    statistic, p_value = kruskal(*dataListF1U1)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("S025")
alpha = 0.05
n_arrays = len(dataListF1S025)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S025[i], dataListF1S025[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S025)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S025[i], dataListF1S025[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1S025)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("S05")
alpha = 0.05
n_arrays = len(dataListF1S05)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S05[i], dataListF1S05[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S05)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S05[i], dataListF1S05[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1S05)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("S075")
alpha = 0.05
n_arrays = len(dataListF1S075)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S075[i], dataListF1S075[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')

# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S075)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S075[i], dataListF1S075[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1S075)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("S1")
alpha = 0.05
n_arrays = len(dataListF1S1)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1S1[i], dataListF1S1[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1S1)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1S1[i], dataListF1S1[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1S1)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("U0")
alpha = 0.05
n_arrays = len(dataListF1U0)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U0[i], dataListF1U0[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')

# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U0)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U0[i], dataListF1U0[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U0)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)


print("U025")
alpha = 0.05
n_arrays = len(dataListF1U025)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U025[i], dataListF1U025[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')

# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U025)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U025[i], dataListF1U025[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U025)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("U05")
alpha = 0.05
n_arrays = len(dataListF1U05)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U05[i], dataListF1U05[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U05)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U05[i], dataListF1U05[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U05)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)

print("U075")
alpha = 0.05
n_arrays = len(dataListF1U075)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U075[i], dataListF1U075[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')

# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U075)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U075[i], dataListF1U075[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')
print('kruskal')
try:
    statistic, p_value = kruskal(*dataListF1U075)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)


print("U1")
alpha = 0.05
n_arrays = len(dataListF1U1)
p_values = np.zeros((n_arrays, n_arrays))

for i in range(n_arrays):
    for j in range(i+1, n_arrays):
        t_statistic, p_value = stats.ttest_ind(dataListF1U1[i], dataListF1U1[j])
        p_values[i][j] = p_value

# Apply Bonferroni correction
bonferroni_alpha = alpha / (n_arrays * (n_arrays - 1) / 2)

# Print results
# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         if p_values[i][j] < bonferroni_alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_values[i][j]}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_values[i][j]}).')
# print('ranksums')
# alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
# n_arrays = len(dataListF1U1)

# for i in range(n_arrays):
#     for j in range(i+1, n_arrays):
#         statistic, p_value = ranksums(dataListF1U1[i], dataListF1U1[j])
#         if p_value < alpha:
#             print(f'Test between Array {i+1} and Array {j+1} is significant (p-value: {p_value}).')
#         else:
#             print(f'Test between Array {i+1} and Array {j+1} is not significant (p-value: {p_value}).')

print('kruskal')
try:

    statistic, p_value = kruskal(*dataListF1U1)

    # Check significance
    alpha = alpha / (n_arrays * (n_arrays - 1) / 2)
    if p_value < alpha:
        print(f'Kruskal-Wallis test is significant (p-value: {p_value}).')
    else:
        print(f'Kruskal-Wallis test is not significant (p-value: {p_value}).')
except Exception as e:
    print(e)
