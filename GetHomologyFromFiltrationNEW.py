from os import system, chdir
import os.path

class Paths:
	path_to_Perseus = None#"/Users/nicolesanderson/Software/Python/JTFworms/PythonScripts77"
	path_to_PHAT = None#"C:\Users\Jamie\Desktop\Work\LizSummer2016\Software\phat-master\src\phat.exe"

def compute_homology(input_file_name, output_file_name, program):
	#chdir(path)
	#print("Calculating persistent homology using %s..." % program)
	if program == "Perseus":
		if Paths.path_to_Perseus is None:
			raise Exception("Must first call 'set_path_to_Perseus(path)'")
		if output_file_name.endswith(".txt"):
			output_file_name = os.path.splitext(output_file_name)[0]#output_file_name.substring(0, len(output_file_name) - 4)
		output_file_name_TRY = '/Users/nicolesanderson/Desktop/Sams\ Worm\ Code/' + output_file_name
		print 'The output file is named %s' % output_file_name_TRY
		system("./perseusMac nmfsimtop %s %s" % (input_file_name, output_file_name_TRY))
	elif program == "PHAT":
		if Paths.path_to_PHAT is None:
			raise Exception("Must first call 'set_path_to_PHAT(path)'")
		system("%s --ascii %s %s" % (Paths.path_to_PHAT, input_file_name, output_file_name))
	else:
		raise Exception("Only supported programs are 'Perseus' and 'PHAT'.")

def set_path_to_Perseus(path):
	Paths.path_to_Perseus = path

def set_path_to_PHAT(path):
	Paths.path_to_PHAT = path