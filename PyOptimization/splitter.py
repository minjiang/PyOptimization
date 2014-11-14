import os
import re
import platform
import fnmatch
import configparser

def splite(path, ext):
	f = open(path, 'r')
	text = f.read()
	f.close()
	data = map(lambda _text: _text.strip(), re.split('[\r\n]\s*[\r\n]', text))
	for index, _text in enumerate(filter(lambda _text: _text, data)):
		parent = os.path.splitext(path)[0]
		os.makedirs(parent, exist_ok = True)
		_path = os.path.join(parent, str(index) + ext)
		_f = open(_path, 'w')
		_f.write(_text)
		_f.close()
	f.close()

def main():
	config = configparser.ConfigParser()
	config.read(os.path.splitext(__file__)[0] + '.ini')
	name = os.path.splitext(os.path.basename(__file__))[0]
	pathRoot = config.get(name, 'root.' + platform.system())
	pattern = config.get(name, 'pattern')
	ext = config.get(name, 'ext')
	paths = []
	for pathParent, _, fileNames in os.walk(pathRoot):
		for fileName in fileNames:
			if fnmatch.fnmatch(fileName, pattern):
				path = os.path.join(pathParent, fileName)
				paths.append(path)
	for path in paths:
		print(path)
		splite(path, ext)

if __name__ == '__main__':
	main()