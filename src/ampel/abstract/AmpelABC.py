#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/abstract/AmpelABC.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 27.12.2017
# Last Modified Date: 27.10.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import inspect

def abstractmethod(func):
	""" Custom decorator to mark selected method as abstract. """
	func.abstractmethod = True
	return func


def raise_error(cls, **kwargs):
	"""
	Abstract classes cannot be instantiated
	:raises: TypeError
	"""
	raise TypeError(
		f"Class {cls.__name__} is abstract and can thus not be instantiated"
	)


# pylint: disable=unused-argument
def __std_new__(mcs, *arg, **kwargs):
	""" Standard class creation """
	cls = None
	for el in mcs.__mro__:
		# stop at first built-in type ('object' by defaut, or say 'dict' for example if 
		# the abstract subclass inherits from a python primitive type.
		# Avoids this kind of error: TypeError: object.__new__(MyDict) is not safe, use dict.__new__()
		if '__new__' in el.__dict__ and type(el.__dict__['__new__']).__name__ == "builtin_function_or_method":
			cls = el
			break
	return cls.__new__(mcs)


class AmpelABC(type):
	"""
	Metaclass that implements similar functionalities to python standart 
	ABC module (Abstract Base Class) while additionaly checking method signatures.
	As a consequence, a child class that extends a class whose 
	metaclass is AmpelABC, will not be able to implement the abstract methods 
	of the parent class with different method arguments.
	Signature checking can be disabled by setting AmpelABC.enforce_signature=False
	Notes:
	- Multi-level and multiple inheritance are supported.
	- Overriding abstractmethod is supported (if subclass itself is abstract)
	- This class relies on the module 'inspect'
	- Setting AmpelABC.enforce_signature = False deactivates signatures check
	"""

	enforce_signature = True

	def __new__(cls, name, bases, d, **kwargs):
		"""
		Creates the class
		:raises NotImplementedError: if an abstract method is not implemented by the child class
		:raises TypeError: if method signatures differ between an abstract method and the \
		corresponding implementation by the child class (provided AmpelABC.enforce_signature is True)
		"""
		
		Klass = type.__new__(cls, name, bases, d)

		# Class is abstract
		if not bases or kwargs.get('abstract'):
			setattr(Klass, '__new__', raise_error)
			
		else:
			setattr(Klass, '__new__', __std_new__)	

			if AmpelABC.enforce_signature:

				# Gather abstract methods (marked by the decorator @abstractmethod)
				abs_methods = {
					method_name: (base_cls, method) 
					for base in bases
						for base_cls in reversed(base.mro())
							for method_name, method in base_cls.__dict__.items()
								if hasattr(method, "abstractmethod")
				}

				# Check implementation
				for method_name, value in abs_methods.items():

					# Check if method was implemented by child
					func = getattr(Klass, method_name)
					if func.__qualname__.split(".")[0] == value[0].__name__:
						raise NotImplementedError(
							f"Class {name} must implement abstract method "
							f"{method_name} defined in class {value[0].__name__}"
						)

					# Get method signatures
					abstract_sig = inspect.signature(value[1])
					impl_sig = inspect.signature(
						getattr(Klass, method_name)
					)

					# Check for equality
					if abstract_sig.parameters.keys() != impl_sig.parameters.keys():
						raise TypeError(
							f"Wrong method signature. Please change the arguments of method "
							f"'{method_name}' to match those defined by the corresponding "
							f"abstract method in class {value[0].__name__}"
						)
		
		return Klass
