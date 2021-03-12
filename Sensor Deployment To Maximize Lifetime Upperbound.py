# We will find a way to deploy sensor so that the upperbound for network lifetime is maximized
import numpy as np
from math import sqrt,sin,cos,pi
import matplotlib.pyplot as plt
import random

r=20
Area=100
n=10
m=20

class point:
    def __init__(self,x,y):
        self.x=x
        self.y=y

def distance(t1,t2):
    a=point(t1[0],t1[1])
    b=point(t2[0],t2[1])
    return sqrt((a.x-b.x)**2+(a.y-b.y)**2)

def coverMatrix(tList,sList):
    M=[[0 for i in range (n)] for j in range(m)]
    for i in range(m):
        for j in range(n):
            if distance(sList[i],tList[j])<=r:
                M[i][j]=1
    return M

def checkMonitorOnce(tList,sList,i):
    for j in range(n):
        if distance(sList[i],tList[j])<=r:
            return True
    return False

def checkMonitorAll(targetSet,sList,i):
    for t in targetSet:
        if distance(t,sList[i])>r:
            return False
    return True

def countMonitored(tList,sList,i):
    count=0
    for j in range(m):
        if distance(tList[i],sList[j])<=r:
            count+=1
    return count

def countMonitor(tList,sList,i):
    targetSet=[]
    for j in range(n):
        if distance(tList[j],sList[i])<=r:
            targetSet.append(tList[j])
    return targetSet

def minMonitored(tList,sList):
    minT=0
    for i in range(n):
        if countMonitored(tList,sList,i)<countMonitored(tList,sList,minT):
            minT=i
    return minT

def firstMove(tList,sList):
    for i in range(m):
        if checkMonitorOnce(tList,sList,i)==False:
            sList[i]=randomInsideCircle(tList,minMonitored(tList,sList))

def arrangeSensor(tList,sList):
    f=lambda i: len(countMonitor(tList,sList,i))
    index = [i for i in range(m)]
    index.sort(key=f)
    sList=[sList[i] for i in index]

def placeAtCenter(targetSet,sList,i):
    s=np.mean(np.array(targetSet),axis=0)
    sList[i]=s.tolist().copy()

def findNextNearest(tList,sList,i):
    targetSet=countMonitor(tList,sList,i)
    tList_temp=[t for t in tList if t not in targetSet]
    f = lambda t : distance(sList[i],t)
    return min(tList_temp,key=f)
    
def mainMove(tList,sList):
    for i in range(m):
        while True:
            targetSet=countMonitor(tList,sList,i)
            placeAtCenter(targetSet,sList,i)
            temp=findNextNearest(tList,sList,i)
            newTargetSet=targetSet+[temp]
            placeAtCenter(newTargetSet,sList,i)
            if checkMonitorAll(newTargetSet,sList,i)==False:
                placeAtCenter(targetSet,sList,i)
                break
        
def LifetimeUpperbound(M):
    lt=[]
    for j in range(n):
        lt.append(sum([M[i][j]*b[i] for i in range(m)])//q[j])
    return min(lt)
        
def randomInsideCircle(tList,i):
    circle_r = r
    # center of the circle (x, y)
    circle_x = tList[i][0]
    circle_y = tList[i][1]
    # random angle
    alpha = 2 * pi * random.random()
    # random radius
    R = circle_r * sqrt(random.random())
    # calculating coordinates
    x = R * cos(alpha) + circle_x
    y = R * sin(alpha) + circle_y
    return [x,y]

# input 
np.random.seed(0)
tList=np.random.randint(0,Area,(n,2)).tolist()
q=np.random.randint(1,3,n).tolist()
sList=np.random.randint(0,Area,(m,2)).tolist()
b=np.random.randint(1,100,m).tolist()

# before moving
M=coverMatrix(tList,sList)
print("Upperbound for lifetime before moving: ",LifetimeUpperbound(M))
fig,ax=plt.subplots(1,2)
for x in range(len(tList)):
    ax[0].add_patch(plt.Circle((tList[x][0], tList[x][1]), r, color='r', alpha=0.2))
    ax[0].plot(tList[x][0],tList[x][1],'b*')
    ax[0].text(tList[x][0],tList[x][1],str(x))
for x in range(len(sList)):
    ax[0].plot(sList[x][0],sList[x][1],'r*')
    ax[0].text(sList[x][0],sList[x][1],str(x))

# moving
firstMove(tList,sList)
arrangeSensor(tList,sList)
mainMove(tList,sList)

# after moving
M=coverMatrix(tList,sList)
print("Upperbound for lifetime after moving: ",LifetimeUpperbound(M))
for x in range(len(tList)):
    ax[1].add_patch(plt.Circle((tList[x][0], tList[x][1]), r, color='r', alpha=0.2))
    ax[1].plot(tList[x][0],tList[x][1],'b*')
    ax[1].text(tList[x][0],tList[x][1],str(x))
for x in range(len(sList)):
    ax[1].plot(sList[x][0],sList[x][1],'r*')
    ax[1].text(sList[x][0],sList[x][1],str(x))
plt.axis('equal')
plt.show()



