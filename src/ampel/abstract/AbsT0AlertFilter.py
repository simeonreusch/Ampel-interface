#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/abstract/AbsT0AlertFilter.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 14.12.2017
# Last Modified Date: 31.10.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Set, Optional, Sequence
from pydantic import validator
from ampel.model.UnitData import UnitData
from ampel.object.AmpelAlert import AmpelAlert
from ampel.abstract.AmpelABC import abstractmethod
from ampel.abstract.AbsAmpelUnit import AbsAmpelUnit
from ampel.model.AmpelBaseModel import AmpelBaseModel


class AbsT0AlertFilter(AbsAmpelUnit, abstract=True):
	"""
	Base class for T0 filters
	"""

	class InitConfig(AmpelBaseModel):
		""" 
		"""
		t2_compute: Optional[Sequence[UnitData]]
		on_match_t2_units: Optional[Sequence[str]] = ()


	@abstractmethod
	def apply(self, ampel_alert: AmpelAlert) -> Optional[Set[str]]:
		"""
		Filters an alert. 
		Return `None` to reject the candidate, 
		or a set of T2 units to run to accept it.
		"""
