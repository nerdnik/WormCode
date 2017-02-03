def build(input_file_name, number_of_steps, dimension = -1):
	if dimension == -1:
		try:
			while True:
				dimension += 1
				yield build_dim(input_file_name, step, number_of_steps, dimension)
		except Exception as e:
			print("EXCEPTION:")
			print(e)
	else:
		yield build_dim(input_file_name, number_of_steps, dimension)


def build_dim(input_file_name,  number_of_steps, dimension):
	real_name = input_file_name + ("_%i.txt" % dimension)
	input_file = open(real_name, "r")
	births = []
	deaths = []
	events = 0
	largest_persistent_feature = 0
	for line in input_file:
		data = line.split()
		events += 1
		id1 = int(data[0])
		id2 = 0
		if data[1] == "-1":
			id2 = number_of_steps - 1 # Requires smart input
		else:
			id2 = int(data[1])
		births.append(id1) # TODO: possible rounding error
		deaths.append(id2)
		#print("Largest feature: %f" % largest_persistent_feature[dimension_index])
		if id2 - id1 > largest_persistent_feature:
			#print("New max: %f" % (fd2 - fd1))
			largest_persistent_feature = id2 - id1
	#print("DI: %i" % dimension_index)
	#print(dimensions)
	return get_rank_function(births, deaths, number_of_steps, events), largest_persistent_feature

def get_rank_function(births, deaths, size, events):
	#print(births)
	#print(deaths)
	#print(events)
	to_return = []#[0]*(size^2 / 2 + (size + 1) / 2)
	decrements = [[]]
	for i in xrange(size + 1):
		decrements.append([])
	x_inc_count = [0] * (size + 2)
	for e in xrange(events):
		decrements[births[e]].append(deaths[e])
		x_inc_count[births[e]] += 1
		x_inc_count[deaths[e] + 1] -= 1
	value = 0
	x_inc = 0
	y_inc = [0] * (size + 1)
	#print(y_inc)
	#print(x_inc_count)
	#print(decrements)
	for x in xrange(size):
		x_inc += x_inc_count[x]
		#print("x_inc: %i" % x_inc)
		for decrement in decrements[x]:
			y_inc[decrement] -= 1
		value += x_inc
		for y in range(x, size):
			to_return.append(value)
			value += y_inc[y]
	return to_return