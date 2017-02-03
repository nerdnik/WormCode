def embed(input_file_name, output_file_name, tau, m, coordinate = 0):
	input_file = open(input_file_name, "r")
	output_file = open(output_file_name, "w")
	output_file.truncate()
	lines = input_file.read().split("\n")
	series = []
	for line in lines:
		if line != "":
			str_coords = [x for x in line.split(" ") if x != ""]
			series.append(float(str_coords[coordinate]))
	end = len(lines) - (tau*(m - 1))
	for i in xrange(end):
		for j in xrange(m):
			output_file.write("%f " % series[i + (j*tau)])
		if i < end:
			output_file.write("\n")
	input_file.close()
	output_file.close()