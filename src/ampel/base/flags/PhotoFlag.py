#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/base/flags/PhotoFlag.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 14.12.2017
# Last Modified Date: 18.01.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>


class PhotoFlag:
	""" """

	# Force subclassing
	def __init__(self):
		raise NotImplementedError() 

	PHOTOPOINT                = None
	UPPERLIMIT                = None
	SUPERSEDED                = None

	IMAGE_BAD_CALIBRATION     = None
	IMAGE_ARTIFACT            = None
	IMAGE_TRACKING_PBLM       = None
	IMAGE_FOCUS_PBLM          = None
