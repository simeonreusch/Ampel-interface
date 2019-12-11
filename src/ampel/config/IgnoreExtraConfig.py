#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/config/IgnoreExtraConfig.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 11.12.2019
# Last Modified Date: 11.12.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from pydantic import BaseConfig, Extra

class IgnoreExtraConfig(BaseConfig):
	"""
	Pydantic configuration which ignores unknown constructor parameters
	Used in classes: Compound, ScienceRecord
	"""
	extra = Extra.ignore
	arbitrary_types_allowed = True
	allow_population_by_field_name = True
