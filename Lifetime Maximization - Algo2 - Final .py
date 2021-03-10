import matplotlib.pyplot as plt
import xlrd
import numpy as np
from ortools.linear_solver import pywraplp
from math import sqrt
import pandas as pd
import xlsxwriter
import time

class point:
    def __init__(self,x,y):
        self.x=x
        self.y=y

class vector:
    def __init__(self,x,y):
        self.x=x
        self.y=y


def distance(t1,t2):
    a=point(t1[0],t1[1])
    b=point(t2[0],t2[1])
    return sqrt((a.x-b.x)**2+(a.y-b.y)**2)


def intersection_point(t1,t2,r):
    a=point(t1[0],t1[1])
    b=point(t2[0],t2[1])
    if sqrt((a.x-b.x)**2+(a.y-b.y)**2)>2*r:
        return []
    m=point((a.x+b.x)/2,(a.y+b.y)/2)
    d=sqrt(r**2-((a.x-b.x)**2+(a.y-b.y)**2)/4)
    n1=d/sqrt((a.x-b.x)**2+(a.y-b.y)**2)
    n2=-n1
    i1=point((m.x+(a.y-b.y)*n1),(m.y+(b.x-a.x)*n1))
    i2=point((m.x+(a.y-b.y)*n2),(m.y+(b.x-a.x)*n2))
    return [[i1.x,i1.y],[i2.x,i2.y]]

def intersectionPoint(x,y,z,t,r):
    d=distance(x,y)
    a=vector(x[0]-y[0],x[1]-y[1])
    b=vector(z[0]-t[0],z[1]-t[1])
    x=point(x[0],x[1])
    z=point(z[0],z[1])
    if a.x*b.y-a.y*b.x!=0:
        t1=((z.x-x.x)*a.y-(z.y-x.y)*a.x)/(b.y*a.x-b.x*a.y)
        i=[(z.x+b.x*t1),(z.y+b.y*t1)]
        if a.x!=0:
            t=(z.x-x.x+b.x*t1)/a.x
        else:
            t=(z.y-x.y+b.y*t1)/a.y
        if distance(i,y)<=r and t>=-1 and d>r:
            return i
        else:
            return []
    else:
        return []
        
def intersectionPointCircle(o,p,r):
    t=r/distance(o,p)
    x=o[0]+(p[0]-o[0])*t
    y=o[1]+(p[1]-o[1])*t
    return [x,y]

def findCommonPart(tList,part,r):
    c=[]
    for i in part:
        l=[]
        erase=[]
        for j in part:
            if j!=i:
                l.extend(intersection_point(tList[i],tList[j],r))
        for x in l:
            check=True
            for j in part:
                if distance(x,tList[j])>r+0.0001:
                    check=False
                    break
            if check==False:
                erase.append(x)
        for x in erase:
            l.remove(x)
        c.append(l)
    return c


def minimalPoint(part,tList,r,p):
    check=True
    for x in part:
        if distance(p,tList[x])>r:
            check=False
    if check==True:
        return p
    if len(part)==1:
        if distance(p,tList[part[0]])>r:
            return intersectionPointCircle(tList[part[0]],p,r)
        else:
            return p
    c=findCommonPart(tList,part,r)
    for i in range(len(part)):
        if len(c[i])!=0:
            z=c[i][0]
            t=c[i][1]
            if z[0]!=t[0] or z[1]!=t[1]:
                if len(intersectionPoint(p,tList[part[i]],z,t,r))>0:
                    return intersectionPointCircle(tList[part[i]],p,r)
            elif intersectionPointCircle(tList[part[i]],p,r)==z and distance(tList[part[i]],p)>=r:
                return z
        
    for x in c:
        if len(x)!=0:
            m=x[0]
            break
    for l in c:
        for x in l:
            if distance(p,x)<=distance(p,m):
                m=x
    return m


def createGraph(tList,r):
    n=len(tList)
    edge=[[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            if j!=i and distance(tList[i],tList[j])<=2*r:
                edge[i][j]=1
    return edge


def notin(i,clique):
    for j in clique:
        if i in j:
            return False
    return True


def check(d):
    n=len(d)
    for i in range(n):
        if d[i]>0:
            return False
    return True


def deg(edge,i):
    c=0
    n=len(edge)
    for j in range(n):
        if j!=i and edge[i][j]==1:
            c+=1
    return c


def update(d,edge,a,b):
    n=len(d)
    l=[]
    for i in range(n):
        if i!=a and i!=b and edge[i][a]==1 and edge[i][b]==1:
            l.append(i)
    for i in range(n):
        edge[i][b]=-1
        edge[b][i]=-1
    d[b]=-1
    for i in range(n):
        if i in l:
            edge[a][i]=1
            edge[i][a]=1
        elif i not in l and i!=a and i!=b:
            edge[a][i]=0
            edge[i][a]=0
    for i in range(n):
        if i!=b:
            d[i]=deg(edge,i)

def checkempty(f):
    for x in f:
        if len(x)>0:
            return False
    return True

def optimizeClique(tList,clique,r):
    for part in clique:
        if len(part)>2:
            f=findCommonPart(tList,part,r)
            if checkempty(f):
                for i in range(len(part)):
                    temp=part.copy()
                    temp.remove(part[i])
                    f1=findCommonPart(tList,temp,r)
                    if checkempty(f1)==False:
                        clique.append([part[i]])
                        part.pop(i)
                        break
            

def cliquePartion(tList,r):
    clique=[]
    n=len(tList)
    edge=createGraph(tList,r)
    d=[0]*n
    for i in range(n):
        count=0
        for j in range(n):
            if j!=i and edge[i][j]==1:
                count+=1
        d[i]=count
    while check(d)==False:
        k=[]
        for i in range(len(d)):
            if d[i]>0:
                k.append(d[i])
        a=d.index(min(k))
        k1=[]
        for i in range(len(d)):
            if i!=a and edge[a][i]==1:
                k1.append(i)
        b=k1[0]
        for j in k1:
            if d[j]<=d[b]:
                b=j
        update(d,edge,a,b)
        if notin(a,clique) and notin(b,clique):
            clique.append([a,b])
        else:
            for i in range(len(clique)):
                if a in clique[i] or b in clique[i]:
                    if a in clique[i]:
                        clique[i].append(b)
                    else:
                        clique[i].append(a)
    for i in range(n):
        if d[i]==0 and notin(i,clique):
            clique.append([i])
    optimizeClique(tList,clique,r)
    return clique

def timematrix(clique,sList,r,e,E,k):
    #e: energy for sensing task
    #E: initial energy
    #k: constant=energy for moving/d
    m=len(sList)
    n=len(clique)
    c=np.zeros((n,m))
    for i in range(n):
        for j in range(m):
            c[i][j]=(E-k*distance(sList[j],minimalPoint(clique[i],tList,r,sList[j])))/e
            if c[i][j]<0:
                c[i][j]=0
    return c


    
def ProcessClique(clique):
    add=[]
    for x in clique:
        if len(x)==1:
            add.append(x[0])
        
    t1List=[]
    for x in add:
        t1List.append(tList[x])
    clique1=cliquePartion(t1List,r)
    clique2=[]
    for x in clique1:
        temp=[]
        for y in x:
            temp.append(add[y])
        clique2.append(temp)
    for x in clique:
        if len(x)>1:
            clique2.append(x)
    return clique2

#THUAT TOAN SAP XEP CHO SENSOR VAO CAC VUNG DA CHIA
def Base(c,Y):
    F=[0]*len(c)
    for i in range(len(c)):
        for j in range(len(c[0])):
            if Y[j]==i:
                F[i]+=c[i][j]
    return F

def checks(A,i,kt,kts,Y,c,F,BaseT):
    kts[i]=1
    u=Y[i]
    if u!=-1:
        kt[u]=1
    if Y[i]==-1 or F[u]-c[u][i]>BaseT:
        Y[i]=A
        F[A]+=c[A][i]
        if u!=-1:
            F[u]-=c[u][i]
        return True
    for j in range(len(c[0])):
        if kts[j]==0 and kt[Y[j]]==0 and F[u]-c[u][i]+c[u][j]>BaseT:
            if checks(u,j,kt,kts,Y,c,F,BaseT):
                Y[i]=A
                F[A]+=c[A][i] 
                F[u]=F[u]-c[u][i]+c[u][j]
                return True
    if u!=-1:
        kt[u]=0
    return False

def checkr(A,c,Y,F):
    BaseT=F[A]
    kts=[0]*len(c[0])
    kt=[0]*len(c)
    for i in range(len(c[0])):
        if c[A][i]>0:
            if checks(A,i,kt,kts,Y,c,F,BaseT):
                return True
    return False

def showSolution(clique,sList,r,e,E,k):
    c=timematrix(clique,sList,r,e,E,k)
    start=time.time()
    Y=[-1]*len(sList)
    while True:
        F=Base(c,Y)
        A=F.index(min(F))
        if checkr(A,c,Y,F)==False:
            end=time.time()
            t=end-start
            file = open("test.txt", "a")
            res=str(n)+" target, "+str(m)+" sensor, r = "+str(r)+", size = "+str(Area)+"x"+str(Area)+"\nNewAlgo: "+str(min(F))+"s"+"\nTime: "+str(t)+"s"
            file.write(res)
            print(min(F))
            break


        
#input target and sensor location
file_location="C:/Users/James/PycharmProjects/sensor/input.xlsx"
wb=xlrd.open_workbook(file_location)
sheet=wb.sheet_by_index(0)
n=20
sheet1=wb.sheet_by_index(1)
r=30
m=40
Area=300
tList=np.random.randint(0,Area,(n,2))
sList=np.random.randint(0,Area,(m,2))
t=tList.tolist()
s=sList.tolist()
df1 = pd.DataFrame({'x':[i[0] for i in t] ,'y':[j[1] for j in t]})
df2 = pd.DataFrame({'x':[i[0] for i in s] ,'y':[j[1] for j in s]})
writer = pd.ExcelWriter('D:/test.xlsx', engine='xlsxwriter')
df1.to_excel(writer, sheet_name="Target")
df2.to_excel(writer, sheet_name="Sensor")
writer.save()
e=sheet1.cell_value(1,6)
E=sheet1.cell_value(1,8)
k=sheet1.cell_value(1,10)


#process clique
clique=ProcessClique(cliquePartion(tList,r))

#show solution and graph
showSolution(clique,sList,r,e,E,k)


