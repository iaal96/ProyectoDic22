import sys

class Error:
	@staticmethod
	def type_mismatch(t, lineno):
		" error type mismatch "
		print("Error: type mismatch en asignacion de '%s' en la linea %d." % (t, lineno))
		exit(0)

	@staticmethod
	def condition_type_mismatch(lineno):
		" error type mismatch en if"
		print("Error: type mismatch en expresion de condicion en la linea %d." % lineno)
		exit(0)

	@staticmethod
	def type_mismatch_module(t, lineno):
		print("Error: type mismatch en llamada de modulo '%s' en la linea %d." % (t, lineno))
		exit(0)

	@staticmethod
	def operation_type_mismatch(lineno):
		"error de operation type mismatch "
		print("Error: type mismatch en operacion en la linea %d." % (lineno))
		exit(0)

	@staticmethod
	def undefined_variable(t,lineno):
		" error de uso de variable indefinida "
		print("Error: uso de variable indefinida '%s' en la linea %d" % (t, lineno))
		exit(0)

	@staticmethod
	def redefinition_of_variable(t, lineno):
		" error de redefinicion de variable "
		print("Error: redefinicion de variable '%s' en la linea %d." % (t, lineno))
		exit(0)

	@staticmethod
	def variable_has_no_assigned_value(t, lineno):
		" error de variable sin valor asignado "
		print("Error: variable '%s' en la linea %d no tiene un valor asignado." %(t, lineno))
		exit(0)

	@staticmethod
	def syntax(t, lineno):
		" error sintactico "
		print("Error sintactico: Token '%s' inesperado en la linea %d" % (t, lineno))
		exit(0)

	@staticmethod
	def undefined_module(t, lineno):
		" error de modulo indefinido "
		print("Error: uso de modulo indefinido '%s' en la linea %d." % (t, lineno))
		exit(0)

	@staticmethod
	def unexpected_number_of_arguments(t, lineno):
		" error de numero equivocado de argumentos "
		print("Error: Numero inesperado de argumentos en llamada de modulo '%s' en la linea  %d." % (t, lineno))
		exit(0)

	@staticmethod
	def return_on_void_function(t, lineno):
		print("Error: return en funcion void en la linea %d." % (lineno))
		exit(0)

	@staticmethod
	def no_return_on_function(t, lineno):
		print("Error: no hay return en funcion con tipo return en la linea %d." % (lineno))
		exit(0) 

	@staticmethod
	def matrix_accessed_as_array(t, lineno):
		print("Error: matriz '%s' accesada como arreglo en linea %d." % (t, t.lexer.lineno))
		exit(0)

	@staticmethod
	def type_mismatch_in_index(t, lineno):
		print("Error: type mismatch en indexacion de variable '%s' en la linea %d." % (t, lineno))
		exit(0)

	@staticmethod
	def variable_not_subscriptable_as_matrix(t, lineno):
		print("Error: variable '%s' en la linea %d no es parte de una matriz" % (t, lineno))
		exit(0)

	@staticmethod
	def variable_not_subscriptable_as_array(id, lineno):
		print("Error: variable '%s' en la linea %d no es parte de un arreglo." % (id, lineno))
		exit(0)

	@staticmethod
	def array_parameter_in_module_call(lineno):
		print("Error: parametro de arreglo en llamada de modulo en la linea %d." % (lineno))
		exit(0)


	@staticmethod
	def invalid_print_on_array_variable(lineno):
		print("Error: print invalido en variable de arreglo en la linea %d." % (lineno))
		exit(0)

	@staticmethod	
	def invalid_operator_on_arrays(lineno):
		print("Error: operador invalido en arreglos en la linea %d." % (lineno))
		exit(0)

	@staticmethod
	def invalid_operation_in_line(lineno):
		print("Error: operacion invalida en la linea %d." % (lineno))
		exit(0)

	@staticmethod
	def dimensions_do_not_match(lineno):
		print("Error: operacion entre variables con dimensiones que no corresponden en la linea %d." % (lineno))
		exit(0)

	@staticmethod
	def invalid_assignment_to_array_variable(lineno):
		print("Error: asignacion a variable de arreglo invalida en la linea %d." % (lineno))
		exit(0)
	
	@staticmethod
	def invalid_determinant_calculation(lineno):
		print("Error: dimensiones de arreglo para el calculo de determinante invalidos en la linea %d." % (lineno))

	@staticmethod
	def array_size_must_be_positive(t, lineno):
		print("Error: tamaño del arreglo '%s' en la linea  %d debe ser positivo." % (t, lineno))
		exit(0)
	
	def index_out_of_bounds():
		print("Error: index out of bounds.")
		exit(0)

	@staticmethod
	def division_by_zero():
		print("Error: division entre cero.")
		exit(0)

	@staticmethod
	def invalid_inverse_calculation(lineno):
		print("Error: dimensiones de arreglo invalidas para el calculo de inversa en la linea %d." % (lineno))
		exit(0)

	@staticmethod
	def type_mismatch_array_assignment(lineno):
		print("Error: type mismatch en asignacion de arreglo en la linea %d." % (lineno))
		exit(0)

	@staticmethod
	def inverse_determinant_zero():
		print("Error: deteminante de la inversa es cero.")
		exit(0)

	@staticmethod
	def type_mismatch_on_return(lineno):
		print("Error: type mismatch en return en la linea %d." % (lineno))
		exit(0) 