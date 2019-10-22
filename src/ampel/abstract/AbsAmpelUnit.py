#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/abstract/AbsAmpelUnit.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 12.10.2019
# Last Modified Date: 19.10.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Tuple, Dict, Any, Optional
from ampel.logging.AmpelLogger import AmpelLogger
from ampel.abstract.AmpelABC import AmpelABC, abstractmethod


class AbsAmpelUnit(metaclass=AmpelABC):
	"""
	Top level abstract class
	"""

	# Named resources required by this unit. 
	# This should be overridden by subclasses 
	# to register dependencies on local resources, 
	# e.g. URLs of #: catalog database servers
	resources : Tuple[str] = tuple()


	@abstractmethod
	def __init__(
		self, logger: AmpelLogger,
		init_config : Optional[Dict[str, Any]] = None,
		resources : Optional[Dict[str, Any]] = None
	):
		"""
		:param logger: logger to use for reporting output
		:param init_config: unit-specific settings
		:param resources: resources configured for this unit. \
		The keys are the elements of :py:attr:`resources`.
		"""

	# pylint: disable=no-member
	def get_version(self) -> str:
		return getattr(self, "version", None)
