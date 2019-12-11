#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/config/AmpelBaseConfig.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 22.10.2019
# Last Modified Date: 22.10.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import json
from functools import reduce
from typing import Dict, List, Any, Union, Optional

from ampel.utils.Freeze import Freeze
from ampel.utils.ReadOnlyDict import ReadOnlyDict


class AmpelBaseConfig:
	""" 
	"""

	def __init__(self, config: Dict[Any, Any], freeze: bool = True):
		""" """
		self._config = Freeze.recursive_freeze(config) if freeze else config


	def get(self, sub_element: Optional[str] = None) -> Union[int, float, str, List, Dict[Any, Any]]:
		""" 
		Optional arguments:
		:param sub_element: sub-config element will be returned. 
		Ex: get("channel.HU_RANDOM") or get(['foo', 'bar', 'baz'])
		"""
		if sub_element is None:
			return self._config

		try:
			array = sub_element.split(".") if isinstance(sub_element, str) else sub_element
			# check for int elements encoded as str
			array = [(el if not el.isdigit() else int(el)) for el in array]
			return reduce(lambda d, k: d.get(k), array, self._config)

		except AttributeError:
			return None


	def print(self, sub_element: Optional[str] = None) -> None:
		"""
		"""
		print(
			json.dumps(
				self.get(sub_element), indent=4
			)
		)


	def is_frozen(self) -> bool:
		""" """ 
		return isinstance(self._config, ReadOnlyDict)
