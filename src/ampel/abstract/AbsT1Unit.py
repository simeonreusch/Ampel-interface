#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/abstract/AbsT1Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 11.10.2019
# Last Modified Date: 19.10.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from ampel.abstract.AmpelABC import abstractmethod
from ampel.abstract.AbsAmpelUnit import AbsAmpelUnit
from typing import List, Dict, Any, Union

class AbsT1Unit(AbsAmpelUnit, abstract=True):
	"""
	To be refined later
	"""

	@abstractmethod
	def create_state(
		self, tran_id: Union[int, str], photo_data: List[Dict[str, Any]]
	) -> Dict[str, Any]:
		""" """
