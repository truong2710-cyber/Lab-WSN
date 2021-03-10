import matplotlib.pyplot as plt
algo2=[38.59625608288254,72.25792909635263,26.175040122616092,73.03738856441817]
algo1=[44.134746776398444,79.76066675768963,27.892161232031487,83.44172178248053]
plt.plot(["10,20,5,50","50,100,15,200","100,200,15,300","150,300,30,300"],algo1,'go-',label="LP")
plt.plot(["10,20,5,50","50,100,15,200","100,200,15,300","150,300,30,300"],algo2,'r^-',label="NewAlgo")
plt.xlabel("Sensor,Target,Radius,Size")
plt.ylabel("Max Lifetime")
legend = plt.legend(loc='best', fontsize='x-large')
plt.show()