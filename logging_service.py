"""
This module is designed to centrally manage logging for the Chat Server.
"""

import datetime
import logging
from functools import wraps


class LoggingService(object):
	"""
	This class is designed to handle logging on the Chat Server.
	"""
	def __init__(self):
		"""
		Initializes the log
		"""
		logging.basicConfig(filename='chat_server.log' , level=logging.INFO)
		logging.info("{}: Started LoggingService")

	@staticmethod
	def logged(orig_func):
		"""
		To be used as a decorator to add logging to funcation calls.
		params:
			orig_func
		"""
		logging.basicConfig(filename='chat_server.log', level=logging.INFO)

		@wraps(orig_func)
		def wrapper(*args, **kwargs):
			logging.info('{}: function {} called with args={}, kwargs={}'
				.format(datetime.datetime, orig_func.__name__, args, kwargs)
			)
			return orig_func(*args, **kwargs)

		return wrapper
