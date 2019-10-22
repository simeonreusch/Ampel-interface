#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/abstract/AbsT2Unit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.12.2017
# Last Modified Date: 19.10.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from ampel.abstract.AmpelABC import abstractmethod
from ampel.abstract.AbsAmpelUnit import AbsAmpelUnit
from typing import Dict, Any, Optional
from ampel.base.LightCurve import LightCurve

class AbsT2Unit(AbsAmpelUnit, abstract=True):
	"""
	"""

	@abstractmethod
	def run(
		self, light_curve: LightCurve, 
		run_config: Optional[Dict[str, Any]]=None
	) -> Dict[str, Any]:
		"""
		returns dictionary containing results
		"""
