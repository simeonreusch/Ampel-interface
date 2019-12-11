#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : ampel/base/PhotoData.py
# License           : BSD-3-Clause
# Author            : vb <vbrinnel@physik.hu-berlin.de>
# Date              : 13.01.2018
# Last Modified Date: 21.02.2019
# Last Modified By  : vb <vbrinnel@physik.hu-berlin.de>

from types import MappingProxyType
from ampel.base.Frozen import Frozen

class PhotoData(Frozen):
	"""
	Photometric data class. 
	Known child implementations: PhotoPoint, UpperLimit.

	This class convenience methods and should be able to 
	accomodate different 'formats' as long as the photometric 
	content is encoded in a one-dimensional dict. 
	The mapping between - let's call them ampel keywords such as 'mag'
	and the keywords of the underlying photopoint dict (for ZTF-IPAC 'magpsf')
	is achieved using the static variable 'default_keywords'
	"""

	default_keywords = {
		'ZTFIPAC': {
			"obsDate": "jd",
			"filter_id": "fid",
			"mag": "magpsf",
			"maglim": "diffmaglim",
			"magerr": "sigmapsf",
			"dec": "dec",
			"ra": "ra",
		}
	}

	@classmethod
	def set_keywords(cls, keywords):
		""" Usually set using ampel config values. """
		PhotoData.default_keywords = keywords


	def __init__(self, content, keywords=None, read_only=True):

		self.keywords = {} if keywords is None else keywords

		# Check wether to freeze this instance.
		if read_only:
			self.content = MappingProxyType(content)
			self.__isfrozen = True
		else:
			self.content = content


	def serialize(self):
		""" """
		return {"content": self.content}


	def get_value(self, field_name):
		""" """
		return self.content[
			self.keywords[field_name] if field_name in self.keywords	
			else field_name
		]


	def get_tuple(self, field1_name, field2_name):
		""" """
		return (
			self.content[
				self.keywords[field1_name] if field1_name in self.keywords 
				else field1_name
			], 
			self.content[
				self.keywords[field2_name] if field2_name in self.keywords 
				else field2_name
			]
		)
	

	def has_parameter(self, field_name):
		"""
		"""
		return (
			field_name in self.content if field_name not in self.keywords
			else self.keywords[field_name] in self.content 
		)


	def get_id(self):
		"""
		"""
		return self.content["_id"]