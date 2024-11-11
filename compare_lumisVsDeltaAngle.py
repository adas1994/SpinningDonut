import os, sys
from matplotlib import pyplot as plt
import numpy as np


fn1 = "trackLumi_DeltaAngleX_0.035_DeltaAngleZ_0.035_.log"
fn2 = "trackLumi_DeltaAngleX_0.15_DeltaAngleZ_0.035_.log"

f1 = open(fn1, "r").readlines()
f2 = open(fn2, "r").readlines()
l1, l2 = [], []

for i, line in enumerate(f1):
    if "PrintLumi" in line :
        slimmedline = line.rstrip('\n').lstrip("PrintLumi  ")
        splitline = slimmedline.split(' ')
        splitline = [eval(elem) for elem in splitline]
        l1.append(splitline)

for i, line in enumerate(f2):
    if "PrintLumi" in line :
        slimmedline = line.rstrip('\n').lstrip("PrintLumi  ")
        splitline = slimmedline.split(' ')
        splitline = [eval(elem) for elem in splitline]
        l2.append(splitline)

l1, l2 = np.asfarray(l1), np.asfarray(l2)
#plt.plot(l1[:, 0], l1[:, 1], color='r', label='DeltaAngleX_0.035_DeltaAngleZ_0.035')
plt.plot(l2[:, 0], l2[:, 1], color='g', label='DeltaAngleX_0.15_DeltaAngleZ_0.035')
plt.plot(l1[:, 0], l1[:, 1], color='r', label='DeltaAngleX_0.035_DeltaAngleZ_0.035')
# Naming the x-axis, y-axis and the whole graph
plt.xlabel("Angle")
plt.ylabel("Magnitude")
plt.title("Sine and Cosine functions")

# Adding legend, which helps us recognize the curve according to it's color
plt.legend()

# To load the display window
plt.show()
