#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/base/flags/TransientFlag.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 14.12.2017
# Last Modified Date: 18.01.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>


class TransientFlag():
	""" """

	# Force subclassing
	def __init__(self):
		raise NotImplementedError() 

	HAS_ERROR                   = None
	HAS_TNS_NAME                = None
	MIXED_DATA_SOURCE           = None
	T1_AUTO_COMPLETE            = None
