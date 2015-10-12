import os
from time import sleep
import datetime
import re
from clint.textui import colored
import sys
import re
import configparser

class Underwatcher:
	
	def __init__(self):
		
		self.running = False
		
		self.validateConfig()
		
		config = configparser.ConfigParser()
		config.read('underwatch.ini')
		
		self.savePath = config['Undertale']['savePath']
		self.outputPath = config['Underwatch']['outputPath']
		if not os.path.exists(self.outputPath):
			os.makedirs(self.outputPath)
		
		self.outputMode = config['Underwatch']['outputMode']
		self.outputMultiple = config.getboolean('Underwatch','outputMultiple')
		self.quietMode = config.getboolean('Underwatch','quietMode')
		self.timestampFormat = config['Underwatch']['timestampFormat']
		if self.timestampFormat == '':
			self.timestamp = False
			self.timestampFormat = "%Y-%m-%d %H.%M.%S"
		else:
			self.timestamp = True
		
		self.watchDescriptions = config.getboolean('Underwatch','watchDescriptions')
		self.persistentMode = config.getboolean('Underwatch','persistentMode')
		self.exit = not self.persistentMode

		self.modtimes = {}
		self.fileContents = {}

		if self.watchDescriptions:
			self.modtimes["_saveFile"] = os.path.getmtime("_saveFile")
		self.setSaveDescriptions()
		
		for file in os.listdir(self.savePath):
			filepath = os.path.join(self.savePath,file)
			self.modtimes[file] = os.path.getmtime(filepath)
			self.readFile(filepath)
	
	def validateConfig(self):
		if os.path.isfile("underwatch.ini"):
			print('Config OK.')
		else:
			self.createConfig()
	
	def createConfig(self):
		print("No config file found. \nCreating one now...")

		config = configparser.ConfigParser()
		
		path = "C:\\Users\\<user>\\AppData\\Local\\UNDERTALE"
		user = os.environ.get("USERNAME")
		path = path.replace("<user>", user)
		print("Using {} as Undertale data path".format(path))
		r = input("Is this correct? y/n: ")
		if "n" in r.lower():
			path = input("Path: ")
			pathIsValid = os.path.exists(path)
			while not (pathIsValid):
				print("The path you entered was not valid.\n")
				path = input("Path: ")
				pathIsValid = os.path.exists(path)
			
		config['Undertale'] = {
			'savePath': path}
		
		defaultOutputPath = os.getcwd()
		defaultOutputPath += "\\outputLogs\\"
		
		config['Underwatch'] = {
			'outputPath': defaultOutputPath,
			'outputMode': 'sequence',
			'outputMultiple': 'false',
			'timestampFormat': '',
			'quietMode':'false',
			'watchDescriptions':'false',
			'persistentMode':'false'
		}
		with open('underwatch.ini', 'w') as configfile:
			config.write(configfile)
		
		self.validateConfig()
	
	
	def setSaveDescriptions(self):
		
		with open("_saveFile", 'r') as f:
			self.saveFileLines = [l.strip('\r\n"') for l in f.read().split(",")]
	
	def readFile(self, filepath):
		
		file = filepath.split("\\")[-1]
		with open(filepath, 'r') as f:
			if 'ini' in file:
				self.fileContents[file] = {}
				for line in f.readlines():
					if '[' in line:
						section = section = line.strip("\r\n[]")
						self.fileContents[file][section] = {}
					elif '=' in line:
						key = line.split("=")[0]
						value = line.split("=")[1].split('"')[1]
						self.fileContents[file][section][key] = value
			else:
				self.fileContents[file] = []
				for line in f.readlines():
					self.fileContents[file].append(line)
	
	def start(self):
		self.running = True
		if not self.quietMode:
			print("Underwatch started.")
		while True:
			try:
				for file in os.listdir(self.savePath):
					self.currentFile = file
					filepath = os.path.join(self.savePath,file)
					modtime = os.path.getmtime(filepath)
					if file in self.modtimes:
						modified = modtime != self.modtimes[file]
					else:
						self.modtimes[file] = modtime
						self.output("File created: {}".format(file))
						if file == "playerachievementcache.dat":
							modified = False
						else:
							modified = True
					if modified:
						if file == "playerachievementcache.dat" and self.exit: # As far as I know this file is only modified when exiting the game
							sys.exit(0)										   # (other than on creation) and it's easier than checking for the process
						self.modtimes[file] = modtime
						if self.timestamp and self.outputMode != "sequence":
							modDatetime = datetime.datetime.fromtimestamp(self.modtimes[file])
							self.output("{}".format(modDatetime.strftime(self.timestampFormat)))
						if self.outputMultiple != True:
							self.output("{} changed".format(file))
						elif not self.quietMode:
							print("{} changed".format(file))
						if '.ini' in file:
							self.parseini(filepath)
						elif 'file' in file:
							self.parseSave(filepath)
						self.output("")
				if self.watchDescriptions:
					modtime = os.path.getmtime("_saveFile")
					if modtime != self.modtimes["_saveFile"]:
						self.modtimes["_saveFile"] = modtime
						self.setSaveDescriptions()
				sleep(0.1)
			except KeyboardInterrupt:
				sys.exit(0)
					
	def output(self,output):
		escapePattern = re.compile(r'\x1b[^m]*m')
		cleanOutput = escapePattern.sub("", output)  # Strip the escape codes used to colour the ouput
		if not self.quietMode:
			print(output)
		if self.outputMode == "file":
			if self.outputMultiple:
				filename = "{}.log".format(self.currentFile)
			else:
				filename = "Underwatch.log"
			filepath = os.path.join(self.outputPath, filename)
			if os.path.isfile(filepath):
				mode = 'a'
			else:
				mode = 'w'
			with open(filepath, mode) as f:
				print(cleanOutput, file=f)
		elif self.outputMode == "sequence":
			if self.outputMultiple:
				filename = "{}.{}.log".format(self.currentFile, "{}")
			else:
				filename = "Underwatch.{}.log"
			modDatetime = datetime.datetime.fromtimestamp(self.modtimes[self.currentFile])
			filepath = os.path.join(self.outputPath, filename.format(modDatetime.strftime(self.timestampFormat)))
			if os.path.isfile(filepath):
				mode = 'a'
			else:
				mode = 'w'
			with open(filepath, mode) as f:
				print(cleanOutput, file=f)
				
	def parseini(self, filepath):
		file = filepath.split("\\")[-1]
		with open(filepath, 'r') as f:
			for line in f.readlines():
				if '[' in line:
					section = line.strip("\r\n[]")
					sectionPrinted = False
					if not file in self.fileContents:
						self.fileContents[file] = {}
					if not section in self.fileContents[file]:
						self.fileContents[file][section] = {}
				elif '=' in line:
					key = line.split("=")[0]
					value = line.split("=")[1].split('"')[1]
					if key not in self.fileContents[file][section]:
						self.fileContents[file][section][key] = "_"
					original = self.fileContents[file][section][key]
					if value != original:
						if not sectionPrinted:
							self.output("[{}]".format(section))
							sectionPrinted = True
						self.output("{}: {} >> {}".format(key, colored.red(original), colored.green(value)))
						self.fileContents[file][section][key] = value

	def parseSave(self, filepath):
		file = filepath.split("\\")[-1]
		with open(filepath, 'r') as f:
			i = 0
			for line in f.readlines():
				if file not in self.fileContents:
					self.fileContents[file] = []
				if len(self.fileContents[file]) <= i:
					self.fileContents[file].append("_")
				original = self.fileContents[file][i]
				if line != original:
					description = self.saveFileLines[i]
					if description == "":
						description = "unknown"
					self.output("({}) {} >> {} ({})".format(i+1, colored.red(original), colored.green(line), description).replace('\n','').replace('\r',''))
					self.fileContents[file][i] = line
				i += 1

if __name__ == "__main__":
	watcher = Underwatcher()
	watcher.start()
