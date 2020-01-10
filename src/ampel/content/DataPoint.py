#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/src/ampel/content/DataPoint.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 12.12.2019
# Last Modified Date: 08.01.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from dataclasses import dataclass, _MISSING_TYPE
from typing import Any, Sequence, Union, Optional, Dict
from ampel.typing import StockId, DataPointId

none_type = type(None)

@dataclass(frozen=True)
class DataPoint: 

	id: DataPointId
	tags: Optional[Sequence[Union[int, str]]]
	stock: Union[StockId, Sequence[StockId]]
	body: Dict[str, Any]

	# Ignore extras, enable aliases
	def __init__(self, **kwargs):

		# pylint: disable=no-member
		fields = self.__dataclass_fields__
		d = self.__dict__

		# Aliases
		if '_id' in kwargs:
			d['id'] = kwargs['_id']

		for k in fields:
			if k in kwargs:
				d[k] = kwargs[k]
			else:
				if k in d: # field value already set by aliases
					continue
				# Optional type
				if '__args__' in fields[k].type.__dict__ and none_type in fields[k].type.__args__: # type: ignore
					d[k] = None
					continue 
				# No default value
				if fields[k].default.__class__ is _MISSING_TYPE:
					raise ValueError(f"Value missing for field '{k}'")
				d[k] = fields[k].default
