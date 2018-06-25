#!/usr/bin/env python3

def pow(a:float, n:int):
    if n==0:
        return 1
    elif n%2==1:
        return pow(a,n-1)*a
    else:
        return pow(a**2,n//2)

print(pow(5,25))
