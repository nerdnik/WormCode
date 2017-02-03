from RunPerseusFromPoints import get_intervals
from BuildRankFunction import build
from operator import add, div
import math

def calc(point_cloud_file_name, output_file_name, worm_length, sample_size, max_filtration_param, num_divisions, downsample = 1, start_sampling = 0, series_dimension = 3):
	point_cloud = open(point_cloud_file_name, "r")
	step = float(max_filtration_param)/float(num_divisions)
	sum_of_rank_functions = [0] * (int(math.pow(num_divisions, 2)) / 2 + (num_divisions + 1) / 2) # Length of list
	#print(sum_of_rank_functions)
	lines = point_cloud.read().split("\n")
	
	# First pass
	l = start_sampling
	#print(l)
	#return
	for i in xrange(sample_size):
		temp = open("Temp.txt", "w")
		temp.truncate() # Deletes previous contents
		temp.write(str(series_dimension) + "\n")
		temp.write(("1 %f %i" % (step, num_divisions)) + "\n")
		for j in xrange(worm_length):
			if (j % downsample == 0):
				temp.write(lines[l] + " " + str(step) + "\n")
			l += 1
		temp.close()
		#return
		get_intervals("Temp.txt", "PersistantHomology", max_filtration_param, num_divisions)
		#return
		for rf in build("PersistantHomology", num_divisions, 1): # Will only have one element if last parameter is passed (which it is)
			#print(sum_of_rank_functions)
			#print(rf)
			sum_of_rank_functions = map(add, sum_of_rank_functions, rf[0])
	average = []
	for num in sum_of_rank_functions:
		average.append(num / sample_size)
	#return
	
	# Second pass
	l = 0
	#point_cloud.seek(0)
	differences = []
	weights = get_weights(num_divisions)
	try:
		while (True):
			#print "Iterating..."
			temp = open("Temp.txt", "w")
			temp.truncate()
			temp.write(str(series_dimension) + "\n")
			temp.write(("1 %f %i" % (step, num_divisions)) + "\n")
			for j in xrange(worm_length):
				#print "j loop..."
				line = lines[l]
				#print line
				if not line:
					raise Exception # Break out of while loop
				#print "After..."
				if (j % downsample == 0):
					temp.write(line + " " + str(step) + "\n")
				l += 1
			temp.close()
			get_intervals("Temp.txt", "PersistantHomology", max_filtration_param, num_divisions)
			for rf in build("PersistantHomology", num_divisions, 1):
				#ta = get_distance(rf[0], average, weights)
				#print ta
				#differences.append(ta)
				differences.append(get_distance(rf[0], average, weights))
	except:# Exception as e:
		pass#print e
	output_file = open(output_file_name, "w")
	for p in differences:
		output_file.write(str(p) + "\n")


def get_weights(size, k = .5):
	to_return = []
	for x in range(1, size + 1):
		for y in range(x, size + 1):
			to_return.append(math.exp(-k * float(y - x)))
	return to_return

def get_distance(f, g, weights):
	if not (len(f) == len(g) == len(weights)):
		raise NameError("Lengths are not the same: %i %i %i" % (len(f), len(g), len(weights)))
	to_return = 0
	for i in xrange(len(f)):
		to_return += float(math.pow(f[i] - g[i], 2)) * weights[i]
	return to_return