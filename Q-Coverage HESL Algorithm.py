import numpy as np
from math import floor

class point:
    def __init__(self,x,y):
        self.x=x
        self.y=y

def distance(t1,t2):
    a=point(t1[0],t1[1])
    b=point(t2[0],t2[1])
    return np.sqrt((a.x-b.x)**2+(a.y-b.y)**2)

def coverMatrix(tList,sList):
    M=[[0 for i in range (n)] for j in range(m)]
    for i in range(m):
        for j in range(n):
            if distance(sList[i],tList[j])<=r:
                M[i][j]=1
    return M

def checkConditionLoop():
    for j in range(n):
        count=0
        for i in range(m):
            if M[i][j]==1 and b[i]>0:
                count+=1
        if count<q[j]:
            return False
    return True

def checkAllCovered(uncover_label):
    for i in range(n):
        if uncover_label[i]>0:
            return False
    return True

def select(uncover_label):
    s=[]
    for i in range(m):
        for j in range(n):
            if M[i][j]==1 and uncover_label[j]>0 :
                s.append(i)
                break
    key=lambda x: b[x]
    return max(s,key=key)

def checkQCoverage(S):
    for i in range(n):
        Q=0
        for s in S:
            if M[s][i]==1:
                Q+=1
        if Q<q[i]:
            return False
    return True
        
def minimize(S):
    for i in S:
        S.remove(i)
        if checkQCoverage(S):
            minimize(S)
        else:
            S.append(i)

def maxLifetime(S):
    b_in_S=[b[i] for i in S]
    return min(b_in_S)

def HESL(w):
    global lifetime
    while checkConditionLoop():
        # generate a Q-Cover S
        S=[]
        uncover_label=q.copy()
        while checkAllCovered(uncover_label) == False:
            s=select(uncover_label)
            S.append(s)
            for i in range(n):
                if M[s][i]:
                    uncover_label[i]-=1
        # minimize S
        minimize(S)
        # assign lifetime for S. Then we will find another Q-Cover set
        w0=min([w,maxLifetime(S)])
        lifetime+=w0
        # update remaining battery for all sensors in S
        for s in S:
            b[s]-=w0

def LifetimeUpperbound(M):
    lt=[]
    for j in range(n):
        lt.append(floor(sum([M[i][j]*b[i] for i in range(m)])/q[j]))
    return min(lt)

#initialization
n=30  # number of targets
m=100 # number of sensors
Area=200
r=70
q=np.random.randint(1,2,n).tolist()
tList=np.random.randint(0,Area,(n,2)).tolist()  
sList=np.random.randint(0,Area,(m,2)).tolist()
b=[1 for i in range(m)]
M=coverMatrix(tList,sList)
print(LifetimeUpperbound(M))
w=0.01
lifetime=0
HESL(w)
print(lifetime)


