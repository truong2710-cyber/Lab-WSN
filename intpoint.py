from math import sqrt
class point:
    def __init__(self,x,y):
        self.x=x
        self.y=y


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

t1=[]
t2=[]
for i in range (0,2):
    t1.append(int(input()))
for i in range (0,2):
    t2.append(int(input()))
r=int(input())
print(intersection_point(t1,t2,r))



