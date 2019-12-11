#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/config/AllowExtraConfig.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 11.12.2019
# Last Modified Date: 11.12.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from pydantic import BaseConfig, Extra

class AllowExtraConfig(BaseConfig):
	"""
	Pydantic configuration which allows unknown constructor parameters
	Used in class: DataPoint
	"""
	extra = Extra.allow
	arbitrary_types_allowed = True
	allow_population_by_field_name = True
