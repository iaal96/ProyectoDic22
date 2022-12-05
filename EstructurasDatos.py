class Stack:
    def __init__(self):
        self.items = []
    
    def isEmpty(self):
        return self.items == []

    def push(self,item):
        self.items.append(item)
    
    def pop(self):
        return self.items.pop()
    
    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)
    
    def print(self):
        print(self.items)

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def size(self):
        return len(self.items)

    def print(self):
        print(self.items)

    def values(self):
        return self.items


currentScope = "global"
currentType = "program"

functionDir = {}
variableTable = {}
semanticCube = {}
operators = Stack()
operands = Stack()
types = Stack()
arrMatOperands = Stack()
addresses = {
    "globalInt": 0,
    "globalFloat": 1000,
    "globalChar": 2000,
    "localInt": 3000,
    "localFloat": 4000,
    "localChar": 5000,
    "temporalInt": 6000,
    "temporalFloat": 7000,
    "temporalChar": 8000,
    "constantInt": 9000,
    "constantFloat": 10000,
    "constantChar": 11000,
    "temporalPoint": 12000,
    "void": 13000
}
ty = {
    0: "int",
    1: "float",
    2: "char"
}
ops = ["+", "-", "*", "/", ">", "<", "<>", "==", "&", "|","<=",">=", "%"]
#print("Cubo Semantico: ")
for i in ty:
    for j in ty:
        for k in ops:
            if i > j:
                semanticCube[(ty[i], ty[j], k)] = ty[i]
            else:
                semanticCube[(ty[i], ty[j], k)] = ty[j]
            if i == 2 or j == 2:
                semanticCube[(ty[i], ty[j], k)] = "error"
            if k == ">" or k == "<" or k == "<>" or k == "==" or k == "|" or k == "&" or k == "<=" or k == ">=":
                if (i == 0 or i == 1) and (j == 0 or j == 1):
                    semanticCube[(ty[i], ty[j], k)] = "int"
                else:
                    semanticCube[(ty[i], ty[j], k)] = "error"
            if k == "<>" or k == "==":
                if i == 2 and j == 2:
                    semanticCube[(ty[i], ty[j], k)] = "int"
            if k == "/":
                if i != 2 and j != 2:
                    semanticCube[(ty[i], ty[j], k)] = "float"


# ejemplo directorio de funciones
'''
    "global": {
        "type": "void",
        "vars": variableTable["global"] -> "i": {
                                                "type": "int"
                                                "value": 1
                                            }
                                            ...
    }
    "main": {
        "type": "void",
        "vars": variableTable["main"] -> "c": {
                                              "type": "char"
                                              "value": "h"
                                         }
                                         ...
    }
    "uno": {
        "type": "int",
        "params": Queue[int, int, float]
        "paramsLength": len(params)
        "vars": variableTable["uno"] -> "x": {
                                            "type": "int"
                                            "value": 1
                                        }
    }
'''

#cubo semantico
'''
    semanticCube[(op1, op2, op)] => int/float/char/error
    semanticCube[("int", "int", "+")] => "int"
    semanticCube[("char", "float", "*")] => "error"
'''