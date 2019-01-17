#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/base/flags/PhotoFlags.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 14.12.2017
# Last Modified Date: 18.01.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from abc import ABCMeta

class PhotoFlags(metaclass=ABCMeta):
	"""
	"""

	PHOTOPOINT                = ()
	UPPERLIMIT                = ()
	SUPERSEDED                = ()

	IMAGE_BAD_CALIBRATION     = ()
	IMAGE_ARTIFACT            = ()
	IMAGE_TRACKING_PBLM       = ()
	IMAGE_FOCUS_PBLM          = ()
