import os
from os import system, chdir

class Paths:
	path_to_gnuplot = "gnuplot"
	path_to_ffmpeg = "ffmpeg"

def set_path_to_gnuplot(path):
	Paths.path_to_gnuplot = path

def set_path_to_ffmpeg(path):
	Paths.path_to_ffmpeg = path

def plot_1_skeleton(filtration, point_locations, filtration_parameter, use_3d, p_2_s = False, script_file_name = "gnuplot_commands.txt", xmin = -1.0, xmax = 1.0, ymin = -1.0, ymax = 1.0, zmin = -1.0, zmax = 1.0, extra_points = None, ps1 = 1.0, ps2 = 0.1, f = None):
	graph_2 = None
	only_plot = f is None
	if only_plot:
		f = open(script_file_name, "w")
		f.truncate()
	f.write("set style arrow 1 nohead\n")
	f.write("set size ratio -1\n")
	f.write("set xrange [%f:%f]\n" % (xmin, xmax))
	f.write("set yrange [%f:%f]\n" % (ymin, ymax))
	f.write("set zrange [%f:%f]\n" % (zmin, zmax))
	if use_3d:
		for point in point_locations:
			f.write("set label at %f,%f,%f point pt 7 ps %f lt rgb \"#FF00FF\"\n" % (point[0], point[1], point[2], ps1))
		if not extra_points is None:
			for point in extra_points:
				f.write("set label at %f,%f,%f point pt 7 ps %f\n" % (point[0], point[1], point[2], ps2))
	else:
		for point in point_locations:
			f.write("set label at %f,%f point pt 7 ps %f lt rgb \"#FF00FF\"\n" % (point[0], point[1], ps1))
		if not extra_points is None:
			for point in extra_points:
				f.write("set label at %f,%f point pt 7 ps %f\n" % (point[0], point[1], ps2))
	graph = [[False for i in xrange(len(point_locations))] for j in xrange(len(point_locations))]
	for simplex_birth in filtration:
		#print ' The type of simplex_birth is : % s ' % str(type(simplex_birth))
		#print ' The size of simplex_birth is : % s ' % str(len(simplex_birth))
		#print ' The type of simplex_birth.landmark_set is : %s' % str(type(simplex_birth.landmark_set))
		#print ' The value of simplex_birth.landmark_set is: %s' % str(simplex_birth.landmark_set)
		if simplex_birth.birth_time <= filtration_parameter:
			for l1 in simplex_birth.landmark_set:
			#	print 'simplex_birth.landmark_set is : %s ' % str(simplex_birth.landmark_set)
				for l2 in simplex_birth.landmark_set:
			#		print 'l1 = %s, l2 = %s' % (str(l1), str(l2))
					if l1 < l2:
						graph[l1][l2] = True			# MAYBE D_COV FILTRATION SIMPLEX BIRTHS CONTAIN WRONG LANDMARK SET DATA I.E. "2078" VS "16"?
						
	for i in xrange(len(point_locations)):
		for j in xrange(len(point_locations)):
			if graph[i][j]:
				l1_location = point_locations[i]
				l2_location = point_locations[j]
				if use_3d:
					f.write("set arrow from %f,%f,%f to %f,%f,%f as 1\n" % (l1_location[0], l1_location[1], l1_location[2], l2_location[0], l2_location[1], l2_location[2]))
				else:
					f.write("set arrow from %f,%f to %f,%f as 1\n" % (l1_location[0], l1_location[1], l2_location[0], l2_location[1]))
	if p_2_s:
		triagles = 1
		f.write("unset border\nunset tics\n")
		graph_2 = [[[False for i in xrange(len(point_locations))] for j in xrange(len(point_locations))] for k in xrange(len(point_locations))]
		for simplex_birth in filtration:
			if simplex_birth.birth_time <= filtration_parameter:
				for l1 in simplex_birth.landmark_set:
					for l2 in simplex_birth.landmark_set:
						for l3 in simplex_birth.landmark_set:
							if l1 < l2 < l3:
								graph_2[l1][l2][l3] = True
		for i in xrange(len(point_locations)):
			for j in xrange(len(point_locations)):
				for k in xrange(len(point_locations)):
					if graph_2[i][j][k]:
						l1_location = point_locations[i]
						l2_location = point_locations[j]
						l3_location = point_locations[k]
						if use_3d:
							f.write("set object %i polygon from \\\n\t%f,%f,%f to \\\n\t%f,%f,%f to \\\n\t%f,%f,%f to \\\n\t%f,%f,%f\n" % (triagles, l1_location[0], l1_location[1], l1_location[2], l2_location[0], l2_location[1], l2_location[2], l3_location[0], l3_location[1], l3_location[2], l1_location[0], l1_location[1], l1_location[2]))
						else:
							f.write("set object %i polygon from \\\n\t%f,%f to \\\n\t%f,%f to \\\n\t%f,%f to \\\n\t%f,%f\n" % (triagles, l1_location[0], l1_location[1], l2_location[0], l2_location[1], l3_location[0], l3_location[1], l1_location[0], l1_location[1]))
						f.write("set object %i fc rgb '#999999' fillstyle solid lw 0\n" % triagles)
						triagles += 1
	
	if use_3d:
		f.write("splot NaN notitle\n")
	else:
		f.write("plot NaN notitle\n")
	if only_plot:
		f.close()
		system("%s -persist %s" % (Paths.path_to_gnuplot, script_file_name))
	return graph, graph_2, triagles

def autoplot_1_skeleton_witness(filtration, step, p_2_s = False, f = None, include_witnesses = True):
	point_locations = filtration[1][0]
	if len(point_locations[0]) == 2:
		xmin = xmax = point_locations[0][0]
		ymin = ymax = point_locations[0][1]
		for point in point_locations:
			if point[0] > xmax:
				xmax = point[0]
			elif point[0] < xmin:
				xmin = point[0]
			if point[1] > ymax:
				ymax = point[1]
			elif point[1] < ymin:
				ymin = point[1]
		return (plot_1_skeleton(filtration[0], point_locations, step, False, extra_points = (filtration[1][1] if include_witnesses else None), xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax, p_2_s = p_2_s, f = f) + (False,))
	elif len(point_locations[0]) >= 3:
		xmin = xmax = point_locations[0][0]
		ymin = ymax = point_locations[0][1]
		zmin = zmax = point_locations[0][2]
		for point in point_locations:
			if point[0] > xmax:
				xmax = point[0]
			elif point[0] < xmin:
				xmin = point[0]
			if point[1] > ymax:
				ymax = point[1]
			elif point[1] < ymin:
				ymin = point[1]
			if point[2] > zmax:
				zmax = point[2]
			elif point[2] < zmin:
				zmin = point[2]
		return (plot_1_skeleton(filtration[0], filtration[1][0], step, True, extra_points = (filtration[1][1] if include_witnesses else None), xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax, zmin = zmin, zmax = zmax, p_2_s = p_2_s, f = f) + (True,))
	else:
		raise Exception("Must have at least 2 dimensional data!")
		
def plot_2_skeleton(filtration, step):
	autoplot_1_skeleton_witness(filtration, step, True)

def get_persistence_diagram(input_file_name, dimension, PHAT_in = "", simultaneous_additions = None, max_dimension = 10, plot = True, max = None, num_steps = None, script_file_name = "gnuplot_commands.txt", ps = 1.0, title = "Untitled", out = None):
	intervals = []
	for i in xrange(max_dimension):
		intervals.append([])
	input_file = open(input_file_name + "_" + str(dimension) + ".txt", 'r')
	lines = input_file.read().split("\n")
	for line in lines:
		if line != "":
			interval = [int(s) for s in line.split(" ")]
			if interval[1] == -1:
				intervals[dimension].append([interval[0], num_steps])
			else:
				intervals[dimension].append(interval)
	if plot:
		plot_persistence_diagram(intervals, dimension, script_file_name, max, num_steps, ps, title, out = out) # TODO: add parameters for real filtration parameter distance.
	return intervals

def rgb_to_hex(rgb):
	return "'#%02x%02x%02x'" % rgb

color_array = [rgb_to_hex(t) for t in [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)]]

def plot_persistence_diagram(intervals, dimension, script_file_name, max, num_steps, ps, title, out = None):
	if max is None or num_steps is None:
		raise Exception("Must supply arguments 'max' and 'num_steps'")
	f = open(script_file_name, "w")
	f.truncate()
	if not out is None:
		f.write("set term pngcairo\n")
		if out.endswith(".png"):
			f.write("set output sprintf('%s')\n" % out)
		else:
			f.write("set output sprintf('%s.png')\n" % out)
	f.write("set size ratio -1\n")
	f.write("set style arrow 1 nohead\n")
	f.write("set title \"%s\" noenhanced font \"sans, 18\"\nset xlabel \"Birth Scale\"\nset ylabel \"Death Scale\"\n" % title)
	f.write("set arrow from 0,0 to %f,%f as 1\n" % (max, max)) # Diagonal y = x
	f.write("set xrange [%f:%f]\n" % (0, max))
	f.write("set yrange [%f:%f]\n" % (0, max))
	num_points = [[0 for i in xrange(num_steps + 1)] for j in xrange(num_steps + 1)]
	for interval in intervals[dimension]:
		f.write("set label at %f,%f point pt 7 lc rgb %s ps %f\n" % (float(interval[0])/float(num_steps)*float(max), float(interval[1])/float(num_steps)*float(max), color_array[min(num_points[interval[0]][interval[1]], 3)], ps))
		num_points[interval[0]][interval[1]] += 1
	f.write("plot NaN notitle\n")
	f.close()
	system("%s -persist %s" % (Paths.path_to_gnuplot, script_file_name))

def make_movie(filtration_tuple, movie_title, framerate = 2.0, view = None, include_witnesses = True, cleanup_images = True, script_file_name = "gnuplot_commands.txt"):
	print("Making movie...")
	f = open(script_file_name, "w")
	f.truncate()
	f.write("set term pngcairo\n")
	if not view is None:
		f.write("set view %s\n" % view)
	f.write("set output sprintf('%s_image_0.png')\n" % movie_title)
	(graph, graph_2, triagles, use_3d) = autoplot_1_skeleton_witness(filtration_tuple, 0, True, f = f, include_witnesses = include_witnesses)
	sorted_filtration = sorted(list(filtration_tuple[0]))
	point_locations = filtration_tuple[1][0]
	step = 1
	progress_through_filtration = 0
	while sorted_filtration[progress_through_filtration].birth_time < 1:
		progress_through_filtration += 1
	while progress_through_filtration < len(sorted_filtration):
		f.write("set output sprintf('%s_image_%i.png')\n" % (movie_title, step))
		while progress_through_filtration < len(sorted_filtration) and sorted_filtration[progress_through_filtration].birth_time == step:
			simplex_birth = sorted_filtration[progress_through_filtration]
			for l1 in simplex_birth.landmark_set:
				for l2 in simplex_birth.landmark_set:
					if l1 < l2:
						if not graph[l1][l2]:
							graph[l1][l2] = True
							l1_location = point_locations[l1]
							l2_location = point_locations[l2]
							if use_3d:
								f.write("set arrow from %f,%f,%f to %f,%f,%f as 1\n" % (l1_location[0], l1_location[1], l1_location[2], l2_location[0], l2_location[1], l2_location[2]))
							else:
								f.write("set arrow from %f,%f to %f,%f as 1\n" % (l1_location[0], l1_location[1], l2_location[0], l2_location[1]))
						for l3 in simplex_birth.landmark_set:
							if l2 < l3:
								if not graph_2[l1][l2][l3]:
									graph_2[l1][l2][l3] = True
									l1_location = point_locations[l1]
									l2_location = point_locations[l2]
									l3_location = point_locations[l3]
									if use_3d:
										f.write("set object %i polygon from \\\n\t%f,%f,%f to \\\n\t%f,%f,%f to \\\n\t%f,%f,%f to \\\n\t%f,%f,%f\n" % (triagles, l1_location[0], l1_location[1], l1_location[2], l2_location[0], l2_location[1], l2_location[2], l3_location[0], l3_location[1], l3_location[2], l1_location[0], l1_location[1], l1_location[2]))
									else:
										f.write("set object %i polygon from \\\n\t%f,%f to \\\n\t%f,%f to \\\n\t%f,%f to \\\n\t%f,%f\n" % (triagles, l1_location[0], l1_location[1], l2_location[0], l2_location[1], l3_location[0], l3_location[1], l1_location[0], l1_location[1]))
									f.write("set object %i fc rgb '#999999' fillstyle solid lw 0\n" % triagles)
									triagles += 1
			progress_through_filtration += 1
		if use_3d:
			f.write("splot NaN notitle\n")
		else:
			f.write("plot NaN notitle\n")
		step += 1
	f.close()
	system("%s -persist %s" % (Paths.path_to_gnuplot, script_file_name))
	system("%s -hide_banner -loglevel panic -y -framerate %f -i \"%s_image_%%d.png\" -r 30 \"%s_movie.mp4\"" % (Paths.path_to_ffmpeg, framerate, movie_title, movie_title))
	if cleanup_images:
		for i in xrange(step):
			os.remove("%s_image_%i.png" % (movie_title, i))
	print("Done. Movie contains %i frames.\n" % step)