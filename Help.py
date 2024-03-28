import math
U=128
I=0.44
P=9
r=P/I/I
z=U/I
X=((z**2)-(r**2))**0.5

grad=math.degrees(math.acos(r/z))
L=X/(2*math.pi*50)
C=1/(X*2*math.pi*50)
print(f"z : {round(z,10)}")
print(f"r : {round(r,2)}")
print(f"X : {round(X,2)}")
print(f"grad : {round(grad,2)}")
print(f"L : {round(L,2)}")
print(f"C : {round(C,5)}")