import ply.yacc as yacc
from cuadruplos import *
from EstructurasDatos import *
import lexer as lexer
from re import U 
#Obtener tokens del lexer
from lexer import tokens
from errores import Error
#Data pretty printer
from pprint import pprint

tokens = lexer.tokens

def p_program(t):
	'''program : PROGRAMA ID globalTable PUNTOYCOMA declaration programFunc main'''
	print("Compilado exitosamente")

# global scope varTable
def p_globalTable(t):
	'''globalTable : '''
	# Inicializar variableTable para global scope y definir nombre y tipo del programa
	variableTable[currentScope] = {}
	variableTable[currentScope][t[-1]] = {"type": "program"}
	# Inicializar functionDir para global scope
	functionDir[currentScope] = {}
	# Definir tipo y variables como referencia a variableTable["global"]
	functionDir[currentScope]["type"] = "void"
	functionDir[currentScope]["vars"] = variableTable[currentScope]

def p_programFunc(t):
	'''programFunc : function programFunc
				   | '''

def p_main(t):
	'''main : mainTable PRINCIPAL LEFTPAR RIGHTPAR LEFTBRACE declaration statement RIGHTBRACE'''

# main scope varTable
def p_mainTable(t):
	'''mainTable : '''
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

def p_assignment(t):
	'''assignment : ID dimArray IGUAL hyperExpression PUNTOYCOMA'''

		
def p_declaration(t):
	'''declaration : VAR declarationPrim
				   | '''

def p_declarationPrim(t):
	'''declarationPrim : primitive vars PUNTOYCOMA declarationPrim
					   | '''

def p_primitive(t):
	'''primitive : INT
				 | FLOAT
				 | CHAR '''
	# Cambiar currentType por declaracion
	global currentType
	currentType = t[1]

def p_return(t):
	'''return : REGRESA LEFTPAR hyperExpression RIGHTPAR PUNTOYCOMA'''

def p_if(t):
	'''if : SI LEFTPAR hyperExpression RIGHTPAR createJumpQuadIf ENTONCES LEFTBRACE statement RIGHTBRACE ifElse updateJumpQuad'''

def p_createJumpQuadIf(t):
	'''createJumpQuadIf : '''

def p_updateJumpQuad(t):
	'''updateJumpQuad : '''

def p_ifElse(t):
	'''ifElse : SINO createJumpQuadElse LEFTBRACE statement RIGHTBRACE
			  | '''

def p_createJumpQuadElse(t):
	'''createJumpQuadElse : '''

def p_comment(t):
	'''comment : COMMENT_TEXT'''

def p_while(t):
	'''while : MIENTRAS pushLoopJump LEFTPAR hyperExpression RIGHTPAR beginLoopAction LEFTBRACE statement RIGHTBRACE endLoopAction'''

def p_pushLoopJump(t):
	'''pushLoopJump : '''

def p_beginLoopAction(t):
	'''beginLoopAction : '''

def p_endLoopAction(t):
	'''endLoopAction : '''

def p_for(t):
	'''for : PARA forAssignment HASTA insertJumpFor hyperExpression createQuadFor LEFTBRACE statement RIGHTBRACE updateQuadFor'''

def p_insertJumpFor(t):
	'''insertJumpFor : '''

def p_createQuadFor(t):
	'''createQuadFor : '''

def p_updateQuadFor(t):
	'''updateQuadFor : '''

def p_forAssignment(t):
	'''forAssignment : ID IGUAL CST_INT addTypeInt'''
	#Checar si el id existe en currentScope y asignar su valor
	if t[1] in variableTable[currentScope]:
		variableTable[currentScope][t[1]]["value"] = t[3]
	#Checar si el id existe en global scope y asignar su valor
	elif t[1] in variableTable["global"]:
		variableTable["global"][t[1]]["value"] = t[3]
	else:
		Error.undefined_variable(t[1], t.lexer.lineno)

def p_vars(t):
	'''vars : ID addVarsToTable varsArray varsComa'''

def p_addVarsToTable(t):
	'''addVarsToTable : '''
#Si el ID ya existe en el scope o global, dar error
	if t[-1] in variableTable[currentScope]:
		Error.redefinition_of_variable(t[-1], t.lexer.lineno)
	else:
		# Agregar ID actual a variableTable(scope)
		variableTable[currentScope][t[-1]] = {"type": currentType}

def p_varsComa(t):
	'''varsComa : COMA vars
				| '''

def p_varsArray(t):
	'''varsArray : LEFTBRACK CST_INT addTypeInt RIGHTBRACK setRows varsMatrix 
				 | '''

def p_setRows(t):
	'''setRows : '''

def p_varsMatrix(t):
	'''varsMatrix : LEFTBRACK CST_INT addTypeInt RIGHTBRACK setCols
				  | '''

def p_setCols(t):
	'''setCols : '''

def p_function(t):
	'''function : functionType ID addFuncToDir LEFTPAR param RIGHTPAR setParamLength LEFTBRACE declaration statement RIGHTBRACE'''
    #Resetear scope a global cuando se salga del scope de la funcion, eliminar varTable y referenciar en functionDir
	global currentScope
	# Variables temporales = longitud del cuadruplo de funcion al maximo y resetear func_quads
	functionDir[currentScope]["varLength"] = len(functionDir[currentScope]["vars"])
	currentScope = "global"

def p_addFuncToDir(t):
	'''addFuncToDir : '''
	# Si la funcion existe en global scope, dar error
	if t[-1] in variableTable["global"]:
		Error.redefinition_of_variable(t[-1], t.lexer.lineno)
	else:
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
   
def p_functionType(t):
	'''functionType : FUNCION primitive
					| FUNCION VOID setVoidType '''

def p_setVoidType(t):
	'''setVoidType : '''
	# Definir void como currentType
	global currentType
	currentType = t[-1]

def p_param(t):
	'''param : primitive ID addFuncParams functionParam
			 | '''

def p_addFuncParams(t):
	'''addFuncParams : '''
	# Si parametro de la funcion existe en el scope, dar error
	if t[-1] in variableTable[currentScope]:
		Error.redefinition_of_variable(t[-1], t.lexer.lineno)
	else:
		# Agregar parametro de la funcion a variableTable de currentScope
		variableTable[currentScope][t[-1]] = {"type": currentType}
	if "params" not in functionDir[currentScope]:
		functionDir[currentScope]["params"] = Queue()
		# Insertar currentTypes en params Queue
		functionDir[currentScope]["params"].enqueue(currentType)

def p_setParamLength(t):
	'''setParamLength : '''
	#Asignar el numero de parametro de la funcion al tamano del Queue params
	functionDir[currentScope]["paramsLength"] = functionDir[currentScope]["params"].size()

def p_functionParam(t):
	'''functionParam : COMA param
					 | '''

def p_cst_prim(t):
	'''cst_prim : CST_INT addTypeInt
				| CST_FLOAT addTypeFloat
				| CST_CHAR addTypeChar'''

def p_addTypeInt(t):
	'''addTypeInt : '''
	types.push("int")

def p_addTypeFloat(t):
	'''addTypeFloat : '''
	types.push("float")

def p_addTypeChar(t):
	'''addTypeChar : '''
	types.push("char")

def p_hyperExpression(t):
	'''hyperExpression : superExpression evaluateHE opHyperExpression hyperExpressionNested
					   | superExpression opMatrix evaluateOpMatrix
					   | superExpression evaluateHE'''

def p_hyperExpressionNested(t):
	'''hyperExpressionNested : superExpression evaluateHE opHyperExpression hyperExpressionNested
							 | superExpression evaluateHE'''

def p_evaluateOpMatrix(t):
	'''evaluateOpMatrix : '''

def p_evaluateHE(t):
	'''evaluateHE : '''

def p_opMatrix(t):
	'''opMatrix : EXCLAMACION addOperator
				| INTERROGACION addOperator
				| SIGNO_DOLAR addOperator '''

def p_opHyperExpression(t):
	'''opHyperExpression : AND addOperator
						 | OR addOperator '''

def p_superExpression(t):
	'''superExpression : exp evaluateSE opSuperExpression exp evaluateSE
					   | exp evaluateSE '''

def p_evaluateSE(t):
	'''evaluateSE : '''

def p_opSuperExpression(t):
	'''opSuperExpression : MAYOR_QUE addOperator
						 | MENOR_QUE addOperator
						 | DIFERENTE_A addOperator 
						 | IGUAL_A addOperator'''

def p_exp(t):
	'''exp : term evaluateTerm expFunction
		   | term evaluateTerm '''

def p_evaluateTerm(t):
	'''evaluateTerm : '''

def p_expFunction(t):
	'''expFunction : MAS addOperator exp
				   | MENOS addOperator exp '''

def p_term(t):
	'''term : factor evaluateFactor termFunction
			| factor evaluateFactor '''

def p_evaluateFactor(t):
	'''evaluateFactor : '''

def p_termFunction(t):
	'''termFunction : MULTIPLICA addOperator term
					| DIVIDE addOperator term '''

def p_addOperator(t):
	'''addOperator : '''

def p_factor(t):
	'''factor : LEFTPAR addFF hyperExpression RIGHTPAR removeFF
			  | cst_prim 
			  | module
			  | ID dimArray'''

def p_addFF(t):
	'''addFF : '''

def p_removeFF(t):
	'''removeFF : '''

def p_read(t):
	'''read : LEE LEFTPAR id_list RIGHTPAR PUNTOYCOMA'''

def p_id_list(t):
	'''id_list : ID dimArray addRead id_listFunction'''

def p_addRead(t):
	'''addRead : '''

def p_id_listFunction(t):
	'''id_listFunction : COMA id_list
					   | '''

def p_print(t):
	'''print : IMPRIME LEFTPAR printFunction RIGHTPAR PUNTOYCOMA'''

def p_printFunction(t):
	'''printFunction : print_param COMA printFunction2
					 | print_param '''

def p_printFunction2(t):
	'''printFunction2 : printFunction'''

def p_print_param(t):
	'''print_param : hyperExpression addPrint
				   | CST_STRING addPrintString '''

def p_addPrint(t):
	'''addPrint : '''

def p_addPrintString(t):
	'''addPrintString : '''

def p_statement(t):
	'''statement : return checkVoidType
				 | if statement
				 | comment statement
				 | read statement
				 | print statement
				 | assignment statement
				 | module PUNTOYCOMA statement
				 | for statement
				 | while statement
				 | checkNonVoidType'''

def p_checkVoidType(t):
	'''checkVoidType : '''
	
def p_checkNonVoidType(t):
	'''checkNonVoidType : '''

def p_module(t):
	'''module : ID checkFuncExists genERASize LEFTPAR moduleFunction nullParam RIGHTPAR genGosub'''

def p_checkFuncExists(t):
	'''checkFuncExists : '''
	if t[-1] not in functionDir:
		Error.undefined_module(t[-1], t.lexer.lineno)
	global funcName
	funcName = t[-1]
	operators.push("module")
	types.push(functionDir[funcName]["type"])

def p_genERASize(t):
	'''genERASize : '''

def p_nullParam(t):
	'''nullParam : '''

def p_genGosub(t):
	'''genGosub : '''

def p_moduleFunction(t):
	'''moduleFunction : hyperExpression genParam nextParam COMA moduleFunction
					  | hyperExpression genParam 
					  | '''

def p_genParam(t):
	'''genParam : '''

def p_nextParam(t):
	'''nextParam : '''

def p_dimArray(t):
	'''dimArray : addOperandId addTypeId LEFTBRACK readIDType hyperExpression verifyRows RIGHTBRACK dimMatrix
				| addOperandId addTypeId '''

def p_addOperandId(t):
	'''addOperandId : '''

def p_addTypeId(t):
	'''addTypeId : '''
	#Hacer push a los tipos al stack de tipos
	if t[-2] in variableTable[currentScope]:
		types.push(variableTable[currentScope][t[-2]]["type"])
	elif t[-2] in variableTable["global"]:
		types.push(variableTable["global"][t[-2]]["type"])
	else:
		Error.undefined_variable(t[-2], t.lexer.lineno)

def p_readIDType(t):
	'''readIDType : '''

def p_verifyRows(t):
	'''verifyRows : '''

def p_dimMatrix(t):
	'''dimMatrix : LEFTBRACK hyperExpression verifyCols RIGHTBRACK
				 | checkMatAsArray '''

def p_verifyCols(t):
	'''verifyCols : '''

def p_checkMatAsArray(t):
	'''checkMatAsArray : '''

def p_error(t):
	'''error : '''
	print("Error sintactico ")
	exit()

import sys 
if len(sys.argv) > 1:
	f = open(sys.argv[1], "r")
else:
	f = open("prog.txt", "r")
program = f.read()

parser = yacc.yacc()

parser.parse(program)
