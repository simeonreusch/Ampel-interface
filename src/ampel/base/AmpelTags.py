#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/base/AmpelTags.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 19.02.2019
# Last Modified Date: 20.02.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from ampel.base.Frozen import Frozen


class AmpelTags(Frozen):
	"""
	"""

	general = (
		"HAS_ERROR", 
		"HAS_EXCEPTION"
	)

	data = (
		"SUPERSEDED",
		"IMAGE_BAD_CALIBRATION",
		"IMAGE_ARTIFACT",
		"IMAGE_TRACKING_PBLM",
		"IMAGE_FOCUS_PBLM",
		"HAS_UPDATED_ZP",
		"CREATED_BY_AMPEL"
	)

	compound = (
		"HAS_UPPER_LIMITS",
		"HAS_AUTOCOMPLETED_PHOTO",
		"HAS_SUPERSEDED_PPS",
		"HAS_EXCLUDED_PPS",
		"HAS_MANUAL_EXCLUSION",
		"HAS_DATARIGHT_EXCLUSION",
		"HAS_CUSTOM_POLICIES"
	)

	transient = (
		"HAS_TNS_NAME",
		"MIXED_DATA_SOURCE",
		"T1_AUTO_COMPLETED"
	)
