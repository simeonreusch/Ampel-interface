#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/base/abstract/AmpelABC.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 27.12.2017
# Last Modified Date: 29.05.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import inspect, types


def abstractmethod(func):
	"""
	Custom decorator to mark selected method as abstract.
	It populates the static array "_abstract_methods" of class AmpelABC.
	"""
	func.__dict__['abstract'] = True 
	return func


def generate_new(abclass):
	"""
	Forbids instantiation of abstract classes.

	:param abclass: the abstract base *class*
	:returns: the method __new__
	"""
	def __new__(mcs, *args, **kwargs):
		if (mcs is abclass):
			raise TypeError("Abstract class "+ abclass.__name__ + " cannot be instantiated")
		return object.__new__(mcs)

	return __new__


class AmpelABC(type):
	"""
	Metaclass with similar functionalities than the python standart ABC module 
	(Abstract Base Class) but that does additionaly check method signatures.
	As a consequence, a child class that extends a parent class defined with metaclass=AmpelABC, 
	will not be able to implement any defined abstract method using different parameters
	than the one specified in the parent abstract class.
	"""
	
	def __new__(cls, name, bases, d):
		
		# no bases means we deal with the abstract class itself
		if len(bases) == 0:
			abclass = type.__new__(cls, name, bases, d)
			setattr(abclass, "__new__", generate_new(abclass))
			return abclass
		
		# we ignore further sub-classing
		if len(bases) > 1:
			return type.__new__(cls, name, bases, d)
				
		# Loop through abstract methods of parent abstract class
		for func_name, func in bases[0].__dict__.items():
			
			if not isinstance(func, types.FunctionType) or 'abstract' not in func.__dict__:
				continue
				
			if func_name not in d.keys():
				raise NotImplementedError(
					"Method %s is not implemented" % func_name
				)

			# Check if method signatures are equal
			abstract_sig = inspect.signature(func)
			child_sig = inspect.signature(d[func_name])

			# Check that number of parameters are equal rather than checking 
			# if parameter names are identical (if abstract_sig != child_sig)
			if len(abstract_sig.parameters) != len(child_sig.parameters):
				raise ValueError(
					"Wrong signature for method %s, expected arguments: %s" %
					(func_name, abstract_sig)
				)
				
		return type.__new__(cls, name, bases, d)
