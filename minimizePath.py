from math import sqrt
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
    if i1.x==i2.x and i1.y==i2.y:
        return [[i1.x,i1.y]]
    else:
        return [[i1.x,i1.y],[i2.x,i2.y]]


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
        k=[]
        for x in l:
            if x not in k:
                k.append(x)
        c.append(k)
    return c


def minimalPoint(part,tList,r,p):
    if len(part)==1:
        return intersectionPointCircle(tList[part[0]],p,r)
    c=findCommonPart(tList,part,r)
    for i in range(len(part)):
        z=c[i][0]
        t=c[i][1]
        if z[0]!=t[0] or z[1]!=t[1]:
            if len(intersectionPoint(p,tList[part[i]],z,t,r))>0:
                return intersectionPointCircle(tList[part[i]],p,r)
    m=c[0][0]
    for l in c:
        for x in l:
            if distance(p,x)<=distance(p,m):
                m=x
    return m
            
n=int(input())
r=float(input())
tList=[]
part=[0,1,2]
for i in range(n):
    x=float(input())
    y=float(input())
    tList.append([x,y])
p=[]
p.append(float(input()))
p.append(float(input()))
print(minimalPoint(part,tList,r,p))      

    
