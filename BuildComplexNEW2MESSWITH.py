from sets import Set, ImmutableSet
import networkx as nx
import sys
import itertools
from heapq import heappush, heappop
import numpy as np
import math

standard_parameter_set = {
	"num_divisions": 50,
	"max_filtration_param": -20,
	"min_filtration_param": 0,
	"start": 0,
	"worm_length": 0,
	"ds_rate": 50,
	"landmark_selector": "maxmin",
	"use_ne_for_maxmin": False,
	"d_speed_amplify": 1,
	"d_orientation_amplify": 1,
	"d_stretch": 1,
	"d_ray_distance_amplify": 1,
	"d_use_hamiltonian": 0,
	"simplex_cutoff": 0,
	"weak": False,
	"absolute": False,
	"use_cliques": False,
	"use_twr": False,
	"m2_d": 0,
	"straight_VB" : False,
	"out": None,
	"program": "Perseus",
	"dimension_cutoff": 2,
	"time_order_landmarks": False,
	"connect_time_1_skeleton": False,
	"reentry_filter": False,
	"store_top_simplices": True,
	"sort_output": False
}

def build_filtration(input_file_name, parameter_set = None, **overrides):
	#print(parameter_set["cutoff"])
	def get_param(key):
		if overrides.has_key(key):
			return overrides.get(key)
		elif (not parameter_set is None) and parameter_set.has_key(key):
			return parameter_set.get(key)
		else:
			# assert standard_parameter_set.has_key(key) # Remove this line once confident I didn't miss any when I rewrote this file.
			return standard_parameter_set.pre_landmarks(key)
	min_speed = None
	max_speed = None
	speed_amplify = float(get_param("d_speed_amplify"))
	orientation_amplify = float(get_param("d_orientation_amplify"))
	stretch = float(get_param("d_stretch"))
	ray_distance_amplify = get_param("d_ray_distance_amplify")
	use_hamiltonian = float(get_param("d_use_hamiltonian"))
	m2_d = float(get_param("m2_d"))
	always_euclidean = speed_amplify == orientation_amplify == stretch == ray_distance_amplify == 1.0 and use_hamiltonian == 0.0
	print 'Is m2_d on: %f' % m2_d
	def get_distance(p1, fp1, p2, fp2, s, nv1, nv2, v1, v2): # Parameters: Witness, Landmark, Speed, Normalized Velocity of Witness, Normalized Velocity of Landmark.
		if always_euclidean:
			return get_euclidean_distance(p1, p2)
		if use_hamiltonian != 0.0:
			#raise Exception(str(p1) + str(v1) + str(p1 + v1))
			if use_hamiltonian < 0:
				h1 = p1 + [-use_hamiltonian*x for x in nv1]
				h2 = p2 + [-use_hamiltonian*x for x in nv2]
				return np.linalg.norm(np.subtract(h2, h1))
			else:
				h1 = p1 + [use_hamiltonian*x for x in v1]
				h2 = p2 + [use_hamiltonian*x for x in v2]
				return np.linalg.norm(np.subtract(h2, h1))
		elif m2_d != 0.0:
			print '%d , %d , %d , %d ' % (p1, fp1, p2, fp2)
			return get_euclidean_distance([p1,fp1],[p2,fp2])	
		elif ray_distance_amplify != 1.0:
			p1 = np.array(p1) 
			p2 = np.array(p2)
			nv1 = np.array(nv1)
			nv2 = np.array(nv2)
			main_vector = p1 - p2
			distance = (np.linalg.norm(main_vector) - ((stretch - 1.0)/stretch)*math.fabs(np.dot(main_vector, nv1)))/(((np.dot(nv1, nv2) + 1)*(orientation_amplify - 1)/2) + 1)/((s - min_speed)/(max_speed - min_speed)*(speed_amplify - 1.0) + 1.0)
			dv = nv1 - nv2
			dv2 = np.dot(dv, dv)
			if dv2 < .00001:
				t = 0
			else:
				w0 = np.subtract(p1, p2)
				t = -np.dot(w0, dv)/dv2
			return distance*np.linalg.norm((p1 + nv1*t) - (p2 + nv2*t))		
		else:
			main_vector = np.subtract(p2, p1)
			return (np.linalg.norm(main_vector) - ((stretch - 1.0)/stretch)*math.fabs(np.dot(main_vector, nv1)))/(((np.dot(nv1, nv2) + 1)*(orientation_amplify - 1)/2) + 1)/((s - min_speed)/(max_speed - min_speed)*(speed_amplify - 1.0) + 1.0)
	def get_euclidean_distance(p1, p2):
		return np.linalg.norm(np.subtract(p2, p1))
	input_file = open(input_file_name+'.txt', "r")
	filtration = Set()
	extra_data = None
	velocities = []
	speeds = []
	normalized_velocities = []
	min_filtration_param = float(get_param("min_filtration_param"))
	max_filtration_param = float(get_param("max_filtration_param"))
	if max_filtration_param < 0 and min_filtration_param != 0:
		raise Exception("Argument 'min_filtration_param' is incompatible with automatic max_filtration_param selection.")
	number_of_vertices = 0
	start = get_param("start")
	worm_length = get_param("worm_length")
	store_top_simplices = get_param("store_top_simplices")
	sort_output = get_param("sort_output")
	absolute = get_param("absolute")
	num_divisions = get_param("num_divisions")
	simplex_cutoff = get_param("simplex_cutoff")
	
	## Read data into witness and landmark lists.
	print("\nReading data from file (lines %i - %i)..." % (start, start + worm_length - 1))
	witnesses = []
	landmarks = []
	landmark_indices = []
	ls = get_param("landmark_selector")
	downsample_rate = get_param("ds_rate")
	maxmin = False
	counter = 0

	for i in xrange(start):
		input_file.readline()
	if ls == "EST":
		counter = 0
		for line in input_file.read().split("\n"):
			if line != "":
				counter += 1
				string_witness = line.split(" ")
				witness = []
				for coordinate in string_witness:
					if coordinate != "":
						witness.append(float(coordinate))
				witnesses.append(witness)
				if counter % downsample_rate == 0:
					landmarks.append(witness)
					landmark_indices.append(counter - 1)
				if counter == worm_length:
					break
	elif ls == "maxmin":
		maxmin = True
		for line in input_file.read().split("\n"):
			if line != "":
				counter += 1
				string_witness = line.split(" ")
				witness = []
				for coordinate in string_witness:
					if coordinate != "":
						witness.append(float(coordinate))
				witnesses.append(witness)
				if counter == worm_length:
					break
	else:
		raise Exception("Only supported landmark selectors are 'EST' and 'maxmin'")
	number_of_datapoints = len(witnesses)
	number_of_vertices = int(number_of_datapoints/downsample_rate)
	num_coordinates = len(witnesses[0])
	for i in xrange(number_of_datapoints - 1):
		velocity = list(np.subtract(witnesses[i + 1], witnesses[i]))
		velocities.append(velocity)
		speed = np.linalg.norm(velocity)
		if min_speed is None or speed < min_speed:
			min_speed = speed
		if max_speed is None or speed > max_speed:
			max_speed = speed
		speeds.append(speed)
		normalized_velocities.append(velocity/speed)
	velocities.append(list(velocities[-1])) # Last one's velocity is just copy of second to last one's velocity.
	normalized_velocities.append(list(normalized_velocities[-1]))
	speeds.append(speeds[-1])
	if maxmin:
		print("Done. There will be %i landmarks and %i witnesses.\n\nAssembling distance matrix..." % (number_of_vertices, number_of_datapoints))
	else:
		print("Done. There are %i landmarks and %i witnesses.\n\nAssembling distance matrix..." % (number_of_vertices, number_of_datapoints))
	
	## Build and sort distance matrix.
	euclidean_distance = []
	d = [] # Possibly non-Euclidean.
	if maxmin:
		use_ne = get_param("use_ne_for_maxmin")
		landmark_times = [] # Temporal ordering of landmarks.
		landmark_times.append((0, 0))
		final_distance = 0.0
		landmark_heaps = []
		e_landmark_heaps = [] # For Euclidean-distance maxmin landmark selection.
		for i in xrange(number_of_datapoints):
			landmark_heaps.append([])
			e_landmark_heaps.append([])
		landmark_to_add_index = 0
		for i in xrange(number_of_vertices):
			landmarks.append(witnesses[landmark_to_add_index])
			landmark_indices.append(landmark_to_add_index)
			max_min_distance_index = 0
			for w in xrange(len(witnesses)):
				if w < len(witnesses) - 1:
					distance = get_distance(witnesses[w], witnesses[w+1], witnesses[landmark_to_add_index], witnesses[landmark_to_add_index + 1], speeds[w], normalized_velocities[w], normalized_velocities[landmark_to_add_index], velocities[w], velocities[landmark_to_add_index]) # FEED witnesses[landmark_to_add_index + 1] - CHECK
					e_distance = get_euclidean_distance(witnesses[landmark_to_add_index], witnesses[w])
					heappush(landmark_heaps[w], LandmarkDistance(i, distance))
					heappush(e_landmark_heaps[w], LandmarkDistance(i, e_distance))
					if use_ne:
						if landmark_heaps[w][0].distance > landmark_heaps[max_min_distance_index][0].distance: # Heap[0] is the smallest element.
							max_min_distance_index = w
					else:
						if e_landmark_heaps[w][0].distance > e_landmark_heaps[max_min_distance_index][0].distance:
							max_min_distance_index = w
				else:
					distance = get_distance(witnesses[w], witnesses[w], witnesses[landmark_to_add_index], witnesses[landmark_to_add_index], speeds[w], normalized_velocities[w], normalized_velocities[landmark_to_add_index], velocities[w], velocities[landmark_to_add_index])
					e_distance = get_euclidean_distance(witnesses[landmark_to_add_index], witnesses[w])
					heappush(landmark_heaps[w], LandmarkDistance(i, distance))
					heappush(e_landmark_heaps[w], LandmarkDistance(i, e_distance))
					if use_ne:
						if landmark_heaps[w][0].distance > landmark_heaps[max_min_distance_index][0].distance: # Heap[0] is the smallest element.
							max_min_distance_index = w
					else:
						if e_landmark_heaps[w][0].distance > e_landmark_heaps[max_min_distance_index][0].distance:
							max_min_distance_index = w	
			if i != number_of_vertices - 1:
				landmark_times.append((i + 1, max_min_distance_index))
			landmark_to_add_index = max_min_distance_index
			if i == number_of_vertices - 2:
				if use_ne:
					final_distance = landmark_heaps[max_min_distance_index][0].distance
				else:
					final_distance = e_landmark_heaps[max_min_distance_index][0].distance
		if get_param("time_order_landmarks"):
			landmark_times.sort(key = lambda landmark_time: landmark_time[1])
			new_id_num = []
			for old_position in xrange(len(landmark_times)):
				for position_in_landmark_times in xrange(len(landmark_times)):
					if landmark_times[position_in_landmark_times][0] == old_position:
						new_id_num.append(position_in_landmark_times)
						break
			def reassigned(ld): # Renumbers landmarks according to their temporal order.
				ld.id_num = new_id_num[ld.id_num]
				return ld
			new_landmark_list = []
			new_landmark_indices = []
			for i in xrange(number_of_vertices):
				new_landmark_list.append([])
				new_landmark_indices.append([])
			for i in xrange(number_of_vertices):
				new_landmark_list[new_id_num[i]] = landmarks[i]
				new_landmark_indices[new_id_num[i]] = new_landmark_indices[i]
			landmarks = new_landmark_list
			landmark_indices = new_landmark_indices
			for w in xrange(len(witnesses)):
				d.append([reassigned(heappop(landmark_heaps[w])) for l in range(len(landmark_heaps[w]))])
		else:
			for w in xrange(len(witnesses)):
				d.append([heappop(landmark_heaps[w]) for l in range(len(landmark_heaps[w]))])
		print("Done. Minimum space between landmarks is %f.\n\nBuilding filtration..." % final_distance)
	else:
		for w in xrange(len(witnesses)+1):
			d.append([])
			euclidean_distance.append([])
			if w < len(witnesses)-1:
				for l in xrange(number_of_vertices+1):

					if l < number_of_vertices - 1:
						print "here"
						d[w].append(LandmarkDistance(l, get_distance(witnesses[w], witnesses[w+1], landmarks[l], landmarks[l + 1], speeds[w], normalized_velocities[w], normalized_velocities[landmark_indices[l]], velocities[w], velocities[landmark_indices[l]]))) # (w[0] - landmarks[l][0])**2.0 + (w[1] - landmarks[l][1])**2.0 + (w[2] - landmarks[l][2])**2.0))
						print d[w]
						euclidean_distance[w].append(LandmarkDistance(l, get_euclidean_distance(witnesses[w], landmarks[l])))
						d[w].sort()
						euclidean_distance[w].sort()
					elif l == number_of_vertices - 1:
						d[w].append(LandmarkDistance(l, get_distance(witnesses[w],witnesses[w+1],landmarks[l], landmarks[l],speeds[w], normalized_velocities[w], normalized_velocities[landmark_indices[l]], velocities[w], velocities[landmark_indices[l]]))) # (w[0] - landmarks[l][0])**2.0 + (w[1] - landmarks[l][1])**2.0 + (w[2] - landmarks[l][2])**2.0))
						euclidean_distance[w].append(LandmarkDistance(l, get_euclidean_distance(witnesses[w], landmarks[l])))
						d[w].sort()
						euclidean_distance[w].sort()
					else:
						filler = 1
			elif w == len(witnesses) - 1:
				for l in xrange(number_of_vertices+1):
					if l < number_of_vertices - 1:
						d[w].append(LandmarkDistance(l, get_distance(witnesses[w], witnesses[w], landmarks[l], landmarks[l + 1], speeds[w], normalized_velocities[w], normalized_velocities[landmark_indices[l]], velocities[w], velocities[landmark_indices[l]]))) # (w[0] - landmarks[l][0])**2.0 + (w[1] - landmarks[l][1])**2.0 + (w[2] - landmarks[l][2])**2.0))
						euclidean_distance[w].append(LandmarkDistance(l, get_euclidean_distance(witnesses[w], landmarks[l])))
						d[w].sort()
						euclidean_distance[w].sort()
					elif l == number_of_vertices - 1:
						d[w].append(LandmarkDistance(l, get_distance(witnesses[w],witnesses[w],landmarks[l], landmarks[l],speeds[w], normalized_velocities[w], normalized_velocities[landmark_indices[l]], velocities[w], velocities[landmark_indices[l]]))) # (w[0] - landmarks[l][0])**2.0 + (w[1] - landmarks[l][1])**2.0 + (w[2] - landmarks[l][2])**2.0))
						euclidean_distance[w].append(LandmarkDistance(l, get_euclidean_distance(witnesses[w], landmarks[l])))
						d[w].sort()
						euclidean_distance[w].sort()
					else:
						filler2 = 1
			else: 
				filler3 = 1
		print("Done.\n\nBuilding filtration...")
	assert len(landmarks) == number_of_vertices
	for i in d:
		print i
		print "======="
	
	## Build filtration
	weak = get_param("weak")
	dimension_cutoff = get_param("dimension_cutoff")
	reentry_filter = get_param("reentry_filter")
	if get_param("connect_time_1_skeleton") or reentry_filter: # Connect time-1-skeleton
		for i in xrange(number_of_vertices - 1):
			filtration.add(SimplexBirth(ImmutableSet([i, i + 1]), 0, sort_output))
	use_cliques = get_param("use_cliques")
	use_twr = get_param("use_twr")
	print '%s' % use_twr
	if use_cliques: # AKA "Lazy" witness relation.
		g = nx.Graph()
		for l in xrange(number_of_vertices):
			g.add_node(l)
	def filter_and_build():
		g2 = None
		if reentry_filter:
			g2 = g.copy()
			to_remove = Set()
			for l1 in xrange(number_of_vertices):
				l2 = l1 + 2
				while l2 < number_of_vertices and g2.has_edge(l1, l2):
					to_remove.add(ImmutableSet([l1, l2]))
					l2 += 1
			for edge in to_remove:
				g2.remove_edge(*tuple(edge)) # May cause weird things to happen because removing edges doesn't remove them from the filtration.
		else:
			g2 = g
		for clique in nx.find_cliques(g2):
			filtration.add(SimplexBirth(clique, q, sort_output))
	if weak: # Builds filtration based on k nearest neighbors.
		if max_filtration_param % 1 != 0:
			raise Exception("Argument 'max_filtration_param' must be an integer if using the weak witness relation.")
		max_filtration_param = int(max_filtration_param)
		for k in xrange(int(math.fabs(max_filtration_param))):
			for witness_index in xrange(number_of_datapoints):
				if use_cliques:
					for i in xrange(k):
						g.add_edge(d[witness_index][i].id_num, d[witness_index][k].id_num)
				elif store_top_simplices:
					filtration.add(SimplexBirth([d[witness_index][landmark_index].id_num for landmark_index in xrange(k + 1)], k, sort_output))
				else:
					if progress > 0:
						for base in itertools.combinations([d[witness_index][landmark_index].id_num for landmark_index in xrange(k)], min(k, dimension_cutoff)):
							new_subset = ImmutableSet(base + (d[witness_index][k].id_num,))
							filtration.add(SimplexBirth(new_subset, k, sort_output))
			if use_cliques:
				filter_and_build()
	if use_twr:
		print 'Using TWR'
		if max_filtration_param < 0: # Automatically determine max.
			depth = int(-max_filtration_param)
			min_distance = None
			for w in xrange(number_of_datapoints):
				new_distance = d[w][depth].distance - (0 if absolute else d[w][0].distance)
				if min_distance is None or new_distance < min_distance:
					min_distance = new_distance
			max_filtration_param = min_distance
		print 'The max_filtration_param is %d ' % max_filtration_param
		step = float(max_filtration_param - min_filtration_param)/float(num_divisions) # Change in epsilon at each step.
		print 'The step size is %f ' % step
		print 'There will be %d steps in the filtration' % num_divisions
		progress_index = [0]*number_of_datapoints
		done = False
		
		good_landmarks = [[] for x in range(number_of_datapoints)]
		for q in xrange(num_divisions):
			threshold = (max_filtration_param if q == num_divisions - 1 else float(q + 1)*step + min_filtration_param)
			print 'The threshold is currently %f' % threshold
			
			Pre_landmarks = []
			for witness_index in xrange(number_of_datapoints):
				pre_landmarks = []
				add_simplex = False
				progress = 0
				while True:
					progress = progress_index[witness_index]
					if simplex_cutoff > 0 and progress >= simplex_cutoff:
						break
					if progress == number_of_vertices:
						done = True
						break	
			
					if d[witness_index][progress].distance < threshold + (0 if absolute else d[witness_index][0].distance):
						pre_landmarks.append(d[witness_index][progress].id_num) # PRE_LANDMARKS CONTAINS ID NUMBER
						progress_index[witness_index] += 1
					else:
					
						pre_landmarks_size = len(pre_landmarks) 
						pre_landmarks_string = str(pre_landmarks) # MAKE LIST TO STRING 
						print 'At threshold value %f, witness %d has %d associated landmarks: %s ' % (threshold, witness_index, pre_landmarks_size, pre_landmarks_string)
						break
				Pre_landmarks.append(pre_landmarks)
				Pre_landmarks_size = len(Pre_landmarks)
			
		 
				
			for witness_index in xrange(number_of_datapoints - downsample_rate):
				if len(Pre_landmarks[witness_index]) == 1:
					set_range = 1
				else:
					set_range = len(Pre_landmarks[witness_index]) 
				for k in range(set_range):
					current_pre_landmark = Pre_landmarks[witness_index][k]
					next_pre_landmark = Pre_landmarks[witness_index][k]+1 # CHECKS ONE STEP UP FROM ID NUMBER *** SEE JAMIE'S COMMENTS ON SUCH OR CLARIFY ***
				#	print 'current pre landmark = %d , next pre landmark = %d' % (current_pre_landmark, next_pre_landmark)
					check_pre_landmark = str(Pre_landmarks[witness_index + downsample_rate]) # HMMMMM 
			#		print 'We are considering the fate of landmark %d witnessed by witness %d...' % (current_pre_landmark, witness_index)
			#		print 'Should witness %d not witness landmark %d, it will be GONE!' % (witness_index + downsample_rate, current_pre_landmark + 1,)
			#		print 'Witness %d has landmark set %s' % (witness_index + downsample_rate, check_pre_landmark)
					print (Pre_landmarks[witness_index][k]) in Pre_landmarks[witness_index]
					if (Pre_landmarks[witness_index][k]+ 1) in Pre_landmarks[witness_index + downsample_rate]: # change from 1, downsample_rate to 0 to test! 
						good_landmarks[witness_index].append(Pre_landmarks[witness_index][k])
				print 'Up to threshold value %f, witness %d has landmark set %s' % (threshold, witness_index, str(good_landmarks[witness_index]))
				if use_cliques:
					for i in xrange(len(good_landmarks[witness_index])):
						for j in xrange(i+1,len(good_landmarks[witness_index])):
								g.add_edge(good_landmarks[witness_index][i], good_landmarks[witness_index][j])
				else:
					if not store_top_simplices and len(good_landmarks[witness_index]) > 0:
						for base in itertools.combinations(good_landmarks[witness_index], min(len(good_landmarks[witness_index]), dimension_cutoff)):
							new_subset = ImmutableSet(base + (good_landmarks[witness_index][i],))
							filtration.add(SimplexBirth(new_subset, q, sort_output))
					add_simplex = True
				if (not use_cliques) and store_top_simplices and add_simplex and len(good_landmarks[witness_index])>= 2:
					filtration.add(SimplexBirth([good_landmarks[witness_index][i] for i in xrange(len(good_landmarks[witness_index]))], q, sort_output))
				if done:
					break
			if use_cliques:
				filter_and_build()
			if done:
				break
		#	print 'We are done with threshold %f' % threshold
	else:
		if max_filtration_param < 0: # Automatically determine max.
			#depth = int(-max_filtration_param)
			depth = 1
			min_distance = None
			for w in xrange(number_of_datapoints):
				print d[w][depth].distance
				new_distance = d[w][depth].distance - (0 if absolute else d[w][0].distance)
				if min_distance is None or new_distance < min_distance:
					min_distance = new_distance
			max_filtration_param = min_distance
		step = float(max_filtration_param - min_filtration_param)/float(num_divisions) # Change in epsilon at each step.
		progress_index = [0]*number_of_datapoints
		done = False
		for q in xrange(num_divisions):
			threshold = (max_filtration_param if q == num_divisions - 1 else float(q + 1)*step + min_filtration_param)
			print 'The threshold is currently %f' % threshold
			for witness_index in xrange(number_of_datapoints):
				add_simplex = False
				progress = 0
				while True:
					progress = progress_index[witness_index]
					if simplex_cutoff > 0 and progress >= simplex_cutoff:
						break
					if progress == number_of_vertices:
						done = True
						break
					if d[witness_index][progress].distance < threshold + (0 if absolute else d[witness_index][0].distance):
						if use_cliques:
							for i in xrange(progress):
								g.add_edge(d[witness_index][i].id_num, d[witness_index][progress].id_num)
						else:
							if not store_top_simplices and progress > 0:
								for base in itertools.combinations([d[witness_index][landmark_index].id_num for landmark_index in xrange(progress)], min(progress, dimension_cutoff)):
									new_subset = ImmutableSet(base + (d[witness_index][progress].id_num,))
									filtration.add(SimplexBirth(new_subset, q, sort_output))
							add_simplex = True
						progress_index[witness_index] += 1
					else:
						break
				if (not use_cliques) and store_top_simplices and add_simplex and progress >= 2:
					list_o_landmarks = []
					for landmark_index in xrange(progress):
						list_o_landmarks.append(d[witness_index][landmark_index].id_num)
					#print 'At threshold %f, witness %d has landmark set %s' % (threshold, witness_index, str(list_o_landmarks))
					filtration.add(SimplexBirth([d[witness_index][landmark_index].id_num for landmark_index in xrange(progress)], q, sort_output))
				if done:
					break
			if use_cliques:
				filter_and_build()
			if done:
				break
	
	extra_data = (landmarks, witnesses)
	if weak:
		max_epsilon = 0.0
		for w in xrange(number_of_datapoints):
			#print("type: %s" % type(d[w][max_filtration_param - 1].distance))
			#print("value: %f" % d[w][max_filtration_param - 1].distance)
			if (d[w][max_filtration_param - 1].distance) > max_epsilon:
				max_epsilon = d[w][max_filtration_param - 1].distance
		print("Done. Filtration contains %i top simplex birth events, with the largest epsilon equal to %f.\n" % (len(filtration), max_epsilon))
	else:
		max_sb_length = 0
		for sb in filtration:
			if len(sb.landmark_set) > max_sb_length:
				max_sb_length = len(sb.landmark_set)
		print("Done. Filtration contains %i top simplex birth events, with the largest one comprised of %i landmarks.\nMax filtration parameter: %s.\n" % (len(filtration), max_sb_length, max_filtration_param))
	
	## Write to output file
	output_file_name = get_param("out")
	if not output_file_name is None:
		output_file = open(output_file_name, "w")
		output_file.truncate()
		program = get_param("program")
		if dimension_cutoff is None:
			print("Writing filtration for input into %s..." % program)
			dimension_cutoff = number_of_vertices
		else:
			print("Writing filtration for input into %s, ignoring simplices above dimension %i..." % (program, dimension_cutoff))
		num_lines = 0
		if program == "Perseus":
			sets_printed_so_far = Set()
			num_lines = len(filtration) + 1
			output_file.write("1\n")
			list_filtration = None
			if (sort_output):
				list_filtration = list(filtration)
				list_filtration.sort()
			for simplex_birth in (list_filtration if sort_output else filtration):
				dimension = len(simplex_birth.landmark_set) - 1
				if dimension > dimension_cutoff:
					for subtuple in itertools.combinations(simplex_birth.landmark_set, dimension_cutoff + 1):
						subset = ImmutableSet(subtuple)
						if not ((subset, simplex_birth.birth_time) in sets_printed_so_far):
							output_file.write(str(dimension_cutoff) + " ")
							for landmark in subset:
								output_file.write(str(landmark + 1) + " ")
							output_file.write(str(simplex_birth.birth_time + 1) + "\n")
							sets_printed_so_far.add((subset, simplex_birth.birth_time))
				else:
					if not ((simplex_birth.landmark_set, simplex_birth.birth_time) in sets_printed_so_far):
						output_file.write(str(dimension) + " ")
						for landmark in (simplex_birth.sll if sort_output else simplex_birth.landmark_set):
							output_file.write(str(landmark + 1) + " ")
						output_file.write(str(simplex_birth.birth_time + 1) + "\n")
						sets_printed_so_far.add((simplex_birth.landmark_set, simplex_birth.birth_time))
		elif program == "PHAT":
			line_map = {}
			for i in xrange(number_of_vertices - 1):
				output_file.write("0\n")
				line_map[ImmutableSet([i])] = i
			output_file.write("0")
			line_map[ImmutableSet([number_of_vertices - 1])] = number_of_vertices - 1
			simultaneous_additions = []
			class Context: # Note: if upgrading to Python 3, one could just use the nonlocal keyword (see below comment).
				line_number = number_of_vertices
			list_filtration = list(filtration)
			list_filtration.sort()
			last_birth_time = 0
			def process_and_get_line_number(s):
				#nonlocal line_number
				if s in line_map:
					return line_map[s]
				else:
					dimension = len(s) - 1
					if dimension > dimension_cutoff:
						for subset in itertools.combinations(s, dimension_cutoff + 1): # Take all subsets of size dimension_cutoff + 1
							process_and_get_line_number(ImmutableSet(subset))
					elif dimension > 0:
						subsets_line_numbers = []
						for e in s:
							subsets_line_numbers.append(process_and_get_line_number(ImmutableSet(s - Set([e]))))
						output_file.write("\n" + str(dimension))
						for l in subsets_line_numbers:
							output_file.write(" " + str(l))
						line_map[s] = Context.line_number
						Context.line_number += 1
						return Context.line_number - 1
					else:
						raise Exception("Should have already added single point for base case: " + str(s))
			for simplex_birth in list_filtration:
				if simplex_birth.birth_time > last_birth_time:
					simultaneous_additions.append((Context.line_number - 1, last_birth_time + 1)) # Every line up to and including that line number (indexing starts at 0) had that birth time or earlier (indexing starts at 1)
					last_birth_time = simplex_birth.birth_time
				process_and_get_line_number(simplex_birth.landmark_set)
			simultaneous_additions.append((sys.maxsize, last_birth_time))
			output_file.write("\n\n# Simultaneous additions: Every line up to and including __ (indexing starts at 0) has birth time __ (or earlier).")
			for addition in simultaneous_additions:
				output_file.write("\n# %20i %20i" % addition)
			extra_data = (extra_data[0], extra_data[1], simultaneous_additions)
			num_lines = Context.line_number
		else:
			raise Exception("Only supported programs are 'Perseus' and 'PHAT'")
		output_file.close()
		print("Done. File contains %i lines.\n" % num_lines)
	print("Filtration has been successfully built!\n")
	return (filtration, extra_data + (max_filtration_param,))

class SimplexBirth: # An object that contains a set of landmarks that define a simplex, and a birth time measured in integer units. IMPORTANT: two SimplexBirths are considered equal iff they have the same landmark set, regardless of birth time.

	include_birth_time = False

	def __init__(self, landmark_list, birth_time, keep_sorted_list):
		if (keep_sorted_list):
			self.sll = sorted(landmark_list)
		else:
			self.sll = None
		self.landmark_set = ImmutableSet(landmark_list)
		self.birth_time = birth_time
	
	def __eq__(self, other): # For hashing
		if SimplexBirth.include_birth_time:
			return self.birth_time == other.birth_time and self.landmark_set.__eq__(other.landmark_set)
		else:
			return self.landmark_set.__eq__(other.landmark_set)
	
	def __cmp__(self, other): # For sorting
		if self.birth_time < other.birth_time:
			return -1
		elif self.birth_time > other.birth_time:
			return 1
		else:
			if len(self.landmark_set) < len(other.landmark_set):
				return -1
			elif len(self.landmark_set) > len(other.landmark_set):
				return 1
			else:
				if self.sll is None:
					return 0
				for i in xrange(len(self.sll)):
					if self.sll[i] < other.sll[i]:
						return -1
					elif self.sll[i] > other.sll[i]:
						return 1
				return 0
	
	def __hash__(self):
		return self.landmark_set.__hash__()

class LandmarkDistance: # An object that contains both the distance to the landmark and that landmark's ID number.
	
	def __init__(self, id_num, distance):
		self.id_num = id_num
		self.distance = float(distance)
	
	def __cmp__(self, other):
		if self.distance < other.distance:
			return -1
		elif self.distance > other.distance:
			return 1
		else:
			return 0
	
	def __le__(self, other): # Called in heap operations.
		return self.distance <= other.distance
	
	def __str__(self):
		return "(%i, %f)" % (self.id_num, self.distance)
	
	__repr__ = __str__