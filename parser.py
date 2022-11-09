import lexer as lexer
import ply.yacc as yacc
from EstructurasDatos import *
from cuadruplos import *
from errores import Error
from maquinavirtual import maquina_virtual

tokens = lexer.tokens
arrMatId = Stack()
arrMatScope = Stack()


def p_program(t):
	'program : PROGRAMA ID globalTable PUNTOYCOMA declaration programFunc main'
	#print("Compilacion exitosa")
	#Mostrar variable table y directorio de funciones
	print()
	for i in functionDir:
		print("\tnombre de funcion: %s" % i)
		print("\t\ttipo: %s" % functionDir[i]["type"])
		print("\t\tvars: %s" % functionDir[i]["vars"])
		if "params" in functionDir[i]:
			print("\t\tparametros: %s" % functionDir[i]["params"].values())
			print("\t\tparamsLength: %d" % functionDir[i]["paramsLength"])
			print("\t\tstart: %d" % functionDir[i]["start"])
			print("\t\tvarLength: %d" % functionDir[i]["varLength"])
			print()
	print("\t\tconstants: %s" % variableTable["constants"])
	print("Lista de operandos: ")
	operands.print()
	print("Lista de tipos: ")
	types.print()
	#Imprimir cuadruplos
	Quadruples.print_all()
	#Imprimir tabla de variables
	'''variableTable.clear()'''

#GlobalTable: Inicializar programa y crear variableTable
def p_globalTable(t):
	'globalTable : '
	variableTable["constants"] = {}
	# Inicializar variableTable para global scope y definir nombre y tipo del programa
	variableTable[currentScope] = {}
	variableTable[currentScope][t[-1]] = {"type": "program"}
	# Inicializar functionDir para global scope
	functionDir[currentScope] = {}
	# Definir tipo y variables como referencia a variableTable["global"]
	functionDir[currentScope]["type"] = "void"
	functionDir[currentScope]["vars"] = variableTable[currentScope]
	#Cuadruplo inicial GOTO
	tmp_quad = Quadruple("GOTO", "_", "_", "_")
	#Hacer push al cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(tmp_quad)
	#Push al id del cuadruplo a pila de saltos
	Quadruples.push_jump(-1)

#Dar error sintactico    
def p_error(t):
	Error.syntax(t.value, t.lexer.lineno)

def p_main(t):
	'main : mainTable PRINCIPAL LEFTPAR RIGHTPAR LEFTBRACE declaration statement RIGHTBRACE'

#mainTable: Agregar main a varTable e inicializar propiedades de la funcion main. Actualizar cuadruplo main para saltar al inicio del programa
def p_mainTable(t):
	'mainTable : '
	global currentScope
	#Agrega main a currentScope varTable
	variableTable[currentScope]["main"] = {"type": "void"}
	currentScope = "main"
	# Inicializar variableTable y functionDir para main scope
	variableTable[currentScope] = {}
	functionDir[currentScope] = {}
	# Definir tipo de funcion y variables como referencia a variableTable["main"]
	functionDir[currentScope]["type"] = "void"
	functionDir[currentScope]["vars"] = variableTable[currentScope]
	#Actualizar cuadruplo inicio para que vaya a principal
	Quadruples.update_jump_quad(Quadruples.pop_jump(), Quadruples.next_id)


def p_programFunc(t):
	'''programFunc : function programFunc
				   | '''

#Assignment: Genera cuadruplo en el varTable correspondiente
def p_assignment(t):
	'''assignment : ID dimArray IGUAL hyperExpression PUNTOYCOMA
				  | ID dimArray IGUAL raizcuadrada
				  | ID dimArray IGUAL pow
				  | ID dimArray IGUAL exponencial
				  | ID dimArray IGUAL areaCirculo
				  | ID dimArray IGUAL perimetroCirculo
				  | ID dimArray IGUAL areaCuadrado
				  | ID dimArray IGUAL perimetroCuadrado
				  | ID dimArray IGUAL areaTriangulo
				  | ID dimArray IGUAL perimetroTriangulo
				  | ID dimArray IGUAL areaRectangulo
				  | ID dimArray IGUAL perimetroRectangulo
				  | ID dimArray IGUAL areaParalelogramo
				  | ID dimArray IGUAL perimetroParalelogramo'''
	# Si se tiene mas de 1 arrMatOperand
	if arrMatOperands.size() > 1:
		#Sacar tipo
		types.pop()
		#Sacar operandos de pila operandos
		operands.pop()
		operands.pop()
		#Sacar operandos de pila de operandos de arreglos
		assign = arrMatOperands.pop()
		address = arrMatOperands.pop()
		#Si no tiene el mismo tipo que la direccion, dar error type mismatch  
		if assign["type"] != address["type"]:
			Error.type_mismatch_array_assignment(t.lexer.lineno)
		#Si no tienen la misma dimension, marcar error de dimensiones.
		if assign["rows"] != address["rows"] or assign["cols"] != address["cols"]:
			Error.dimensions_do_not_match(t.lexer.lineno-1)
		#Si si tienen la misma dimension, generar cuadruplo
		temp_quad = Quadruple("ARR=", assign, "_", address)
		#Hacer push al cuadruplo a la lista de cuadruplos
		Quadruples.push_quad(temp_quad)
	#Si hay 1 arrMatOperand marcar error
	elif arrMatOperands.size() == 1:
		Error.invalid_assignment_to_array_variable(t.lexer.lineno-1)
		#Si id esta en el varTable del scope
	elif t[1] in variableTable[currentScope]:
		#Si son del mismo tipo
		if types.pop() == variableTable[currentScope][t[1]]["type"]:
			#Si es un arreglo
			if "rows" in variableTable[currentScope][t[1]]:
				#Sacar tipo de la pila de tipos
				types.pop()
				#Sacar operandos de la pila de operandos
				assign = operands.pop()
				address = operands.pop()
				#Generar cuadruplo
				temp_quad = Quadruple("=", assign, "_", address)
			#Si no es arreglo
			else:
				#Sacar tipo
				types.pop()
				#Sacar direccion de la tabla de variables
				address = variableTable[currentScope][t[1]]["address"]
				#Generar cuadruplo
				temp_quad = Quadruple("=", operands.pop(), '_', address)
				#Sacar operando de la pila de operandos
				operands.pop()
			#Hacer push al cuadruplo a la lista de cuadruplos
			Quadruples.push_quad(temp_quad)
		#Si los tipos no son compatibles marcar error type mismatch
		else:
			Error.type_mismatch(t[1],t.lexer.lineno - 1)
	# Si id esta en global scope
	elif t[1] in variableTable["global"]:
		#Si los tipos son iguales
		if types.pop() == variableTable["global"][t[1]]["type"]:
			#Si es arreglo
			if "rows" in variableTable["global"][t[1]]:
				#Sacar tipo de la pila de tipos
				types.pop()
				#Sacar operandos
				assign = operands.pop()
				address = operands.pop()
				#Generar cuadruplo
				temp_quad = Quadruple("=", assign, "_", address)
			else:
				#Sacar tipo de la pila de tipos
				types.pop()
				#Sacar direccion de la tabla de variables del scope global
				address = variableTable["global"][t[1]]["address"]
				#Generar cuadruplo
				temp_quad = Quadruple("=", operands.pop(), '_', address)
				#Sacar operando de la pila de oprandos
				operands.pop()
			#Hacer push al cuadruplo a la lista de cuadruplos
			Quadruples.push_quad(temp_quad)
		#Si los tipos no son compatibles marcar error type mismatch
		else:
			Error.type_mismatch(t[1],t.lexer.lineno - 1)
	#Si la variable no existe marcar error de variable indefinida
	else:
		Error.undefined_variable(t[1], t.lexer.lineno - 1)

#Declaration: Asignar cuadruplo start para una funcion.
def p_declaration(t):
	'''declaration : VAR declarationPrim
				   | '''
	#Asignar cuadruplo start para funcion
	functionDir[currentScope]["start"] = Quadruples.next_id

#primitive=Primitive Data Types
def p_declarationPrim(t):
	'''declarationPrim : primitive vars PUNTOYCOMA declarationPrim
					   | '''

#primitive: Cambiar el currentType por declaracion
def p_primitive(t):
	'''primitive : INT
				 | FLOAT
				 | CHAR '''
	global currentType
	currentType = t[1]
    

def p_return(t):
	'return : REGRESA LEFTPAR hyperExpression RIGHTPAR PUNTOYCOMA'

def p_if(t):
	'if : SI LEFTPAR hyperExpression RIGHTPAR createJQif ENTONCES LEFTBRACE statement RIGHTBRACE ifElse updateJQ'

#Jump Quad if: Checar tipo y valor de la expresion y generar cuadruplo para "saltar"
def p_createJQif(t):
	'createJQif : '
	#Sacar tipo de la expresion de la pila de tipos
	result_type = types.pop()
	#Checar tipo y valor de la expresion evaluada y generar cuadruplo
	if result_type == "int":
			#Sacar de la pila operandos
			res = operands.pop()
			#Generar GOTOF
			operator = "GOTOF"
			#Generar cuadruplo
			temp_quad = Quadruple(operator, res, '_', '_')
			#Hacer push a la lista de cuadruplos
			Quadruples.push_quad(temp_quad)
			#Hacer push al id del cuadruplo y hacer push a pila de saltos
			Quadruples.push_jump(-1)
	else: 
		#Type mismatch
		Error.condition_type_mismatch(t[1],t.lexer.lineno)

#Update Jump Quad: Actualiza el cuadruplo con el id del cuadruplo al que debe "saltar"
def p_updateJQ(t):
	'updateJQ : '
	#Actualizar cuadruplos GOTOF
	#Hacer POP al id del cuadruplo de la pila de saltos
	tmp_end = Quadruples.pop_jump()
	#Saca el id del siguiente cuadruplo (al que debe de saltar)
	tmp_count = Quadruples.next_id
	#Agrega id del cuadruplo al que debe ir el cuadruplo que va a saltar.
	Quadruples.update_jump_quad(tmp_end, tmp_count)

def p_ifElse(t):
	'''ifElse : SINO createJQelse LEFTBRACE statement RIGHTBRACE
			  | '''

#Jump Quad else: Crear cuadruplo de "salto" para else
def p_createJQelse(t):
	'createJQelse : '
	#Crear cuadruplo para else
	#Generar GOTO
	operator = "GOTO"
	tmp_quad = Quadruple(operator, '_', '_', '_')
	#Hacer push a la lista de cuadruplos
	Quadruples.push_quad(tmp_quad)
	#Hacer POP al id del cuadruplo de la pila de saltos
	tmp_false = Quadruples.pop_jump()
	tmp_count = Quadruples.next_id
	#Agrega id del cuadruplo de salto al cuadruplo
	Quadruples.update_jump_quad(tmp_false, tmp_count)
	#Hace push al id del cuadruplo y hace push al jump stack
	Quadruples.push_jump(-1)

def p_for(t):
	'for : PARA forAssignment HASTA pushJumpFor hyperExpression createQuadFor LEFTBRACE statement RIGHTBRACE updateQuadFor'

#pushJumpFor: Push al id del cuadruplo para "saltar" al stack de saltos.
def p_pushJumpFor(t):
	'pushJumpFor : '
	#Hace push al id del cuadruplo y hace push al jump stack
	Quadruples.push_jump(0)

#createQuadFor: Agregar GOTOF a cuadruplos
def p_createQuadFor(t):
	'createQuadFor : '
	#Sacar tipo del resultado de la pila de tipos
	result_type = types.pop()
	#Checar tipo y valor de la expresion y agregar cuadruplo al stack
	#Si tipo resultante es entero
	if result_type == "int":
			#Hacer pop a pila de operandos y asignar a res
			res = operands.pop()
			#Generar GOTOF
			operator = "GOTOF"
			#Generar cuadruplo
			temp_quad = Quadruple(operator, res, '_', '_')
			#Hacer push del cuadruplo a la lista de cuadruplos
			Quadruples.push_quad(temp_quad)
			#Hace push al id del cuadruplo y hacer push a pila de saltos
			Quadruples.push_jump(-1)
	#Si no es entero, generar error type mismatch
	else: 
		Error.type_mismatch(t[1],t.lexer.lineno)

#updateQuadFor: Actualizar cuadruplo GOTOF con el id del cuadruplo al cual debe "saltar"
def p_updateQuadFor(t):
	'updateQuadFor : '
	#Actualizar cuadruplo GOTOF cuando termine el for
	tmp_end = Quadruples.jump_stack.pop()
	tmp_rtn = Quadruples.jump_stack.pop()
	#Generar cuadruplo
	tmp_quad = Quadruple("GOTOFOR", "_", "_", tmp_rtn)
	#Hacer push del cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(tmp_quad)
	#Actualiza tmp_count a la cantidad de cuadruplos que haya en la lista de cuadruplos.
	tmp_count = Quadruples.next_id
	#Agrega id del cuadruplo de salto al cuadruplo
	Quadruples.update_jump_quad(tmp_end, tmp_count)

#forAssignment: Agrega iterador a la tabla de constantes y crea una variable iterativa
def p_forAssignment(t):
	'forAssignment : ID IGUAL CST_INT addTypeInt'
	#Se le asigna constant int al tipo de direccion
	address_type = "constantInt"
	cstAddress = 0
	#Si la variable no esta en tabla de constantes
	if t[3] not in variableTable["constants"]:
		#Se le asigna la direccion a la variable
		variableTable["constants"][t[3]] = {"address": addresses[address_type], "type": "int"}
		#Se le asigna a cstAddress la direccion dependiendo del tipo que sea la variable
		cstAddress = addresses[address_type]
		#Se le suma 1 para darselo a la siguiente variable
		addresses[address_type] += 1
	else:
		#Si si esta, se le asigna la direccion a cstAddress
		cstAddress = variableTable["constants"][t[3]]["address"]
	#Si no es arreglo
	if "rows" not in variableTable[currentScope][t[1]]:
		# Checar si id existe en currentscope y asignar valor
		if t[1] in variableTable[currentScope]:
			#Sacar direccion de varTable y asignar a address
			address = variableTable[currentScope][t[1]]["address"]
			#Generar cuadruplo 
			temp_quad = Quadruple("=", cstAddress, '_', address)
			#Hacer push al cuadruplo a la lista de cuadruplos
			Quadruples.push_quad(temp_quad)
		# Check si id existe en global scope y asignar valor
		elif t[1] in variableTable["global"]:
			#Sacar direccion de varTable y asignar a address
			address = variableTable["global"][t[1]]["address"]
			#Generar cuadruplo 
			temp_quad = Quadruple("=", t[3], '_', address)
			#Hacer push al cuadruplo a la lista de cuadruplos
			Quadruples.push_quad(temp_quad)
		#Si no existe, marcar error variable indefinida
		else:
			Error.undefined_variable(t[1], t.lexer.lineno)
	#Si es arreglo marcar error asignacion invalida
	else:
		Error.invalid_assignment_to_array_variable(t.lexer.lineno)


#pushLoop: Push al id del cuadruplo al stack de "saltos"
def p_pushLoop(t):
	'pushLoop : '
	#Hace push al id del siguiente cuadruplo disponible y hace push al jump stack
	Quadruples.push_jump(1)

#startLoop: Checar tipo del resultado de la expresion, generar cuadruplo y hacer push al id de salto al stack de salto.
def p_startLoop(t):
	'startLoop : '
	#Sacar tipo del resultado de la pila de tipos
	result_type = types.pop()
	#Checar tipo y valor de expresion y agregar cuadruplo al stack
	if result_type == "int":
		#Si es BOOLEANO
		#if operands.peek() == 1 or operands.peek() == 0:
			#Pop a pila de operandos y asignar a res
			res = operands.pop()
			#Generar Operador GOTOF
			operator = "GOTOF"
			# Generar cuadruplo y hacerle push a la lista de cuadruplos
			tmp_quad = Quadruple(operator, res, "_", "_")
			Quadruples.push_quad(tmp_quad)
			# Hacer push al id del cuadruplo y hacer push a pila de saltos
			Quadruples.push_jump(-1)
		#Si no es BOOLEANO, marcar error type mismatch.
		#else:
			#Error.type_mismatch(t[1],t.lexer.lineno)
	#Si el resultado no es INT, marcar error type mismatch
	else :
		Error.type_mismatch(t[1],t.lexer.lineno)

#endLoop: Generar cuadruplo despues de que el estatuto de while termine y actualizar el GOTOF con id al final del cuadruplo loop.
def p_endLoop(t):
	'endLoop : '
	#Hacer pop del id del cuadruplo que este en la pila de saltos
	false_jump = Quadruples.pop_jump()
	#Hacer pop del id del cuadruplo que este en la pila de saltos
	return_jump = Quadruples.pop_jump()
	#Generar cuadruplo cuando el while termine
	tmp_quad = Quadruple("GOTO", "_", "_", return_jump-1)
	#Hacer push del cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(tmp_quad)
	next_id = Quadruples.next_id
	#Actualizar GOTOF
	Quadruples.update_jump_quad(false_jump, next_id)

def p_comment(t):
	'comment : COMMENT_TEXT'

def p_while(t):
	'while : MIENTRAS pushLoop LEFTPAR hyperExpression RIGHTPAR startLoop LEFTBRACE statement RIGHTBRACE endLoop'

def p_vars(t):
	'vars : ID addVarsToTable varsArray varsComa'

#addVarsToTable: Agrega ID actual (y su tipo) a varTable 
def p_addVarsToTable(t):
	'addVarsToTable : '
	#Si el ID ya existe en el scope o global, dar error redefinicion de variable
	if t[-1] in variableTable[currentScope]:
		Error.redefinition_of_variable(t[-1], t.lexer.lineno)
	else:
		# Si no existe, agregar ID a variableTable[scope]
		variableTable[currentScope][t[-1]] = {"type": currentType}
		#Si el scope es global, el tipo de direccion va a ser global
		address_type = "global"
		#Si no es global, va a ser de tipo local
		if currentScope != "global":
			address_type = "local"
		#Si el tipo es entero, se le asigna la variable va a ser tipo+entero (localInt o globalInt)
		if currentType == "int":
			address_type += "Int"
		#Si el tipo es float, se le asigna la variable va a ser tipo+entero (localFloat o globalFloat)
		elif currentType == "float":
			address_type += "Float"
		#Si el tipo es char, se le asigna la variable va a ser tipo+entero (localChar o globalChar)
		else:
			address_type += "Char"
		#Se le asigna la direccion a la variable 
		variableTable[currentScope][t[-1]]["address"] = addresses[address_type]
		#Se le suma 1 para darselo a la siguiente variable que este dentro del scope
		addresses[address_type] += 1
		global arrMatId
		arrMatId = Stack()
		arrMatId.push(t[-1])

def p_varsComa(t):
	'''varsComa : COMA vars
				| '''

#Guarda la direccion base de una variable de arreglo en las constantes de la tabla de variables
def p_varsArray(t):
	'''varsArray : LEFTBRACK CST_INT addTypeInt RIGHTBRACK setRows varsMatrix 
				 | '''
	#Asigna tipo de direccion a global
	address_type = "global"
	const_address = "constant"
	#Si currentScope no es global, cambia el address type a local
	if currentScope != "global":
		address_type = "local"
	#Si tipo es entero, sera localInt y asigna constantInt a const_address
	if currentType == "int":
		address_type += "Int"
		const_address += "Int"
	#Si tipo es float, sera localFloat y asigna constantFloat a const_address
	if currentType == "float":
		address_type += "Float"
		const_address += "Float"
	#Si tipo es char, sera localChar y asigna constantChar a const_address
	if currentType == "char":
		address_type += "Char"
		const_address += "Char"
	global arrMatId
	#Asigna direccion al arreglo
	arrMatAddress = variableTable[currentScope][arrMatId.peek()]["address"]
	#Si el arreglo es de 1 dimension
	if "rows" in variableTable[currentScope][arrMatId.peek()] and "cols" not in variableTable[currentScope][arrMatId.peek()]:
		#Asigna el numero de filas a rows
		rows = variableTable[currentScope][arrMatId.peek()]["rows"]
		#Asigna como direccion la direccion actual mas la cantidad de filas (o elementos) - 1.
		addresses[address_type] += rows - 1
		#Mete la direccion en la tabla de variables
		variableTable["constants"][arrMatAddress] = {"address": addresses[const_address], "type": "int"}
		#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
		addresses[const_address] += 1
	#Si es de 2 dimensiones
	if "cols" in variableTable[currentScope][arrMatId.peek()]:
		#Asigna el numero de filas a rows
		rows = variableTable[currentScope][arrMatId.peek()]["rows"]
		#Asigna el numero de columnas a cols
		cols = variableTable[currentScope][arrMatId.peek()]["cols"]
		#Asigna como direccion la direccion actual mas (rows * cols) - 1.
		addresses[address_type] += rows * cols - 1
		#Mete la direccion en la tabla de variables
		variableTable["constants"][arrMatAddress] = {"address": addresses[const_address], "type": "int"}
		#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
		addresses[const_address] += 1
	#Saca el Id de la pila
	arrMatId.pop()

#Definir cantidad de filas para una variable dimensionada
def p_setRows(t):
	'setRows : '
	global arrMatId
	#Si la cantidad de filas es un numero positivo
	if int(t[-3]) > 0:
		#Le asigna el numero de filas al ID en la tabla de variables
		variableTable[currentScope][arrMatId.peek()]["rows"] = int(t[-3])
		#Saca operando de la pila
		operands.pop()
		#Saca tipo de la pila
		types.pop()
	#Si la cantidad de filas es un numero negativo
	else:
		Error.array_size_must_be_positive(arrMatId.peek(), t.lexer.lineno)

#Guarda la direccion base en las constantes de la tabla de variables
def p_varsMatrix(t):
	'''varsMatrix : LEFTBRACK CST_INT addTypeInt RIGHTBRACK setCols
				  | '''

#Definir cantidad de columnas para una variable dimensionada
def p_setCols(t):
	'setCols : '
	global arrMatId
	#Si el numero de columnas es positivo
	if int(t[-3]) > 0:
		#Asigna el numero de columnas al arreglo en la tabla de variables
		variableTable[currentScope][arrMatId.peek()]["cols"] = int(t[-3])
		#Sacar operando de la pila
		operands.pop()
		#Saca tipo de la pila
		types.pop()
	#Si el numero de columnas es negativo, dar error.
	else:
		Error.array_size_must_be_positive(arrMatId.peek(), t.lexer.lineno)

#function: Crea cuadruplo ENDFUNC y define tabla de variables locales.
def p_function(t):
	'function : functionType ID addFuncToDir LEFTPAR param RIGHTPAR setParamLength LEFTBRACE declaration statement RIGHTBRACE'
    #Resetear scope a global cuando se salga del scope de la funcion, eliminar varTable y referenciar en functionDir
	global currentScope
	# Crear cuadruplo endfuc para terminar funcion
	temp_quad = Quadruple("ENDFUNC", "_", "_", "_")
	#Hacer push del cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(temp_quad)
	# Variables temporales = longitud del cuadruplo de funcion al maximo
	functionDir[currentScope]["varLength"] = len(functionDir[currentScope]["vars"])
	#Resetear function quads
	Quadruples.function_quads = 0
	#Regresar scope a global
	currentScope = "global"
	#Una vez que termine la funcion, Resetear direcciones locales 
	addresses["localInt"] -= addresses["localInt"] % 1000
	addresses["localFloat"] -= addresses["localFloat"] % 1000
	addresses["localChar"] -= addresses["localChar"] % 1000
	global returnMade
	returnMade = False

def p_param(t):
	'''param : primitive ID addFuncParams functionParam
			 | '''

def p_functionParam(t):
	'''functionParam : COMA param
					 | '''

#addFuncParams: Agrega una lista de tipos de parametros al scope de la funcion.
def p_addFuncParams(t):
	'addFuncParams : '
	# Si parametro de la funcion ya existe en el scope, dar error redefinicion de variable
	if t[-1] in variableTable[currentScope]:
		Error.redefinition_of_variable(t[-1], t.lexer.lineno)
	else:
		# Si no existe, agregar parametro de la funcion a variableTable de currentScope
		variableTable[currentScope][t[-1]] = {"type": currentType}
		#Si el tipo es entero
		if currentType == "int":
			#Se agrega la direccion tipo localInt
			variableTable[currentScope][t[-1]]["address"] = addresses["localInt"]
			#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
			addresses["localInt"] += 1
		elif currentType == "float":
			#Se agrega la direccion tipo localFloat
			variableTable[currentScope][t[-1]]["address"] = addresses["localFloat"]
			#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
			addresses["localFloat"] += 1
		else:
			#Se agrega la direccion tipo localChar
			variableTable[currentScope][t[-1]]["address"] = addresses["localChar"]
			#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
			addresses["localChar"] += 1
		if "params" not in functionDir[currentScope]:
			functionDir[currentScope]["params"] = Queue()
		# Insertar currentTypes en params Queue
		functionDir[currentScope]["params"].enqueue(currentType)

#setParamLength: Asignar el numero de parametros en la funcion
def p_setParamLength(t):
	'setParamLength : '
	#Asignar el numero de parametro de la funcion al tamano del Queue params
	functionDir[currentScope]["paramsLength"] = functionDir[currentScope]["params"].size()

def p_functionType(t):
	'''functionType : FUNCION primitive
					| FUNCION VOID setVoidType'''

def p_cst_primitive(t):
	'''cst_primitive : CST_INT addTypeInt
				| CST_FLOAT addTypeFloat
				| CST_CHAR addTypeChar'''
	t[0] = t[1]

#addTypeInt: Guardar int en tabla de constantes y hacer push al operando al stack de operandos.
def p_addTypeInt(t):
	'addTypeInt : '
	#Push a int a la pila de tipos
	types.push("int")
	#Se le asigna constantInt al tipo de direccion
	address_type = "constantInt"
	#Si la variable no esta en la tabla de constantes
	if t[-1] not in variableTable["constants"]:
		#Asigna la direccion de tipo entero a la variable
		variableTable["constants"][t[-1]] = {"address": addresses[address_type], "type": "int"}
		#Se le hace push a la direccion a la pila de operandos
		operands.push(variableTable["constants"][t[-1]]["address"])
		#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
		addresses[address_type] += 1
	else:
		#Se le hace push a la direccion a la pila de operandos
		operands.push(variableTable["constants"][t[-1]]["address"])

#addTypeFloat: Guardar float en tabla de constantes y hacer push al operando al stack de operandos.
def p_addTypeFloat(t):
	'addTypeFloat : '
	#Push a float a la pila de tipos
	types.push("float")
	#Se le asigna constantFloat al tipo de direccion
	address_type = "constantFloat"
	#Si la variable no esta en la tabla de constantes
	if t[-1] not in variableTable["constants"]:
		#Asigna la direccion de tipo entero a la variable
		variableTable["constants"][t[-1]] = {"address": addresses[address_type], "type": "float"}
		#Se le hace push a la direccion a la pila de operandos
		operands.push(variableTable["constants"][t[-1]]["address"])
		#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
		addresses[address_type] += 1
	else:
		#Se le hace push a la direccion a la pila de operandos
		operands.push(variableTable["constants"][t[-1]]["address"])

#addTypeChar: Guardar char en tabla de constantes y hacer push al operando al stack de operandos.
def p_addTypeChar(t):
	'addTypeChar : '
	#Push a char a la pila de tipos
	types.push("char")
	#Se le asigna constantChar al tipo de direccion
	address_type = "constantChar"
	if t[-1] not in variableTable["constants"]:
		#Asigna la direccion de tipo entero a la variable
		variableTable["constants"][t[-1]] = {"address": addresses[address_type]}
		#Se le hace push a la direccion a la pila de operandos
		operands.push(variableTable["constants"][t[-1]]["address"])
		#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
		addresses[address_type] += 1
	else:
		#Se le hace push a la direccion a la pila de operandos
		operands.push(variableTable["constants"][t[-1]]["address"])

#addFuncToDir: Verifica tipo de funcion e inserta la funcion al directorio de funciones con tipo, varTable y parametros.
def p_addFuncToDir(t):
	'addFuncToDir : '
	# Si la funcion existe en global scope, dar error redefinicion de variable.
	if t[-1] in variableTable["global"]:
		Error.redefinition_of_variable(t[-1], t.lexer.lineno)
	else:
		#Si no existe
		global currentScope
		global currentType
		# Agregar funcion a variableTable de currentScope
		variableTable["global"][t[-1]] = {"type": currentType}
		#Si el tipo es entero
		if currentType == "int":
			#Se le asigna el tipo globalInt a la direccion
			address = addresses["globalInt"]
			#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
			addresses["globalInt"] += 1
		#Si el tipo es float
		elif currentType == "float":
			#Se le asigna el tipo globalFloat a la direccion
			address = addresses["globalFloat"]
			#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
			addresses["globalFloat"] += 1
		#Si el tipo es char
		elif currentType == "char":
			#Se le asigna el tipo globalChar a la direccion
			address = addresses["globalChar"]
			#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
			addresses["globalChar"] += 1
		#Si es void
		else:
			address = addresses["void"]
		variableTable["global"][t[-1]]["address"] = address
		# Cambiar scope al nuevo id de la funcion
		currentScope = t[-1]
		# Inicializar variableTable y functionDir por nuevo id de la funcion
		variableTable[currentScope] = {}
		functionDir[currentScope] = {}
		# Definir nuevo tipo de funcion y vars como referencia a variableTable[currentScope]
		functionDir[currentScope]["type"] = currentType
		functionDir[currentScope]["vars"] = variableTable[currentScope]
		functionDir[currentScope]["params"] = Queue()

def p_hyperExpression(t):
    '''hyperExpression : superExpression evaluateHyperExp opHyperExpression Expression2Nested
                       | superExpression opMatrix 
                       | superExpression evaluateHyperExp'''

def p_Expression2Nested(t):
    '''Expression2Nested : superExpression evaluateHyperExp opHyperExpression Expression2Nested
                             | superExpression evaluateHyperExp'''

#evaluateHyperExp: Evalua operador y operandos de expresiones booleanas del tipo AND Y or
def p_evaluateHyperExp(t):
	'evaluateHyperExp : '
	if operators.size() != 0:
		#Generar cuadruplos para and y or
		if operators.peek() == "|" or operators.peek() == "&":
			#Pop a pila de operandos
			rOp = operands.pop()
			lOp = operands.pop()
			#Pop a pila de operadores
			oper = operators.pop()
			#Pop a pila de tipos
			rType = types.pop()
			lType = types.pop()
			#Checar cubo semantico con tipos y operador
			resType = semanticCube[(lType, rType, oper)]
			#Checar tipo y valor, si no hay error
			if resType != "error":
				#Asignar temporal a tipo de direccion
				address_type = "temporal"
				#Si es entero, el tipo sera temporal entero
				if resType == "int":
					address_type += "Int"
				#Si es float, el tipo sera temporal float
				elif resType == "float":
					address_type += "Float"
				#Si es char, el tipo sera f char
				else:
					address_type += "Char"
				#Generar cuadruplo con operando, operadores y direccion
				temp_quad = Quadruple(oper, lOp, rOp, addresses[address_type])
				#Hacer push del cuadruplo a la lista de cuadruplos
				Quadruples.push_quad(temp_quad)
				#Hacer push de la direccion a la pila de operandos
				operands.push(addresses[address_type])
				#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
				addresses[address_type] += 1
				#Se le hace push al tipo de resultado a la pila de tipos.
				types.push(resType)
			#Dar error type mismatch en operacion
			else:
				Error.operation_type_mismatch(lOp, rOp,t.lexer.lineno)

def p_opHyperExpression(t):
    '''opHyperExpression : AND addOperator
                    | OR addOperator'''

def p_superExpression(t):
    '''superExpression : exp evaluateSuperExp opSuperExpression exp evaluateSuperExp
                       | exp evaluateSuperExp'''

def p_opSuperExpression(t):
	'''opSuperExpression : MAYOR_QUE addOperator
						 | MENOR_QUE addOperator
						 | MAYOR_IGUAL addOperator
						 | MENOR_IGUAL addOperator
						 | DIFERENTE_A addOperator 
						 | IGUAL_A addOperator'''

#evaluateSuperExp: Evalua operador y operandos de expresiones booleanas del tipo >, < , == , y <>.
def p_evaluateSuperExp(t):
	'evaluateSuperExp : '
	if operators.size() != 0:
		#Generar cuadruplos para operadores de comparacion
		if operators.peek() == ">" or operators.peek() == "<" or operators.peek() == "<>" or operators.peek() == "==" or operators.peek() == "<=" or operators.peek() == ">=":
			#Pop a pila de operandos
			rOp = operands.pop()
			lOp = operands.pop()
			#Pop a pila de operadores
			oper = operators.pop()
			#Pop a pila de tipos
			rType = types.pop()
			lType = types.pop()
			# Checar cubo semantico para tipos y operador
			resType = semanticCube[(lType, rType, oper)]
			# Checar tipo de resultado y evaluar expresion si no es error
			if resType != "error":
				#Asignar temporal a tipo de direccion
				address_type = "temporal"
				#Si es entero, el tipo sera temporal entero
				if resType == "int":
					address_type += "Int"
				#Si es float, el tipo sera temporal float
				elif resType == "float":
					address_type += "Float"
				#Si es char, el tipo sera temporal char
				else:
					address_type += "Char"
				#Generar cuadruplo con operando, operadores y direccion
				temp_quad = Quadruple(oper, lOp, rOp, addresses[address_type])
				#Hacer push del cuadruplo a la lista de cuadruplos
				Quadruples.push_quad(temp_quad)
				#Hacer push de la direccion a la pila de operandos
				operands.push(addresses[address_type])
				#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
				addresses[address_type] += 1
				#Se le hace push al tipo de resultado a la pila de tipos.
				types.push(resType)
			#Dar error type mismatch en operacion
			else:
				Error.operation_type_mismatch(lOp, rOp, t.lexer.lineno)

def p_opMatrix(t):
	'''opMatrix : EXCLAMACION addOperator
				| INTERROGACION addOperator
				| SIGNO_DOLAR addOperator '''

def p_exp(t):
	'''exp : term evaluateTerm expFunction
		   | term evaluateTerm '''

#evaluateTerm: evalua operador y operandos del tipo + y - para variables y variables dimensionadas.
def p_evaluateTerm(t):
	'evaluateTerm : '
	#Si si hay operadores
	if operators.size() != 0:
		# Si el operador es + o -
		if operators.peek() == "+" or operators.peek() == "-":
			# Sacar operandos de la pila y asignar a rOp y lOp
			rOp = operands.pop()
			lOp = operands.pop()
			# Sacar operador de la pila
			oper = operators.pop()
			# Sacar tipos de la pila y asignar a rType y lType
			rType = types.pop()
			lType = types.pop()
			# Checar cubo semantico con tipos y operador
			resType = semanticCube[(lType, rType, oper)]
			# Checar y validar tamaño y operandos del arreglo/matriz
			if arrMatOperands.size() > 1:
				rId = arrMatOperands.pop()
				lId = arrMatOperands.pop()
				# Validar dimensiones
				# Si no tiene columnas, asigna 1 al numero de columnas
				if "cols" not in lId:
					lId["cols"] = 1
				if "cols" not in rId:
					rId["cols"] = 1
				#Si las dimensiones son iguales
				if lId["rows"] == rId["rows"] and lId["cols"] == rId["cols"]:
					#Si el operador es +, cambiarlo a ARR+ para cuadruplo
					if oper == "+":
						oper = "ARR+"
					#Si el operador es -, cambiarlo a ARR- para cuadruplo
					else:
						oper = "ARR-"
					#Asignar Arreglo 1 a lOp
					lOp = {
						"address": lId["address"],
						"rows": lId["rows"],
						"cols": lId["cols"]
					}
					#Asignar Arreglo 2 a rOp
					rOp = {
						"address": rId["address"],
						"rows": rId["rows"],
						"cols": rId["cols"]
					}
				#Si las dimensiones no son iguales, marcar error dimensiones no compatibles.
				else:
					Error.dimensions_do_not_match(t.lexer.lineno)
			#Si solo hay 1 operando marcar error operacion invalida.
			elif arrMatOperands.size() == 1:
				Error.invalid_operation_in_line(t.lexer.lineno)
			# Checar tipo del resultado y evaluar la expresion
			#Si el tipo de resultado no es error
			if resType != "error":
				#Asignar temporal a tipo de direccion
				address_type = "temporal"
				#Si es int, asignar temporalInt a tipo de direccion
				if resType == "int":
					address_type += "Int"
				#Si es float, asignar temporalFloat a tipo de direccion
				elif resType == "float":
					address_type += "Float"
				#Si es int, asignar temporalChar a tipo de direccion
				else:
					address_type += "Char"
				#Genera cuadruplo 
				temp_quad = Quadruple(oper, lOp, rOp, addresses[address_type])
				#Hace push al cuadruplo a la lista de cuadruplos
				Quadruples.push_quad(temp_quad)
				#Hace push a la direccion a la pila de operandos
				operands.push(addresses[address_type])
				#Si el operador es ARR+ o ARR-
				if oper == "ARR+" or oper == "ARR-":
					#Hace push al arreglo a la pila de operandos
					arrMatOperands.push({
						"address": addresses[address_type],
						"rows": lOp["rows"],
						"cols": lOp["cols"],
						"type": resType
					})
					#Multiplica filas y columnas para saber en que direccion empieza la siguiente variable
					addresses[address_type] += lOp["rows"] * lOp["cols"]
				#Si el operador es otro diferente a ARR+ o ARR-
				else:
					#Se le suma 1 a la direccion para darselo a la siguiente variable de ese tipo
					addresses[address_type] += 1
				#Hace push al tipo de resultado a la pila de tipos
				types.push(resType)
			#Si el tipo de resultado da Error dar type mismatch.
			else:
				Error.operation_type_mismatch(t.lexer.lineno)


def p_expFunction(t):
    '''expFunction : MAS addOperator exp
                   | MENOS addOperator exp '''

#setVoidType: Define tipo de funcion como Void
def p_setVoidType(t):
	'setVoidType : '
	# Definir void como currentType
	global currentType
	currentType = t[-1]

def p_term(t):
        '''term : factor evaluateFactor termFunction
            | factor evaluateFactor'''

#evaluateFactor: Evalua operador y operandos el tipo * y / para variables y variables dimensionadas (multiplicacion)
def p_evaluateFactor(t):
	'evaluateFactor : '
	#Si si hay operadores
	if operators.size() != 0:
		# Si el operador es * o /
		if operators.peek() == "*" or operators.peek() == "/":
			# Sacar operandos de la pila
			rOp = operands.pop()
			lOp = operands.pop()
			# Sacar operador de la pila
			oper = operators.pop()
			# Sacar tipos de la pila y asignar a rType y lType
			rType = types.pop()
			lType = types.pop()
			# Checar cubo semantico con operador y tipos
			resType = semanticCube[(lType, rType, oper)]
			# Checar y validar tamaño y operandos del arreglo/matriz
			if arrMatOperands.size() > 1:
				rId = arrMatOperands.pop()
				lId = arrMatOperands.pop()
				# Validar dimensiones
				# Si no tiene columnas, asigna 1 al numero de columnas
				if "cols" not in lId:
					lId["cols"] = 1
				if "cols" not in rId:
					rId["cols"] = 1
				#Si las dimensiones son iguales
				if lId["cols"] == rId["rows"]:
					#Si el operador es *, cambiarlo a ARR* para cuadruplo
					if oper == "*":
						oper = "ARR*"
					#Si el operador es diferente, marcar error operador invalido en arreglos
					else:
						Error.invalid_operator_on_arrays(t.lexer.lineno)
					#Asignar Arreglo 1 a lOp
					lOp = {
						"address": lId["address"],
						"rows": lId["rows"],
						"cols": lId["cols"]
					}
					#Asignar Arreglo 2 a lOp
					rOp = {
						"address": rId["address"],
						"rows": rId["rows"],
						"cols": rId["cols"]
					}
				#Si no el numero de columnas de arreglo 1 es diferente a numero de renglones del arreglo 2 marcar error operacion invalida
				else:
					Error.invalid_operation_in_line(t.lexer.lineno)
			#Si solo hay 1 operando marcar error operacion invalida.
			elif arrMatOperands.size() == 1:
				Error.invalid_operation_in_line(t.lexer.lineno)
			# Checar tipo de resultado, si no es error
			if resType != "error":
				#Asignar temporal a address type
				address_type = "temporal"
				#Si es entero, asignar temporalInt
				if resType == "int":
					address_type += "Int"
				#Si es float, asignar temporalFloat
				elif resType == "float":
					address_type += "Float"
				#Si es char, asignar temporal Char
				else:
					address_type += "Char"
				#Generar cuadruplo
				temp_quad = Quadruple(oper, lOp, rOp, addresses[address_type])
				#Meter cuadruplo a la lista de cuadruplos
				Quadruples.push_quad(temp_quad)
				#Meter direccion a la pila de operandos
				operands.push(addresses[address_type])
				#Si el operador es ARR*
				if oper == "ARR*":
					#Mete al arreglo a la pila de operandos
					arrMatOperands.push({
						"address": addresses[address_type],
						"rows": lOp["rows"],
						"cols": rOp["cols"],
						"type": resType
					})
					#Multiplica filas y columnas para saber en que direccion empieza la siguiente variable
					addresses[address_type] += lOp["rows"] * rOp["cols"]
				#Mete el tipo de resultado a la pila de tipos
				types.push(resType)
			#Si resType es error marcar error type mismatch.
			else:
				Error.operation_type_mismatch(t.lexer.lineno)
				
def p_termFunction(t):
	'''termFunction : MULTIPLICA addOperator term
					| DIVIDE addOperator term '''

#addOperator: Push a operador read al stack de operadores
def p_addOperator(t):
	'addOperator : '
	operators.push(t[-1])

def p_factor(t):
	'''factor : LEFTPAR addFF hyperExpression RIGHTPAR removeFF
			  | cst_primitive
			  | module
			  | ID dimArray'''

def p_addFF(t):
	'addFF : '
	operators.push("(")

def p_removeFF(t):
	'removeFF : '
	operators.pop()


#def p_addOperand(t):
	#'addOperand : '
	#operands.push(t[-1])

#addTypeId: ***
def p_addTypeId(t):
	'addTypeId : '
	# Si la variable existe en la tabla de variables
	if arrMatId.peek() in variableTable[currentScope]:
		#Hace push al tipo a la pila de tipos
		types.push(variableTable[currentScope][arrMatId.peek()]["type"])
	# Si la variable existe en la tabla de variables globales
	elif arrMatId.peek() in variableTable["global"]:
		#Hace pusha al tipo de la variable global a la pila de tipos
		types.push(variableTable["global"][arrMatId.peek()]["type"])
	#Si la variable no existe marcar error variable indefinida
	else:
		Error.undefined_variable(arrMatId.peek(), t.lexer.lineno)

#addOperandId: Mete el ID del arreglo a la pila de IDs de array y el scope a la pila de scopes.
def p_addOperandId(t):
	'addOperandId : '
	# Agrega variable a la pila
	arrMatId.push(t[-1])
	# Agrega direccion del operando del scope a pila de operandos, si es que existe
	if arrMatId.peek() in variableTable[currentScope]:
		operands.push(variableTable[currentScope][arrMatId.peek()]["address"])
		arrMatScope.push(currentScope)
	# Agrega direccion del operando del scope global a pila de operandos, si es que existe
	elif arrMatId.peek() in variableTable["global"]:
		operands.push(variableTable["global"][arrMatId.peek()]["address"])
		arrMatScope.push("global")
	#Si no existe, marcar error variable indefinida
	else:
		Error.undefined_variable(arrMatId.peek(), t.lexer.lineno)
	#Si es un arreglo
	if "rows" in variableTable[arrMatScope.peek()][t[-1]]:
		#Si es un arreglo de una dimension (sin columnas)
		if "cols" not in variableTable[arrMatScope.peek()][t[-1]]:
			#Asignar arreglo a variable
			variable = variableTable[arrMatScope.peek()][t[-1]]
			#Meter operandos a la pila
			arrMatOperands.push({
				#Asignar la direccion a address
				"address": variable["address"],
				#Asignar la cantidad de filas a rows
				"rows": variable["rows"],
				#Asignar 1 a cols
				"cols": 1
			})
		#Si si es arreglo de 2 dimensiones, meterlo a la pila de operandos.
		else:
			arrMatOperands.push(variableTable[arrMatScope.peek()][t[-1]])


def p_read(t):
	'read : LEE LEFTPAR id_list RIGHTPAR PUNTOYCOMA'

def p_id_list(t):
	'''id_list : ID dimArray addRead id_listFunction'''

def p_id_listFunction(t):
	'''id_listFunction : COMA id_list
					   | '''

#addRead: Genera un cuadruplo read y le hace push a la lista de cuadruplos
def p_addRead(t):
	'addRead : '
	#Si al variable esta en la tabla de variables
	if t[-2] in variableTable[currentScope]:
		#Saca la direccion de la variable y se la asigna a address
		address = variableTable[currentScope][t[-2]]["address"]
		#Se crea el cuadruplo LEE con la direccion
		temp_quad = Quadruple("lee", '_', '_', address)
		#Se hace push al cuadruplo a la lista de cuadruplos
		Quadruples.push_quad(temp_quad)
	#Si al variable esta en la tabla de variables globales
	elif t[-2] in variableTable["global"]:
		#Saca la direccion de la variable y se la asigna a address
		address = variableTable["global"][t[-2]]["address"]
		#Se crea el cuadruplo LEE con la direccion
		temp_quad = Quadruple("lee", '_', '_', address)
		#Se hace push al cuadruplo a la lista de cuadruplos
		Quadruples.push_quad(temp_quad)
	#Si no existe, marcar error variable indefinida
	else:
		Error.undefined_variable(t[-2], t.lexer.lineno)

def p_print(t):
	'''print : IMPRIME LEFTPAR printFunction RIGHTPAR PUNTOYCOMA
			 | IMPRIME LEFTPAR raizcuadrada addPrint RIGHTPAR PUNTOYCOMA
			 | IMPRIME LEFTPAR pow addPrint RIGHTPAR PUNTOYCOMA
			 | IMPRIME LEFTPAR exponencial addPrint RIGHTPAR PUNTOYCOMA
			 | IMPRIME LEFTPAR areaCirculo addPrint RIGHTPAR PUNTOYCOMA
			 | IMPRIME LEFTPAR perimetroCirculo addPrint RIGHTPAR PUNTOYCOMA
			 | IMPRIME LEFTPAR areaCuadrado addPrint RIGHTPAR PUNTOYCOMA
			 | IMPRIME LEFTPAR perimetroCuadrado addPrint RIGHTPAR PUNTOYCOMA
			 | IMPRIME LEFTPAR areaTriangulo addPrint RIGHTPAR PUNTOYCOMA
			 | IMPRIME LEFTPAR perimetroTriangulo addPrint RIGHTPAR PUNTOYCOMA
			 | IMPRIME LEFTPAR areaRectangulo addPrint RIGHTPAR PUNTOYCOMA
			 | IMPRIME LEFTPAR perimetroRectangulo addPrint RIGHTPAR PUNTOYCOMA
			 | IMPRIME LEFTPAR areaParalelogramo addPrint RIGHTPAR PUNTOYCOMA
			 | IMPRIME LEFTPAR perimetroParalelogramo addPrint RIGHTPAR PUNTOYCOMA'''

def p_printFunction(t):
	'''printFunction : print_param COMA printFunction2
					 | print_param '''

def p_printFunction2(t):
	'printFunction2 : printFunction'

#addPrint: Genera un cuadruplo print y le hace push a la lista de cuadruplos
def p_addPrint(t):
	'addPrint : '
	#Genera cuadruplo print
	temp_quad = Quadruple("imprime", '_', '_', operands.pop())
	#Hace push al cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(temp_quad)
	#Pop a la pila de tipos
	types.pop()


def p_print_param(t):
	'''print_param : hyperExpression addPrint
				   | CST_STRING addPrintString '''

#addPrintString: Lee un string y lo guarda en la tabla de constantes para luego imprimpirlo con el operador PRINT
def p_addPrintString(t):
	'addPrintString : '
	address = 0
	stringToPrint = t[-1][1:len(t[-1]) - 1]
	#Si el string no esta en la tabla de variables constantes
	if stringToPrint not in variableTable["constants"]:
		#Saca la direccion de la variable y se la asigna a stringToPrint
		variableTable["constants"][stringToPrint] = {"address": addresses["cChar"]}
		#Se le asigna esa direccion a address
		address = variableTable["constants"][stringToPrint]["address"]
		#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
		addresses["cChar"] += 1
	else:
		#Se le asigna la direccion de la variable a address
		address = variableTable["constants"][stringToPrint]["address"]
	#Genera cuadruplo imprime con la direccion del string
	temp_quad = Quadruple("imprime", '_', '_', address)
	#Se hace push al cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(temp_quad)

def p_checkVoidType(t):
	'checkVoidType : '
	global currentScope
	#Si el tipo de la funcion es void, marcar error return en funcion void
	if functionDir[currentScope]["type"] == "void":
		Error.return_on_void_function(0, t.lexer.lineno)
	#Saca tipo de la pila de tipos, es igual al tipo de la funcion
	if types.pop() == functionDir[currentScope]["type"]:
		#Genera cuadruplo REGRESA
		tmp_quad = Quadruple("REGRESA", "_", "_", operands.pop())
		#Hace push al cuadruplo a la lista de cuadruplos
		Quadruples.push_quad(tmp_quad)
		global returnMade
		returnMade = True
	#Si el tipo no es igual, marcar error type mismatch en return
	else:
		Error.type_mismatch_on_return(t.lexer.lineno)
	
def p_checkNonVoidType(t):
	'checkNonVoidType : '
	#Si el tipo de la funcion no es void, marcar error no hay return en funcion
	if functionDir[currentScope]["type"] != "void":
		Error.no_return_on_function(0, t.lexer.lineno)

def p_module(t):
	'module : ID checkFunctionExists generateERASize LEFTPAR moduleFunction nullParam RIGHTPAR generateGosub'

#checkFunctionExists: Verifica que la funcion existe en el directorio de Funciones y le hace push al operador del modulo al stack.
def p_checkFunctionExists(t):
	'checkFunctionExists : '
	#Si la funcion no esta en functionDir, marcar error modulo indefinido
	if t[-1] not in functionDir:
		Error.undefined_module(t[-1], t.lexer.lineno)
	#Si si, asignar nombre a la funcion
	global funcName
	funcName = t[-1]
	#Hace push a modulo a la pila de operadores
	operators.push("modulo")
	#Hacer push del tipo de la funcion a la pila de tipos
	types.push(functionDir[funcName]["type"])

#generateERASize: Crea el cuadruplo ERA con el directorio de la funcion que sera llamada.
def p_generateERASize(t):
	'generateERASize : '
	#Generar tamano ERA pendiente...
	global funcName
	#Generar cuadruplo ERA con su direccion
	tmp_quad = Quadruple("ERA", variableTable["global"][funcName]["address"], "_", "_")
	#Hacer push al cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(tmp_quad)
	global paramNum
	paramNum = 1


#nullParam: Lanza error si falta un parametro en una llamada de funcion
def p_nullParam(t):
	'nullParam : '
	global paramNum
	global funcName
	#Si params de la funcion es mayor que la cantidad de argumentos que el usuario esta dando, dar error
	if paramNum < len(functionDir[funcName]["params"].values()):
		Error.unexpected_number_of_arguments(funcName, t.lexer.lineno)

#generateGosub: Crea el cuadruplo Gosub con la direccion de la funcion a llamar **
def p_generateGosub(t):
	'generateGosub : '
	global funcName
	#Generar cuadruplo GOSUB
	tmp_quad = Quadruple("GOSUB", variableTable["global"][funcName]["address"], "_", functionDir[funcName]["start"])
	#Hacer push del cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(tmp_quad)
	#PARCHE GUADALUPANO
	#Si el tipo de la funcion no es void
	if functionDir[funcName]["type"] != "void":
		#Si es entero
		if functionDir[funcName]["type"] == "int":
			#La direccion va a ser tipo temporal entero
			tmpAddress = addresses["temporalInt"]
			#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
			addresses["temporalInt"] += 1
		#Si es float
		if functionDir[funcName]["type"] == "float":
			#La direccion va a ser tipo temporal float
			tmpAddress = addresses["temporalFloat"]
			#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
			addresses["temporalFloat"] += 1
		#Si es char
		if functionDir[funcName]["type"] == "char":
			#La direccion va a ser tipo temporal char
			tmpAddress = addresses["temporalChar"]
			#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
			addresses["temporalChar"] += 1
		#Genera cuadruplo con la direccion de la funcion y tmpAddress
		tmp_quad = Quadruple("=", variableTable["global"][funcName]["address"], "_", tmpAddress)
		#Se le hace push al cuadruplo a la lista de cuadruplos
		Quadruples.push_quad(tmp_quad)
		#Se le hace push a direccion temporal a la pila de operandos
		operands.push(tmpAddress)
		#Se le hace push al tipo de la funcion a la pila de tipos
		types.push(variableTable["global"][funcName]["type"])
	#Se saca el operador de la pila de operadores
	operators.pop()

#generateParam: Crea el cuadruplo PARAM con el opreando que esta siendo leido.
def p_generateParam(t):
	'generateParam : '
	global funcName
	global paramNum
	#Pop a pila de operandos y se lo asigna a argumento
	arg = operands.pop()
	#Pop a la pila de tipos y se lo asigna a tipo de argumento
	argType = types.pop()
	#Saca la lista de parametros de la funcion
	paramList = functionDir[funcName]["params"].values()
	counter = paramNum
	#Si tiene mas argumentos de los que debe tener, lanzar error
	if paramNum > len(paramList):
		Error.unexpected_number_of_arguments(funcName, t.lexer.lineno)
	#Si los tipos son los correctos
	if argType == paramList[-paramNum]:
		for var in functionDir[funcName]["vars"]:
			if counter == 1:
				address = functionDir[funcName]["vars"][var]["address"]
			counter -= 1
		#Generar cuadruplo con PARAM
		tmp_quad = Quadruple("PARAM", arg, '_', address)
		#Hacer push al cuadruplo a la lista de cuadruplos
		Quadruples.push_quad(tmp_quad)
	#Si los argumentos no son del tipo esperado lanzar error type mismatch
	else:
		Error.type_mismatch_module(funcName, t.lexer.lineno)

#nextParam: agrega 1 al iterador de param.
def p_nextParam(t):
	'nextParam : '
	global paramNum
	paramNum += 1

def p_dimArray(t):
	'''dimArray : addOperandId addTypeId LEFTBRACK readIDType hyperExpression verifyRows RIGHTBRACK dimMatrix
				| addOperandId addTypeId '''
	global arrMatId
	arrMatId.pop()
	arrMatScope.pop()

def p_readIDType(t):
	'readIDType : '
	#Se saca el operando de la pila de operandos
	operands.pop()
	#Se hace push a la pila de operadores a Mat
	operators.push("Mat")
	#Se saca operando de la pila de operandos
	arrMatOperands.pop()
	#Si la variable existe en la tabla de variables
	if arrMatId.peek() in variableTable[currentScope]:
		#Se saca el tipo de la pila y si no es igual al de la variable, marcar error type mismatch
		if types.pop() != variableTable[currentScope][arrMatId.peek()]["type"]:
			Error.type_mismatch(arrMatId.peek(), t.lexer.lineno)
		#Si la variable no tiene filas (no es arreglo), marcar error.
		if "rows" not in variableTable[currentScope][arrMatId.peek()]:
			Error.variable_not_subscriptable_as_array(arrMatId.peek(), t.lexer.lineno)
	#Si la variable existe en la tabla de variables globales
	elif arrMatId.peek() in variableTable["global"]:
		#Se saca el tipo de la pila y si no es igual al de la variable, marcar error type mismatch
		if types.pop() != variableTable["global"][arrMatId.peek()]["type"]:
			Error.type_mismatch(arrMatId.peek(), t.lexer.lineno)
		#Si la variable no tiene filas (no es arreglo), marcar error.
		if "rows" not in variableTable["global"][arrMatId.peek()]:
			Error.variable_not_subscriptable_as_array(arrMatId.peek(), t.lexer.lineno)

def p_statement(t):
	'''statement : return checkVoidType
				 | if statement
				 | comment statement
				 | read statement
				 | print statement
				 | assignment statement
				 | module PUNTOYCOMA statement
				 | for statement
				 | raizcuadrada statement
				 | areaCirculo statement
				 | perimetroCirculo statement
				 | areaCuadrado statement
				 | perimetroCuadrado statement
				 | pow statement
				 | areaTriangulo statement
				 | areaRectangulo statement
				 | perimetroRectangulo statement
				 | areaParalelogramo statement
				 | perimetroParalelogramo statement
				 | exponencial statement
				 | cuadratica statement
				 | perimetroTriangulo statement
				 | while statement 
				 | checkNonVoidType'''

#Genera el cuadruplo verify del indice utilizado para verificar que este dentro del rango correcto de numero de filas
def p_verifyRows(t):
	'verifyRows : '
	#Si el tipo no es entero, marcar error type mismatch en indice
	if types.pop() != "int":
		Error.type_mismatch_in_index(arrMatId.peek(), t.lexer.lineno)
	#Saca direccion y asignar a baseAdd (direccion base)
	baseAdd = variableTable[arrMatScope.peek()][arrMatId.peek()]["address"]
	#Calcular limite superior
	upperLim = baseAdd + variableTable[arrMatScope.peek()][arrMatId.peek()]["rows"] - 1
	#Generar cuadruplo VERIFY con direccion base y limite superior
	tmp_quad = Quadruple("VERIFY", operands.peek(), baseAdd, upperLim)
	#Meter cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(tmp_quad)

#Genera cuadruplo para agregar la direccion base y la constante del indice para acceder al espacio de memoria correcto
def p_dimMatrix(t):
	'''dimMatrix : LEFTBRACK hyperExpression verifyCols RIGHTBRACK
				 | checkMatAsArray '''
	#Sacar operador de la pila
	operators.pop()
	#Asignar temporal como tipo de direccion
	address_type = "temporal"
	#Si el tipo del ID es int cambiar a temporalInt
	if variableTable[arrMatScope.peek()][arrMatId.peek()]["type"] == "int":
		address_type += "Int"
	#Si el tipo del ID es float cambiar a temporalFloat
	elif variableTable[arrMatScope.peek()][arrMatId.peek()]["type"] == "float":
		address_type += "Float"
	#Si el tipo del ID es Char cambiar a temporalChar
	else:
		address_type += "Char"
	#Sacar direccion del arreglo y asignar a direccion base
	baseAdd = variableTable[arrMatScope.peek()][arrMatId.peek()]["address"]
	#Sacar direccion de la direccion base y asignar a addressCst
	addressCst = variableTable["constants"][baseAdd]["address"]
	#Generar cuadruplo con temporal pointer
	tmp_quad = Quadruple("+", addressCst, operands.pop(), addresses["temporalPoint"])
	#Meter cuadruplo a la pila de cuadruplos
	Quadruples.push_quad(tmp_quad)
	#Meter temporal pointer a la pila de operandos
	operands.push(addresses["temporalPoint"])
	#Meter tipo del ID a la pila de tipos
	types.push(variableTable[arrMatScope.peek()][arrMatId.peek()]["type"])
	#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
	addresses["temporalPoint"] += 1

#Genera el cuadruplo verify del indice utilizado para verificar que este dentro del rango correcto de numero de columnas
def p_verifyCols(t):
	'verifyCols : '
	#Si la variable no tiene columnas marcar error
	if "cols" not in variableTable[arrMatScope.peek()][arrMatId.peek()]:
		Error.variable_not_subscriptable_as_matrix(arrMatId, t.lexer.lineno)
	#Si el tipo no es int, marcar error type mismatch
	if types.pop() != "int":
		Error.type_mismatch_in_index(arrMatId.peek(),t.lexer.lineno)
	# Formula para calculo de direccion para arreglos C-style
	#Saca numero de filas como string y asigna a constant_value
	constant_value = str(variableTable[arrMatScope.peek()][arrMatId.peek()]["rows"])
	cstIntAddr = variableTable["constants"][constant_value]["address"]
	#Genera cuadruplo
	tmp_quad = Quadruple("*", operands.pop(), cstIntAddr, addresses["temporalInt"])
	#Mete cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(tmp_quad)
	#Mete direccion temporal a pila de operandos
	operands.push(addresses["temporalInt"])
	#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
	addresses["temporalInt"] += 1
	#Genera cuadruplo
	tmp_quad = Quadruple("+", operands.pop(), operands.pop(), addresses["temporalInt"])
	#Mete cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(tmp_quad)
	#Mete direccion temporal a la pila de operandos
	operands.push(addresses["temporalInt"])
	#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
	addresses["temporalInt"] += 1
	#Sacar direccion base
	baseAdd = variableTable[currentScope][arrMatId.peek()]["address"]
	#Calcular limite superior
	upperLim = baseAdd + variableTable[currentScope][arrMatId.peek()]["rows"] * variableTable[currentScope][arrMatId.peek()]["cols"] - 1
	#Generar cuadruplo
	tmp_quad = Quadruple("VERIFY", operands.peek(), baseAdd, upperLim)
	#Meter cuadruplo a la pila de cuadruplos
	Quadruples.push_quad(tmp_quad)

#Dar error si una matriz solo tiene un indice 
def p_checkMatAsArray(t):
	'checkMatAsArray : '
	global arrMatId
	#Si el ID existe en la tabla de variables
	if arrMatId.peek() in variableTable[currentScope]:
		#Si solo tiene columnas sin renglones, marcar error
		if "cols" in variableTable[currentScope][arrMatId.peek()]:
			Error.matrix_accessed_as_array(arrMatId.peek(), t.lexer.lineno)
	#Si el ID existe en la tabla de variables globales
	elif arrMatId.peek() in variableTable["global"]:
		#Si solo tiene columnas sin renglones, marcar error
		if "cols" in variableTable["global"][arrMatId.peek()]:
			Error.matrix_accessed_as_array(arrMatId.peek(), t.lexer.lineno)

def p_addRaiz(t):
	'addRaiz : '
	resType = types.pop()
#Asignar temporal a tipo de direccion
	address_type = "temporal"
	#Si es entero, el tipo sera temporal entero
	if resType == "int":
		address_type += "Int"
		#Si es float, el tipo sera temporal float
	elif resType == "float":
		address_type += "Float"
	#Si es char, el tipo sera temporal char
	else:
		address_type += "Char"
	#Generar cuadruplo con operando, operadores y direccion
	temp_quad = Quadruple("raizcuadrada", operands.pop(), '_', addresses[address_type])
	#Hacer push del cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(temp_quad)
	#Hacer push de la direccion a la pila de operandos
	operands.push(addresses[address_type])
	#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
	addresses[address_type] += 1
	#Se le hace push al tipo de resultado a la pila de tipos.
	types.push(resType)


def p_raiz_param(t):
	'''raiz_param : hyperExpression addRaiz
				  | pow addRaiz
				  | exponencial addRaiz'''

def p_raizcuadrada(t):
	'''raizcuadrada : RAIZCUADRADA LEFTPAR raiz_param RIGHTPAR PUNTOYCOMA
					| RAIZCUADRADA LEFTPAR raiz_param RIGHTPAR'''

def p_cuadratica_param1(t):
	'''cuadratica_param1 : hyperExpression
						 | raizcuadrada
						 | exponencial
						 | pow'''

def p_cuadratica_param2(t):
	'''cuadratica_param2 : hyperExpression
						 | raizcuadrada
						 | exponencial
						 | pow'''

def p_cuadratica_param3(t):
	'''cuadratica_param3 : hyperExpression addCuadratica
						 | raizcuadrada
						 | exponencial
						 | pow'''

def p_addCuadratica(t):
	'addCuadratica : '
	resType = types.pop()
#Asignar temporal a tipo de direccion
	address_type = "temporal"
	#Si es entero, el tipo sera temporal entero
	if resType == "int":
		address_type += "Int"
		#Si es float, el tipo sera temporal float
	elif resType == "float":
		address_type += "Float"
	#Si es char, el tipo sera temporal char
	else:
		address_type += "Char"
	operando3 = operands.pop()
	operando2 = operands.pop()
	operando1 = operands.pop()
	#Genera cuadruplo print
	temp_quad = Quadruple("cuadratica", operando1, operando2, operando3)
	#Hace push al cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(temp_quad)
	#Pop a la pila de tipos
	types.pop()

def p_cuadratica(t):
	'''cuadratica : CUADRATICA LEFTPAR cuadratica_param1 COMA cuadratica_param2 COMA cuadratica_param3 RIGHTPAR PUNTOYCOMA'''

def p_pow(t):
	'''pow : POW LEFTPAR pow_param1 COMA pow_param2 RIGHTPAR PUNTOYCOMA
		   | POW LEFTPAR pow_param1 COMA pow_param2 RIGHTPAR'''

def p_pow_param1(t):
	'''pow_param1 : hyperExpression
						 | raizcuadrada
						 | exponencial'''

def p_pow_param2(t):
	'''pow_param2 : hyperExpression addPow
						 | raizcuadrada
						 | exponencial'''

def p_addPow(t):
	'addPow : '
	resType = types.pop()
	rOp = operands.pop()
	lOp = operands.pop()
#Asignar temporal a tipo de direccion
	address_type = "temporal"
	#Si es entero, el tipo sera temporal entero
	if resType == "int":
		address_type += "Int"
		#Si es float, el tipo sera temporal float
	elif resType == "float":
		address_type += "Float"
	#Si es char, el tipo sera temporal char
	else:
		address_type += "Char"
	#Generar cuadruplo con operando, operadores y direccion
	temp_quad = Quadruple("pow", lOp, rOp, addresses[address_type])
	#Hacer push del cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(temp_quad)
	#Hacer push de la direccion a la pila de operandos
	operands.push(addresses[address_type])
	#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
	addresses[address_type] += 1
	#Se le hace push al tipo de resultado a la pila de tipos.
	types.push(resType)

def p_exponencial(t):
	'''exponencial : EXPONENCIAL LEFTPAR exp_param RIGHTPAR PUNTOYCOMA
					| EXPONENCIAL LEFTPAR exp_param RIGHTPAR'''

def p_exp_param(t):
	'''exp_param : hyperExpression addExponencial
				  | pow addExponencial
				  | raizcuadrada addExponencial'''

def p_addExponencial(t):
	'addExponencial : '
	resType = types.pop()
#Asignar temporal a tipo de direccion
	address_type = "temporal"
	#Si es entero, el tipo sera temporal entero
	if resType == "int":
		address_type += "Int"
		#Si es float, el tipo sera temporal float
	elif resType == "float":
		address_type += "Float"
	#Si es char, el tipo sera temporal char
	else:
		address_type += "Char"
	#Generar cuadruplo con operando, operadores y direccion
	temp_quad = Quadruple("exponencial", operands.pop(), '_', addresses[address_type])
	#Hacer push del cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(temp_quad)
	#Hacer push de la direccion a la pila de operandos
	operands.push(addresses[address_type])
	#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
	addresses[address_type] += 1
	#Se le hace push al tipo de resultado a la pila de tipos.
	types.push(resType)


def p_moduleFunction(t):
	'''moduleFunction : hyperExpression generateParam nextParam COMA moduleFunction
					  | hyperExpression generateParam
					  | '''

def p_areaCirculo(t):
	'''areaCirculo : AREA PUNTO CIRCULO LEFTPAR areaCirculo_param RIGHTPAR PUNTOYCOMA
				   | AREA PUNTO CIRCULO LEFTPAR areaCirculo_param RIGHTPAR'''

def p_areaCirculo_param(t):
	'''areaCirculo_param : hyperExpression addAreaCirculo'''

def p_addAreaCirculo(t):
	'addAreaCirculo : '
	resType = types.pop()
#Asignar temporal a tipo de direccion
	address_type = "temporal"
	#Si es entero, el tipo sera temporal entero
	if resType == "int":
		address_type += "Int"
		#Si es float, el tipo sera temporal float
	elif resType == "float":
		address_type += "Float"
	#Si es char, el tipo sera temporal char
	else:
		address_type += "Char"
	#Generar cuadruplo con operando, operadores y direccion
	temp_quad = Quadruple("AreaCirculo", operands.pop(), '_', addresses[address_type])
	#Hacer push del cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(temp_quad)
	#Hacer push de la direccion a la pila de operandos
	operands.push(addresses[address_type])
	#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
	addresses[address_type] += 1
	#Se le hace push al tipo de resultado a la pila de tipos.
	types.push(resType)

def p_perimetroCirculo(t):
	'''perimetroCirculo : PERIMETRO PUNTO CIRCULO LEFTPAR perimetroCirculo_param  RIGHTPAR PUNTOYCOMA
						| PERIMETRO PUNTO CIRCULO LEFTPAR perimetroCirculo_param  RIGHTPAR'''

def p_perimetroCirculo_param(t):
	'''perimetroCirculo_param : hyperExpression addPerimetroCirculo'''

def p_addPerimetroCirculo(t):
	'addPerimetroCirculo : '
	resType = types.pop()
#Asignar temporal a tipo de direccion
	address_type = "temporal"
	#Si es entero, el tipo sera temporal entero
	if resType == "int":
		address_type += "Int"
		#Si es float, el tipo sera temporal float
	elif resType == "float":
		address_type += "Float"
	#Si es char, el tipo sera temporal char
	else:
		address_type += "Char"
	#Generar cuadruplo con operando, operadores y direccion
	temp_quad = Quadruple("PerimetroCirculo", operands.pop(), '_', addresses[address_type])
	#Hacer push del cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(temp_quad)
	#Hacer push de la direccion a la pila de operandos
	operands.push(addresses[address_type])
	#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
	addresses[address_type] += 1
	#Se le hace push al tipo de resultado a la pila de tipos.
	types.push(resType)

def p_areaCuadrado(t):
	'''areaCuadrado : AREA PUNTO CUADRADO LEFTPAR areaCuadrado_param RIGHTPAR PUNTOYCOMA
				   | AREA PUNTO CUADRADO LEFTPAR areaCuadrado_param RIGHTPAR'''

def p_areaCuadrado_param(t):
	'''areaCuadrado_param : hyperExpression addAreaCuadrado'''

def p_addAreaCuadrado(t):
	'addAreaCuadrado : '
	resType = types.pop()
#Asignar temporal a tipo de direccion
	address_type = "temporal"
	#Si es entero, el tipo sera temporal entero
	if resType == "int":
		address_type += "Int"
		#Si es float, el tipo sera temporal float
	elif resType == "float":
		address_type += "Float"
	#Si es char, el tipo sera temporal char
	else:
		address_type += "Char"
	#Generar cuadruplo con operando, operadores y direccion
	temp_quad = Quadruple("AreaCuadrado", operands.pop(), '_', addresses[address_type])
	#Hacer push del cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(temp_quad)
	#Hacer push de la direccion a la pila de operandos
	operands.push(addresses[address_type])
	#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
	addresses[address_type] += 1
	#Se le hace push al tipo de resultado a la pila de tipos.
	types.push(resType)

def p_perimetroCuadrado(t):
	'''perimetroCuadrado : PERIMETRO PUNTO CUADRADO LEFTPAR perimetroCuadrado_param  RIGHTPAR PUNTOYCOMA
						| PERIMETRO PUNTO CUADRADO LEFTPAR perimetroCuadrado_param  RIGHTPAR'''

def p_perimetroCuadrado_param(t):
	'''perimetroCuadrado_param : hyperExpression addPerimetroCuadrado'''

def p_addPerimetroCuadrado(t):
	'addPerimetroCuadrado : '
	resType = types.pop()
#Asignar temporal a tipo de direccion
	address_type = "temporal"
	#Si es entero, el tipo sera temporal entero
	if resType == "int":
		address_type += "Int"
		#Si es float, el tipo sera temporal float
	elif resType == "float":
		address_type += "Float"
	#Si es char, el tipo sera temporal char
	else:
		address_type += "Char"
	#Generar cuadruplo con operando, operadores y direccion
	temp_quad = Quadruple("PerimetroCuadrado", operands.pop(), '_', addresses[address_type])
	#Hacer push del cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(temp_quad)
	#Hacer push de la direccion a la pila de operandos
	operands.push(addresses[address_type])
	#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
	addresses[address_type] += 1
	#Se le hace push al tipo de resultado a la pila de tipos.
	types.push(resType)

def p_areaTriangulo(t):
	'''areaTriangulo : AREA PUNTO TRIANGULO LEFTPAR areaTriangulo_param1 COMA areaTriangulo_param2 RIGHTPAR PUNTOYCOMA
		   | AREA PUNTO TRIANGULO LEFTPAR areaTriangulo_param1 COMA areaTriangulo_param2 RIGHTPAR'''

def p_areaTriangulo_param1(t):
	'''areaTriangulo_param1 : hyperExpression
						 | raizcuadrada
						 | exponencial'''

def p_areaTriangulo_param2(t):
	'''areaTriangulo_param2 : hyperExpression addareaTriangulo
						 | raizcuadrada
						 | exponencial'''

def p_addareaTriangulo(t):
	'addareaTriangulo : '
	resType = types.pop()
	rOp = operands.pop()
	lOp = operands.pop()
#Asignar temporal a tipo de direccion
	address_type = "temporal"
	#Si es entero, el tipo sera temporal entero
	if resType == "int":
		address_type += "Int"
		#Si es float, el tipo sera temporal float
	elif resType == "float":
		address_type += "Float"
	#Si es char, el tipo sera temporal char
	else:
		address_type += "Char"
	#Generar cuadruplo con operando, operadores y direccion
	temp_quad = Quadruple("AreaTriangulo", lOp, rOp, addresses[address_type])
	#Hacer push del cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(temp_quad)
	#Hacer push de la direccion a la pila de operandos
	operands.push(addresses[address_type])
	#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
	addresses[address_type] += 1
	#Se le hace push al tipo de resultado a la pila de tipos.
	types.push(resType)

def p_perimetroTriangulo_param1(t):
	'''perimetroTriangulo_param1 : hyperExpression
						 | raizcuadrada
						 | exponencial
						 | pow'''

def p_perimetroTriangulo_param2(t):
	'''perimetroTriangulo_param2 : hyperExpression
						 | raizcuadrada
						 | exponencial
						 | pow'''

def p_perimetroTriangulo_param3(t):
	'''perimetroTriangulo_param3 : hyperExpression addperimetroTriangulo
						 | raizcuadrada
						 | exponencial
						 | pow'''

def p_addperimetroTriangulo(t):
	'addperimetroTriangulo : '
	resType = types.pop()
#Asignar temporal a tipo de direccion
	address_type = "temporal"
	#Si es entero, el tipo sera temporal entero
	if resType == "int":
		address_type += "Int"
		#Si es float, el tipo sera temporal float
	elif resType == "float":
		address_type += "Float"
	#Si es char, el tipo sera temporal char
	else:
		address_type += "Char"
	operando3 = operands.pop()
	operando2 = operands.pop()
	operando1 = operands.pop()
	#Genera cuadruplo print
	temp_quad = Quadruple("PerimetroTriangulo", operando1, operando2, operando3 )
	#Hace push al cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(temp_quad)
	#Pop a la pila de tipos
	types.pop()

def p_perimetroTriangulo(t):
	'''perimetroTriangulo : PERIMETRO PUNTO TRIANGULO LEFTPAR perimetroTriangulo_param1 COMA perimetroTriangulo_param2 COMA perimetroTriangulo_param3 RIGHTPAR PUNTOYCOMA
						  | PERIMETRO PUNTO TRIANGULO LEFTPAR perimetroTriangulo_param1 COMA perimetroTriangulo_param2 COMA perimetroTriangulo_param3 RIGHTPAR'''

def p_areaRectangulo(t):
	'''areaRectangulo : AREA PUNTO RECTANGULO LEFTPAR areaRectangulo_param1 COMA areaRectangulo_param2 RIGHTPAR PUNTOYCOMA
		   | AREA PUNTO RECTANGULO LEFTPAR areaRectangulo_param1 COMA areaRectangulo_param2 RIGHTPAR'''

def p_areaRectangulo_param1(t):
	'''areaRectangulo_param1 : hyperExpression
						 | raizcuadrada
						 | exponencial'''

def p_areaRectangulo_param2(t):
	'''areaRectangulo_param2 : hyperExpression addareaRectangulo
						 | raizcuadrada
						 | exponencial'''

def p_addareaRectangulo(t):
	'addareaRectangulo : '
	resType = types.pop()
	rOp = operands.pop()
	lOp = operands.pop()
#Asignar temporal a tipo de direccion
	address_type = "temporal"
	#Si es entero, el tipo sera temporal entero
	if resType == "int":
		address_type += "Int"
		#Si es float, el tipo sera temporal float
	elif resType == "float":
		address_type += "Float"
	#Si es char, el tipo sera temporal char
	else:
		address_type += "Char"
	#Generar cuadruplo con operando, operadores y direccion
	temp_quad = Quadruple("AreaRectangulo", lOp, rOp, addresses[address_type])
	#Hacer push del cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(temp_quad)
	#Hacer push de la direccion a la pila de operandos
	operands.push(addresses[address_type])
	#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
	addresses[address_type] += 1
	#Se le hace push al tipo de resultado a la pila de tipos.
	types.push(resType)

def p_perimetroRectangulo(t):
	'''perimetroRectangulo : PERIMETRO PUNTO RECTANGULO LEFTPAR perimetroRectangulo_param1 COMA perimetroRectangulo_param2 RIGHTPAR PUNTOYCOMA
		   | PERIMETRO PUNTO RECTANGULO LEFTPAR perimetroRectangulo_param1 COMA perimetroRectangulo_param2 RIGHTPAR'''

def p_perimetroRectangulo_param1(t):
	'''perimetroRectangulo_param1 : hyperExpression
						 | raizcuadrada
						 | exponencial'''

def p_perimetroRectangulo_param2(t):
	'''perimetroRectangulo_param2 : hyperExpression addperimetroRectangulo
						 | raizcuadrada
						 | exponencial'''

def p_addperimetroRectangulo(t):
	'addperimetroRectangulo : '
	resType = types.pop()
	rOp = operands.pop()
	lOp = operands.pop()
#Asignar temporal a tipo de direccion
	address_type = "temporal"
	#Si es entero, el tipo sera temporal entero
	if resType == "int":
		address_type += "Int"
		#Si es float, el tipo sera temporal float
	elif resType == "float":
		address_type += "Float"
	#Si es char, el tipo sera temporal char
	else:
		address_type += "Char"
	#Generar cuadruplo con operando, operadores y direccion
	temp_quad = Quadruple("PerimetroRectangulo", lOp, rOp, addresses[address_type])
	#Hacer push del cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(temp_quad)
	#Hacer push de la direccion a la pila de operandos
	operands.push(addresses[address_type])
	#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
	addresses[address_type] += 1
	#Se le hace push al tipo de resultado a la pila de tipos.
	types.push(resType)


def p_areaParalelogramo(t):
	'''areaParalelogramo : AREA PUNTO PARALELOGRAMO LEFTPAR areaParalelogramo_param1 COMA areaParalelogramo_param2 RIGHTPAR PUNTOYCOMA
		   | AREA PUNTO PARALELOGRAMO LEFTPAR areaParalelogramo_param1 COMA areaParalelogramo_param2 RIGHTPAR'''

def p_areaParalelogramo_param1(t):
	'''areaParalelogramo_param1 : hyperExpression
						 | raizcuadrada
						 | exponencial'''

def p_areaParalelogramo_param2(t):
	'''areaParalelogramo_param2 : hyperExpression addareaParalelogramo
						 | raizcuadrada
						 | exponencial'''

def p_addareaParalelogramo(t):
	'addareaParalelogramo : '
	resType = types.pop()
	rOp = operands.pop()
	lOp = operands.pop()
#Asignar temporal a tipo de direccion
	address_type = "temporal"
	#Si es entero, el tipo sera temporal entero
	if resType == "int":
		address_type += "Int"
		#Si es float, el tipo sera temporal float
	elif resType == "float":
		address_type += "Float"
	#Si es char, el tipo sera temporal char
	else:
		address_type += "Char"
	#Generar cuadruplo con operando, operadores y direccion
	temp_quad = Quadruple("AreaParalelogramo", lOp, rOp, addresses[address_type])
	#Hacer push del cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(temp_quad)
	#Hacer push de la direccion a la pila de operandos
	operands.push(addresses[address_type])
	#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
	addresses[address_type] += 1
	#Se le hace push al tipo de resultado a la pila de tipos.
	types.push(resType)

def p_perimetroParalelogramo(t):
	'''perimetroParalelogramo : PERIMETRO PUNTO PARALELOGRAMO LEFTPAR perimetroParalelogramo_param1 COMA perimetroParalelogramo_param2 RIGHTPAR PUNTOYCOMA
		   | PERIMETRO PUNTO PARALELOGRAMO LEFTPAR perimetroParalelogramo_param1 COMA perimetroParalelogramo_param2 RIGHTPAR'''

def p_perimetroParalelogramo_param1(t):
	'''perimetroParalelogramo_param1 : hyperExpression
						 | raizcuadrada
						 | exponencial'''

def p_perimetroParalelogramo_param2(t):
	'''perimetroParalelogramo_param2 : hyperExpression addperimetroParalelogramo
						 | raizcuadrada
						 | exponencial'''

def p_addperimetroParalelogramo(t):
	'addperimetroParalelogramo : '
	resType = types.pop()
	rOp = operands.pop()
	lOp = operands.pop()
#Asignar temporal a tipo de direccion
	address_type = "temporal"
	#Si es entero, el tipo sera temporal entero
	if resType == "int":
		address_type += "Int"
		#Si es float, el tipo sera temporal float
	elif resType == "float":
		address_type += "Float"
	#Si es char, el tipo sera temporal char
	else:
		address_type += "Char"
	#Generar cuadruplo con operando, operadores y direccion
	temp_quad = Quadruple("PerimetroParalelogramo", lOp, rOp, addresses[address_type])
	#Hacer push del cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(temp_quad)
	#Hacer push de la direccion a la pila de operandos
	operands.push(addresses[address_type])
	#Se le suma 1 para darselo a la siguiente variable de ese tipo que este dentro del scope
	addresses[address_type] += 1
	#Se le hace push al tipo de resultado a la pila de tipos.
	types.push(resType)

if len(sys.argv) > 1:
	f = open(sys.argv[1], "r")
else:
	f = open("test.txt", "r")
program = f.read()

parser = yacc.yacc()

parser.parse(program)
#maquina_virtual()