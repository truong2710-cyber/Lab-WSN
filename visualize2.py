import matplotlib.pyplot as plt
algo2=[1.8861624410752995,17.37838858505675,25.7258702092762,35.21163839734313]
algo1=[1.8861624410752993,21.275471492513077,28.902620259494686,42.26511213660478]
algo3=[1.8861624410752995,8.491548998911952,16.568123286337674,16.666666666666675]
plt.plot(["10,20","25,50","50,100","75,150"],algo1,'go--',label="LP")
plt.plot(["10,20","25,50","50,100","75,150"],algo2,'r^--',label="NewAlgo")
plt.plot(["10,20","25,50","50,100","75,150"],algo3,'bo--',label="Partioning-Shifting")
plt.xlabel("Sensor, Target, Radius=10, Size=200x200")
plt.ylabel("Max Lifetime")
legend = plt.legend(loc='best', fontsize='x-large')
plt.show()