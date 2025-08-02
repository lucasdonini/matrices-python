from operator import add, sub

def operation(v1, v2, operator):
    return operator(v1, v2)


print(operation(1.0, 2.0, float.__sub__))