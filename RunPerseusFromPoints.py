from os import system, chdir

def get_intervals(input_file_name, output_file_name, format = False, max_filtration_param = 0.0, num_steps = 0, temp_file_name = "Temp.txt", series_dimension = 3):
	#input_file = open(input_file_name, "r")
	#output_file = open(output_file_name, "w")
	#TODO: run Dionysus, remove test line below
	#output_file.write("0 .2 .8\n0 .4 1.3\n0 1 1.1\n1 .5 1.2\n1 1.1 1.8")
	if format:
		input_file = open(input_file_name, "r")
		temp_file = open(temp_file_name, "w")
		temp_file.truncate()
		step = float(max_filtration_param)/float(num_steps)
		lines = input_file.read().split("\n")
		temp_file.write(str(series_dimension) + "\n")
		temp_file.write("1 %f %i\n" % (step, num_steps))
		for line in lines:
			temp_file.write("%s %f\n" % (line, step))
		input_file_name = temp_file_name
		input_file.close()
		temp_file.close()
	chdir("/Users/nicolesanderson/Desktop/Sams\ Worm\ Code")
	system("./perseusMac brips %s %s" % (input_file_name, output_file_name))