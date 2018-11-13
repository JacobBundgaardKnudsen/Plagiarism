
bands = 5
M = []

signature = [i for i in range(20)]
r = len(signature)/bands

for band in range(0, len(signature), r):
    M.append(signature[band:band+r]) 
print(M)