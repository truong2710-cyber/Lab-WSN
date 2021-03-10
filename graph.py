import xlrd
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


def optimizeClique(tList,clique,r):
    add=[]
    for part in clique:
        if len(part)>2:
            for i in part:
                check1=False
                l1=[]
                for k in part:
                    if k!=i:
                        l1.extend(intersection_point(tList[i],tList[k],r))
                for x in l1:
                    c=True
                    for z in part:
                        if z!=i:
                           if distance(x,tList[z])>r+0.0001:
                                c=False
                                break
                    if c==True:
                        check1=True
                        break
                temp=part.copy()
                temp.remove(i)
                j=temp[0]
                l=[]
                for k in temp:
                    if j!=k:
                        l.extend(intersection_point(tList[j],tList[k],r))
                check=False
                for x in l:
                    c=True
                    for y in temp:
                        if y!=j:
                            if distance(x,tList[y])>r+0.0001:
                                c=False
                                break
                    if c==True:
                        check=True
                        break
                if check==True and check1==False:
                    part.remove(i)
                    add.append(i)
                    break
    for i in add:
        clique.append([i])
            

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


tList=[]
file_location="C:/Users/James/PycharmProjects/sensor/input.xlsx"
wb=xlrd.open_workbook(file_location)
sheet=wb.sheet_by_index(0)
for i in range(1,sheet.nrows):
    tList.append([sheet.cell_value(i,1),sheet.cell_value(i,2)])
n=int(sheet.cell_value(sheet.nrows-1,0))
sheet1=wb.sheet_by_index(1)
r=sheet1.cell_value(1,4)
print(cliquePartion(tList,r)) 
   
                
                
    
        
    
