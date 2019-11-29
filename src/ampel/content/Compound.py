#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/content/Compound.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : Unspecified
# Last Modified Date: 18.12.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from dataclasses import dataclass, _MISSING_TYPE
from typing import Any, Sequence, Union, Optional, Dict

none_type = type(None)

@dataclass(frozen=True)
class Compound: 

	id: Union[int, str, Dict]
	tags: Optional[Sequence[Union[int, str]]]
	stock: Union[int, str, Sequence[Union[int, str]]]
	channels: Sequence[Union[int, str]]
	data: Sequence[Dict[str, Any]]
	added: float
	tier: int
	len: int

	# Ignore extras, enable aliases, set defaults (none for now)
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
				if '__args__' in fields[k].type.__dict__ and none_type in fields[k].type.__args__:
					d[k] = None
					continue # Optional type
				# No default value
				if fields[k].default.__class__ is _MISSING_TYPE:
					raise ValueError(f"Value missing for field '{k}'")
				d[k] = fields[k].default
