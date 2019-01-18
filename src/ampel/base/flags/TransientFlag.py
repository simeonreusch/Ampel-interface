#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/base/flags/TransientFlag.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 14.12.2017
# Last Modified Date: 18.01.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from abc import ABCMeta

class TransientFlag(metaclass=ABCMeta):
	"""
	"""
	HAS_ERROR                   = ()
	HAS_TNS_NAME                = ()
	MIXED_DATA_SOURCE           = ()
	T1_AUTO_COMPLETE            = ()
