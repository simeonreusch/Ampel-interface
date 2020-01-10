#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/src/ampel/typing.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 02.12.2019
# Last Modified Date: 27.12.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

# type: ignore
# pylint: disable=import-self
from __future__ import absolute_import
from typing import TypeVar

StockId = TypeVar('StockId', bytes, int, str)
DataPointId = TypeVar('DataPointId', bytes, int)
StrictIterable = TypeVar('StrictIterable', list, set, tuple, frozenset)
strict_iterable = StrictIterable.__constraints__
