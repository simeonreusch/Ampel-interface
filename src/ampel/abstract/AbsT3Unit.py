#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/abstract/AbsT3Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 23.02.2018
# Last Modified Date: 19.10.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence
from ampel.abstract.AmpelABC import abstractmethod
from ampel.abstract.AbsAmpelUnit import AbsAmpelUnit
from ampel.dataclass.JournalUpdate import JournalUpdate
#from ampel.dataclass.GlobalInfo import GlobalInfo

class AbsT3Unit(AbsAmpelUnit, abstract=True):
	"""
	"""

	#@abstractmethod
	#def set_global_info(self, global_info: GlobalInfo) -> None:
	#	""" Implementing T3 units get TransientViews via this this method """

	@abstractmethod
	def add(self, transients) -> Sequence[JournalUpdate]:
		""" Implementing T3 units get TransientViews via this this method """

	@abstractmethod
	def done(self) -> None:
		""" Method called after all transients have been processed """
