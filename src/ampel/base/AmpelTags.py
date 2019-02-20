#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/base/AmpelTags.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 19.02.2019
# Last Modified Date: 20.02.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from ampel.base.Frozen import Frozen
import hashlib, sys


class AmpelTags(Frozen):
	"""
	"""

	hashes = {}

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

	@staticmethod
	def add_hashes(cls):
		"""
		*static* method accepting cls as argument so that say AmpelTags.add_hashes(ZITags) is possible 
		"""
		for el in [getattr(cls, name) for name in ("general", "data", "compound", "transient") if hasattr(cls, name)]:
			for ell in el:
				AmpelTags.hashes[ell] = int.from_bytes(
					# don't undestand why pylint complains about  digest_size
					# pylint: disable=unexpected-keyword-arg
					hashlib.blake2b(
						bytes(ell, "ascii"), 
						digest_size=7
					).digest(), 
					byteorder=sys.byteorder
				)
	
		if len(AmpelTags.hashes) != len(set(AmpelTags.hashes.values())):
			raise ValueError("Hash collision detected")

AmpelTags.add_hashes(AmpelTags)
