import os

def get_filename(pathfile) :
	return pathfile.split(os.sep)[-1]

def get_path(pathfile) :
	return os.sep.join(pathfile.split(os.sep)[:-1])
	
def loud(*args, **kwargs) :
	print(" *******", *args, *kwargs, "******** ")
