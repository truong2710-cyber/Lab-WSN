import matplotlib.pyplot as plt
import xlrd
import numpy as np
from ortools.linear_solver import pywraplp
from math import sqrt,ceil
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
            mp=x[0]
            break
    for l in c:
        for x in l:
            if distance(p,x)<=distance(p,mp):
                mp=x
    return mp


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

def timematrix(clique,tList,sList,r,e,E,k):
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

def solve(data):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    n=len(data)
    m=len(data[0])
    #create 2D-variables
    x={}
    for i in range(n):
        for j in range(m):
            x[i,j]=solver.IntVar(0,1,'')
    for j in range(m):
        solver.Add(solver.Sum([x[i,j] for i in range(n)])==1)
    t=[]
    for i in range(n):
        t.append(sum([x[i,j]*data[i][j] for j in range(m)]))
    a=solver.NumVar(0,solver.infinity(),'')
    for i in range (n):
        solver.Add(a<=t[i])
    opjective=solver.Maximize(a)
    solver.Solve()
    return solver.Objective().Value()

    
def ProcessClique(clique,tList):
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
        t=[]
        for y in x:
            t.append(add[y])
        clique2.append(t)
    for x in clique:
        if len(x)>1:
            clique2.append(x)
    return clique2

def result(tList,sList,r,e,E,k):
    clique=ProcessClique(cliquePartion(tList,r),tList)
    c=timematrix(clique,tList,sList,r,e,E,k)
    return solve(c)

def shifting(x,y):
    s=ceil((size-2*x*r)/(2*q*r))+2
    subtList=[[[] for i in range(s)] for j in range(s)] 
    subsList=[[[] for i in range(s)] for j in range(s)] 
    for i in range(s):
        for j in range(s):
            for t in tList:
                if max(2*x*r+2*(i-1)*q*r,0)<=t[0]<min(2*x*r+2*i*q*r,size) and max(2*y*r+2*(j-1)*q*r,0)<=t[1]<min(2*y*r+2*j*q*r,size):
                    subtList[i][j].append(t)
            for v in sList:
                if max(2*x*r+2*(i-1)*q*r,0)<=v[0]<min(2*x*r+2*i*q*r,size) and max(2*y*r+2*(j-1)*q*r,0)<=v[1]<min(2*y*r+2*j*q*r,size):
                    subsList[i][j].append(v)
    sol=[]
    for i in range(s):
        for j in range(s):
            if len(subtList[i][j])>0:
                sol.append(result(subtList[i][j],subsList[i][j],r,e,E,k))
    return min(sol)


#input target and sensor locations
file_location="D:/test.xlsx"
wb=xlrd.open_workbook(file_location)
sheet=wb.sheet_by_index(0)
sheet1=wb.sheet_by_index(1)
r=10

tList=[]
sList=[]

for i in range(1,sheet.nrows):
    tList.append([sheet.cell_value(i,1),sheet.cell_value(i,2)])
n=len(tList)

for i in range(1,sheet1.nrows):
    sList.append([sheet1.cell_value(i,1),sheet1.cell_value(i,2)])
m=len(sList)

e=3
E=50
k=1
size=200
q=4
#Show target and sensor locations 
fig, ax = plt.subplots()
for x in range(len(tList)):
    ax.add_patch(plt.Circle((tList[x][0], tList[x][1]), r, color='r', alpha=0.2))
    plt.plot(tList[x][0],tList[x][1],'b*')
    plt.text(tList[x][0],tList[x][1],str(x))
for x in range(len(sList)):
    plt.plot(sList[x][0],sList[x][1],'r*')
    plt.text(sList[x][0],sList[x][1],str(x))
ax.set_aspect('equal', adjustable='datalim')
plt.suptitle("Target")
ax.plot()  

#show gridline
start=time.time()
s=ceil(size/(2*q*r))
subtList=[[[] for i in range(s)] for j in range(s)] 
subsList=[[[] for i in range(s)] for j in range(s)] 
for i in range(s):
    for j in range(s):
        for t in tList:
            if 2*i*q*r<=t[0]<min(2*(i+1)*q*r,size) and 2*j*q*r<=t[1]<min(2*(j+1)*q*r,size):
                subtList[i][j].append(t)
        for v in sList:
            if 2*i*q*r<=v[0]<min(2*(i+1)*q*r,size) and 2*j*q*r<=v[1]<min(2*(j+1)*q*r,size):
                subsList[i][j].append(v)
sol=[]
for i in range(s):
    for j in range(s):
        if len(subtList[i][j])>0:
            sol.append(result(subtList[i][j],subsList[i][j],r,e,E,k))
res=[]
res.append(min(sol))
for x in range(1,q):
    for y in range(1,q):
        res.append(shifting(x,y))
end=time.time()
ti=end-start
print(max(res))
file = open("test.txt", "a")
re="\nP-S: "+str(max(res))+"s"+"\nTime: "+str(ti)+"s"+"\n\n-----------------------------------------\n\n"
file.write(re)

x=[2*q*r*i for i in range(s)]
y=[2*q*r*j for j in range(s)]
for i in range(s):
    plt.plot([x[i],x[i]],[0,size],'r--')
for i in range(s):
    plt.plot([0,size],[y[i],y[i]],'r--')
plt.plot([0,200],[200,200],"r--")
plt.plot([200,200],[0,200],"r--")


plt.show()



