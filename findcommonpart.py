from math import sqrt
class point:
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
                
n=int(input())
r=float(input())
tList=[]
part=[0,1,2]
for i in range(n):
    x=float(input())
    y=float(input())
    tList.append([x,y])
print(findCommonPart(tList,part,r))      
