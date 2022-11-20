import sys

class Error:
	@staticmethod
	def type_mismatch(t, lineno):
		" error type mismatch "
		print("Error Semántico: type mismatch en asignacion de '%s' en la linea %d." % (t, lineno))
		exit(0)

	@staticmethod
	def condition_type_mismatch(lineno):
		" error type mismatch en if"
		print("Error Semántico: type mismatch en expresion de condicion en la linea %d." % lineno)
		exit(0)

	@staticmethod
	def type_mismatch_module(t, lineno):
		print("Error Semántico: type mismatch en llamada de modulo '%s' en la linea %d." % (t, lineno))
		exit(0)

	@staticmethod
	def operation_type_mismatch(lineno):
		"error de operation type mismatch "
		print("Error Semántico: type mismatch en operacion en la linea %d." % (lineno))
		exit(0)

	@staticmethod
	def undefined_variable(t,lineno):
		" error de uso de variable indefinida "
		print("Error Semántico: uso de variable indefinida '%s' en la linea %d" % (t, lineno))
		exit(0)

	@staticmethod
	def redefinition_of_variable(t, lineno):
		" error de redefinicion de variable "
		print("Error Semántico: redefinicion de variable '%s' en la linea %d." % (t, lineno))
		exit(0)

	@staticmethod
	def redefinition_of_function(t, lineno):
		" error de redefinicion de funcion "
		print("Error Semántico: redefinicion de funcion '%s' en la linea %d." % (t, lineno))
		exit(0)

	@staticmethod
	def variable_has_no_assigned_value(t, lineno):
		" error de variable sin valor asignado "
		print("Error Semántico: variable '%s' en la linea %d no tiene un valor asignado." %(t, lineno))
		exit(0)

	@staticmethod
	def syntax(t, lineno):
		" error sintactico "
		print("Error sintactico: Token '%s' inesperado en la linea %d" % (t, lineno))
		exit(0)

	@staticmethod
	def undefined_module(t, lineno):
		" error de modulo indefinido "
		print("Error Semántico: uso de modulo indefinido '%s' en la linea %d." % (t, lineno))
		exit(0)

	@staticmethod
	def unexpected_number_of_arguments(t, lineno):
		" error de numero equivocado de argumentos "
		print("Error Semántico: Numero inesperado de argumentos en llamada de modulo '%s' en la linea  %d." % (t, lineno))
		exit(0)

	@staticmethod
	def return_on_void_function(t, lineno):
		print("Error Semántico: regresa en funcion void en la linea %d." % (lineno))
		exit(0)

	@staticmethod
	def no_return_on_function(t, lineno):
		print("Error Semántico: no hay regresa en funcion con tipo regresa en la linea %d." % (lineno))
		exit(0) 

	@staticmethod
	def matrix_accessed_as_array(lineno):
		print("Error Semántico: matriz accesada como arreglo en linea %d." % (lineno))
		exit(0)

	@staticmethod
	def type_mismatch_in_index(t, lineno):
		print("Error Semántico: type mismatch en indexacion de variable '%s' en la linea %d." % (t, lineno))
		exit(0)

	@staticmethod
	def variable_not_subscriptable_as_matrix(t, lineno):
		print("Error Semántico: variable '%s' en la linea %d no es parte de una matriz" % (t, lineno))
		exit(0)

	@staticmethod
	def variable_not_subscriptable_as_array(id, lineno):
		print("Error Semántico: variable '%s' en la linea %d no es parte de un arreglo." % (id, lineno))
		exit(0)

	@staticmethod
	def array_parameter_in_module_call(lineno):
		print("Error Semántico: parametro de arreglo en llamada de modulo en la linea %d." % (lineno))
		exit(0)


	@staticmethod
	def invalid_print_on_array_variable(lineno):
		print("Error Semántico: print invalido en variable de arreglo en la linea %d." % (lineno))
		exit(0)

	@staticmethod	
	def invalid_operator_on_arrays(lineno):
		print("Error Semántico: operador invalido en arreglos en la linea %d." % (lineno))
		exit(0)

	@staticmethod
	def invalid_operation_in_line(lineno):
		print("Error Semántico: operacion invalida en la linea %d." % (lineno))
		exit(0)

	@staticmethod
	def dimensions_do_not_match(lineno):
		print("Error Semántico: operacion entre variables con dimensiones que no corresponden en la linea %d." % (lineno))
		exit(0)

	@staticmethod
	def invalid_assignment_to_array_variable(lineno):
		print("Error Semántico: asignacion a variable de arreglo invalida en la linea %d." % (lineno))
		exit(0)
	

	@staticmethod
	def array_size_must_be_positive(t, lineno):
		print("Error Semántico: tamaño del arreglo '%s' en la linea  %d debe ser positivo." % (t, lineno))
		exit(0)

	def index_out_of_bounds(lineno):
		print("Error en Compilación: indice fuera del rango en la linea %d." % (lineno))
		exit(0)

	@staticmethod
	def division_by_zero():
		print("Error Semántico: division entre cero.")
		exit(0)

	@staticmethod
	def type_mismatch_array_assignment(lineno):
		print("Error Semántico: type mismatch en asignacion de arreglo en la linea %d." % (lineno))
		exit(0)

	@staticmethod
	def type_mismatch_on_return(lineno):
		print("Error Semántico: type mismatch en regresa en en la linea %d." % (lineno))
		exit(0) 