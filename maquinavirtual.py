from cuadruplos import Quadruples,Quadruple
from memoria import Memory
from EstructurasDatos import variableTable
from errores import *
import re
import math
import numpy as np

#Mapa de memoria de constantes
cstMemMap = {}

#Inicializa una memoria global
globalMem = Memory()
#Inicializa una memoria local
localMem = Memory()
#Inicializa una memoria temporal
tempMem = Memory()


localMemStack = []
functionReturnStack = []
currentFunctionStack = []
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
    #Recibe cuadruplos
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
    #Si el operador del cuadruplo es >, ejecuta la instruccion mayorQue
    elif quad.operator == ">":
        return mayorQue(quad)
    #Si el operador del cuadruplo es <, ejecuta la instruccion menorQue
    elif quad.operator == "<":
        return menorQue(quad)
    #Si el operador del cuadruplo es >=, ejecuta la instruccion mayorIgual
    elif quad.operator == ">=":
        return mayorIgual(quad)
    #Si el operador del cuadruplo es <=, ejecuta la instruccion menorIgual
    elif quad.operator == "<=":
        return menorIgual(quad)
    #Si el operador del cuadruplo es <>, ejecuta la instruccion diferenteA
    elif quad.operator == "<>":
        return diferenteA(quad)
    #Si el operador del cuadruplo es ==, ejecuta la instruccion igualA
    elif quad.operator == "==":
        return igualA(quad)
    #Si el operador del cuadruplo es | , ejecuta la instruccion OR
    elif quad.operator == "|":
        return ORop(quad)
    #Si el operador del cuadruplo es &, ejecuta la instruccion AND
    elif quad.operator == "&":
        return ANDop(quad)
    #Si el operador del cuadruplo es raizcuadrada, ejecuta la instruccion raizcuadrada
    elif quad.operator == "raizcuadrada":
        return raizcuadrada(quad)
    #Si el operador del cuadruplo es cuadratica, ejecuta la instruccion cuadratica
    elif quad.operator == "cuadratica":
        return cuadratica(quad)
    #Si el operador del cuadruplo es pow, ejecuta la instruccion pow
    elif quad.operator == "pow":
        return pow(quad)
    #Si el operador del cuadruplo es exponencial, ejecuta la instruccion exponencial
    elif quad.operator == "exponencial":
        return exponencial(quad)
    #Si el operador del cuadruplo es redondearArriba, ejecuta la instruccion redondearArriba
    elif quad.operator == "redondearArriba":
        return redondearArriba(quad)
    #Si el operador del cuadruplo es redondearAbajo, ejecuta la instruccion redondearAbajo
    elif quad.operator == "redondearAbajo":
        return redondearAbajo(quad)
    #Si el operador del cuadruplo es gamma, ejecuta la instruccion gamma
    elif quad.operator == "gamma":
        return gamma(quad)
    #Si el operador del cuadruplo es residuo, ejecuta la instruccion residuo
    elif quad.operator == "residuo":
        return residuo(quad)
    #Si el operador del cuadruplo es radianes, ejecuta la instruccion radianes
    elif quad.operator == "radianes":
        return radianes(quad)
    #Si el operador del cuadruplo es grados, ejecuta la instruccion grados
    elif quad.operator == "grados":
        return grados(quad)
    #Si el operador del cuadruplo es logaritmo, ejecuta la instruccion logaritmo
    elif quad.operator == "logaritmo":
        return logaritmo(quad)
    #Si el operador del cuadruplo es logaritmoGamma, ejecuta la instruccion logaritmoGamma
    elif quad.operator == "logaritmoGamma":
        return logaritmoGamma(quad)
    #Si el operador del cuadruplo es seno, ejecuta la instruccion seno
    elif quad.operator == "seno":
        return seno(quad)
    #Si el operador del cuadruplo es coseno, ejecuta la instruccion coseno
    elif quad.operator == "coseno":
        return coseno(quad)
    #Si el operador del cuadruplo es tangente, ejecuta la instruccion tangente
    elif quad.operator == "tangente":
        return tangente(quad)
    #Si el operador del cuadruplo es lee, ejecuta la instruccion leer
    elif quad.operator == "lee":
        return leer(quad)
    #Si el operador del cuadruplo es ENDFUNC, ejecuta la instruccion endFunc
    elif quad.operator == "ENDFUNC":
        return endFunc(quad)
    #Si el operador del cuadruplo es GOTOF, ejecuta la instruccion gotof
    elif quad.operator == "GOTOF":
        return gotof(quad)
    #Si el operador del cuadruplo es GOTO, ejecuta la instruccion goto
    elif quad.operator == "GOTO":
        return goto(quad)
    #Si el operador del cuadruplo es GOTOFOR, ejecuta la instruccion gotofor
    elif quad.operator == "GOTOFOR":
        return gotofor(quad)
    #Si el operador del cuadruplo es GOSUB, ejecuta la instruccion gosub
    elif quad.operator == "GOSUB":
        return gosub(quad)
    #Si el operador del cuadruplo es ERA, ejecuta la instruccion era
    elif quad.operator == "ERA":
        return era(quad)
    #Si el operador del cuadruplo es PARAM, ejecuta la instruccion param
    elif quad.operator == "PARAM":
        return param(quad)
    #Si el operador del cuadruplo es REGRESA, ejecuta la instruccion regresa
    elif quad.operator == "REGRESA":
        return regresa(quad)
    #Si el operador del cuadruplo es VERIFICA, ejecuta la instruccion verifica
    elif quad.operator == "VERIFICA":
        return verifica(quad)
    #Si el operador del cuadruplo es ARR=, ejecuta la instruccion verifica arrayAssign
    elif quad.operator == "ARR=":
        return arrayAssign(quad)
    #Si el operador del cuadruplo es ARR+, ejecuta la instruccion verifica arraySuma
    elif quad.operator == "ARR+":
        return arraySuma(quad)
    #Si el operador del cuadruplo es ARR-, ejecuta la instruccion verifica arrayResta
    elif quad.operator == "ARR-":
        return arrayResta(quad)
    #Si el operador del cuadruplo es ARR*, ejecuta la instruccion verifica arrayMultiplica
    elif quad.operator == "ARR*":
        return arrayMultiplica(quad)
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
            tempMem.insertFloat(tempMem.getFloat(quad.left_operand), quad.result)
        #Si la direccion es 4000-4999, sacar float de memoria local e insertar en memoria temporal.
        elif lOp == 4:
            tempMem.insertFloat(localMem.getFloat(quad.left_operand), quad.result)
        #Si la direccion es 1000-1999, sacar float de memoria global e insertar en memoria temporal.
        elif lOp == 1:
            tempMem.insertFloat(globalMem.getFloat(quad.left_operand), quad.result)

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
    # Para arreglos y matrices (direccion base + index de acceso)
    elif res_address == 12:
        while len(pointerMemStack) <= quad.result % 1000:
            pointerMemStack.append(0)
        pointerMemStack[quad.result % 1000] = lOp + rOp

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

def mayorQue(quad):
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        #Saca valor de operando izquierdo y asigna a lOp
        lOp = getValueFromAddress(quad.left_operand)
    # Si operando derecho es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    else:
        #Saca valor de operando derecho y asigna a rOp
        rOp = getValueFromAddress(quad.right_operand)
    #Compara lOp con rOp y asignar valor a result
    result = lOp > rOp
    #Insertar int (0 o 1) en memoria temporal 
    tempMem.insertInt(result, quad.result)

def menorQue(quad):
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        #Saca valor de operando izquierdo y asigna a  lOp
        lOp = getValueFromAddress(quad.left_operand)
    # Si operando derecho es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    else:
        #Saca valor de operando derecho y asigna a rOp
        rOp = getValueFromAddress(quad.right_operand)
    #Compara lOp con rOp y asignar valor a result
    result = lOp < rOp
    #Insertar int (0 o 1) en memoria temporal 
    tempMem.insertInt(result, quad.result)

def mayorIgual(quad):
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        #Saca valor de operando izquierdo y asigna a lOp
        lOp = getValueFromAddress(quad.left_operand)
    # Si operando derecho es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    else:
        #Saca valor de operando derecho y asigna a rOp
        rOp = getValueFromAddress(quad.right_operand)
    #Compara lOp con rOp y asignar valor a result
    result = lOp >= rOp
    #Insertar int (0 o 1) en memoria temporal 
    tempMem.insertInt(result, quad.result)

def menorIgual(quad):
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        #Saca valor de operando izquierdo y asigna a  lOp
        lOp = getValueFromAddress(quad.left_operand)
    # Si operando derecho es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    else:
        #Saca valor de operando derecho y asigna a rOp
        rOp = getValueFromAddress(quad.right_operand)
    #Compara lOp con rOp y asignar valor a result
    result = lOp <= rOp
    #Insertar int (0 o 1) en memoria temporal 
    tempMem.insertInt(result, quad.result)

def diferenteA(quad):
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        #Saca valor de operando izquierdo y asigna a lOp
        lOp = getValueFromAddress(quad.left_operand)
    # Si operando derecho es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    else:
        #Saca valor de operando derecho y asigna a rOp
        rOp = getValueFromAddress(quad.right_operand)
    #Compara lOp con rOp y asignar valor a result
    result = (lOp != rOp)
    #Insertar int (0 o 1) en memoria temporal 
    tempMem.insertInt(result, quad.result)

def igualA(quad):
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        #Saca valor de operando izquierdo y asigna a lOp
        lOp = getValueFromAddress(quad.left_operand)
    # Si operando derecho es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    else:
        #Saca valor de operando derecho y asigna a rOp
        rOp = getValueFromAddress(quad.right_operand)
    #Compara lOp con rOp y asignar valor a result
    result = (lOp == rOp)
    #Insertar int (0 o 1) en memoria temporal
    tempMem.insertInt(result, quad.result)

def ORop(quad):
    #Se divide la direccion entre 1000
    res_address = quad.result // 1000
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        #Saca valor de operando izquierdo y asigna a lOp
        lOp = getValueFromAddress(quad.left_operand)
    # Si operando derecjp es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    else:
        #Saca valor de operando derecho y asigna a rOp
        rOp = getValueFromAddress(quad.right_operand)
    #Hace operacion OR con lOp y rOp y se asigna a result
    result = (lOp or rOp)
    #Si es int se inserta int en memoria temporal
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    #Si es float se inserta float en memoria temporal
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)
    #Si es char se inserta char en memoria temporal
    if res_address == 8:
        tempMem.insertChar(result, quad.result)

def ANDop(quad):
     #Se divide la direccion entre 1000
    res_address = quad.result // 1000
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        #Saca valor de operando izquierdo y asigna a lOp
        lOp = getValueFromAddress(quad.left_operand)
    # Si operando derecho es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.right_operand >= 12000:
        rOp = getValueFromAddress(getValueFromAddress(quad.right_operand))
    else:
        #Saca valor de operando derecho y asigna a rOp
        rOp = getValueFromAddress(quad.right_operand)
    #Hace operacion AND con lOp y rOp y se asigna a result
    result = (lOp and rOp)
    #Si es int se inserta int en memoria temporal
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    #Si es float se inserta float en memoria temporal
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)
    #Si es char se inserta char en memoria temporal
    if res_address == 8:
        tempMem.insertChar(result, quad.result)

def raizcuadrada(quad):
    #Se divide la direccion entre 1000
    res_address = quad.result // 1000
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    #Si operando izquierdo tiene otra direccion
    else:
        #Saca el valor del operando izquierdo
        lOp = getValueFromAddress(quad.left_operand)
    #Suma operando izquierdo mas operando derecho y guarda en result
    result = math.sqrt(lOp)
    #Si es int se inserta int en memoria temporal
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    #Si es float se inserta float en memoria temporal
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)
    #Si es char se inserta char en memoria temporal
    if res_address == 8:
        tempMem.insertChar(result, quad.result)

def gamma(quad):
    #Se divide la direccion entre 1000
    res_address = quad.result // 1000
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    #Si operando izquierdo tiene otra direccion
    else:
        #Saca el valor del operando izquierdo
        lOp = getValueFromAddress(quad.left_operand)
    #Suma operando izquierdo mas operando derecho y guarda en result
    result = math.gamma(lOp)
    #Si es int se inserta int en memoria temporal
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    #Si es float se inserta float en memoria temporal
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)
    #Si es char se inserta char en memoria temporal
    if res_address == 8:
        tempMem.insertChar(result, quad.result)

def logaritmo(quad):
    #Se divide la direccion entre 1000
    res_address = quad.result // 1000
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    #Si operando izquierdo tiene otra direccion
    else:
        #Saca el valor del operando izquierdo
        lOp = getValueFromAddress(quad.left_operand)
    #Suma operando izquierdo mas operando derecho y guarda en result
    result = math.log(lOp)
    #Si es int se inserta int en memoria temporal
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    #Si es float se inserta float en memoria temporal
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)
    #Si es char se inserta char en memoria temporal
    if res_address == 8:
        tempMem.insertChar(result, quad.result)

def logaritmoGamma(quad):
    #Se divide la direccion entre 1000
    res_address = quad.result // 1000
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    #Si operando izquierdo tiene otra direccion
    else:
        #Saca el valor del operando izquierdo
        lOp = getValueFromAddress(quad.left_operand)
    #Suma operando izquierdo mas operando derecho y guarda en result
    result = math.lgamma(lOp)
    #Si es int se inserta int en memoria temporal
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    #Si es float se inserta float en memoria temporal
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)
    #Si es char se inserta char en memoria temporal
    if res_address == 8:
        tempMem.insertChar(result, quad.result)

def grados(quad):
    #Se divide la direccion entre 1000
    res_address = quad.result // 1000
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    #Si operando izquierdo tiene otra direccion
    else:
        #Saca el valor del operando izquierdo
        lOp = getValueFromAddress(quad.left_operand)
    #Suma operando izquierdo mas operando derecho y guarda en result
    result = math.degrees(lOp)
    #Si es int se inserta int en memoria temporal
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    #Si es float se inserta float en memoria temporal
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)
    #Si es char se inserta char en memoria temporal
    if res_address == 8:
        tempMem.insertChar(result, quad.result)

def radianes(quad):
    #Se divide la direccion entre 1000
    res_address = quad.result // 1000
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    #Si operando izquierdo tiene otra direccion
    else:
        #Saca el valor del operando izquierdo
        lOp = getValueFromAddress(quad.left_operand)
    #Suma operando izquierdo mas operando derecho y guarda en result
    result = math.radians(lOp)
    #Si es int se inserta int en memoria temporal
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    #Si es float se inserta float en memoria temporal
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)
    #Si es char se inserta char en memoria temporal
    if res_address == 8:
        tempMem.insertChar(result, quad.result)

def seno(quad):
    #Se divide la direccion entre 1000
    res_address = quad.result // 1000
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    #Si operando izquierdo tiene otra direccion
    else:
        #Saca el valor del operando izquierdo
        lOp = getValueFromAddress(quad.left_operand)
    #Suma operando izquierdo mas operando derecho y guarda en result
    result = math.sin(lOp)
    #Si es int se inserta int en memoria temporal
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    #Si es float se inserta float en memoria temporal
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)
    #Si es char se inserta char en memoria temporal
    if res_address == 8:
        tempMem.insertChar(result, quad.result)

def coseno(quad):
    #Se divide la direccion entre 1000
    res_address = quad.result // 1000
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    #Si operando izquierdo tiene otra direccion
    else:
        #Saca el valor del operando izquierdo
        lOp = getValueFromAddress(quad.left_operand)
    #Suma operando izquierdo mas operando derecho y guarda en result
    result = math.cos(lOp)
    #Si es int se inserta int en memoria temporal
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    #Si es float se inserta float en memoria temporal
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)
    #Si es char se inserta char en memoria temporal
    if res_address == 8:
        tempMem.insertChar(result, quad.result)

def tangente(quad):
    #Se divide la direccion entre 1000
    res_address = quad.result // 1000
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    #Si operando izquierdo tiene otra direccion
    else:
        #Saca el valor del operando izquierdo
        lOp = getValueFromAddress(quad.left_operand)
    #Suma operando izquierdo mas operando derecho y guarda en result
    result = math.tan(lOp)
    #Si es int se inserta int en memoria temporal
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    #Si es float se inserta float en memoria temporal
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)
    #Si es char se inserta char en memoria temporal
    if res_address == 8:
        tempMem.insertChar(result, quad.result)


def redondearArriba(quad):
    #Se divide la direccion entre 1000
    res_address = quad.result // 1000
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    #Si operando izquierdo tiene otra direccion
    else:
        #Saca el valor del operando izquierdo
        lOp = getValueFromAddress(quad.left_operand)
    #Suma operando izquierdo mas operando derecho y guarda en result
    result = math.ceil(lOp)
    #Si es int se inserta int en memoria temporal
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    #Si es float se inserta float en memoria temporal
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)
    #Si es char se inserta char en memoria temporal
    if res_address == 8:
        tempMem.insertChar(result, quad.result)

def redondearAbajo(quad):
    #Se divide la direccion entre 1000
    res_address = quad.result // 1000
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    #Si operando izquierdo tiene otra direccion
    else:
        #Saca el valor del operando izquierdo
        lOp = getValueFromAddress(quad.left_operand)
    #Suma operando izquierdo mas operando derecho y guarda en result
    result = math.floor(lOp)
    #Si es int se inserta int en memoria temporal
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    #Si es float se inserta float en memoria temporal
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)
    #Si es char se inserta char en memoria temporal
    if res_address == 8:
        tempMem.insertChar(result, quad.result)

def pow(quad):
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

    result = math.pow(lOp,rOp)

    #Si es int se inserta int en memoria temporal
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    #Si es float se inserta float en memoria temporal
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)
    #Si es char se inserta char en memoria temporal
    if res_address == 8:
        tempMem.insertChar(result, quad.result)

def residuo(quad):
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

    result = math.remainder(lOp,rOp)

    #Si es int se inserta int en memoria temporal
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    #Si es float se inserta float en memoria temporal
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)
    #Si es char se inserta char en memoria temporal
    if res_address == 8:
        tempMem.insertChar(result, quad.result)

def cuadratica(quad):
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
    # Si operando derecho es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.result >= 12000:
        quadResult = getValueFromAddress(getValueFromAddress(quad.result))
    #Si operando derecho tiene otra direccion
    else:
        #Saca el valor del operando derecho
        quadResult = getValueFromAddress(quad.result)
  
    respuesta1 = (-rOp + (math.sqrt(math.pow(rOp, 2) - (4 * lOp * quadResult)))) / (2 * lOp)
    respuesta2 = (-rOp - (math.sqrt(math.pow(rOp, 2) - (4 * lOp * quadResult)))) / (2 * lOp)

    #Si es int se inserta int en memoria temporal
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    #Si es float se inserta float en memoria temporal
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)
    #Si es char se inserta char en memoria temporal
    if res_address == 8:
        tempMem.insertChar(result, quad.result)

    print(respuesta1)
    print(respuesta2)


def exponencial(quad):
    #Se divide la direccion entre 1000
    res_address = quad.result // 1000
    # Si operando izquierdo es apuntador a espacio de arreglo (direcciones 12000-12999)
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    #Si operando izquierdo tiene otra direccion
    else:
        #Saca el valor del operando izquierdo
        lOp = getValueFromAddress(quad.left_operand)
    #Suma operando izquierdo mas operando derecho y guarda en result
    result = math.exp(lOp)
    #Si es int se inserta int en memoria temporal
    if res_address == 6:
        tempMem.insertInt(result, quad.result)
    #Si es float se inserta float en memoria temporal
    if res_address == 7:
        tempMem.insertFloat(result, quad.result)
    #Si es char se inserta char en memoria temporal
    if res_address == 8:
        tempMem.insertChar(result, quad.result)

def leer(quad):
    address = quad.result // 1000
    input_val = input()
    if re.match(r'[0-9]+\.[0-9]+', input_val):
        input_val = float(input_val)
        if address == 1:
            globalMem.insertFloat(input_val, quad.result)
        elif address == 4:
            localMem.insertFloat(input_val, quad.result)
    elif re.match(r'[0-9]+', input_val):
        input_val = int(input_val)
        if address == 0:
            globalMem.insertInt(input_val, quad.result)
        elif address == 3:
            localMem.insertInt(input_val, quad.result)
    elif re.match(r'("(\\"|[^"])*")|(\'(\\\'|[^\'])*\')', input_val):
        input_val = input_val[1]
        if address == 2:
            globalMem.insertChar(input_val, quad.result)
        elif address == 5:
            localMem.insertChar(input_val, quad.result)
    elif re.match(r'("(\\"|[^"])?")|(\'(\\\'|[^\'])?\')', input_val):
        if address == 2:
            globalMem.insertChar(input_val, quad.result)
        elif address == 5:
            localMem.insertChar(input_val, quad.result)
    else:
        input_val = input_val[0]
        if address == 2:
            globalMem.insertChar(input_val, quad.result)
        elif address == 5:
            localMem.insertChar(input_val, quad.result)

#Mata la memoria y saca la "migajita"
def endFunc(quad):
    global localMem
    currentFunctionStack.pop()
    localMem = localMemStack.pop()
    #Saca migajita
    return functionReturnStack.pop()

def gotof(quad):
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        lOp = getValueFromAddress(quad.left_operand)
    if lOp == 0:
        return quad.result

def goto(quad):
    return quad.result

def gotofor(quad):
    conditionInt = Quadruples.quadruples[quad.result - 1].result
    localMem.insertInt(getValueFromAddress(conditionInt) + 1, conditionInt)
    return quad.result

#Brinco indondicional que cambia el instruction pointer a una linea especifica de codigo y ademas guarda la "migajita"
def gosub(quad):
    global newMem
    global localMem
    localMem = newMem
    #Guarda migajita
    functionReturnStack.append(quad.id + 1)
    return quad.result

#Genera nueva memoria para la llamada de funcion
def era(quad):
    localMemStack.append(localMem)
    global newMem
    newMem = Memory()
    currentFunctionStack.append(quad.left_operand)

#Asignar el valor actual al parametro
def param(quad):
    address = quad.result // 1000
    if quad.left_operand >= 12000:
        lOp = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        lOp = getValueFromAddress(quad.left_operand)
    #Asigna valor a parametro
    if address == 3:
        newMem.insertInt(lOp, quad.result)
    if address == 4:
        newMem.insertFloat(lOp, quad.result)
    if address == 5:
        newMem.insertChar(lOp, quad.result)    

#Return
def regresa(quad):
    address = quad.result // 1000
    rtn_address = Quadruples.quadruples[functionReturnStack[len(functionReturnStack) - 1]].result
    if quad.result >= 12000:
        rtnVal = getValueFromAddress(getValueFromAddress(quad.result))
    else:
        rtnVal = getValueFromAddress(quad.result)
    if address == 0 or address == 3 or address == 6 or address == 9:
        tempMem.insertInt(rtnVal, rtn_address)
        globalMem.insertInt(rtnVal, currentFunctionStack[len(currentFunctionStack) - 1])
    elif address == 1 or address == 4 or address == 7 or address == 10:
        tempMem.insertFloat(rtnVal, rtn_address)
        globalMem.insertFloat(rtnVal, currentFunctionStack[len(currentFunctionStack) - 1])
    else:
        tempMem.insertChar(rtnVal, rtn_address)
        globalMem.insertChar(rtnVal, currentFunctionStack[len(currentFunctionStack) - 1])
    newIndex = quad.id + 1
    if Quadruples.quadruples[newIndex].operator != "ENDFUNC":
        while Quadruples.quadruples[newIndex].operator != "ENDFUNC":
            newIndex += 1
        return newIndex

#Verifica que el indice de arreglo este dentro del rango correcto
def verifica(quad):
    arrType = quad.result // 1000
    if quad.left_operand >= 12000:
        verifica = getValueFromAddress(getValueFromAddress(quad.left_operand))
    else:
        verifica = getValueFromAddress(quad.left_operand)
    #Si operando izquierdo es mayor a resultado menos operando derecho dar error indice furea de rango
    if verifica > quad.result - quad.right_operand:
        print("Error en Compilación: Indice", verifica, "en arreglo está fuera de rango. Debe estar entre", quad.right_operand, "y", quad.result, ".")
        exit(0)
    if arrType == 3:
        localMem.adjustIntArrSize(quad.result)
    elif arrType == 4:
        localMem.adjustFloatArrSize(quad.result)
    elif arrType == 5:
        localMem.adjustCharArrSize(quad.result)

#Asignacion de arreglos
def arrayAssign(quad):
    arrType = quad.result["address"] // 1000
    #Calcular cuantas direcciones va a tener el arreglo multiplicando filas por columnas
    spacesToAssign = quad.left_operand["rows"] * quad.left_operand["cols"]
    leftOpAddress = quad.left_operand["address"]
    #Asigna valores a las direcciones
    for i in range(spacesToAssign):
        leftOp = getValueFromAddress(leftOpAddress)
        if arrType == 0:
            globalMem.insertInt(leftOp, quad.result["address"] + i)
        elif arrType == 1:
            globalMem.insertFloat(leftOp, quad.result["address"] + i)
        elif arrType == 2:
            globalMem.insertChar(leftOp, quad.result["address"] + i)
        elif arrType == 3:
            localMem.insertInt(leftOp, quad.result["address"] + i)
        elif arrType == 4:
            localMem.insertFloat(leftOp, quad.result["address"] + i)
        elif arrType == 5:
            localMem.insertChar(leftOp, quad.result["address"] + i)
        #Para asignar la siguiente "casilla"
        leftOpAddress += 1

def arraySuma(quad):
    arrType = quad.result // 1000
    #Calcular cuantas direcciones va a tener el arreglo multiplicando filas por columnas
    spacesToAdd = quad.left_operand["rows"] * quad.left_operand["cols"]
    #Ajusta tamaño 
    if quad.left_operand["address"] // 1000 == 3:
        localMem.adjustIntArrSize(quad.left_operand["address"] + spacesToAdd)
    elif quad.left_operand["address"] // 1000 == 4:
        localMem.adjustFloatArrSize(quad.left_operand["address"] + spacesToAdd)
    if quad.right_operand["address"] // 1000 == 3:
        localMem.adjustIntArrSize(quad.right_operand["address"] + spacesToAdd)
    elif quad.right_operand["address"] // 1000 == 4:
        localMem.adjustFloatArrSize(quad.right_operand["address"] + spacesToAdd)
    leftOpAddress = quad.left_operand["address"]
    rightOpAddress = quad.right_operand["address"]
    for i in range(spacesToAdd):
        #Saca valores de las direcciones
        leftOp = getValueFromAddress(leftOpAddress)
        rightOp = getValueFromAddress(rightOpAddress)
        #Hace la suma e inserta en memoria temporal
        if arrType == 6:
            tempMem.insertInt(leftOp + rightOp, quad.result + i)
        elif arrType == 7:
            tempMem.insertFloat(leftOp + rightOp, quad.result + i)
        #Direccion de siguientes indices
        leftOpAddress += 1
        rightOpAddress += 1

def arrayResta(quad):
    arrType = quad.result // 1000
     #Calcular cuantas direcciones va a tener el arreglo multiplicando filas por columnas
    spacesToSubtract = quad.left_operand["rows"] * quad.left_operand["cols"]
    #Ajusta tamaño 
    if quad.left_operand["address"] // 1000 == 3:
        localMem.adjustIntArrSize(quad.left_operand["address"] + spacesToSubtract)
    elif quad.left_operand["address"] // 1000 == 4:
        localMem.adjustFloatArrSize(quad.left_operand["address"] + spacesToSubtract)
    if quad.right_operand["address"] // 1000 == 3:
        localMem.adjustIntArrSize(quad.right_operand["address"] + spacesToSubtract)
    elif quad.right_operand["address"] // 1000 == 4:
        localMem.adjustFloatArrSize(quad.right_operand["address"] + spacesToSubtract)
    leftOpAddress = quad.left_operand["address"]
    rightOpAddress = quad.right_operand["address"]
    for i in range(spacesToSubtract):
        #Saca valores de las direcciones
        leftOp = getValueFromAddress(leftOpAddress)
        rightOp = getValueFromAddress(rightOpAddress)
         #Hace la resta e inserta en memoria temporal
        if arrType == 6:
            tempMem.insertInt(leftOp - rightOp, quad.result + i)
        elif arrType == 7:
            tempMem.insertFloat(leftOp - rightOp, quad.result + i)
         #Direccion de siguientes indices
        leftOpAddress += 1
        rightOpAddress += 1

def arrayMultiplica(quad):
    arrType = quad.result // 1000
    #Calcular cuantas direcciones va a tener el arreglo sacando el cuadrado de filas del arreglo1
    spacesToMultiply = quad.left_operand["rows"] * quad.left_operand["rows"]
    #Ajusta tamaño 
    if quad.left_operand["address"] // 1000 == 3:
        localMem.adjustIntArrSize(quad.left_operand["address"] + spacesToMultiply)
    elif quad.left_operand["address"] // 1000 == 4:
        localMem.adjustFloatArrSize(quad.left_operand["address"] + spacesToMultiply)
    if quad.right_operand["address"] // 1000 == 3:
        localMem.adjustIntArrSize(quad.right_operand["address"] + spacesToMultiply)
    elif quad.right_operand["address"] // 1000 == 4:
        localMem.adjustFloatArrSize(quad.right_operand["address"] + spacesToMultiply)
    leftOpAddress = quad.left_operand["address"]
    rightOpAddress = quad.right_operand["address"]
    #Genera matriz de misma dimension a matriz1 pero con ceros
    leftOpArray = np.zeros((quad.left_operand["rows"], quad.left_operand["cols"]))
    memoryIterator = 0
    #Meter los valores a la matriz nueva
    for i in range(quad.left_operand["cols"]):
        for j in range(quad.left_operand["rows"]):
            leftOpArray[j][i] = getValueFromAddress(leftOpAddress + memoryIterator)
            memoryIterator += 1
    memoryIterator = 0
    #Genera matriz de misma dimension a matriz2 pero con ceros
    rightOpArray = np.zeros((quad.right_operand["rows"], quad.right_operand["cols"]))
    #Meter los valores a la matriz nueva
    for i in range(quad.right_operand["cols"]):
        for j in range(quad.right_operand["rows"]):
            rightOpArray[j][i] = getValueFromAddress(rightOpAddress + memoryIterator)
            memoryIterator += 1
        #Hace multiplicacion de matrices
    resultArray = np.dot(leftOpArray, rightOpArray)
    memoryIterator = 0
    arrayIterator = 0
    #Mete la matriz resultante a memoria temporal
    for i in range(len(resultArray[0])):
        for j in range(len(resultArray)):
            if arrType == 6:
                tempMem.insertInt(int(resultArray[j][arrayIterator]), quad.result + memoryIterator)
                memoryIterator += 1
            elif arrType == 7:
                tempMem.insertFloat(resultArray[j][arrayIterator], quad.result + memoryIterator)
                memoryIterator += 1
        arrayIterator += 1

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
