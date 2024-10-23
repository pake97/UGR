import numpy as np
contents = []

with open("fincen_isolation") as f:
    contents = f.readlines()


f10=[]
f125=[]
f150=[]
f175=[]
f11=[]
f1D=[]
f1U=[]
f1N=[]
f1S=[]

for i in range(len(contents)):
    if(i%90 == 5):
        f10.append(float(contents[i].split(":")[1].strip()))
    if(i%90 == 15):
        f125.append(float(contents[i].split(":")[1].strip()))
    if(i%90 == 25):
        f150.append(float(contents[i].split(":")[1].strip()))
    if(i%90 == 35):
        f175.append(float(contents[i].split(":")[1].strip()))
    if(i%90 == 45):
        f11.append(float(contents[i].split(":")[1].strip()))
    if(i%90 == 55):
        f1D.append(float(contents[i].split(":")[1].strip()))
    if(i%90 == 65):
        f1U.append(float(contents[i].split(":")[1].strip()))
    if(i%90 == 75):
        f1N.append(float(contents[i].split(":")[1].strip()))
    if(i%90 == 85):
        f1S.append(float(contents[i].split(":")[1].strip()))


print("f10")
print(np.mean(f10), np.std(f10))
print("f125")
print(np.mean(f125), np.std(f125))
print("f150")
print(np.mean(f150), np.std(f150))
print("f175")
print(np.mean(f175), np.std(f175))
print("f11")
print(np.mean(f11), np.std(f11))
print("fD")
print(np.mean(f1D), np.std(f1D))
print("f1U")
print(np.mean(f1U), np.std(f1U))
print("f1N")
print(np.mean(f1N), np.std(f1N))
print("f1S")
print(np.mean(f1S), np.std(f1S))

        