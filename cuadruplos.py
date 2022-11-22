from EstructurasDatos import Stack
import sys

class Quadruple(object):
	"""Clase Cuadruplo
	
	Cuadruplo
	"""
	def __init__(self, operator, left_operand, right_operand, result):
		"""Construir cuadruplo
		
		Construir cuadruplo
		
		Argumentos:
			operator {int} -- operator
			left_operand {operand} -- left operand
			right_operand {operand} -- right operand
			result {operand} -- result operand
		"""
		self.id = -1 #va incrementando
		self.operator = operator
		self.left_operand = left_operand
		self.right_operand = right_operand
		self.result = result
	#Imprimir cuadruplo
	def print(self):
		print("Q"+ str(self.id), self.operator, self.left_operand, self.right_operand, self.result)


class Quadruples(object):
	"""Clase Cuadruplos
	
	Administra clase cuadruplos
	"""
	# Variables
	quadruples = []
	jump_stack = Stack()
	next_id = 0
	function_quads = 0
	__shared_state = {}
	def __init__(self):
		self.__dict__ = self.__shared_state

	#Metodos
	@classmethod
	def push_quad(cls, quad):
		"""Push Cuadruplo
		
		Hace push a la lista de cuadruplos
		
		Arguments:
			quad {Quadruple} -- Quadruple
		"""
		quad.id = cls.next_id
		cls.quadruples.append(quad)
		cls.next_id = len(cls.quadruples)
		cls.function_quads += 1

	@classmethod
	def pop_quad(cls):
		"""Pop cuadruplo
		
		Hace pop de la lista de cuadruplos
		
		Regresa:
			Quadruple -- Quadruple
		"""
		cls.next_id = len(cls.quadruples) - 1
		return cls.quadruples.pop()

	@classmethod
	def update_jump_quad(cls, quad_id, jump_id):
		"""update jump quad
		
		Agrega jump quadruple id (jump_id) a quadruple
		
		Argumentos:
			quad_id {int} -- quadruple id
			jump_int {int} -- int
		"""
		cls.quadruples[quad_id].result = jump_id

	# Jump Stack Methods
	@classmethod
	def push_jump(cls, offset):
		"""Push jump
		
		Hace push al id del siguiente cuadruplo disponible y hace push al jump stack
		
		Argumentos:
			offset {int} -- number
		"""
		cls.jump_stack.push(cls.next_id + offset)

	@classmethod
	def pop_jump(cls):
		"""Pop jump
		
		Hace pop al id del cuadruplo del jump stack
		
		Regresa:
			int -- number
		"""
		return cls.jump_stack.pop()

	@classmethod
	def peek_jump(cls):
		"""Peek jump
		
		Hace peek al id del cuadruplo de salto
		
		Regresa:
			int -- number
		"""
		return cls.jump_stack.peek()

	@classmethod
	def print_all(cls):
		"""Imprime todos los cuadruplos de la lista"""
		print("CUADRUPLOS:")
		for x in cls.quadruples:
			x.print() 