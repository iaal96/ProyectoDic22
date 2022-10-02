import ply.yacc as yacc
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

def p_programFunc(t):
	'''programFunc : function programFunc
				   | '''

def p_main(t):
	'''main : mainTable PRINCIPAL LEFTPAR RIGHTPAR LEFTBRACE declaration statement RIGHTBRACE'''

# main scope varTable
def p_mainTable(t):
	'''mainTable : '''

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

def p_vars(t):
	'''vars : ID addVarsToTable varsArray varsComa'''

def p_addVarsToTable(t):
	'''addVarsToTable : '''

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

def p_addFuncToDir(t):
	'''addFuncToDir : '''

def p_functionType(t):
	'''functionType : FUNCION primitive
					| FUNCION VOID setVoidType '''

def p_setVoidType(t):
	'''setVoidType : '''

def p_param(t):
	'''param : primitive ID addFuncParams functionParam
			 | '''

def p_addFuncParams(t):
	'''addFuncParams : '''

def p_setParamLength(t):
	'''setParamLength : '''

def p_functionParam(t):
	'''functionParam : COMA param
					 | '''

def p_cst_prim(t):
	'''cst_prim : CST_INT addTypeInt
				| CST_FLOAT addTypeFloat
				| CST_CHAR addTypeChar'''

def p_addTypeInt(t):
	'''addTypeInt : '''

def p_addTypeFloat(t):
	'''addTypeFloat : '''

def p_addTypeChar(t):
	'''addTypeChar : '''

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
