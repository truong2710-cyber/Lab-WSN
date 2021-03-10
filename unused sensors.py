import matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10,4), sharey=True, dpi=120)
n1=[20,23,33,47,49,64]
n2=[21,31,51,57,70,69]
x=[40,60,80,100,120,140]
ax1.plot(x,n1,'go--',label="20 Targets")
ax1.plot(x,n2,'r^--',label="40 Targets")

ax1.set_xlabel("Number of sensor, Radius=30, Size=300x300, E=50, e=3, k=1")
ax1.set_ylabel("Number of unused sensor")
legend = ax1.legend(loc='best', fontsize='x-large')


x1=[40,60,80]
n3=[20,23,33]
n4=[5,17,19]
ax2.plot(x1,n3,'go--',label="E=50")
ax2.plot(x1,n4,'r^--',label="E=100")

ax2.set_xlabel("Number of sensor, Radius=30, Size=300x300, e=3, k=1, 20 Targets")
ax2.set_ylabel("Number of unused sensor")
legend = ax2.legend(loc='best', fontsize='x-large')
plt.show()