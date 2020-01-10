#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : Ampel-interface/src/ampel/view/ItemView.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.01.2018
# Last Modified Date: 10.01.2020
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from datetime import datetime
from dataclasses import dataclass
from typing import Dict, Optional, Union, Tuple, Any, Literal

from ampel.typing import StockId
from ampel.content.DataPoint import DataPoint
from ampel.content.Compound import Compound
from ampel.content.T2Record import T2Record


@dataclass(frozen=True)
class ItemView:
	"""
	A view of a given ampel object/item (with unique stock id).
	This class can contain various instances of objects (mostly from ampel.content)
	originating from different ampel tiers (T0, T1 and T2).
	It can also contain external/composite objects in the dict called 'extra' 
	(such as spectra or ampel.view.LightCurve instances for ex.)
	The T3 InitConfig process parameters will determine which information are present or not.
	
	Typically, instances of this class (or of a sub-class such as TransientView) are provided to T3 modules.
	"""

	stock_id: StockId
	names: Optional[Tuple[str, ...]]
	tags: Optional[Tuple[Union[int, str], ...]]
	channels: Tuple[Union[int, str], ...]
	journal: Tuple[Dict[str, Any], ...]
	datapoints: Optional[Tuple[DataPoint, ...]]
	compounds: Optional[Tuple[Compound, ...]]
	t2records: Optional[Tuple[T2Record, ...]]
	extra: Optional[Dict[str, Any]]


	def get_t2_records(self, 
		unit_id: Optional[Union[int, str]] = None,
		compound_id: Optional[bytes] = None
	) -> Optional[Tuple[T2Record, ...]]:
		""" 
		:param unit_id: limits the returned science record(s) to the one with the provided t2 unit id
		:param compound_id: whether to return the latest science record(s) or not (default: False)
		"""

		if self.t2records is None:
			return None

		if compound_id:

			if unit_id:
				return tuple(
					rec for rec in self.t2records 
					if rec.link == compound_id and rec.unit == unit_id
				)

			return tuple(rec for rec in self.t2records if rec.link == compound_id)

		if unit_id:
			return tuple(rec for rec in self.t2records if rec.unit == unit_id)

		return self.t2records


	def get_journal_entries(self, 
		tier: Optional[Literal[0, 1, 2, 3]] = None, 
		process_name: Optional[str] = None, 
		latest: bool = False
	) -> Optional[Union[Dict[str, Any], Tuple[Dict[str, Any], ...]]]:
		"""
		:param process_name: return only journal entries associated with a given process name
		:param last: return only the latest entry in the journal (the latest in time)
		Returns journal entries corresponding to a given tier and/or job.
		"""
		entries = self.journal

		if tier:
			entries = tuple(j for j in self.journal if j['tier'] == tier)

		if process_name:
			entries = tuple(j for j in entries if j['processName'] == process_name)

		if latest:
			return sorted(entries, key=lambda x: x['dt'])[-1]

		return entries


	def get_time_created(self, 
		output: Literal['raw', 'datetime', 'str'] = 'raw'
	) -> Optional[Union[float, datetime, str]]:
		""" """
		# Note: journal cannot be empty
		return self._get_time(self.journal[0], output)


	def get_time_modified(self, 
		output: Literal['raw', 'datetime', 'str'] = 'raw'
	) -> Optional[Union[float, datetime, str]]:
		""" """
		# Note: journal cannot be empty
		return self._get_time(self.journal[-1], output)

		
	@classmethod
	def _get_time(cls,
		entry: Dict[str, Any], 
		output: Optional[Union[bool, str]] = None
	) -> Union[float, str, datetime]:
		""" """
		if output == 'raw':
			return entry['dt']

		dt = datetime.fromtimestamp(entry['dt'])

		if output == 'datetime':
			return dt

		return dt.strftime('%d/%m/%Y %H:%M:%S')


	@staticmethod
	def content_summary(view: 'ItemView') -> str:
		""" """
		return "DP: %i, CP: %i, T2: %i" % (
			len(view.datapoints) if view.datapoints else 0, 
			len(view.compounds) if view.compounds else 0, 
			len(view.t2records) if view.t2records else 0
		)
