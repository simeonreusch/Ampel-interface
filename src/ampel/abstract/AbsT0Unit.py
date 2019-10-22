#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/abstract/AbsT0Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 07.10.2019
# Last Modified Date: 19.10.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from ampel.abstract.AmpelABC import abstractmethod
from ampel.abstract.AbsAmpelUnit import AbsAmpelUnit
from typing import Dict, Any, List

class AbsT0Unit(AbsAmpelUnit, abstract=True):
	"""
	To be defined more precisely later
	"""

	@abstractmethod
	def shape(self, data_list: List[Dict[str, Any]], id_field_name: str) -> List[Dict[str, Any]]:
		"""
		"""
