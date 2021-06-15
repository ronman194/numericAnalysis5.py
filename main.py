import math
from array import *
#///////////////////////////////////////////////////////////////

def getMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getDet(m):
    if len(m) == 2: # if the matrix is 2x2, will return value
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    det = 0
    for i in range(len(m)):
        det += ((-1)**i)*m[0][i]*getDet(getMinor(m,0,i))
    return det

def mulMatrix(mat1,mat2):
    return [[sum(a*b for a,b in zip(mat1_row,mat2_col)) for mat2_col in zip(*mat2)] for mat1_row in mat1]

def MatrixInverse(m):
    det = getDet(m)
    if det == 0:
        print("det is 0, cant inverse")
        return 0
    #base case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/det, -1*m[0][1]/det],
                [-1*m[1][0]/det, m[0][0]/det]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getDet(minor))
        cofactors.append(cofactorRow)
    cofactors = list(map(list,zip(*cofactors)))
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/det
    return cofactors
#////////////////////////////////////////////////////////////////////////////////

def linearInterpulation(table,point):
    '''

        :param table: table of x,y points
        :param point: x value that we want to find his y value
        :return: y value at the given x by linear interpolation
        '''
    for i in range (0,len(table)):
        if point<table[i+1][0] and point > table[i][0]:
            print("f(x)=((y₁-y₂)/(x₁-x₂))*point + (y₂x₁ - y₁x₂)/(x₁-x₂)")
            y1=table[i][1]
            y2=table[i+1][1]
            x1=table[i][0]
            x2=table[i+1][0]
            sol=((y1-y2)/(x1-x2))*point+(y2*x1-y1*x2)/(x1-x2)
            print("f(x)=(({0}-{1})/({2}-{3}))*{10} + ({4} * {5} - {6} * {7})/({8}-{9}) ".format(y1,y2,x1,x2,y2,x1,y1,x2,x1,x2,point))
            print("f({0}) = {1}".format(point,sol))
           # return sol
    return "Not sol for this table "
#////////////////////////////////////////////////////////////////////////////////
def polynomialInterpulation(table,point):
    '''

        :param table: table of x,y points
        :param point: x value that we want to find his y value
        :return: y value at the given x by polynomial interpolation
        '''
    size = len(table)
    A = []
    for i in range(size):
        col = []
        for j in range(size):
            col.append(math.pow(table[i][0],j))
        A.append(col)
    b=[]
    for i in range(size):
        col = []
        for j in range(1):
            col.append(table[i][1])
        b.append(col)
    A1 = MatrixInverse(A)  # A1 is inverted A
    x=mulMatrix(A1,b)
    sol=0
    print("P{0}(x) = a0".format(len(x)-1), end=" ")
    for i in range (1,len(x)):
        print("+",end=" ")
        print("a{0}x^{1}".format(i,i),end=" ")
    print(" ")
    print("P{0}({1}) = {2}".format(len(x) - 1,point,x[0]), end=" ")
    for i in range(1, len(x)):
        print("+", end=" ")
        print("{0}*{1}^{2}".format(x[i],i, i), end=" ")
    print(" ")
    for i in range(size):
        sol+=x[i][0]*math.pow(point,i)
    print("P{0}({1}) = {2}".format(len(x) - 1,point,sol))
#////////////////////////////////////////////////////////////////////////////////
def lagrangeInterpolation(table,point):
    '''

        :param table: table of x,y points
        :param point: x value that we want to find his y value
        :return: y value at the given x by lagrange interpolation
        '''
    sol=0
    l=1
    counter=0
    p="P{0}({1})".format(len(table)-1,point)

    for i in range(len(table)):
        print("l{0}({1})=".format(i,point),end=" ")
        for j in range(len(table)):
            if i != j :
                if (i==len(table)-1) and j == (len(table) - 2):
                    print("(({0}-{1})/({2}-{3}))=".format(point, table[j][0], table[counter][0], table[j][0]), end=" ")
                elif j != len(table)-1:
                    print("(({0}-{1})/({2}-{3}))*".format(point,table[j][0],table[counter][0],table[j][0]),end=" ")
                else:
                    print("(({0}-{1})/({2}-{3}))=".format(point, table[j][0], table[counter][0], table[j][0]), end=" ")
                l*=(point-table[j][0])/(table[counter][0]-table[j][0])
        print(l,end=" ")
        print(" ")
        l*=table[counter][1]
        counter+=1
        sol+=l
        l=1
    print("P{0}({1}) = ".format(len(table)-1,point),end=" ")
    for i in range (len(table)):
        if i == len(table)-1:
            print("l{0}({1})*y{2}  ".format(i,point,i),end=" ")
        else:
            print("l{0}({1})*y{2} + ".format(i,point,i),end=" ")
    print(" ")
    print(sol)
    return (sol)
#////////////////////////////////////////////////////////////////////////////////
def nevilleInterpulation(table,point):
    '''

    :param table: table of x,y points
    :param point: x value that we want to find his y value
    :return: y value at the given x by neville interpolation
    '''
    size=len(table)
    p=size*[0]
    for i in range(size):
        for j in range(size-i):
            if i == 0:
                p[j]=table[j][1]
            else:
                p[j]=(((point-table[i+j][0])*p[j])-((point-table[j][0])*p[j+1]))
                p[j]=p[j]/(table[j][0]-table[i+j][0])
    print(p[0])
#////////////////////////////////////////////////////////////////////////////////
def menu():
    """
    Create a table by getting from the user the number of points in the table than fill the table than enter a point and
    finally choose the interpolation method that you want to see.
    :return: y value at the given x by the selecting interpolation
    """
    col=2
    row=(int)(input("How much points you want in the table?"))
    table = [[0 for x in range(col)] for y in range(row)]
    for i in range (row):
        for j in range(col):
            if j == 0:
                val=(float) (input("Enter value for x point num {0} in the table:".format(i+1)))
                table[i][j]=val
            else:
                val = (float)(input("Enter value for y point num {0} in the table:".format(i + 1)))
                table[i][j] = val
    point=(float)(input("Enter the x point that you want to find her y point:"))
    answer = (int) (input("Press 1 for linear interpolation / 2 for Polynomyal interpolation / 3 for Lagrange interpolation / 4 for neville interpolation:"))
    if answer == 1:
        linearInterpulation(table,point)
    elif answer == 2:
        polynomialInterpulation(table,point)
    elif answer == 3:
        lagrangeInterpolation(table,point)
    elif answer == 4:
        nevilleInterpulation(table,point)


#////////////////////////////////////////////////////////////////////////////////
menu()

#////////////////////////////////////////////////////////////////
#You can test interpolation manually on this way to set a table and send a table and point to the interpolation you want to test.
#Lines 166-180 are example for ho to do manually test
#s=[[1, 0], [1.2, 0.112463], [1.3, 0.167996], [1.4, 0.222709]] #table of points [x,y]
#l=[[0, 1], [1.3, 0.6200], [1.6, 0.4554], [1.9, 0.2818], [2.2, 0.1103]] #table of points [x,y]
#g=[[0, 3], [1, 2], [2, 3], [3, 6]] #table of points [x,y]
#matrix_table=[[1, 0.8415], [2, 0.9093], [3,0.1411]] #table of points [x,y]
#p=[[1,1],[2,0],[4,1.5]]
#n=[[1.2,1.5095], [1.3,1.6984], [1.4,1.9043], [1.5,2.1293], [1.6,2.3756]]
#k=[[0.2, 13.7241], [0.35, 13.9776], [0.45, 14.0625], [0.6, 13.9776], [0.75,13.7241], [0.85, 13.3056], [0.9, 12.7281]]
#lagrangeInterpolation(p, 3)
#linearInterpulation(k, 0.65)
#polynomialInterpulation(k, 0.65)
#nevilleInterpulation(k, 0.65)
#nevilleInterpulation(s,1.28)
#lagrangeInterpulation(p,3)
#polynomialInterpulation(matrix_table,2.5)
#linearInterpulation(matrix_table,2.5)