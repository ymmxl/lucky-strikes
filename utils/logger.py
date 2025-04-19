import logging
import logging.handlers
import os
import sys
import typing
import colorama
from datetime import datetime as dt
colorama.init(strip=False)
EscapeCodes = typing.Mapping[str, str]
LogColors = typing.Mapping[str, str]
default_log_colors = {
	"DEBUG": "white",
	"INFO": "blue",
	"WARNING": "yellow",
	"ERROR": "red",
	"CRITICAL": "bold_red",
}
default_format = {"{":"{log_color}[{name}][{levelname}][{asctime}.{msecs:0>3.0f}][{threadName:<7}] {message}"}
	#msecs is float and 0>3.0f round up and concantenate to 
	# logging.basicConfig(style = "{",
	# 	format="[{levelname}][{asctime}.{msecs:0>3.0f}][{threadName:<11}] {message}",
	# 	datefmt="%H:%M:%S",level=logging.INFO)

class EscapeCodeClass():
	@staticmethod
	def parse_colors(string: str) -> str:
		"""Return escape codes from a color sequence string."""
		return "".join(escape_codes[n] for n in string.split(",") if n)
	@staticmethod
	def esc(*codes: int) -> str:
		return "\033[" + ";".join(str(code) for code in codes) + "m"
		#\033[30;32m
escape_codes = {
	"reset": EscapeCodeClass.esc(0),
	"bold": EscapeCodeClass.esc(1),
	"thin": EscapeCodeClass.esc(2)
}
escape_codes_foreground = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "purple": 35,
    "cyan": 36,
    "white": 37,
    "light_black": 90,
    "light_red": 91,
    "light_green": 92,
    "light_yellow": 93,
    "light_blue": 94,
    "light_purple": 95,
    "light_cyan": 96,
    "light_white": 97,
}
class ColoredRecord:
	"""
	Wraps a LogRecord, adding escape codes to the internal dict.

	The internal dict is used when formatting the message (by the PercentStyle,
	StrFormatStyle, and StringTemplateStyle classes).
	"""

	def __init__(self, record: logging.LogRecord, escapes: EscapeCodes) -> None:
		self.__dict__.update(record.__dict__)
		self.__dict__.update(escapes)

class ColoredFormatter(logging.Formatter):
	def __init__(
		self,
		fmt = None,
		datefmt = None,
		style = "{",
		log_colors = None,
		reset = True,
		validate = True,
		stream = None,
		no_color = False
		) -> None:
		fmt = default_format[style] if fmt is None else fmt
		datefmt = "%H:%M:%S" if datefmt is None else datefmt
		super().__init__(fmt,datefmt,style,validate)
		self.log_colors = log_colors if log_colors is not None else default_log_colors
		self.reset = reset
		self.stream = stream
		self.no_color = no_color

	def formatMessage(self, record: logging.LogRecord) -> str:
		"""Format a message from a record object."""
		escapes = self._escape_code_map(record.levelname)
		wrapper = ColoredRecord(record, escapes)
		message = super().formatMessage(wrapper)  # type: ignore
		message = self._append_reset(message, escapes)
		return message

	def _escape_code_map(self,item:str) -> EscapeCodes:
		"""
		Build a map of keys to escape codes for use in message formatting.

		If _blank_escape_codes() returns True, all values will be an empty string.
		"""
		# Foreground without prefix
		for name, code in escape_codes_foreground.items():
		    escape_codes["%s" % name] = EscapeCodeClass.esc(code)
		    escape_codes["bold_%s" % name] = EscapeCodeClass.esc(1, code)
		    escape_codes["thin_%s" % name] = EscapeCodeClass.esc(2, code)

		# Foreground with fg_ prefix
		for name, code in escape_codes_foreground.items():
		    escape_codes["fg_%s" % name] = EscapeCodeClass.esc(code)
		    escape_codes["fg_bold_%s" % name] = EscapeCodeClass.esc(1, code)
		    escape_codes["fg_thin_%s" % name] = EscapeCodeClass.esc(2, code)

		# # Background with bg_ prefix
		# for name, code in escape_codes_background.items():
		#     escape_codes["bg_%s" % name] = EscapeCodeClass.esc(code)

		# 256 colour support
		for code in range(256):
		    escape_codes["fg_%d" % code] = EscapeCodeClass.esc(38, 5, code)
		    escape_codes["bg_%d" % code] = EscapeCodeClass.esc(48, 5, code)		
		
		codes = {**escape_codes}
		codes.setdefault("log_color",self._get_escape_code(self.log_colors, item))
		if self._blank_escape_codes():
			codes = {key: "" for key in codes.keys()}
		return codes

	def _blank_escape_codes(self):
		"""Return True if we should be prevented from printing escape codes."""
		if self.no_color:
			return True
		if self.stream is not None and not self.stream.isatty():
			return True
		return False
	@staticmethod
	def _get_escape_code(log_colors: LogColors,item: str) -> str:
		"""Extract a color sequence from a mapping, and return escape codes."""
		return EscapeCodeClass.parse_colors(log_colors.get(item, ""))

	def _append_reset(self, message: str, escapes: EscapeCodes) -> str:
		"""Add a reset code to the end of the message, if it's not already there."""
		reset_escape_code = escapes["reset"]
		if self.reset and not message.endswith(reset_escape_code):
			message+= reset_escape_code
		return message

class LevelFormatter:
	"""An extension of ColoredFormatter that uses per-level format strings."""
	def __init__(self, fmt: typing.Mapping[str, str], **kwargs: typing.Any) -> None:
		"""
		Configure a ColoredFormatter with its own format string for each log level.

		Supports fmt as a dict. All other args are passed on to the
		``colorlog.ColoredFormatter`` constructor.

		:Parameters:
		- fmt (dict):
			A mapping of log levels (represented as strings, e.g. 'WARNING') to
			format strings. (*New in version 2.7.0)
		(All other parameters are the same as in colorlog.ColoredFormatter)

		Example:

		formatter = colorlog.LevelFormatter(
			fmt={
				"DEBUG": "%(log_color)s%(message)s (%(module)s:%(lineno)d)",
				"INFO": "%(log_color)s%(message)s",
				"WARNING": "%(log_color)sWRN: %(message)s (%(module)s:%(lineno)d)",
				"ERROR": "%(log_color)sERR: %(message)s (%(module)s:%(lineno)d)",
				"CRITICAL": "%(log_color)sCRT: %(message)s (%(module)s:%(lineno)d)",
			}
		)
		"""
		self.formatters = {
			level: ColoredFormatter(fmt=f, **kwargs) for level, f in fmt.items()
		}
		def format(self, record: logging.LogRecord) -> str:
	   		return self.formatters[record.levelname].format(record)

def setup_logger(LOGFILEPATH=None,name=None):
	logging.addLevelName(35,"SUCCESS")
	formatter = ColoredFormatter(reset=True,
		log_colors={
			"DEBUG": "cyan",
			"INFO": "cyan",
			"SUCCESS": "green",
			"WARNING": "yellow",
			"ERROR": "red",
			"CRITICAL": "red",		
		},)
	stream = logging.StreamHandler()
	stream.setLevel(logging.INFO)
	stream.setFormatter(formatter)

	LOGFILEPATH = os.path.join(os.getcwd(),"logs")
	if not os.path.exists(LOGFILEPATH):
		os.mkdir(LOGFILEPATH)
	now = dt.now().strftime("%y%m%d %H-%M-%S")	
	rfile = logging.handlers.RotatingFileHandler(
		f"{LOGFILEPATH}\\{now}.log",maxBytes=2000000,backupCount=5)
	format2 = logging.Formatter(style="{",fmt="[{name}][{levelname}][{asctime}.{msecs:0>3.0f}][{threadName:<11}] {message}",datefmt="%H:%M:%S")
	rfile.setFormatter(format2)	
	rfile.setLevel(logging.DEBUG)
	logging.basicConfig(
		datefmt = None,
		style = "{",
		level = logging.DEBUG,
		handlers=[
			stream,
			rfile],
		force=True
		)
	def success(self,message,*args,**kwargs):
		if self.isEnabledFor(35):
			#if yes: logger takes in *args and **kwargs
			self._log(35,message,args,**kwargs)
	if name:
		logger = logging.getLogger(name)
	else:
		logger = logging.getLogger(__name__)
	logging.Logger.success = success
	logging.success = success
	# print(logger.handlers)
	# print(len(logging.root.handlers))
	return logger
	# if name:
	# 	logger = logging.getLogger(name)
	# else:
	# 	logger = logging.getLogger(__name__)
	# logger.propagate = False
	# handler = logging.StreamHandler(sys.stdout)
	# handler.setFormatter(formatter)
	# logger.addHandler(handler)

	# LOGFILEPATH = os.path.join(os.getcwd(),"logs")
	# #rint(LOGFILEPATH)
	# if not os.path.exists(LOGFILEPATH):
	# 	os.mkdir(LOGFILEPATH)
	# now = dt.now().strftime("%y%m%d %H-%M-%S")
	# hand2 = logging.handlers.RotatingFileHandler(
	# 	f"{LOGFILEPATH}\\{now}.log",maxBytes=2000000,backupCount=5)
	# format2 = logging.Formatter(style="{",fmt="[{levelname}][{asctime}.{msecs:0>3.0f}][{threadName:<11}] {message}",datefmt="%H:%M:%S")
	# hand2.setFormatter(format2)
	# logger.addHandler(hand2)
	# logger.setLevel(logging.DEBUG)
	# def success(self,message,*args,**kwargs):
	# 	if self.isEnabledFor(35):
	# 		#if yes: logger takes in *args and **kwargs
	# 		self._log(35,message,args,**kwargs)
	# logging.Logger.success = success
	# logging.success = success
	# print(logger.handlers)
	# print(len(logging.root.handlers))
	# return logger

if __name__ == '__main__':
	log = setup_logger()
	log.success("green green green!")
	log.debug("a debug message")
	log.info("an info message")
	log.warning("a warning message")
	log.error("an error message")
	log.critical("a critical message")

