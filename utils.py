import os

def get_filename(pathfile) :
	return pathfile.split(os.sep)[-1]

def get_path(pathfile) :
	return os.sep.join(pathfile.split(os.sep)[:-1])

def exclude_ignores(parent: str, dirs: list, ignores: list) -> list :
	includes = []
	for dir in dirs :
		if dir.startswith(".") : # like .git
			continue
		joindir = pathjoin(parent, dir)
		for ignore in ignores :
			if os.path.relpath(joindir, ignore) == "." : # ignore == current dir
				break
		else : # didn't break
			includes.append(dir)
	return includes

def pathjoin(*paths) :
	return os.sep.join(paths)

def exists(path, error = True) :
	exist = os.path.exists(path)
	if not exist :
		raise Exception(f"There is no directory or file \"{path}\", Check it again")
	

def loud(*args, **kwargs) :
	print(" *******", *args, *kwargs, "******** ")
