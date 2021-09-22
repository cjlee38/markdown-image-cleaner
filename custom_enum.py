from enum import Enum, auto
import re
class CleanType(Enum) :
	DISPLAY = auto()
	SWEEP = auto()

class RegexHandler() :
	MARKDOWN_FILE = re.compile(".md$|.markdown$")
	IMAGE_FILE = re.compile(".jpg$|.png$")
	IMAGE_LINK = re.compile("!\[(.*?)\]\((.*?)\)")

	@staticmethod
	def is_pattern_match(name, regex) :
		return regex.search(name) is not None

class ContentType(Enum) :
	DIRECTORY = auto()
	FILE = auto()
