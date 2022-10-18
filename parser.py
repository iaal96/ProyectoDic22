import lexer as lexer
import ply.yacc as yacc
from EstructurasDatos import types, operands, operators, variableTable, Queue
from EstructurasDatos import functionDir, temp, currentScope, currentType, semanticCube
from cuadruplos import *
from errores import Error

tokens = lexer.tokens


def p_program(t):
	'program : PROGRAMA ID globalTable PUNTOYCOMA programVars programFunc main'
	print("Compilacion exitosa")
	# Mostrar variable table y directorio de funciones
	# print()
	# for i in functionDir:
	# 	print("\tfunction name: %s" % i)
	# 	print("\t\ttype: %s" % functionDir[i]["type"])
	# 	print("\t\tvars: %s" % functionDir[i]["vars"])
	# 	if "params" in functionDir[i]:
	# 		print("\t\tparams: %s" % functionDir[i]["params"].values())
	# 		print("\t\tparamsLength: %d" % functionDir[i]["paramsLength"])
	# 		print("\t\tstart: %d" % functionDir[i]["start"])
	# 		print("\t\tvarLength: %d" % functionDir[i]["varLength"])
	# 	print()

	#operands.print()
	#types.print()
	#operators.print()
	#Imprimir cuadruplos
	Quadruples.print_all()
	#Imprimir tabla de variables
	variableTable.clear()

#GlobalTable: Inicializar programa y crear variableTable
def p_globalTable(t):
	'globalTable : '
	# Inicializar variableTable para global scope y definir nombre y tipo del programa
	variableTable[currentScope] = {}
	variableTable[currentScope][t[-1]] = {"type": "program"}
	# Inicializar functionDir para global scope
	functionDir[currentScope] = {}
	# Definir tipo y variables como referencia a variableTable["global"]
	functionDir[currentScope]["type"] = "void"
	functionDir[currentScope]["vars"] = variableTable[currentScope]

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

def p_programVars(t):
	'''programVars : globalDeclaration
				   | '''

def p_globalDeclaration(t):
	'globalDeclaration : VAR declarationPrim'

def p_programFunc(t):
	'''programFunc : function programFunc
				   | '''

#Assignment: Genera cuadruplo en el varTable correspondiente
def p_assignment(t):
	'assignment : ID IGUAL hyperExpression PUNTOYCOMA'
	#Si id esta en currentScope, generar cuadruplo y asignar su valor en varTable
	if t[1] in variableTable[currentScope]:
		if types.pop() == variableTable[currentScope][t[1]]["type"]:
			#Genera cuadruplo
			temp_quad = Quadruple("=", operands.peek(), '_', t[1])
			Quadruples.push_quad(temp_quad)
			variableTable[currentScope][t[1]]["value"] = operands.pop()
		else:
			#Type mismatch
			Error.type_mismatch(t[1],t.lexer.lineno - 1)
	#Si id esta en globalScope, generar cuadruplo y asignar su valor en varTable
	elif t[1] in variableTable["global"]:
		if types.pop() == variableTable["global"][t[1]]["type"]:
			temp_quad = Quadruple("=", operands.peek(), '_', t[1])
			Quadruples.push_quad(temp_quad)
			variableTable["global"][t[1]]["value"] = operands.pop()
		else:
			#Type mismatch
			Error.type_mismatch(t[1],t.lexer.lineno - 1)
	else:
		#Si la variable no esta en varTable, dar error variable indefinida.
		Error.undefined_variable(t[1], t.lexer.lineno - 1)

#Declaration: Asignar cuadruplo start para una funcion.
def p_declaration(t):
	'declaration : VAR declarationPrim'
	#Asignar cuadruplo start para funcion
	functionDir[currentScope]["start"] = Quadruples.next_id

#primitive=Primitive Data Types
def p_declarationPrim(t):
	'''declarationPrim : primitive vars PUNTOYCOMA declarationPrim
					   | '''

#primitive: Cambiar el currentType de declaracion
def p_primitive(t):
	'''primitive : INT
				 | FLOAT
				 | CHAR '''
	# Cambiar currentType por declaracion
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
		#Si operands.peek() es BOOLEANO
		if operands.peek() == 1 or operands.peek() == 0:
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
			Error.type_mismatch(t[1],t.lexer.lineno)
	else: 
		#Type mismatch
		Error.type_mismatch(t[1],t.lexer.lineno)

#Update Jump Quad: Actualiza el cuadruplo con el id del cuadruplo al que debe "saltar"
def p_updateJQ(t):
	'updateJQ : '
	#Actualizar cuadruplos GOTOF
	#Hacer POP al id del cuadruplo de la pila de saltos
	tmp_end = Quadruples.pop_jump()
	tmp_count = Quadruples.next_id
	#Agrega id del cuadruplo de salto al cuadruplo
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
		#Peek a pila de operandos y si es BOOLEANO, 0 o 1
		if operands.peek() == 1 or operands.peek() == 0:
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
		#Si no es BOOLEANO, marcar error type mismatch
		else: 
			Error.type_mismatch(t[1],t.lexer.lineno)
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
	tmp_quad = Quadruple("GOTO", "_", "_", tmp_rtn)
	#Hacer push del cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(tmp_quad)
	#Actualiza tmp_count a la cantidad de cuadruplos que haya en la lista de cuadruplos.
	tmp_count = Quadruples.next_id
	#Agrega id del cuadruplo de salto al cuadruplo
	Quadruples.update_jump_quad(tmp_end, tmp_count)

#forAssignment: Agrega iterador a la tabla de constantes y crea una variable iterativa
def p_forAssignment(t):
	'forAssignment : ID IGUAL CST_INT'
	#Checar si el id existe en currentScope y asignar su valor
	if t[1] in variableTable[currentScope]:
		#Generar cuadruplo de asignacion
		temp_quad = Quadruple("=", t[3], '_', t[1])
		#Push al cuadruplo a la lista del cuadruplos
		Quadruples.push_quad(temp_quad)
		#Cambiar valor de la variable en varTable
		variableTable[currentScope][t[1]]["value"] = t[3]
	#Checar si el id existe en global scope y asignar su valor
	elif t[1] in variableTable["global"]:
		#Generar cuadruplo de asignacion
		temp_quad = Quadruple("=", t[3], '_', t[1])
		#Push al cuadruplo a la lista del cuadruplos
		Quadruples.push_quad(temp_quad)
		#Cambiar valor de la variable en varTable
		variableTable["global"][t[1]]["value"] = t[3]
	else:
	#Si no existe el id, marcar error variable indefinida
		Error.undefined_variable(t[1], t.lexer.lineno)


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
		if operands.peek() == 1 or operands.peek() == 0:
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
		else:
			Error.type_mismatch(t[1],t.lexer.lineno)
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
	#Si el ID ya existe en el scope o global, dar error
	if t[-1] in variableTable[currentScope]:
		Error.redefinition_of_variable(t[-1], t.lexer.lineno)
	else:
		#Si no existe, Agregar ID actual a variableTable(scope)
		variableTable[currentScope][t[-1]] = {"type": currentType}

def p_varsComa(t):
	'''varsComa : COMA vars
				| '''

def p_varsMatrix(t):
	'''varsMatrix : LEFTBRACK CST_INT RIGHTBRACK
				  | '''

#varsArray: Declaracion de arreglo
def p_varsArray(t):
	'''varsArray : LEFTBRACK CST_INT RIGHTBRACK varsMatrix
				 | '''

#function: Crea cuadruplo ENDFUNC y define tabla de variables locales.
def p_function(t):
	'function : functionType ID addFuncToDir LEFTPAR param RIGHTPAR setParamLength LEFTBRACE declaration statement RIGHTBRACE'
    #Resetear scope a global cuando se salga del scope de la funcion, eliminar varTable y referenciar en functionDir
	global currentScope
    #delete variableTable[currentScope]
    #delete functionDir[currentScope]["vars"]
	# Crear cuadruplo endfuc para terminar funcion
	temp_quad = Quadruple("ENDFUNC", "_", "_", "_")
	#Hacer push del cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(temp_quad)
	# Variables temporales = longitud del cuadruplo de funcion al maximo
	functionDir[currentScope]["varLength"] = Quadruples.function_quads
	#Resetear function quads
	Quadruples.function_quads = 0
	#Regresar scope a global
	currentScope = "global"

def p_param(t):
	'''param : primitive ID addFuncParams functionParam
			 | '''

def p_functionParam(t):
	'''functionParam : COMA param
					 | '''

#addFuncParams: Agrega una lista de tipos de parametros al scope de la funcion.
def p_addFuncParams(t):
	'addFuncParams : '
	# Si parametro de la funcion ya existe en el scope, dar error
	if t[-1] in variableTable[currentScope]:
		Error.redefinition_of_variable(t[-1], t.lexer.lineno)
	else:
		# Si no existe, agregar parametro de la funcion a variableTable de currentScope
		variableTable[currentScope][t[-1]] = {"type": currentType}
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
	types.push("int")

#addTypeFloat: Guardar float en tabla de constantes y hacer push al operando al stack de operandos.
def p_addTypeFloat(t):
	'addTypeFloat : '
	types.push("float")

#addTypeChar: Guardar char en tabla de constantes y hacer push al operando al stack de operandos.
def p_addTypeChar(t):
	'addTypeChar : '
	types.push("char")

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
		# Cambiar scope al nuevo id de la funcion
		currentScope = t[-1]
		# Inicializar variableTable y functionDir por nuevo id de la funcion
		variableTable[currentScope] = {}
		functionDir[currentScope] = {}
		# Definir nuevo tipo de funcion y vars como referencia a variableTable[currentScope]
		functionDir[currentScope]["type"] = currentType
		functionDir[currentScope]["vars"] = variableTable[currentScope]

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
	global temp
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
			#Checar tipo y valor
			if resType == "int":
				result = 0
				lOp = int(lOp)
				rOp = int(rOp)
				#si lOp o rOp no son BOOL, marcar error type mismatch de operacion
				if (lOp != 0 and lOp != 1) or (rOp != 0 and rOp != 1):
					Error.operation_type_mismatch(lOp, rOp,t.lexer.lineno)
				#Evaluar expresion y hacerle push a cuadruplo
				#Si oper es | hacer OR
				if oper == "|":
					result = lOp or rOp
				else: 
					#si es & hacer AND
					result = lOp and rOp
				#Generar cuadruplo
				temp_quad = Quadruple(oper, lOp, rOp, result)
				#Push a cuadruplo a la lista de cuadruplos
				Quadruples.push_quad(temp_quad)
				#Push de resultado a la lista de operandos
				operands.push(result)
				#Push del tipo del resultado a la lista de tipos
				types.push(resType)
				temp += 1
			#Si el tipo no es int, dar error type mismatch
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
						 | DIFERENTE_A addOperator 
						 | IGUAL_A addOperator'''

#evaluateSuperExp: Evalua operador y operandos de expresiones booleanas del tipo >, < , == , y <>.
def p_evaluateSuperExp(t):
	'evaluateSuperExp : '
	global temp
	if operators.size() != 0:
		#Generar cuadruplos para operadores de comparacion
		if operators.peek() == ">" or operators.peek() == "<" or operators.peek() == "<>" or operators.peek() == "==":
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
				result = 0
				#Si el operador es >, comparar lOp con rOp para ver si es mayor
				if oper == ">": 
					result = float(lOp) > float(rOp)
				#Si el operador es <, comparar lOp con rOp para ver si es menor
				if oper == "<": 
					result = float(lOp) < float(rOp)
				#Si el operador es <>, comparar lOp con rOp para ver si son diferentes
				if oper == "<>": 
					result = float(lOp) != float(rOp)
				#Si el operador es == , comparar lOp con rOp para ver si son iguales
				if oper == "==": 
					result = float(lOp) == float(rOp)
				#Convertir result a int
				result = int(result)
				# Generar cuadruplo para expresion
				temp_quad = Quadruple(oper, lOp, rOp, result)
				#Push a cuadruplo a la lista de cuadruplo
				Quadruples.push_quad(temp_quad)
				#Push a resultado a la lista de operandos
				operands.push(result)
				#Push al tipo del resultado a la pila de tipos
				types.push(resType)
				temp += 1
			#Si el tipo no es int, dar error type mismatch
			else:
				Error.operation_type_mismatch(lOp, rOp,t.lexer.lineno)

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
	global temp
	#Si si hay operadores
	if operators.size() != 0:
		# Generar cuadruplos para operadores de suma y resta
		if operators.peek() == "+" or operators.peek() == "-":
			# Pop a pila operandos
			rOp = operands.pop()
			lOp = operands.pop()
			# Pop a pila de operadores
			oper = operators.pop()
			# Pop a pila de tipos
			rType = types.pop()
			lType = types.pop()
			# Checar cubo semantico con tipos y operador
			resType = semanticCube[(lType, rType, oper)]
			# Checar tipo de resultado y evaluar expresion
			# Si no marca error
			if resType != "error":
				result = 0
				#Si el operador es +, sumar operandos
				if oper == "+": 
					result = float(lOp) + float(rOp)
				#Si el operador es -, restar operandos
				if oper == "-": 
					result = float(lOp) - float(rOp)
				#Si resultado modulo 1 es 0, hacer el resultado int.
				if result % 1 == 0:
					result = int(result)
				# Generar cuadruplo para expresion
				temp_quad = Quadruple(oper, lOp, rOp, result)
				#Hacer push al cuadruplo a la lista de cuadruplos
				Quadruples.push_quad(temp_quad)
				#Hacer push al resultado a la pila de operandos
				operands.push(result)
				#Hacer push al tipo de resultado a la pila de tipos
				types.push(resType)
				temp += 1
			#Si no son compatibles, generar error type mismatch.
			else:
				Error.operation_type_mismatch(lOp, rOp, t.lexer.lineno)


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
	global temp
	#Si si hay operadores
	if operators.size() != 0:
		# Generar cuadruplos para operadores de multiplicacion y division
		if operators.peek() == "*" or operators.peek() == "/":
			# Pop a pila de operandos
			rOp = operands.pop()
			lOp = operands.pop()
			# Pop a pila de operadores
			oper = operators.pop()
			# Pop a pila de tipos
			rType = types.pop()
			lType = types.pop()
			# Checar cubo semantico con tipos y operador
			resType = semanticCube[(lType, rType, oper)]
			# Checar tipo de resultado y evaluar expresion
			# Si no marca error
			if resType != "error":
				#Si el operador es *, multiplicar operandos
				if oper == "*": 
					result = float(lOp) * float(rOp)
				#Si el operador es /, dividir operandos
				if oper == "/": 
					result = float(lOp) / float(rOp)
				#Si resultado modulo 1 es 0, hacer el resultado int.
				if result % 1 == 0:
					result = int(result)
				# Generar cuadruplo para expresion
				temp_quad = Quadruple(oper, lOp, rOp, result)
				#Hacer push del cuadruplo a la lista de cuadruplos
				Quadruples.push_quad(temp_quad)
				#Hace push al resultado a la pila de operandos
				operands.push(result)
				#Hace push al tipo del resultado a la pila de tipos
				types.push(resType)
				temp += 1
			else:
				Error.operation_type_mismatch(lOp, rOp,t.lexer.lineno)
				
def p_termFunction(t):
	'''termFunction : MULTIPLICA addOperator term
					| DIVIDE addOperator term '''

#addOperator: Push a operador read al stack de operadores
def p_addOperator(t):
	'addOperator : '
	operators.push(t[-1])

def p_factor(t):
	'''factor : LEFTPAR addFF hyperExpression RIGHTPAR removeFF
			  | cst_primitive addOperandCst
			  | module
			  | ID addOperandId addTypeId'''

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
	#Hacer push a los tipos al stack de tipos
	#Si la variable esta en currentScope, hacer push del tipo a la pila de tipos de la tabla de variables de currentScope
	if t[-2] in variableTable[currentScope]:
		types.push(variableTable[currentScope][t[-2]]["type"])
	#Si la variable esta en globalscope, hacer push del tipo a la pila de tipos de la tabla de variables de globalScope
	elif t[-2] in variableTable["global"]:
		types.push(variableTable["global"][t[-2]]["type"])
	else:
	#Si no encuentra la variable, marcar error de variable indefinida.
		Error.undefined_variable(t[-1], t.lexer.lineno)


def p_addOperandCst(t):
	'addOperandCst : '
	operands.push(t[-1])

#addOperandId: ***
def p_addOperandId(t):
	'addOperandId : '
	#Agregar el valor del operando de currentcope al stack de operandos
	if t[-1] in variableTable[currentScope]:
		#Si value esta en la tabla de variables de CurrentScope
		if "value" in variableTable[currentScope][t[-1]]:
			#Hacer push al operando a la pila de operandos de currentscope
			operands.push(variableTable[currentScope][t[-1]]["value"])
		else:
			#Si no esta, marcar error variable no tiene valor asignado.
			Error.variable_has_no_assigned_value(t[-1], t.lexer.lineno)
	#Agregar el valor del operando de global scope al stack de operandos
	elif t[-1] in variableTable["global"]:
		#Si value esta en la tabla de variables de global scope
		if "value" in variableTable["global"][t[-1]]:
			#Hacer push al operando a la pila de operandos de globalscope
			operands.push(variableTable["global"][t[-1]]["value"])
		else:
			#Si no esta, marcar error variable no tiene valor asignado.
			Error.variable_has_no_assigned_value(t[-1], t.lexer.lineno)
	else:
		#Si no encuentra la variable en ningun scope, marcar error variable indefinida.
		Error.undefined_variable(t[-1], t.lexer.lineno)


def p_read(t):
	'read : LEE LEFTPAR id_list RIGHTPAR PUNTOYCOMA'

def p_id_list(t):
	'id_list : ID addRead id_listFunction'

def p_id_listFunction(t):
	'''id_listFunction : COMA id_list
					   | '''

#addRead: Genera un cuadruplo read y le hace push a la lista de cuadruplos
def p_addRead(t):
	'addRead : '
	#Genera cuadruplo Read, si la variable esta en varTable
	if t[-1] in variableTable[currentScope] or t[-1] in variableTable["global"]:
		#Generar cuadruplo
		temp_quad = Quadruple("lee", '_', '_', t[-1])
		#Hacer push al cuadruplo a lista de cuadruplos
		Quadruples.push_quad(temp_quad)
	else:
		#Si no esta, dar error variable indefinida
		Error.undefined_variable(t[-1], t.lexer.lineno)

def p_print(t):
	'print : IMPRIME LEFTPAR printFunction RIGHTPAR PUNTOYCOMA'

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
	#Agrega string al cuadruplo print
	temp_quad = Quadruple("imprime", '_', '_', t[-1])
	#Hace push al cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(temp_quad)

def p_module(t):
	'module : ID checkFunctionExists generateERASize LEFTPAR moduleFunction nullParam RIGHTPAR generateGosub PUNTOYCOMA'

#checkFunctionExists: Verifica que la funcion existe en el directorio de Funciones y le hace push al operador del modulo al stack.
def p_checkFunctionExists(t):
	'checkFunctionExists : '
	#Si la funcion no esta en functionDir, marcar error modulo indefinido
	if t[-1] not in functionDir:
		Error.undefined_module(t[-1], t.lexer.lineno)
	#Si si, asignar nombre a la funcion
	global funcName
	funcName = t[-1]

#generateERASize: Crea el cuadruplo ERA con el directorio de la funcion que sera llamada.
def p_generateERASize(t):
	'generateERASize : '
	#Generar tamano ERA pendiente...
	global funcName
	#Generar cuadruplo con ERA
	tmp_quad = Quadruple("ERA", funcName, "_", "_")
	#Hacer push al cuadruplo a la lista de cuadruplos
	Quadruples.push_quad(tmp_quad)
	global k
	k = 1

#nullParam: Lanza error si falta un parametro en una llamada de funcion
def p_nullParam(t):
	'nullParam : '
	global k
	global funcName
	#Si params de la funcion es mayor que la cantidad de argumentos que el usuario esta dando, dar error
	if k < len(functionDir[funcName]["params"].values()):
		Error.unexpected_number_of_arguments(funcName, t.lexer.lineno)

#generateGosub: Crea el cuadruplo Gosub con la direccion de la funcion a llamar **
def p_generateGosub(t):
	'generateGosub : '
	#Genera cuadruplo con GOSUB
	tmp_quad = Quadruple("GOSUB", funcName, "_", functionDir[funcName]["start"])
	#Push al cuadruplo a la lista de cuadruplos.
	Quadruples.push_quad(tmp_quad)

#generateParam: Crea el cuadruplo PARAM con el opreando que esta siendo leido.
def p_generateParam(t):
	'generateParam : '
	global k
	#Pop a pila de operandos y se lo asigna a argumento
	arg = operands.pop()
	#Pop a la pila de tipos y se lo asigna a tipo de argumento
	argType = types.pop()
	#Saca la lista de parametros de la funcion
	paramList = functionDir[funcName]["params"].values()
	#Si tiene mas argumentos de los que debe tener, lanzar error
	if k > len(paramList):
		Error.unexpected_number_of_arguments(funcName, t.lexer.lineno)
	#Si los tipos son los correctos
	if argType == paramList[-k]:
		#Generar cuadruplo con PARAM
		tmp_quad = Quadruple("PARAM", arg, '_', "param%d" % k)
		#Hacer push al cuadruplo a la lista de cuadruplos
		Quadruples.push_quad(tmp_quad)
	#Si los argumentos no son del tipo esperado lanzar error type mismatch
	else:
		Error.type_mismatch_module(funcName, t.lexer.lineno)

#nextParam: agrega 1 al iterador de param.
def p_nextParam(t):
	'nextParam : '
	global k
	k += 1


def p_statement(t):
	'''statement : return
				 | if statement
				 | comment statement
				 | read statement
				 | print statement
				 | assignment statement
				 | module statement
				 | for statement
				 | while statement 
				 | '''


def p_moduleFunction(t):
	'''moduleFunction : hyperExpression generateParam nextParam COMA moduleFunction
					  | hyperExpression generateParam
					  | '''


if len(sys.argv) > 1:
	f = open(sys.argv[1], "r")
else:
	f = open("test.txt", "r")
program = f.read()

parser = yacc.yacc()

parser.parse(program)