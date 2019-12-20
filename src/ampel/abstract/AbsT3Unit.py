#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/base/abstract/AbsT3Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 23.02.2018
# Last Modified Date: 15.10.2018
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from ampel.base.abstract.AmpelABC import AmpelABC, abstractmethod

class AbsT3Unit(metaclass=AmpelABC):
	"""
	"""

	resources = tuple()

	@abstractmethod
	def __init__(self, logger, base_config=None, run_config=None, global_info=None):
		pass

	@abstractmethod
	def add(self, transients):
		pass

	@abstractmethod
	def done(self):
		pass
