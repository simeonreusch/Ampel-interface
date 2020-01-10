#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/content/T2Record.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.01.2018
# Last Modified Date: 20.12.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Sequence, Union, Optional
from dataclasses import dataclass, _MISSING_TYPE
none_type = type(None)


@dataclass(frozen=True)
class T2Record:

	id: bytes
	unit: Union[int, str] # int to enable future potential hash optimizations
	link: bytes
	col: Optional[str]
	tags: Optional[Sequence[Union[int, str]]]
	stock: Union[int, str, Sequence[Union[int, str]]]
	channels: Sequence[Union[int, str]]
	results: Sequence[dict] # value(s) returned by t2 unit execution(s)
	config: dict
	state: int

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
				# Optional type
				if '__args__' in fields[k].type.__dict__ and none_type in fields[k].type.__args__: # type: ignore
					d[k] = None
					continue
				# No default value
				if fields[k].default.__class__ is _MISSING_TYPE:
					raise ValueError(f"Value missing for field '{k}'")
				d[k] = fields[k].default
