import argparse
import os

class ArgParser() :

	def __init__(self) :
		self.parser = argparse.ArgumentParser(description = 'markdown-image-cleaner')
		self.parser.add_argument('--clean-type', '-c', 
							type = str,
							choices = ["display", "collect", "sweep"],
							help = "Determine type to clean. \
								Options are display, collect, sweep. \
								Default value is display")
		self.parser.add_argument('--directory', '-d',
							type = str,
							help = "select directory to mark and clean. \
								Default is current directory(.)")
		self.parser.add_argument('--ignore-image', '-i',
							type = str,
							nargs = '+',
							help = "Ignore directories which contain image files.")
		self.parser.add_argument('--ignore-markdown', '-m',
							type = str,
							nargs = '+',
							help = "Ignore directories which contain markdown files.")

	def parse(self, configs: dict) -> dict :
		args = self.parser.parse_args()
		argv = dict(
			directory = args.directory,
			clean_type = args.clean_type,
			ignore_image = args.ignore_image,
			ignore_markdown = args.ignore_markdown
		)
		
		self.update(configs, argv)
		self.toabspath(configs)
		return configs

	def update(self, configs: dict, argv: dict) -> None : # inplace
		for key in configs.keys() :
			if argv[key] :
				configs[key] = argv[key]

	def toabspath(self, configs: dict) -> None : # inplace 
		configs['directory'] = os.path.abspath(configs['directory'])
		configs['ignore_image'] = [os.path.abspath(d) for d in configs['ignore_image']]
		configs['ignore_markdown'] = [os.path.abspath(d) for d in configs['ignore_markdown']]

		
		
