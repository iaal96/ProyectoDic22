from cuadruplos import Quadruples
from memoria import Memory
from EstructurasDatos import variableTable
from errores import *
import re
cstMemMap = {}

globalMem = Memory()
localMem = Memory()
tempMem = Memory()
pointerMemStack = []

#Sacar valor de la variable que este en la direccion dada
def getValueFromAddress(address):
    #Se divide la direccion entre 1000
    add_type = address // 1000
    #Si esta entre 0 y 999, saca Int de la direccion de la memoria global
    if add_type == 0:
        return globalMem.getInt(address)
    #Si esta entre 1000 y 1999, saca Float de la direccion de la memoria global
    if add_type == 1:
        return globalMem.getFloat(address)
    #Si esta entre 2000 y 2999, saca Char de la direccion de la memoria global
    if add_type == 2:
        return globalMem.getChar(address)
    #Si esta entre 3000 y 3999, saca Int de la direccion de la memoria local
    if add_type == 3:
        return localMem.getInt(address)
    #Si esta entre 4000 y 4999, saca float de la direccion de la memoria local
    if add_type == 4:
        return localMem.getFloat(address)
    #Si esta entre 5000 y 5999, saca char de la direccion de la memoria local
    if add_type == 5:
        return localMem.getChar(address)
    #Si esta entre 6000 y 6999, saca int de la direccion de la memoria temporal
    if add_type == 6:
        return tempMem.getInt(address)
    #Si esta entre 7000 y 7999, saca float de la direccion de la memoria temporal
    if add_type == 7:
        return tempMem.getFloat(address)
    #Si esta entre 8000 y 8999, saca char de la direccion de la memoria temporal
    if add_type == 8:
        return tempMem.getChar(address)
    #Si esta entre 12000 y 12999, saca la direccion de pila de pointer memory
    if add_type == 12:
        return pointerMemStack[address % 1000]
    else:
        return cstMemMap[address]

def maquina_virtual():
    for cst in variableTable["constants"]:
        if "type" in variableTable["constants"][cst]:
            if variableTable["constants"][cst]["type"] == "int":
                cstMemMap[variableTable["constants"][cst]["address"]] = int(cst)
            elif variableTable["constants"][cst]["type"] == "float":
                cstMemMap[variableTable["constants"][cst]["address"]] = float(cst)
        else:
            cstMemMap[variableTable["constants"][cst]["address"]] = cst
    #Leer cuadruplos, una vez que index sea mayor que la lista de cuadruplos debe parar.
    index = 0
    while len(Quadruples.quadruples) > index:    
        quad = Quadruples.quadruples[index]
        newIndex = executeInstruction(quad)
        if newIndex:
            index = newIndex
        else:
            index += 1                    

def executeInstruction(quad):
    #Si el operador del cuadruplo es = , ejecuta la instruccion asignar
    if quad.operator == "=":
        return asignar(quad)
    #Si el operador del cuadruplo es + , ejecuta la instruccion suma
    elif quad.operator == "+":
        return suma(quad)
    #Si el operador del cuadruplo es - , ejecuta la instruccion resta
    elif quad.operator == "-":
        return resta(quad)
    #Si el operador del cuadruplo es * , ejecuta la instruccion multiplica
    elif quad.operator == "*":
        return multiplica(quad)
    #Si el operador del cuadruplo es / , ejecuta la instruccion divide
    elif quad.operator == "/":
        return divide(quad)
    #Si el operador del cuadruplo es imprime , ejecuta la instruccion printScreen
    elif quad.operator == "imprime":
        return printScreen(quad)

def asignar(quad):
    #Dividir direcciones entre 1000 (sin decimal)
    add_type = quad.result // 1000
    lOp = quad.left_operand // 1000

    #Si es INT  global
    if add_type == 0:
        #Si la direccion es 12000-12999, sacar int de la direccion a la que apunta el pointer e insertar en memoria global
        if lOp == 12:
            globalMem.insertInt(getValueFromAddress(getValueFromAddress(quad.left_operand)), quad.result)
        #Si la direccion es 9000-9999, sacar int de constantMemoryMap e insertar en memoria global.
        elif lOp == 9:
            globalMem.insertInt(cstMemMap[quad.left_operand], quad.result)
        #Si la direccion es 6000-6999, sacar int de la memoria temporal e insertar en memoria global.
        elif lOp == 6:
            globalMem.insertInt(tempMem.getInt(quad.left_operand), quad.result)
        #Si la direccion es 3000-3999, sacar int de la memoria local e insertar en memoria global.
        elif lOp == 3:
            globalMem.insertInt(localMem.getInt(quad.left_operand), quad.result)
        #Si la direccion es 0-999, sacar int de la memoria global e insertar en memoria global.
        elif lOp == 0:
            globalMem.insertInt(globalMem.getInt(quad.left_operand), quad.result)

    #Si es FLOAT  global
    if add_type == 1:
        #Si la direccion es 12000-12999, sacar float de la direccion a la que apunta el pointer e insertar en memoria global
        if lOp == 12:
            globalMem.insertFloat(getValueFromAddress(getValueFromAddress(quad.left_operand)), quad.result)
        #Si la direccion es 10000-10999, sacar float de constantMemoryMap e insertar en memoria global.
        elif lOp == 10:
            globalMem.insertFloat(cstMemMap[quad.left_operand], quad.result)
        #Si la direccion es 7000-7999, sacar float de memoria temporal e insertar en memoria global.
        elif lOp == 7:
            globalMem.insertFloat(tempMem.getFloat(quad.left_operand), quad.result)
        #Si la direccion es 4000-4999, sacar float de memoria local e insertar en memoria global.
        elif lOp == 4:
            globalMem.insertFloat(localMem.getFloat(quad.left_operand), quad.result)
        #Si la direccion es 1000-1999, sacar float de memoria global e insertar en memoria global.
        elif lOp == 1:
            globalMem.insertFloat(globalMem.getFloat(quad.left_operand), quad.result)

    #Si es CHAR global
    if add_type == 2:
        #Si la direccion es 12000-12999, sacar char de la direccion a la que apunta el pointer e insertar en memoria global
        if lOp == 12:
            globalMem.insertChar(getValueFromAddress(getValueFromAddress(quad.left_operand)), quad.result)
        #Si la direccion es 11000-11999, sacar char de constantMemoryMap e insertar en memoria global.
        elif lOp == 11:
            globalMem.insertChar(cstMemMap[quad.left_operand], quad.result)
        #Si la direccion es 8000-8999, sacar char de memoria temporal e insertar en memoria global.
        elif lOp == 8:
            globalMem.insertChar(tempMem.getChar(quad.left_operand), quad.result)
        #Si la direccion es 5000-5999, sacar char de memoria local e insertar en memoria global.
        elif lOp == 5:
            globalMem.insertChar(localMem.getChar(quad.left_operand), quad.result)
        #Si la direccion es 2000-2999, sacar char de memoria global e insertar en memoria global.
        elif lOp == 2:
            globalMem.insertChar(globalMem.getChar(quad.left_operand), quad.result)

    #Si es INT local
    if add_type == 3:
        #Si la direccion es 12000-12999, sacar int de la direccion a la que apunta el pointer e insertar en memoria local
        if lOp == 12:
            localMem.insertInt(getValueFromAddress(getValueFromAddress(quad.left_operand)), quad.result)
        #Si la direccion es 9000-9999, sacar int de constantMemoryMap e insertar en memoria local.
        elif lOp == 9:
            localMem.insertInt(cstMemMap[quad.left_operand], quad.result)
        #Si la direccion es 6000-6999, sacar int de memoria temporal e insertar en memoria local.
        elif lOp == 6:
            localMem.insertInt(tempMem.getInt(quad.left_operand), quad.result)
        #Si la direccion es 3000-3999, sacar int de memoria local e insertar en memoria local.
        elif lOp == 3:
            localMem.insertInt(localMem.getInt(quad.left_operand), quad.result)
        #Si la direccion es 0-999, sacar int de memoria global e insertar en memoria local.
        elif lOp == 0:
            localMem.insertInt(globalMem.getInt(quad.left_operand), quad.result)

    #Si es FLOAT local
    if add_type == 4:
        #Si la direccion es 12000-12999, sacar float de la direccion a la que apunta el pointer e insertar en memoria local
        if lOp == 12:
            localMem.insertFloat(getValueFromAddress(getValueFromAddress(quad.left_operand)), quad.result)
        #Si la direccion es 10000-10999, sacar float de constantMemoryMap e insertar en memoria local.
        elif lOp == 10:
            localMem.insertFloat(cstMemMap[quad.left_operand], quad.result)
        #Si la direccion es 7000-7999, sacar float de memoria temporal e insertar en memoria local.
        elif lOp == 7:
            localMem.insertFloat(tempMem.getFloat(quad.left_operand), quad.result)
        #Si la direccion es 4000-4999, sacar float de memoria local e insertar en memoria local.
        elif lOp == 4:
            localMem.insertFloat(localMem.getFloat(quad.left_operand), quad.result)
        #Si la direccion es 1000-1999, sacar float de memoria global e insertar en memoria local.
        elif lOp == 1:
            localMem.insertFloat(globalMem.getFloat(quad.left_operand), quad.result)
    
    #Si es CHAR local
    if add_type == 5:
        #Si la direccion es 12000-12999, sacar char de la direccion a la que apunta el pointer e insertar en memoria local
        if lOp == 12:
            localMem.insertChar(getValueFromAddress(getValueFromAddress(quad.left_operand)), quad.result)
        #Si la direccion es 11000-11999, sacar char de constantMemoryMap e insertar en memoria local.
        elif lOp == 11:
            localMem.insertChar(cstMemMap[quad.left_operand], quad.result)
        #Si la direccion es 8000-8999, sacar char de memoria temporal e insertar en memoria local.
        elif lOp == 8:
            localMem.insertChar(tempMem.getChar(quad.left_operand), quad.result)
        #Si la direccion es 5000-5999, sacar char de memoria local e insertar en memoria local.
        elif lOp == 5:
            localMem.insertChar(localMem.getChar(quad.left_operand), quad.result)
        #Si la direccion es 2000-2999, sacar char de memoria global e insertar en memoria local.
        elif lOp == 2:
            localMem.insertChar(globalMem.getChar(quad.left_operand), quad.result)

    #Si es INT temporal
    if add_type == 6:
        #Si la direccion es 12000-12999, sacar int de la direccion a la que apunta el pointer e insertar en memoria temporal
        if lOp == 12:
            tempMem.insertInt(getValueFromAddress(getValueFromAddress(quad.left_operand)), quad.result)
        #Si la direccion es 9000-9999, sacar int de constantMemoryMap e insertar en memoria temporal.
        elif lOp == 9:
            tempMem.insertInt(cstMemMap[quad.left_operand], quad.result)
        #Si la direccion es 6000-6999, sacar int de memoria temporal e insertar en memoria temporal.
        elif lOp == 6:
            tempMem.insertInt(tempMem.getInt(quad.left_operand), quad.result)
        #Si la direccion es 3000-3999, sacar int de memoria local e insertar en memoria temporal.
        elif lOp == 3:
            tempMem.insertInt(localMem.getInt(quad.left_operand), quad.result)
        #Si la direccion es 0-999, sacar int de memoria global e insertar en memoria temporal.
        elif lOp == 0:
            tempMem.insertInt(globalMem.getInt(quad.left_operand), quad.result)

    #Si es FLOAT temporal
    if add_type == 7:
        #Si la direccion es 12000-12999, sacar float de la direccion a la que apunta el pointer e insertar en memoria temporal
        if lOp == 12:
            tempMem.insertFloat(getValueFromAddress(getValueFromAddress(quad.left_operand)), quad.result)
        #Si la direccion es 10000-10999, sacar float de constantMemoryMap e insertar en memoria temporal.
        elif lOp == 10:
            tempMem.insertFloat(cstMemMap[quad.left_operand], quad.result)
        #Si la direccion es 7000-7999, sacar float de memoria temporal e insertar en memoria temporal.
        elif lOp == 7:
            tempMem.insertFloat(tempMem.getInt(quad.left_operand), quad.result)
        #Si la direccion es 4000-4999, sacar float de memoria local e insertar en memoria temporal.
        elif lOp == 4:
            tempMem.insertFloat(localMem.getInt(quad.left_operand), quad.result)
        #Si la direccion es 1000-1999, sacar float de memoria global e insertar en memoria temporal.
        elif lOp == 1:
            tempMem.insertFloat(globalMem.getInt(quad.left_operand), quad.result)

    #Si es CHAR temporal
    if add_type == 8:
        #Si la direccion es 12000-12999, sacar char de la direccion a la que apunta el pointer e insertar en memoria temporal
        if lOp == 12:
            tempMem.insertChar(getValueFromAddress(getValueFromAddress(quad.left_operand)), quad.result)
        #Si la direccion es 11000-11999, sacar char de constantMemoryMap e insertar en memoria temporal.
        elif lOp == 11:
            tempMem.insertChar(cstMemMap[quad.left_operand], quad.result)
        #Si la direccion es 8000-8999, sacar char de memoria temporal e insertar en memoria temporal.
        elif lOp == 8:
            tempMem.insertChar(tempMem.getInt(quad.left_operand), quad.result)
        #Si la direccion es 5000-5999, sacar char de memoria local e insertar en memoria temporal.
        elif lOp == 5:
            tempMem.insertChar(localMem.getInt(quad.left_operand), quad.result)
        #Si la direccion es 2000-2999, sacar char de memoria global e insertar en memoria temporal.
        elif lOp == 2:
            tempMem.insertChar(globalMem.getInt(quad.left_operand), quad.result)

    #Si es POINTER temporal
    if add_type == 12:
        #Saca el valor de la direccion del resultado del cuadruplo
        add_type = getValueFromAddress(quad.result)
        asignar(Quadruple(quad.operator, quad.left_operand, "_", add_type))

#Instruccion para sumar
def suma(quad):
    #Se divide la direccion entre 1000
    res_address = quad.result // 1000
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    #Si operando izquierdo tiene otra direccion
    else:
        #Saca el valor del operando izquierdo
        lOp = getValueFromAddress(quad.left_operand)
    # Si operando derecho es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    #Si operando derecho tiene otra direccion
    else:
        #Saca el valor del operando derecho
        rOp = getValueFromAddress(quad.right_operand)
    #Suma operando izquierdo mas operando derecho y guarda en result
    result = lOp + rOp
    #Si la direccion de res_address esta entre 6000-6999, es Int temporal, guardar int en memoria temporal
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    #Si la direccion de res_address esta entre 7000-7999, es Float temporal, guardar float en memoria temporal
    elif res_address == 7:
        tempMem.insertFloat(result, quad.result)

#Instruccion para restar
def resta(quad):
    #Se divide la direccion entre 1000
    res_address = quad.result // 1000
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    #Si operando izquierdo tiene otra direccion
    else:
        #Saca el valor del operando izquierdo
        lOp = getValueFromAddress(quad.left_operand)
    # Si operando derecho es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    #Si operando derecho tiene otra direccion
    else:
        #Saca el valor del operando derecho
        rOp = getValueFromAddress(quad.right_operand)
    #Resta operando derecho al operando izquierdo y asigna a result
    result = lOp - rOp
    #Si la direccion de res_address esta entre 6000-6999, es Int temporal, guardar int en memoria temporal
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    #Si la direccion de res_address esta entre 7000-7999, es Float temporal, guardar float en memoria temporal
    elif res_address == 7:
        tempMem.insertFloat(result, quad.result)

#Instruccion para multiplicar
def multiplica(quad):
    #Se divide la direccion entre 1000
    res_address = quad.result // 1000
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    #Si operando izquierdo tiene otra direccion
    else:
        #Saca el valor del operando izquierdo
        lOp = getValueFromAddress(quad.left_operand)
     # Si operando derecho es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    #Si operando derecho tiene otra direccion
    else:
        #Saca el valor del operando derecho
        rOp = getValueFromAddress(quad.right_operand)
    #Multiplicar operando izquierdo por operando derecho y asignar a result
    result = lOp * rOp
    #Si la direccion de res_address esta entre 6000-6999, es Int temporal, guardar int en memoria temporal
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    #Si la direccion de res_address esta entre 7000-7999, es Float temporal, guardar float en memoria temporal
    elif res_address == 7:
        tempMem.insertFloat(result, quad.result)

#Instruccion para dividir
def divide(quad):
    #Se divide la direccion entre 1000
    res_address = quad.result // 1000
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    #Si operando izquierdo tiene otra direccion
    else:
        #Saca el valor del operando izquierdo
        lOp = getValueFromAddress(quad.left_operand)
    # Si operando derecho es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    #Si operando derecho tiene otra direccion
    else:
        #Saca el valor del operando derecho
        rOp = getValueFromAddress(quad.right_operand)
    #Si operando derecho es 0, dar mensaje de error division entre cero.
    if rOp == 0:
        Error.division_by_zero()
    #Dividir operando izquierdo entre operador derecho y asignar a result
    result = lOp / rOp
    #Si la direccion de res_address esta entre 6000-6999, es Int temporal, guardar int en memoria temporal
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    #Si la direccion de res_address esta entre 7000-7999, es Float temporal, guardar float en memoria temporal
    elif res_address == 7:
        tempMem.insertFloat(result, quad.result)

#Instruccion para imprimir en pantalla
def printScreen(quad):
    #Si el resultado tiene direccion entre 12000 o 12999, sacar valor de la direccion que tenga la direccion del cuadruplo. (Apuntador)
    if quad.result >= 12000:
        #Imprimir valor
        print(getValueFromAddress(getValueFromAddress(quad.result)))
    #Si tiene otra direccion, sacar valor de la direccion que tenga el cuadruplo como resultado.
    else:
        #Imprimir valor
        print(getValueFromAddress(quad.result))
