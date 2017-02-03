from BuildComplex_WFL import build_filtration, standard_parameter_set
from GetHomologyFromFiltrationNEW import compute_homology
from PlotterNEW import plot_1_skeleton, get_persistence_diagram, autoplot_1_skeleton_witness, make_movie
import os
import os.path
from os import system
import timeit

def make_worm_movies(input_file_name, number_of_worms, parameter_set = None, format_type = 1, persistence_plot_dimension = 1, framerate = 1.0, cleanup_images = True, view = None, **overrides):
	print("")
	if parameter_set is None:
		parameters = {}
	else:
		parameters = parameter_set.copy()
	for k in overrides.keys():
		parameters[k] = overrides[k]
	def get_param(key):
		if (not parameters is None) and parameters.has_key(key):
			return parameter_set.get(key)
		else:
			return standard_parameter_set.get(key)
	input_file = open(input_file_name, "r")
	number_of_lines = len(input_file.read().split("\n"))
	input_file.close()
	worm_length = get_param("worm_length")
	last_line_start = float(number_of_lines - worm_length)
	input_file_base_name = os.path.splitext(input_file_name)[0]
	mfp = get_param("max_filtration_param")
	for s in xrange(number_of_worms):
		center_string = "WORM %i / %i" % (s + 1, number_of_worms)
		dashes_string = "-"*len(center_string)
		print("%s\n%s\n%s" % (dashes_string, center_string, dashes_string))
		line_start = int(last_line_start*float(s)/float(number_of_worms - 1))
		if format_type == 1:
			segment_title_base = "%s_worm" % input_file_base_name
		elif format_type == 2:
			segment_title_base = "%s_sAmp%i_oAmp%i_worm" % (input_file_base_name, get_param("d_speed_amplify"), get_param("d_orientation_amplify"))
		elif format_type == 3:
			segment_title_base = "%s_%iL_sAmp%i_oAmp%i_worm" % (input_file_base_name, worm_length/get_param("ds_rate"), get_param("d_orientation_amplify"), get_param("d_speed_amplify"), get_param("d_orientation_amplify"))
		segment_title = segment_title_base + str(s + 1)
		(f, new_max) = points_to_persistence_diagram(input_file_base_name, parameters, persistence_plot_dimension = persistence_plot_dimension, start = line_start, cleanup_intermediate_files = True, return_new_max = True, title = segment_title)
		if mfp < 0:
			parameters["max_filtration_param"] = new_max
		make_movie(f, segment_title, view = view, include_witnesses = True)
	movie_title = "%s_persistence_diagrams" % input_file_base_name
	print ' ** MAKING PERSISTENCE DIAGRAM MOVIE!!! ****' 
	system("ffmpeg -hide_banner -loglevel panic -y -framerate %f -i \"%s%%d_persistence_diagram.png\" -r 30 \"%s_movie.mp4\"" % (framerate, segment_title_base, movie_title))
	print 'ffmpeg -hide_banner -loglevel panic -y -framerate %f -i \"%s%%d_persistence_diagram.png\" -r 30 \"%s_movie.mp4\ ' % (framerate, segment_title_base, movie_title) # TRYING TO FIGURE OUT WHAT %d IS! HOW TO PULL CORRECT FILES FROM DIRECTORY TO MAKE 'TAU-RANGE PD MOVIE' 
	if cleanup_images:
		for i in xrange(number_of_worms):
			os.remove("%s%i_persistence_diagram.png" % (segment_title_base, i + 1))

def points_to_persistence_diagram(input_file_base_name, parameter_set = None, cleanup_intermediate_files = False, return_new_max = False, title = None, use_popup = False, persistence_plot_dimension = 1, **overrides):
#kind_of_complex, input_file_name, max_filtration_param, num_divisions, program, persistence_plot_dimension, cleanup_intermediate_files = False, return_new_max = False, title = None, **parameters):
	if parameter_set is None:
		parameters = {}
	else:
		parameters = parameter_set.copy()
	for k in overrides.keys():
		parameters[k] = overrides[k]
	def get_param(key):
		if (not parameters is None) and parameters.has_key(key):
			return parameter_set.get(key)
		else:
			return standard_parameter_set.get(key)
	if input_file_base_name.endswith(".txt"):
		input_file_base_name = os.path.splitext(input_file_base_name)[0]
	if title is None:
		title = input_file_base_name
	program = get_param("program")
	complex_file_name = input_file_base_name + "_complex_for_" + program + ".txt"
	parameters["out"] = complex_file_name
	start_time = timeit.default_timer()
	filtration = build_filtration(input_file_base_name , parameters)
	if filtration is None:
		print "UHH: Filtration is empty of edges."
	else:
		max_filtration_param = filtration[1][-1]
	homology_file_name = input_file_base_name + "_" + program + "_homology" 
	print 'Hello There!'
	if program != "Perseus":
		homology_file_name = homology_file_name + ".txt"
	compute_homology(complex_file_name, homology_file_name, program)
	if program == "PHAT":
		get_persistence_diagram(homology_file_name, persistence_plot_dimension, PHAT_in = complex_file_name, simultaneous_additions = filtration[1][2], max = max_filtration_param, num_steps = get_param("num_divisions"), title = title, out = (None if use_popup else title + "_persistence_diagram.png"))
	else:
		get_persistence_diagram(homology_file_name, persistence_plot_dimension, max = max_filtration_param, num_steps = get_param("num_divisions"), title = title, out = (None if parameters.get("use_popup") else title + "_persistence_diagram.png"))
	if cleanup_intermediate_files:
		os.remove(complex_file_name)
		#os.remove("gnuplot_commands.txt")
		if program == "PHAT":
			os.remove(homology_file_name)
		else:
			os.remove(homology_file_name + "_betti.txt")
			i = 0
			try:
				while True:
					os.remove("%s_%i.txt" %(homology_file_name, i))
					i += 1
			except OSError:
				pass
	end_time = timeit.default_timer()
	print("Time elapsed: %f seconds.\n" % (end_time - start_time))
	if (return_new_max):
		return (filtration, max_filtration_param)
	else:
		return filtration
