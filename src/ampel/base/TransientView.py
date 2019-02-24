#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/base/TransientView.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.01.2018
# Last Modified Date: 20.02.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import warnings
from datetime import datetime
from bson.binary import Binary
from typing import Dict, Optional

from ampel.base.Frozen import Frozen
from ampel.base.LightCurve import LightCurve
from ampel.base.PlainPhotoPoint import PlainPhotoPoint
from ampel.base.PlainUpperLimit import PlainUpperLimit

class TransientView(Frozen):
	"""
	Container class referencing various instances of objects:
	
	- :py:class:`ampel.base.PlainPhotoPoint.PlainPhotoPoint`
	- :py:class:`ampel.base.PlainUpperLimit.PlainUpperLimit`
	- :py:class:`ampel.base.Compound.Compound`
	- :py:class:`ampel.base.LightCurve.LightCurve`
	- :py:class:`ampel.base.ScienceRecord.ScienceRecord`
	
	Instances of this class are provided to T3 modules and are typically 
	generated using a TransientData instance created by DBContentLoader.
	"""

	def __init__(self, 
		tran_id, tags, journal, tran_names=None, latest_state=None,
		photopoints=None, upperlimits=None, compounds=None, 
		lightcurves=None, t2records=None, channel=None
	):
		"""
		"""
		self.tran_id = tran_id
		self.tran_names = tran_names
		self.tags = tags
		self.journal = journal
		self.latest_state = latest_state
		self.photopoints = photopoints
		self.upperlimits = upperlimits
		self.compounds = compounds
		self.lightcurves = lightcurves
		self.t2records = t2records
		self.channel = channel
		self.__isfrozen = True


	def serialize(self):
		""" """
		return {
			k: getattr(self, k) for k in [
				"tran_id", "tran_names", "tags", "journal", "latest_state", "photopoints", 
				"upperlimits", "compounds", "lightcurves", "t2records", "channel"
			]
		}


	def get_tags(self):
		""" """
		return self.tags


	def get_latest_lightcurve(self, logger=None):
		""" 
		"""
		if logger is None:
			warn = warnings.warn
		else:
			warn = logger.warn
		if self.latest_state is None:
			warn('Request for latest lightcurve cannot complete (latest state not set)')
			return None

		if len(self.lightcurves) == 0:
			warn('Request for latest lightcurve cannot complete (No lightcurve was loaded)')
			return None

		res = next(filter(lambda x: x.id == self.latest_state, self.lightcurves), None)
		if res is None:
			warn(
				'Request for latest lightcurve cannot complete (Lightcurve %s not found)' % 
				self.latest_state		
			)
			return None

		return res


	def get_latest_state(self, to_hex=False):
		""" """
		if self.latest_state is None:
			return None

		return self.latest_state.hex() if to_hex else self.latest_state


	def get_photopoints(self) -> Optional[Dict[int,PlainPhotoPoint]]:
		"""
		:returns: a dict of photopoint ids and photopoints, or None if photopoints were not loaded
		"""
		return self.photopoints
	

	def get_upperlimits(self) -> Optional[Dict[int,PlainUpperLimit]]:
		"""
		:returns: a dict of upper limit ids and upper limits, or None if upper limits were not loaded
		"""
		return self.upperlimits


	def get_compounds(self, copy=False):
		"""
		Returns a tuple of MappingProxyType instances or None if Compounds were not loaded 
		"""
		return self.compounds


	def get_compound(self, compound_id):
		""" 
		Returns an instance of MappingProxyType or None if no Compound exists with the provided id
		lightcurve_id: either a bson Binary instance (with subtype 5) or a string with length 32
		"""
		if type(compound_id) is str:
			compound_id = Binary(bytes.fromhex(compound_id), 5)
		return next(filter(lambda x: x.id == compound_id, self.compounds), None)


	def get_lightcurves(self):
		"""
		Returns a tuple of ampel.base.LightCurve instances or None if Compounds were not loaded 
		"""
		return self.lightcurves

	
	def get_lightcurve(self, lightcurve_id):
		""" 
		Returns an instance of ampel.base.LightCurve 
		or None if no LightCurve exists with the provided lightcurve_id
		lightcurve_id: either a bson Binary instance (with subtype 5) or a string with length 32
		"""
		if type(lightcurve_id) is str:
			lightcurve_id = Binary(bytes.fromhex(lightcurve_id), 5)
		return next(filter(lambda x: x.id == lightcurve_id, self.lightcurves), None)


	def get_science_records(self, t2_unit_id=None, latest=False):
		""" 
		Returns an instance or a tuple of instances of ampel.base.ScienceRecord 
		t2_unit_id: string. Limit returned science record(s) to the one with the provided t2 unit id
		latest: boolean. Whether to return the latest science record(s) or not
		"""
		if latest:

			if self.latest_state is None:
				return None
		
			if t2_unit_id is None:
				return next(
					filter(
						lambda x: self.latest_state in x.compound_id,
						self.t2records
					), None
				)
			else:
				return next(
					filter(
						lambda x: self.latest_state in x.compound_id and x.t2_unit_id == t2_unit_id,
						self.t2records
					), None
				)
		else:

			if t2_unit_id is None:
				return self.t2records
			else:
				return tuple(
					filter(
						lambda x: x.t2_unit_id == t2_unit_id,
						self.t2records
					)
				)


	def get_journal_entries(self, tier=None, t3JobName=None, filterFunc=None, latest=False):
		"""
			return journal entries corresponding to a given tier, job, or fulfilling
			some user defined criteria.
			
			:param tier: string, filter according to je.get('tier') == tier 
			:param t3JobName: string, filter to get('t3JobName') == t3JobName
			:param filteFunc: callable: je --> bool, used to filter according to filteFunc(je).
			:param latest: bool, return just the last entry in the journal.
		"""
		if tier is None and t3JobName is None and filterFunc is None:
			entries = self.journal
		elif not filterFunc is None:
			entries = tuple(filter(filterFunc, self.journal))
		else:
			if None in (tier, t3JobName):
				entries = (
					tuple(filter(lambda x: x.get('t3JobName') == t3JobName, self.journal)) if tier is None
					else tuple(filter(lambda x: x.get('tier') == tier, self.journal))
				)
			else:
				entries = tuple(filter(
					lambda x: x.get('tier') == tier and x.get('t3JobName') == t3JobName, self.journal
				))

		if len(entries) == 0:
			return None

		if not latest:
			return entries
		else:
			return sorted(entries, key=lambda x: x['dt'])[-1]
#		return entries[-1] if latest else entries


	def get_time_created(self, format_time=None):
		""" """
		if self.journal is None or len(self.journal) == 0:
			return None
		return self._get_time(self.journal[0], format_time)


	def get_time_modified(self, format_time=None):
		""" """
		if self.journal is None or len(self.journal) == 0:
			return None
		return self._get_time(self.journal[-1], format_time)

		
	def _get_time(self, entry, format_time=None):
		""" """
		if format_time is None:
			return entry['dt']
		else:
			return datetime.fromtimestamp(entry['dt']).strftime(
				'%d/%m/%Y %H:%M:%S' if format_time is True else format_time
			)


	def print_info(self, logger):
		"""
		:param logger: instance of logging.Logger
		Prints "Content: PP: %i, UL: %i, CP: %i, LC: %i, SR: %i"
		Abbreviations: 
		- PP: photometric point 
		- UL: upper limit
		- CP: compound (set of pp/ul ids)
		- LC: light curve
		- SR: science record (output of T2 modules)

		:returns: None
		"""
		logger.info(
			"TransientView content: %s" % 
			TransientView.content_summary(self)
		)


	@staticmethod
	def content_summary(tran_view):
		"""
		:param tran_view: instance of ampel.base.TransientView
		:returns: str
		"""
		return "PP: %i, UL: %i, CP: %i, LC: %i, SR: %i" % (
			len(tran_view.photopoints) if tran_view.photopoints is not None else 0, 
			len(tran_view.upperlimits) if tran_view.upperlimits is not None else 0, 
			len(tran_view.compounds) if tran_view.compounds is not None else 0, 
			len(tran_view.lightcurves) if tran_view.lightcurves is not None else 0, 
			len(tran_view.t2records) if tran_view.t2records is not None else 0
		)
