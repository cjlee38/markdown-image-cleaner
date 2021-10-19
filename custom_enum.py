from enum import Enum, auto
import re

class RegexHandler() :
	MARKDOWN_FILE = re.compile(".md$|.markdown$")
	IMAGE_FILE = re.compile(".jpg$|.png$|.gif$")
	IMAGE_LINK = re.compile("!\[(.*?)\]\((.*?)\)")

	@staticmethod
	def is_pattern_match(name, regex) :
		return regex.search(name) is not None

class ContentType(Enum) :
	DIRECTORY = auto()
	FILE = auto()
