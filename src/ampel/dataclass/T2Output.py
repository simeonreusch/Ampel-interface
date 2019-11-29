#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/dataclass/T2Output.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 29.11.2019
# Last Modified Date: 29.11.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from typing import Any, Dict, Union, Optional
from pydantic.dataclasses import dataclass

@dataclass
class T2Output:
	journal: Optional[Dict[str, Union[float, int, str]]]
	content: Dict[str, Any]
