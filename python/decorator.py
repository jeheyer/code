#!/usr/bin/env python

def decorator(func):

    def inside_func(y):
        print("Here inside", y)

    return inside_func

@decorator
def something(x):
    print("blah", x)

something("derp")
