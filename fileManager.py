import os.path
import json

def openJson(path):
	with open(path, "r") as f:
		try:
			return json.load(f)
		except json.decoder.JSONDecodeError:
			return {}

def writeJson(path, text, indent = 4):
	with open(path, "w") as f:
		f.write(json.dumps(text, indent = indent))

def joinPath(path, add):
	return os.path.join(path, add)

def baseName(path):
	return os.path.split(path)[1]

def exists(path):
	return os.path.exists(path)

def split(path):
	return os.path.split(path)