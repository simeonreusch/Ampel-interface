#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/base/AmpelAlert.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 14.12.2017
# Last Modified Date: 18.01.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

import operator
from types import MappingProxyType
from ampel.base.Frozen import Frozen

class AmpelAlert(Frozen):
	"""
	T0 base class containing a read-only list of read-only photopoint dictionaries.
	(read-only convertion occurs in constructor).
	During pipeline processing, an alert is loaded and its content used to instantiate this class. 
	Then, the AmpelAlert instance is fed to every active T0 filter.
	"""

	alert_keywords = {}
	alert_kws_set = set()

	ops = {
		'>': operator.gt,
		'<': operator.lt,
		'>=': operator.ge,
		'<=': operator.le,
		'==': operator.eq,
		'!=': operator.ne,
		'is': operator.is_,
		'is not': operator.is_not
	}


	@staticmethod
	def load_ztf_alert(arg):
		"""	
		Convenience method.
		Do not use for production!
		"""
		import fastavro
		with open(arg, "rb") as fo:
			al = next(fastavro.reader(fo), None)

		if al.get('prv_candidates') is None:
			return AmpelAlert(
				al['objectId'], tuple([MappingProxyType(al['candidate'])]), None
			)
		else:
			pps = [MappingProxyType(d) for d in al['prv_candidates'] if d.get('candid') is not None]
			pps.insert(0,  MappingProxyType(al['candidate']))
			return AmpelAlert(
				al['objectId'], tuple(pps), 
				tuple(MappingProxyType(d) for d in al['prv_candidates'] if d.get('candid') is None)
			)


	@classmethod
	def set_alert_keywords(cls, alert_keywords):
		"""
		Set using ampel config values. For ZTF IPAC alerts:
		.. code-block:: python
		
			alert_keywords = {
				"transient_id" : "objectId",
				"photopoint_id" : "candid",
				"obs_date" : "jd",
				"filter_id" : "fid",
				"mag" : "magpsf"
			}
		"""
		cls.alert_keywords = alert_keywords
		cls.alert_kws_set = set(alert_keywords.keys())


	def __init__(self, tran_id, list_of_pps, list_of_uls=None):
		""" 
		AmpelAlert constructor
		Parameters:
		:param alertid: unique identifier of the alert (for ZTF: candid of most recent photopoint)
		:param tran_id: the astronomical transient object ID, for ZTF IPAC alerts 'objectId'
		:param list_of_pps: a flat list of photopoint dictionaries. 
		Ampel makes sure that each dictionary contains an alTags key 
		"""
		self.tran_id = tran_id
		self.pps = list_of_pps
		self.uls = list_of_uls

		# Freeze this instance
		self.__isfrozen = True


	def get_values(self, param_name, filters=None, upper_limits=False):
		"""
		ex: instance.get_values("mag")
		"""
		if param_name in AmpelAlert.alert_keywords:
			param_name = AmpelAlert.alert_keywords[param_name]

		photo_objs = self._get_photo_objs(filters, upper_limits)
		if photo_objs is None:
			return None

		return tuple(el[param_name] for el in photo_objs if param_name in el)


	def get_tuples(self, param1, param2, filters=None, upper_limits=False):
		"""
		ex: instance.get_tuples("obs_date", "mag")
		"""
		if param1 in AmpelAlert.alert_keywords:
			param1 = AmpelAlert.alert_keywords[param1]

		if param2 in AmpelAlert.alert_keywords:
			param2 = AmpelAlert.alert_keywords[param2]

		photo_objs = self._get_photo_objs(filters, upper_limits)
		if photo_objs is None:
			return None

		return tuple(
			(el[param1], el[param2]) 
			for el in photo_objs if param1 in el and param2 in el
		)


	def get_ntuples(self, params, filters=None, upper_limits=False):
		"""
		:param params: list of strings
		ex: instance.get_ntuples(["fid", "obs_date", "mag"])
		"""
		# If any of the provided parameter matches defined keyword mappings
		if AmpelAlert.alert_kws_set & set(params):
			for i, param in enumerate(params):
				if param in AmpelAlert.alert_keywords:
					params[i] = AmpelAlert.alert_keywords[param]
	
		photo_objs = self._get_photo_objs(filters, upper_limits)
		if photo_objs is None:
			return None

		return tuple(
			tuple(el[param] for param in params) 
			for el in photo_objs if all(param in el for param in params)
		)


	def _get_photo_objs(self, filters, upper_limits):
		""" """

		# Filter photopoints if filter was provided
		if filters is None:
			return self.uls if upper_limits else self.pps
		else:
			return self.apply_filter(self.uls, filters) if upper_limits else self.apply_filter(self.pps, filters)


	def get_photopoints(self):
		""" returns a list of dicts """
		return self.pps


	def get_upperlimits(self):
		""" returns a list of dicts """
		return self.uls


	def get_id(self):
		"""
		returns the transient Id (ZTF: objectId)
		"""
		return self.tran_id


	def apply_filter(self, match_objs, filters):
		"""
		"""

		if type(filters) in (dict, MappingProxyType):
			filters = [filters]
		else:
			if filters is None or type(filters) not in (list, tuple):
				raise ValueError("filters must be of type dict or list/tuple")

		for filter_el in filters:

			operator = AmpelAlert.ops[
				filter_el['operator']
			]

			filter_attr_name = filter_el['attribute']
			attr_name = (
				filter_attr_name if not filter_attr_name in AmpelAlert.alert_keywords 
				else AmpelAlert.alert_keywords[filter_attr_name]
			)

			match_objs = tuple(
				filter(
					lambda el: attr_name in el and operator(el[attr_name], filter_el['value']), 
					match_objs
				)
			)

		return match_objs
