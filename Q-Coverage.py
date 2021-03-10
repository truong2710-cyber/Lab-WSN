import matplotlib.pyplot as plt
import xlrd
import numpy as np
from ortools.linear_solver import pywraplp
from math import sqrt
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

def intersection_point_2circle(t1,t2,r):
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

def condition(x):
    return x[0]

def arrange(t,points):
    under=[x for x in points if x[1]<=t[1]]
    above=[x for x in points if x[1]>t[1]]
    under.sort(key=condition)
    above.sort(key=condition, reverse=True)
    points=above+under
    return points

def findIntersectionPoints(tList,t):
    points=[]
    for x in tList:
        if x!=t and distance(t,x)<2*r:
            points.extend(intersection_point_2circle(t,x,r))
    return points

def findIntersectionTargets(tList,point):
    intersection_targets=[]
    for t in tList:
        if distance(point,t)<=r+0.0005:
            intersection_targets.append(tList.index(t))
    return intersection_targets

def findArc(tList,t,p1,p2):
    target_set_1 = findIntersectionTargets(tList,p1) 
    target_set_2 = findIntersectionTargets(tList,p2)
    target_set_1=set(target_set_1)
    target_set_2=set(target_set_2)
    return list(target_set_1 & target_set_2)

def findCriticalRegion(tList,t):
    arc=[]
    points=findIntersectionPoints(tList,t)
    points=arrange(t,points)
    points.append(points[0])
    for x in range(len(points)-1):
        arc.append(findArc(tList,t,points[x],points[x+1]))
    return list(set(max(arc,key=len)))

def isSubset(x,region):
    for i in x:
        if i not in region:
            return False
    return True

def delete(regions):
    erase=[]
    for x in regions:
        for region in regions: 
            if x!=region and isSubset(x,region):
                erase.append(x)
    for x in erase:
        if x in regions:
            regions.remove(x)
    return regions
            
def findAllCriticalRegions(tList):
    regions=[]
    for t in tList:
        if len(findIntersectionPoints(tList,t))>0:
            if findCriticalRegion(tList,t) not in regions:
                regions.append(findCriticalRegion(tList,t))
        else:
            regions.append([tList.index(t)])
    regions=delete(regions)
    return regions
    
def solve(tList,regions,q):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    x=[[]]*len(regions)
    for i in range(len(regions)):
        x[i]=solver.IntVar(0,solver.infinity(),' ')
    for j in range(len(tList)):
        solver.Add(solver.Sum([x[i] for i in range(len(regions)) if j in regions[i]])>=q[j])
    M=solver.Sum(x)
    opjective=solver.Minimize(M)
    solver.Solve()
    #for i in range(len(regions)):
    #    print(int(x[i].solution_value()),end=' ')
    return [int(x[i].solution_value()) for i in range(len(regions))]

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

def findCommonPart(tList,part,r):
    c=[]
    for i in part:
        l=[]
        erase=[]
        for j in part:
            if j!=i:
                l.extend(intersection_point_2circle(tList[i],tList[j],r))
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

#input 
np.random.seed(97)
r=60
Area=1000
Base=[0,0]
res=[]
for n in [10,20,50,100,200,500,1000]:
#solve
    q=np.random.randint(1,30,n).tolist()
    tList=np.random.randint(0,Area,(n,2)).tolist()
    regions=findAllCriticalRegions(tList)
#print(regions)
    x=solve(tList,regions,q)
    res.append(np.sum(np.array(x)))
plt.plot([10,20,50,100,200,500,1000],res)
plt.show()
#for i in range(len(regions)):
#    print("Place",x[i],"sensor(s) at",minimalPoint(regions[i],tList,r,Base))
#    print("NUMBER OF SENSORS NEEDED: ", np.sum(np.array(x)))
#show illustration
#fig, ax = plt.subplots()
#for x in range(len(tList)):
#    ax.add_patch(plt.Circle((tList[x][0], tList[x][1]), r, color='r', alpha=0.2))
#    plt.plot(tList[x][0],tList[x][1],'b*')
#    plt.text(tList[x][0],tList[x][1],str(x))
    #for x in range(len(sList)):
    #    plt.plot(sList[x][0],sList[x][1],'r*')
    #    plt.text(sList[x][0],sList[x][1],str(x))
#plt.plot(Base[0],Base[1],"r*",markersize=5)
#plt.text(Base[0],Base[1],"Base",horizontalalignment="center",verticalalignment="top",fontsize=12)
#ax.set_aspect('equal', adjustable='datalim')
#plt.suptitle("Target")
#ax.plot()  
#plt.show()

