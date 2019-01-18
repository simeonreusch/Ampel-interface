#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/base/flags/AmpelMetaFlag.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.06.2018
# Last Modified Date: 18.01.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from enum import IntFlag

class AmpelMetaFlag(type):

	def __new__(metacls, name, bases, d, extends):

		flags=[]
		i=0

		for el in extends if type(extends) is list else [extends]:
			for ell in el.__dict__:
				if not ell.startswith('_'):
					flags.append((ell, 2**i))
					i+=1

		for k in d.keys():
			if not k.endswith('__'):
				flags.append((k, 2**i))
				i+=1

		return IntFlag(name, flags, module=d['__module__'])
