import matplotlib.pyplot as plt
algo2=[11,14,19,19,22,23,21,23,26,26,25,26]
algo1=[11,14,19,20,23,27,27,29,34,36,35,31]
x=[20,40,60,80,100,120,140,160,180,200,220,240]
plt.plot(x,algo1,'go--',label="Heuristic")
plt.plot(x,algo2,'r^--',label="LP")

plt.xlabel("Number of target, Radius=30, Size=300x300")
plt.ylabel("Number of Regions")
legend = plt.legend(loc='best', fontsize='x-large')
plt.show()