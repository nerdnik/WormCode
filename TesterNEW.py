from WormSliding import calc
import BuildRankFunction
from RunPerseusFromPoints import get_intervals
from sets import Set, ImmutableSet
from BuildComplex_WFL import build_filtration, SimplexBirth, standard_parameter_set
from GetHomologyFromFiltrationNEW import compute_homology, set_path_to_Perseus, set_path_to_PHAT
from PlotterNEW import plot_1_skeleton, get_persistence_diagram, autoplot_1_skeleton_witness, plot_2_skeleton, make_movie
from TestFileGenerator import generate
import networkx as nx
import sys
import os
import os.path
from os import system
import timeit
from DelayCoordinateEmbedding import embed
from TestingFunctionsNEW import make_worm_movies, points_to_persistence_diagram
from TRYplotter19 import make_PD_movie, make_filtration_succession


test = int(sys.argv[1])

old_parameter_set = {
	"num_divisions": 50, 
	"max_filtration_param": -20,
	"min_filtration_param": 0,
	"start": 0, # where to start reading in the witness file
	"worm_length": 10000, # how many witnesses to read
	"ds_rate": 50,  # if using EST, what down sample rate to use
	"landmark_selector": "maxmin",
	"use_ne_for_maxmin": False,
	"d_speed_amplify": 1, # 
	"d_orientation_amplify": 1, #
	"d_stretch": 1, #
	"d_ray_distance_amplify": 1, #
	"d_use_hamiltonian": 0, #
	"d_cov" : 0, #
	"simplex_cutoff": 0, #
	"weak": False, #
	"absolute": False, #
	"use_cliques": False, #
	"use_twr": False,
	"m2_d": 0,  #Set to anything but 0 to run, set 'time_order_landmarks' = TRUE (don't think i need last part anymore - CHECK)
	"straight_VB": 0, #
	"out": None,
	"program": "Perseus",
	"dimension_cutoff": 2,
	"time_order_landmarks": False,
	"connect_time_1_skeleton": False,
	"reentry_filter": False,
	"store_top_simplices": True,
	"sort_output": False
}

set_path_to_Perseus("")
set_path_to_PHAT("")

if test == 3 or test == 4 or test == 18 or test == 19 or test == 20 or test == 21:
	number_of_steps = 50.0
	max = 1.2
	step = max / number_of_steps

if test == 1:
	calc("Input.txt", "Rank Function Distance Graph.txt", 3, 2, 2, 20)
elif test == 2:
	calc("btc200thou.txt", "BlendedOutput.txt", 20000, 4, .6, 20, 500)
elif test == 3:
	point_cloud = open("btc200thou.txt", "r")
	temp = open("Temp.txt", "w")
	temp.truncate()
	temp.write("3\n")
	temp.write(("1 %f %i" % (step, number_of_steps)) + "\n")
	lines = point_cloud.read().split("\n")
	for j in xrange(75):
		temp.write(lines[j] + (" %f\n" % step))
elif test == 4:
	get_intervals("Temp.txt", "PersistantHomology", max, number_of_steps)
elif test == 5:
	calc("btc2mil.txt", "btc2milOUT.txt", 20000, 10, .6, 50, 400)
elif test == 6:
	calc("btc2mil.txt", "btc2milOUT.txt", 20000, 10, .6, 50, 400, 1400000)
elif test == 7:
	point_cloud = open("btc200thou.txt", "r")
	temp = open("Temp.txt", "w")
	temp.truncate()
	temp.write("3\n")
	temp.write(("1 %f %i" % (step, number_of_steps)) + "\n")
	lines = point_cloud.read().split("\n")
	for j in xrange(75):
		temp.write(lines[j] + (" %f\n" % step))
elif test == 8:
	complex1 = Set([Set([0, 1]),Set([1,2]),Set([2,0])])
	complex2 = Set([Set([2, 1]),Set([0,2])])
	print(complex1.__eq__(complex2))
	complex2.add(Set([0,1]))
	print(complex1.__eq__(complex2))
	complex2.add(Set([0,1]))
	print(complex1.__eq__(complex2))
	print(complex2)
elif test == 9:
	build_filtration("Witness", "Input.txt", 2, 5, landmark_selector = "EST", ds_rate = 2, out = "Output.txt", program = "Perseus")
elif test == 10:
	build_filtration("Witness", "btc200thou.txt", 1, 20, absolute = True, landmark_selector = "EST", ds_rate = 10, out = "btc_100_point_Absolute_Witness_Complex_Perseus.txt", program = "Perseus", cutoff = 100)
	compute_homology("btc_100_point_Absolute_Witness_Complex_Perseus.txt", "btc_100_point_homology", "Perseus")
elif test == 11:
	build_filtration("Witness", "btc200thou.txt", 1, 20, absolute = False, landmark_selector = "EST", ds_rate = 10, out = "btc_100_point_Witness_Complex_Perseus.txt", program = "Perseus", cutoff = 100)
	compute_homology("btc_100_point_Witness_Complex_Perseus.txt", "btc_100_point_homology", "Perseus")
elif test == 12:
	filtration_and_landmarks = build_filtration("Witness", "btc200thou.txt", 1, 20, absolute = False, landmark_selector = "EST", ds_rate = 10, cutoff = 100)
	plot_1_skeleton(filtration_and_landmarks[0], filtration_and_landmarks[1][0], 12, True)
elif test == 13:
	filtration = build_filtration("Witness", "btc200thou.txt", 1, 50, absolute = False, landmark_selector = "EST", ds_rate = 10, cutoff = 1000, out = "Output.txt", program = "Perseus")
	plot_1_skeleton(filtration[0], filtration[1][0], 1, True, extra_points = filtration[1][1], xmin = -.3, xmax = .3, ymin = -.3, ymax = .3, zmin = -.3, zmax = .3)
elif test == 14:
	filtration = build_filtration("Witness", "btc200thou.txt", 1, 50, absolute = False, landmark_selector = "EST", ds_rate = 10, cutoff = 1000, out = "Output.txt", program = "Perseus")
	plot_1_skeleton(filtration[0], filtration[1][0], 5, True, extra_points = filtration[1][1], xmin = -.3, xmax = .3, ymin = -.3, ymax = .3, zmin = -.3, zmax = .3)
elif test == 15:
	build_filtration("Witness", "btc200thou.txt", 1, 20, absolute = False, landmark_selector = "EST", ds_rate = 10, out = "btc_100_point_Witness_Complex_Perseus.txt", program = "Perseus", cutoff = 100)
	compute_homology("btc_100_point_Witness_Complex_Perseus.txt", "btc_100_point_homology", "Perseus")
elif test == 16:
	build_filtration("Witness", "btc200thou.txt", 1, 20, absolute = False, landmark_selector = "EST", ds_rate = 10, out = "btc_100_point_Witness_Complex_Perseus.txt", program = "Perseus", cutoff = 190)
	compute_homology("btc_100_point_Witness_Complex_Perseus.txt", "btc_100_point_homology", "Perseus")
elif test == 17:
	build_filtration("Witness", "btc200thou.txt", 1, 20, absolute = False, landmark_selector = "EST", ds_rate = 10, out = "btc_100_point_Witness_Complex_Perseus.txt", program = "Perseus", cutoff = 200)
	compute_homology("btc_100_point_Witness_Complex_Perseus.txt", "btc_100_point_homology", "Perseus")
elif test == 18:
	get_intervals("For_Test_18.txt", "Test_18_Homology", True, max, number_of_steps)
elif test == 19:
	get_intervals("For_Test_19.txt", "Test_19_Homology", True, max, number_of_steps)
elif test == 20:
	get_intervals("For_Test_20.txt", "Test_20_Homology", True, max, number_of_steps)
elif test == 21:
	get_intervals("For_Test_21.txt", "Test_21_Homology", True, max, number_of_steps)
elif test == 22:
	generate("Ellipse200.txt", "Ellipse", 205, rad_x = 10, rad_y = 5)
elif test == 23:
	filtration = build_filtration("Witness", "Ellipse200.txt", 12, 50, absolute = False, landmark_selector = "EST", ds_rate = 20, out = "Ellipse200Out.txt", program = "Perseus")
	compute_homology("Ellipse200.txt", "Ellipse200Homology", "Perseus")
	plot_1_skeleton(filtration[0], filtration[1][0], 2, False, extra_points = filtration[1][1], xmin = -11, xmax = 11, ymin = -11, ymax = 11)
	plot_1_skeleton(filtration[0], filtration[1][0], 15, False, extra_points = filtration[1][1], xmin = -11, xmax = 11, ymin = -11, ymax = 11)
	plot_1_skeleton(filtration[0], filtration[1][0], 35, False, extra_points = filtration[1][1], xmin = -11, xmax = 11, ymin = -11, ymax = 11)
elif test == 24:
	m = {}
	m[ImmutableSet([0,1])] = 3
	print(ImmutableSet([0,1]) in m)
	print(ImmutableSet([0,2]) in m)
	print(m[ImmutableSet([0, 1])])
	print(m[ImmutableSet([0,2])])
	print(type(m))
elif test == 25:
	filtration = build_filtration("Witness", "Ellipse200.txt", 12, 50, absolute = False, landmark_selector = "EST", ds_rate = 20, out = "Ellipse200Out.txt", program = "PHAT")
elif test == 26:
	filtration = build_filtration("Witness", "Ellipse200.txt", 12, 50, absolute = False, landmark_selector = "EST", ds_rate = 20, out = "Ellipse200Out_Phat.txt", program = "PHAT")
	compute_homology("Ellipse200Out_Phat.txt", "Ellipse200_Phat_Homology.txt", "PHAT")
	get_persistence_diagram("Ellipse200_Phat_Homology.txt", 1, PHAT_in = "Ellipse200Out_Phat.txt", simultaneous_additions = filtration[1][2], max = 12, num_steps = 50)
elif test == 27:
	filtration = build_filtration("Witness", "Ellipse200.txt", 12, 50, absolute = False, landmark_selector = "EST", ds_rate = 20, out = "Ellipse200Out_Phat.txt", program = "PHAT")
	compute_homology("Ellipse200Out_Phat.txt", "Ellipse200_Phat_Homology.txt", "PHAT")
	get_persistence_diagram("Ellipse200_Phat_Homology.txt", 1, PHAT_in = "Ellipse200Out_Phat.txt", simultaneous_additions = filtration[1][2], max = 12, num_steps = 50)
elif test == 28:
	filtration = build_filtration("Witness", "Ellipse200.txt", 12, 50, absolute = False, landmark_selector = "EST", ds_rate = 13, out = "Ellipse200Out_Phat.txt", program = "PHAT")
	compute_homology("Ellipse200Out_Phat.txt", "Ellipse200_Phat_Homology.txt", "PHAT")
	get_persistence_diagram("Ellipse200_Phat_Homology.txt", 1, PHAT_in = "Ellipse200Out_Phat.txt", simultaneous_additions = filtration[1][2], max = 12, num_steps = 50)
elif test == 29:
	filtration = build_filtration("Witness", "Ellipse200.txt", 12, 50, absolute = False, landmark_selector = "EST", ds_rate = 10, out = "Ellipse200Out_Phat.txt", program = "PHAT", dimension_cutoff = 2)
	#print(filtration)
	compute_homology("Ellipse200Out_Phat.txt", "Ellipse200_Phat_Homology.txt", "PHAT")
	get_persistence_diagram("Ellipse200_Phat_Homology.txt", 1, PHAT_in = "Ellipse200Out_Phat.txt", simultaneous_additions = filtration[1][2], max = 12, num_steps = 50)
elif test == 30:
	filtration = build_filtration("Witness", "Ellipse200.txt", 12, 50, absolute = False, landmark_selector = "EST", ds_rate = 10, out = "Ellipse200Out_Perseus.txt", program = "Perseus", dimension_cutoff = 2)
	compute_homology("Ellipse200Out_Perseus.txt", "Ellipse200_Perseus_Homology.txt", "Perseus")
	#get_persistence_diagram("Ellipse200_Phat_Homology.txt", 1, max = 12, num_steps = 50)
elif test == 31:
	generate("Ellipse2000.txt", "Ellipse", 2000, rad_x = 10, rad_y = 5)
elif test == 32:
	filtration = build_filtration("Witness", "Ellipse2000.txt", 12, 50, absolute = False, landmark_selector = "EST", ds_rate = 20, out = "Ellipse2000Out_Phat.txt", program = "PHAT", dimension_cutoff = 2)
	compute_homology("Ellipse2000Out_Phat.txt", "Ellipse2000_Phat_Homology.txt", "PHAT")
	get_persistence_diagram("Ellipse2000_Phat_Homology.txt", 1, PHAT_in = "Ellipse2000Out_Phat.txt", simultaneous_additions = filtration[1][2], max = 12, num_steps = 50)
elif test == 33:
	filtration = build_filtration("Witness", "Ellipse2000.txt", 12, 50, absolute = False, landmark_selector = "EST", ds_rate = 20, out = "Ellipse2000Out_Perseus.txt", program = "Perseus", dimension_cutoff = 2)
	compute_homology("Ellipse2000Out_Perseus.txt", "Ellipse2000_Perseus_Homology.txt", "Perseus")
	#get_persistence_diagram("Ellipse200_Phat_Homology.txt", 1, max = 12, num_steps = 50)
elif test == 34:
	filtration = build_filtration("Witness", "btc200thou.txt", 1, 50, absolute = False, landmark_selector = "EST", ds_rate = 10, cutoff = 1000, out = "Output.txt", program = "Perseus")
	autoplot_1_skeleton_witness(filtration, 5)
elif test == 35:
	points_to_persistence_diagram("Witness", "Ellipse200", 12, 50, absolute = False, landmark_selector = "EST", ds_rate = 20, program = "PHAT", dimension_cutoff = 2, persistence_plot_dimension = 1)
elif test == 36:
	points_to_persistence_diagram("Witness", "Ellipse200", 12, 50, absolute = False, landmark_selector = "EST", ds_rate = 20, program = "Perseus", dimension_cutoff = 2, persistence_plot_dimension = 1)
elif test == 37:
	generate("VarCircle.txt", "VarCircle", 0)
	#filtration = build_filtration("Witness", "VarCircle.txt", 1, 50, absolute = False, landmark_selector = "EST", ds_rate = 100, out = "VarCircleOut.txt", program = "PHAT")
	#autoplot_1_skeleton_witness(filtration, 5)
elif test == 38:
	generate("Figure8.txt", "Figure8", 200)
	filtration = build_filtration("Witness", "Figure8.txt", 1, 50, absolute = False, landmark_selector = "EST", ds_rate = 10)#, out = "Figure8Out.txt", program = "PHAT")
	autoplot_1_skeleton_witness(filtration, 15)
elif test == 39:
	points_to_persistence_diagram("Witness", "Ellipse200", 12, 50, absolute = False, landmark_selector = "EST", ds_rate = 20, program = "PHAT", use_cliques = False, persistence_plot_dimension = 1)
elif test == 40:
	points_to_persistence_diagram("Witness", "Ellipse200", 12, 50, absolute = False, landmark_selector = "EST", ds_rate = 20, program = "PHAT", use_cliques = True, persistence_plot_dimension = 1)
elif test == 41:
	g = nx.Graph()
	g.add_nodes_from([1,2,3,4,5])
	g.add_edges_from([(1,2), (2,3), (3,1), (3,4), (4,5), (5,3)])
	for c in nx.find_cliques(g):
		print(c)
	print("")
	g.add_edge(2,4)
	for c in nx.find_cliques(g):
		print(c)
	print("")
	g.add_edge(2,5)
	for c in nx.find_cliques(g):
		print(c)
elif test == 42:
	f = points_to_persistence_diagram("Witness", "Ellipse200", 12, 50, absolute = False, landmark_selector = "EST", ds_rate = 20, program = "PHAT", use_cliques = False, persistence_plot_dimension = 1, connect_1_skeleton = True)
	autoplot_1_skeleton_witness(f, 2)
elif test == 43:
	f = points_to_persistence_diagram("Witness", "Figure8", 1, 50, absolute = False, landmark_selector = "EST", ds_rate = 10, program = "PHAT", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, connect_1_skeleton = False)
	plot_2_skeleton(f, 15)
elif test == 44:
	f = points_to_persistence_diagram("Witness", "Figure8", 1, 50, absolute = False, landmark_selector = "EST", ds_rate = 10, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, connect_1_skeleton = False)
	plot_2_skeleton(f, 15)
elif test == 45:
	f = points_to_persistence_diagram("Witness", "Figure8", 1, 50, absolute = False, landmark_selector = "EST", ds_rate = 10, program = "PHAT", use_cliques = True, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = True)
	for i in [0, 5, 15, 20, 30]:
		plot_2_skeleton(f, i)
elif test == 46:
	f = points_to_persistence_diagram("Witness", "Figure8", 1, 50, absolute = False, landmark_selector = "EST", ds_rate = 10, program = "Perseus", use_cliques = True, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = True)
	for i in [0, 5, 15, 20, 30]:
		plot_2_skeleton(f, i)
elif test == 47:
	f = points_to_persistence_diagram("Witness", "Ellipse2000", 30, 50, absolute = False, landmark_selector = "EST", ds_rate = 20, program = "PHAT", use_cliques = True, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = True)
	for i in [0, 5, 15, 20, 30]:
		plot_2_skeleton(f, i)
elif test == 48:
	f = points_to_persistence_diagram("Witness", "Ellipse2000", 12, 50, absolute = False, landmark_selector = "EST", ds_rate = 20, program = "Perseus", use_cliques = True, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = True)
elif test == 49:
	generate("Annulus1.txt", "Annulus1", 20, rad = 1, layers = 4, delta_r = 1)
	f = points_to_persistence_diagram("Witness", "Annulus1", 2, 50, absolute = False, landmark_selector = "EST", ds_rate = 4, program = "PHAT", use_cliques = True, dimension_cutoff = 2, persistence_plot_dimension = 1)
	for i in [0, 5, 15, 20, 30]:
		plot_2_skeleton(f, i)
elif test == 50:
	generate("Annulus2.txt", "Annulus2", 60, rad = 1, layers = 4, delta_r = 1)
	f = points_to_persistence_diagram("Witness", "Annulus2", 2, 50, absolute = False, landmark_selector = "EST", ds_rate = 10, program = "PHAT", use_cliques = True, dimension_cutoff = 2, persistence_plot_dimension = 1)
	for i in [0, 5, 15, 20, 30]:
		plot_2_skeleton(f, i)
elif test == 51:
	generate("Annulus3.txt", "Annulus3", 60, rad = 1, layers = 4, delta_r = 1)
	f = points_to_persistence_diagram("Witness", "Annulus3", 2, 50, absolute = False, landmark_selector = "EST", ds_rate = 10, program = "PHAT", use_cliques = True, dimension_cutoff = 2, persistence_plot_dimension = 1)
	for i in [0, 5, 15, 20, 30]:
		plot_2_skeleton(f, i)
elif test == 52:
	generate("Superformula1.txt", "Superformula", 1000, m = 7, n1 = 3, n2 = 4, n3 = 17)
	filtration = build_filtration("Witness", "Superformula1.txt", 1, 50, absolute = False, landmark_selector = "EST", ds_rate = 20, use_cliques = False)
	plot_2_skeleton(filtration, 5)
elif test == 53:
	f = points_to_persistence_diagram("Witness", "Ellipse200", 5, 50, absolute = False, landmark_selector = "EST", ds_rate = 20, program = "PHAT", use_cliques = True, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = True)
elif test == 54:
	f = points_to_persistence_diagram("Witness", "Ellipse200", 5, 50, absolute = False, landmark_selector = "EST", ds_rate = 20, program = "Perseus", use_cliques = True, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = True)
elif test == 55:
	f = points_to_persistence_diagram("Witness", "btc200thou", .1, 50, absolute = False, landmark_selector = "EST", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000)
	plot_2_skeleton(f, 25)
elif test == 56:
	f = points_to_persistence_diagram("Witness", "btc200thou", .1, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000)
	plot_2_skeleton(f, 25)
	plot_2_skeleton(f, 50)
elif test == 57:
	f = points_to_persistence_diagram("Witness", "btc200thou", .01, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 2, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10)
	autoplot_1_skeleton_witness(f, 25)
	autoplot_1_skeleton_witness(f, 50)
elif test == 58:
	f = points_to_persistence_diagram("Witness", "btc200thou", .1, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, connect_1_skeleton = True)
	plot_2_skeleton(f, 25)
elif test == 59:
	f = points_to_persistence_diagram("Witness", "btc200thou", .1, 50, absolute = False, landmark_selector = "EST", ds_rate = 100, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, connect_1_skeleton = True)
	plot_2_skeleton(f, 25)
elif test == 60:
	f = points_to_persistence_diagram("Witness", "btc200thou", .1, 5, absolute = False, landmark_selector = "maxmin", ds_rate = 2, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10, connect_1_skeleton = True)
	make_movie(f, "Test")
elif test == 61:
	f = points_to_persistence_diagram("Witness", "btc200thou", .1, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 62:
	f = points_to_persistence_diagram("Witness", "btc200thou", .1, 50, absolute = False, landmark_selector = "EST", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000)
	make_movie(f, "Lorenz10000EST")
elif test == 63:
	f = points_to_persistence_diagram("Witness", "btc200thou", .08, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 40, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000)
	make_movie(f, "Lorenz10000")
elif test == 64:
	f = points_to_persistence_diagram("Witness", "btc200thou", .08, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 25, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000)
	make_movie(f, "Lorenz10000")
elif test == 65:
	f = points_to_persistence_diagram("Witness", "btc200thou", .1, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = True, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000)
	make_movie(f, "Lorenz10000")
elif test == 66: # (Like 61, but connecting the time 1-skeleton)
	f = points_to_persistence_diagram("Witness", "btc200thou", .1, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, connect_1_skeleton = True, reentry_filter = False, cutoff = 10000)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 67:
	f = points_to_persistence_diagram("Witness", "btc200thou", .1, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, connect_1_skeleton = True, reentry_filter = False, cutoff = 10000)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 68:
	f = points_to_persistence_diagram("Witness", "btc200thou", .1, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000)
	make_movie(f, "Lorenz10000", cleanup_images = False)
elif test == 69:
	f = points_to_persistence_diagram("Witness", "btc200thou", .1, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, d_stretch = 2)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 70:
	f = points_to_persistence_diagram("Witness", "btc200thou", .08, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, d_speed_amplify = 2)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 71:
	f = points_to_persistence_diagram("Witness", "btc200thou", .06, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, d_speed_amplify = 3)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 72:
	f = points_to_persistence_diagram("Witness", "btc200thou", .06, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, d_stretch = 2, d_speed_amplify = 2)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 73:
	f = points_to_persistence_diagram("Witness", "btc200thou", .08, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = True, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, d_speed_amplify = 2)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 74:
	f = points_to_persistence_diagram("Witness", "btc200thou", .05, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = True, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, d_speed_amplify = 2)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 75:
	f = points_to_persistence_diagram("Witness", "btc200thou", .05, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, d_speed_amplify = 5)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 76:
	f = points_to_persistence_diagram("Witness", "btc200thou", .05, 50, absolute = True, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, d_speed_amplify = 5)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 77:
	f = points_to_persistence_diagram("Witness", "btc200thou", .06, 50, absolute = True, min_filtration_param = .01, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, d_speed_amplify = 5)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 78:
	f = points_to_persistence_diagram("Witness", "btc200thou", .02, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, d_stretch = 4, d_speed_amplify = 4)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 79:
	f = points_to_persistence_diagram("Witness", "btc200thou", -15, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, d_speed_amplify = 5)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 80:
	f = points_to_persistence_diagram("Witness", "btc200thou", .08, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "PHAT", use_cliques = True, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, d_speed_amplify = 2)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 81:
	f = points_to_persistence_diagram("Witness", "btc200thou", .02, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, d_stretch = 4)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 82:
	f = points_to_persistence_diagram("Witness", "btc200thou", .05, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = True, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, d_speed_amplify = 5)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 83:
	f = points_to_persistence_diagram("Witness", "btc200thou", .03, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, d_orientation_amplify = 4)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 84:
	f = points_to_persistence_diagram("Witness", "btc200thou", -21, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, d_stretch = 4)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 85:
	f = points_to_persistence_diagram("Witness", "btc200thou", -21, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, d_speed_amplify = 4)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 86:
	f = points_to_persistence_diagram("Witness", "btc200thou", -21, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, d_orientation_amplify = 3, d_speed_amplify = 3)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 87:
	f = points_to_persistence_diagram("Witness", "btc200thou", .1, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "PHAT", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 88:
	f = points_to_persistence_diagram("Witness", "btc200thou", -21, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, d_orientation_amplify = 9)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 89:
	f = points_to_persistence_diagram("Witness", "btc200thou", -21, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, d_speed_amplify = 9)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 90: # New storage
	f = points_to_persistence_diagram("Witness", "btc200thou", .1, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, store_top_simplices = False)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 91:
	f = points_to_persistence_diagram("Witness", "btc200thou", .1, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000)
	#make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 92:
	r = open("btc200thou_complex_for_Perseus.txt", "r")
	set_filt = Set()
	r.readline()
	for line in r.read().split("\n"):
		if line != "":
			line_data = [int(s) for s in line.split(" ")]
			set_filt.add(SimplexBirth(line_data[1:-1], line_data[-1], True))
	r.close()
	list_filt = sorted(list(set_filt))
	w = open("btc200thou_complex_for_Perseus_SORTED.txt", "w")
	w.truncate()
	w.write("1\n")
	for simplex_birth in list_filt:
		w.write(str(len(simplex_birth.landmark_set) - 1) + " ")
		for landmark in simplex_birth.sll:
			w.write(str(landmark) + " ")
		w.write(str(simplex_birth.birth_time) + "\n")
	w.close()
elif test == 93: # Old storage
	f = points_to_persistence_diagram("Witness", "btc200thou", .1, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 94:
	f = points_to_persistence_diagram("Witness", "btc200thou", -21, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000, d_orientation_amplify = 3, d_speed_amplify = 3)
elif test == 95:
	f = points_to_persistence_diagram("Witness", "btc2milIC123", .1, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 96: # Took 9.2 minutes
	make_worm_movies("btc2milIC123.txt", 4)
elif test == 97:
	make_worm_movies("btc2milIC123.txt", 2, landmark_selector = "EST")
elif test == 98:
	make_worm_movies("btc2milIC123.txt", 3, d_speed_amplify = 3)
elif test == 99:
	f = points_to_persistence_diagram("Witness", "btc2milIC123", .1, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, start = 1990000, cutoff = 10000, d_speed_amplify = 3)
	make_movie(f, "Rossler_End", include_witnesses = True)
elif test == 100:
	f = points_to_persistence_diagram("Witness", "btc2milIC123", .1, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, start = 1990000, cutoff = 10000, d_orientation_amplify = 3)
	make_movie(f, "Rossler_End", include_witnesses = True)
elif test == 101:
	f = points_to_persistence_diagram("Witness", "btc2milIC123", -20, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, start = 1990000, cutoff = 10000, d_speed_amplify = 27)
	make_movie(f, "Rossler_End", include_witnesses = True)
elif test == 102:
	for amp_factor in (1, 3, 6, 9, 15):
		make_worm_movies("btc2milIC123.txt", 3, format_type = 2, d_speed_amplify = amp_factor, ds_rate = 500, max_filtration_param = -15)
		make_worm_movies("btc2milIC123.txt", 3, format_type = 2, d_orientation_amplify = amp_factor, ds_rate = 500, max_filtration_param = -15)
elif test == 103: # Call with command: python -u Tester.py 103 > Test103ConsoleOutput.txt
	global_start_time = timeit.default_timer()
	make_worm_movies("btc2milIC123.txt", 9)
	for amp_factor in (3, 6, 9, 15):
		print("\n---------------- AMP FACTOR %i ----------------" % amp_factor)
		make_worm_movies("btc2milIC123.txt", 9, format_type = 2, d_speed_amplify = amp_factor)
		make_worm_movies("btc2milIC123.txt", 9, format_type = 2, d_orientation_amplify = amp_factor)
	global_end_time = timeit.default_timer()
	print("\n\n\n\nALL TESTS FINISHED!!!!\n\nTotal time elapsed: %f seconds.\n" % (global_end_time - global_start_time))
elif test == 104:
	f = points_to_persistence_diagram("Witness", "btc200thou", -21, 50, absolute = False, landmark_selector = "EST", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, cutoff = 10000)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 105:
	for dsr in (66.6, 100, 200, 400):
		make_worm_movies("btc2milIC123.txt", 9, format_type = 3, ds_rate = dsr)
		make_worm_movies("btc2milIC123.txt", 9, format_type = 3, d_orientation_amplify = 3, ds_rate = dsr)
elif test == 106:
	f = points_to_persistence_diagram("Witness", "btc2milIC123", .1, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, start = 1243750, cutoff = 10000, d_speed_amplify = 3)
	make_movie(f, "Rossler_End", include_witnesses = True)
elif test == 107:
	f = points_to_persistence_diagram("Witness", "btc2milIC123", .05, 50, absolute = False, landmark_selector = "maxmin", ds_rate = 50, program = "Perseus", use_cliques = False, dimension_cutoff = 2, persistence_plot_dimension = 1, reentry_filter = False, start = 1243750, cutoff = 10000, d_orientation_amplify = 3)
	make_movie(f, "Rossler_End", include_witnesses = True)
	
## NEW VERSION

elif test == 108:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 109:
	f = points_to_persistence_diagram("btc2milIC123", old_parameter_set, max_filtration_param = .2, simplex_cutoff = 15, start = 1243750)
	make_movie(f, "Worm_7", include_witnesses = True)
elif test == 110:
	f = points_to_persistence_diagram("btc2milIC123", old_parameter_set, max_filtration_param = .2, simplex_cutoff = 15)
	make_movie(f, "Worm_7", include_witnesses = True)
elif test == 111:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set)
elif test == 112:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, worm_length = 500, max_filtration_param = .1)
elif test == 113:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, worm_length = 500, max_filtration_param = .1, use_cliques = True)
elif test == 114:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, cutoff = 1000, max_filtration_param = .1)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 115:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, cutoff = 1000, max_filtration_param = 15, weak = True)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 116:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, cutoff = 10000, max_filtration_param = 15, weak = True)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 117:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, cutoff = 10000, max_filtration_param = 10, weak = True, d_orientation_amplify = 9)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 118:
	make_worm_movies("btc2milIC123.txt", 9, old_parameter_set, weak = True, max_filtration_param = 5, d_orientation_amplify = 9)
elif test == 119:
	make_worm_movies("btc2milIC123.txt", 9, old_parameter_set, simplex_cutoff = 6, max_filtration_param = .3, d_orientation_amplify = 9)
elif test == 120:
	make_worm_movies("btc2milIC123.txt", 41, old_parameter_set, simplex_cutoff = 8, max_filtration_param = .3, d_orientation_amplify = 9)
elif test == 121:
	make_worm_movies("btc2milIC123.txt", 5, old_parameter_set, simplex_cutoff = 8, max_filtration_param = .3)
elif test == 122:
	f = points_to_persistence_diagram("btc2milIC123", old_parameter_set, max_filtration_param = .3, simplex_cutoff = 8, d_orientation_amplify = 9, start = 1641750, cutoff = 20000, ds_rate = 100) # Starts at 34 / 41
	make_movie(f, "Worm_3435", include_witnesses = True)
elif test == 123:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, d_use_hamiltonian = 100)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 124:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, d_use_hamiltonian = 10)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 125:
	f = points_to_persistence_diagram("WobblyTorus0", old_parameter_set)
	make_movie(f, "WobblyTorus0", include_witnesses = False)
elif test == 126:
	f = points_to_persistence_diagram("WobblyTorus0", old_parameter_set, dimension_cutoff = 3, persistence_plot_dimension = 2)
	make_movie(f, "WobblyTorus0", include_witnesses = True)
elif test == 127:
	make_worm_movies("btc2milIC123.txt", 21, old_parameter_set, d_use_hamiltonian = -1)
elif test == 128:
	f = build_filtration("btc2milIC123.txt", old_parameter_set, d_use_hamiltonian = -1, start = 1791000)
	plot_2_skeleton(f, 30)
	plot_2_skeleton(f, 40)
elif test == 129:
	for s in [1393000, 1492500,1592000, 1691500, 1791000]:
		f = build_filtration("btc2milIC123.txt", old_parameter_set, d_use_hamiltonian = -1, use_cliques = True, start = s)
		plot_2_skeleton(f, 30)
elif test == 130:
	embed("EmbeddingTest.txt", "EmbeddingTestOut.txt", 2, 2)
elif test == 131:
	embed("btc2milIC123.txt", "btc2milIC123_embedded.txt", 17, 3)
elif test == 132:
	f = points_to_persistence_diagram("btc2milIC123_embedded", old_parameter_set)
	make_movie(f, "Embedded", include_witnesses = True)
elif test == 133:
	make_worm_movies("btc2milIC123_embedded.txt", 9, old_parameter_set, view = "0,0")
elif test == 134:
	make_worm_movies("btc2milIC123_embedded.txt", 9, old_parameter_set, d_use_hamiltonian = -1, view = "0,0")
elif test == 135:
	make_worm_movies("btc2milIC123_embedded.txt", 9, old_parameter_set, simplex_cutoff = 8)
elif test == 136:
	make_worm_movies("btc2milIC123_embedded.txt", 41, old_parameter_set)
elif test == 137:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, d_ray_distance_amplify = 2)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 138:
	f = points_to_persistence_diagram("btc2milIC123_embedded", old_parameter_set, d_ray_distance_amplify = 2, start = 149247)
	make_movie(f, "Lorenz10000", include_witnesses = True)
elif test == 139:
	make_worm_movies("btc2milIC123_embedded.txt", 9, old_parameter_set)
elif test == 140:
	make_worm_movies("btc2milIC123_embedded.txt", 9, old_parameter_set, d_ray_distance_amplify = 2)
elif test == 141:
	make_worm_movies("btc2milIC123.txt", 9, old_parameter_set)
elif test == 142:
	f = points_to_persistence_diagram("btc2milIC123_embedded.txt", old_parameter_set, d_orientation_amplify = 9, start = 99498)
	make_movie(f, "142", include_witnesses = True)
elif test == 143:
	f = points_to_persistence_diagram("btc2milIC123_embedded.txt", old_parameter_set, d_ray_distance_amplify = 2, start = 99498)
	make_movie(f, "143", include_witnesses = True)
elif test == 144:
	embed("btc2milIC123.txt", "btc2milIC123_embedded_z.txt", 17, 3, 2)
elif test == 145:
	f = points_to_persistence_diagram("btc2milIC123_embedded_z.txt", old_parameter_set, start = 99498)
	make_movie(f, "142", include_witnesses = True)
elif test == 146:
	f = points_to_persistence_diagram("btc2milIC123_embedded_z.txt", old_parameter_set)
	make_movie(f, "142", include_witnesses = True)
elif test == 147:
	f = build_filtration("btc2milIC123_embedded_z.txt", old_parameter_set)
	plot_2_skeleton(f, 15)
elif test == 148:
	embed("btc2milIC123.txt", "btc2milIC123_embedded_z_t7.txt", 7, 3, 2)
elif test == 149:
	f = points_to_persistence_diagram("btc2milIC123_embedded_z_t7.txt", old_parameter_set, start = 99498)
	make_movie(f, "EmbeddedZ", include_witnesses = True)
elif test == 150:
	f = points_to_persistence_diagram("btc2milIC123.txt", old_parameter_set, use_twr = True)
	make_movie(f, "TWR", include_witnesses = True)

elif test == 200:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, d_use_hamiltonian = 1)
	make_movie(f, "Hamiltonian1", include_witnesses = True)
elif test == 201:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, d_use_hamiltonian = 2)
	make_movie(f, "Hamiltonian2", include_witnesses = True)
elif test == 202:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, d_use_hamiltonian = 5)
	make_movie(f, "Hamiltonian5", include_witnesses = True)
elif test == 203:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, d_use_hamiltonian = 10)
	make_movie(f, "Hamiltonian10", include_witnesses = True)
elif test == 204:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, d_use_hamiltonian = 20)
	make_movie(f, "Hamiltonian20", include_witnesses = True)
elif test == 205:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, d_use_hamiltonian = 50)
	make_movie(f, "Hamiltonian50", include_witnesses = True)
elif test == 206:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, d_use_hamiltonian = .1)
	make_movie(f, "Hamiltonianp1", include_witnesses = True)
elif test == 207:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, d_use_hamiltonian = .5)
	make_movie(f, "Hamiltonianp5", include_witnesses = True)
elif test == 208:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, d_use_hamiltonian = 0)
	make_movie(f, "HamiltonianCONTROL", include_witnesses = True)
elif test == 209:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, d_use_hamiltonian = -1)
	make_movie(f, "Hamiltonian1", include_witnesses = True)
elif test == 210:
	make_worm_movies("btc2milIC123.txt", 21, old_parameter_set) # 21 worm CONTROL
elif test == 211:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, title = NHp1,  d_use_hamiltonian = -.1)
	make_movie(f, "NHamiltonianp1", include_witnesses = True)
elif test == 212:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, title = NHp25, d_use_hamiltonian = -.25)
	make_movie(f, "NHamiltonianp25", include_witnesses = True)
elif test == 213:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, title = NHp15, d_use_hamiltonian = -.5)
	make_movie(f, "NHamiltonianp5", include_witnesses = True)
elif test == 214:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, title = NH1, d_use_hamiltonian = -1)
	make_movie(f, "NHamiltonian1", include_witnesses = True)
elif test == 215:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, title = NH2, d_use_hamiltonian = -2)
	make_movie(f, "NHamiltonian2", include_witnesses = True)
elif test == 216:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, title = NH5, d_use_hamiltonian = -4)
	make_movie(f, "NHamiltonian4", include_witnesses = True)
elif test == 217:
		embed("btc2milIC123.txt", "btc2milIC123_embedded.txt", 17, 3)
elif test == 218:
	make_worm_movies("btc2milIC123_embedded.txt", 9, old_parameter_set, d_orientation_amplify = 9)
elif test == 219:
	make_worm_movies("btc2milIC123.txt", 9, old_parameter_set, title = "SimCutoff1", max_filtration_param = .3, simplex_cutoff = 1)
elif test == 221:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, title = "SimCutoff2", max_filtration_param = .3, simplex_cutoff = 2)
	make_movie(f, "SimCutoff2", include_witnesses = True)
elif test == 222:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, title = "SimCutoff3", max_filtration_param = .3, simplex_cutoff = 3)
	make_movie(f, "SimCutoff3", include_witnesses = True)
elif test == 223:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, title = "SimCutoff4", max_filtration_param = .3, simplex_cutoff = 4)
	make_movie(f, "SimCutoff4", include_witnesses = True)
elif test == 224:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, title = "SimCutoff5", max_filtration_param = .3, simplex_cutoff = 5)
	make_movie(f, "SimCutoff5", include_witnesses = True)
elif test == 225:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, title = "SimCutoff6", max_filtration_param = .3, simplex_cutoff = 6)
	make_movie(f, "SimCutoff6", include_witnesses = True)
elif test == 226:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, title = "SimCutoff7", max_filtration_param = .3, simplex_cutoff = 7)
	make_movie(f, "SimCutoff7", include_witnesses = True)
elif test == 227:
	f = points_to_persistence_diagram("btc200thou", old_parameter_set, title = "SimCutoff8", max_filtration_param = .3, simplex_cutoff = 8)
	make_movie(f, "SimCutoff8", include_witnesses = True)
elif test == 228:
	f = points_to_persistence_diagram("WobblyTorus0", old_parameter_set, title = "WT0_NH1", d_use_hamiltonian = -1)
	make_movie(f, "WT0_NHamiltonian1", include_witnesses = True)
elif test == 229:
	f = points_to_persistence_diagram("WobblyTorus2", old_parameter_set, title = "WT2_NH1", d_use_hamiltonian = -1)
	make_movie(f, "WT2_NHamiltonian1", include_witnesses = True)
elif test == 230:
	f = points_to_persistence_diagram("WobblyTorus10", old_parameter_set, title = "WT10_NH1", d_use_hamiltonian = -1)
	make_movie(f, "WT10_NHamiltonian1", include_witnesses = True)
elif test == 231:
	f = points_to_persistence_diagram("WobblyTorus0", old_parameter_set, title = "WT0_09", d_orientation_amplify = 9)
	make_movie(f, "WT0_O9", include_witnesses = True)
elif test == 232:
	f = points_to_persistence_diagram("WobblyTorus2", old_parameter_set, title = "WT2_09", d_orientation_amplify = 9)
	make_movie(f, "WT2_O9", include_witnesses = True)
elif test == 233:
	f = points_to_persistence_diagram("WobblyTorus10", old_parameter_set, title = "WT10_09", d_orientation_amplify = 9)
	make_movie(f, "WT10_O9", include_witnesses = True)
elif test == 234:
	embed("btc2milIC123.txt", "btc2milIC123_embedded.txt", 17, 3)
elif test == 235:
	make_worm_movies("btc2milIC123_embedded.txt", 9, old_parameter_set, simplex_cutoff = 8, d_orientation_amplify = 9) 
elif test == 236:
	embed("btc2milIC123.txt", "btc2milIC123_embedded.txt", 17, 3)
elif test == 237:
	make_worm_movies("btc2milIC123_embedded.txt", 9, old_parameter_set, d_use_hamiltonian = -1)

elif test == 238:
	make_worm_movies("btc2milIC123_embedded.txt", 3, old_parameter_set, use_twr = True) # Did not run, memory issues
elif test == 239:
	make_worm_movies("btc2milIC123_embedded.txt", 3, old_parameter_set, ds_rate = 100, use_twr = True)
elif test == 240:
	make_worm_movies("btc2milIC123_embedded.txt", 3, old_parameter_set, ds_rate = 1000, use_twr = True)
elif test == 241:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, worm_length = 1000, ds_rate = 100, use_twr = True)
elif test == 242:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 1000, use_twr = True)
elif test == 243:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, max_filtration_param = .3, ds_rate = 1000, use_twr = True)
	
elif test == 244:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, worm_length = 1000, ds_rate = 100, use_twr = True, use_clique = True)
elif test == 245:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, worm_length = 1000, ds_rate = 100, max_filtration_param = .3, use_twr = True, use_cliques = True)
elif test == 246:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, worm_length = 1000, max_filtration_param = .3, ds_rate = 50, use_cliques = True, use_twr = True)
elif test == 247:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, worm_length = 1000, max_filtration_param = .3, ds_rate = 20, use_cliques = True, use_twr = True)
elif test == 248:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, worm_length = 1000, max_filtration_param = .3, ds_rate = 20, use_twr = True)
elif test == 249:
	make_worm_movies("btc2milIC123.txt", 2, old_parameter_set,  max_filtration_param = .3, landmark_selector = "EST", use_twr = True, use_cliques = True)
elif test == 250:
	make_worm_movies("btc2milIC123.txt", 2, old_parameter_set, landmark_selector = "EST", use_twr = True, use_cliques = True)
elif test == 251:
	make_worm_movies("btc2milIC123.txt", 2, old_parameter_set, landmark_selector = "EST", use_twr = True)
elif test == 252:
	make_worm_movies("btc2milIC123.txt", 2, old_parameter_set, use_twr = True)
elif test == 253:
	make_worm_movies("btc2milIC123.txt", 2, old_parameter_set,  max_filtration_param = .1, landmark_selector = "EST", use_twr = True)
elif test == 254:
	make_worm_movies("btc2milIC123.txt", 2, old_parameter_set,  worm_length = 4000, ds_rate = 100, max_filtration_param = .3, landmark_selector = "EST", use_twr = True)


elif test == 255:
	f = points_to_persistence_diagram("Annulus1_np100r1L8dp25", old_parameter_set, ds_rate = 20, landmark_selector = "EST", use_twr = True, title = "Annulus1_np100r1L8dp25")
	make_movie(f, "Annulus1_np100r1L8dp25", include_witnesses = True)
elif test == 256:
	f = points_to_persistence_diagram("Annulus1_np100r1L8dp25", old_parameter_set, ds_rate = 40, max_filtration_param = -19, landmark_selector = "EST", use_twr = True, title = "Annulus1_np100r1L8dp25")
	make_movie(f, "Annulus1_np100r1L8dp25", include_witnesses = True)
elif test == 257:
	f = points_to_persistence_diagram("Annulus1_np100r1L8dp25", old_parameter_set, ds_rate = 40, landmark_selector = "EST", title = "Annulus1_np100r1L8dp25")
	make_movie(f, "Annulus1_np100r1L8dp25", include_witnesses = True)
	
elif test == 258:
	generate("Annulus1_np20r1L5dp1", "Annulus1", 20, rad = 1, layers = 5, delta_r = 1)
	
elif test == 259:
	f = points_to_persistence_diagram("Annulus1_np20r1L5dp1", old_parameter_set, ds_rate = 4, landmark_selector = "EST", title = "Annulus1_np20r1L5dp1")
	make_movie(f, "Annulus1_np20r1L5dp1", include_witnesses = True)
	
elif test == 260:
	f = points_to_persistence_diagram("Annulus1_np20r1L5dp1", old_parameter_set, ds_rate = 4, landmark_selector = "EST", use_twr = True, title = "Annulus1_np20r1L5dp1")
	make_movie(f, "Annulus1_np20r1L5dp1", include_witnesses = True)

elif test == 261:
	f = points_to_persistence_diagram("Annulus1_np20r1L5dp1", old_parameter_set, ds_rate = 4, num_divisions = 10, landmark_selector = "EST", use_twr = True, title = "Annulus1_np20r1L5dp1")
	make_movie(f, "Annulus1_np20r1L5dp1", include_witnesses = True)

elif test == 262:
	f = points_to_persistence_diagram("Annulus1_np20r1L5dp1", old_parameter_set, ds_rate = 4, num_divisions = 10, max_filtration_param = -10, landmark_selector = "EST", use_twr = True, title = "Annulus1_np20r1L5dp1")
	make_movie(f, "Annulus1_np20r1L5dp1", include_witnesses = True)
	
elif test == 263:
	f = points_to_persistence_diagram("Annulus1_np20r1L5dp1", old_parameter_set, ds_rate = 4, num_divisions = 10, max_filtration_param = -30, landmark_selector = "EST", use_twr = True, title = "Annulus1_np20r1L5dp1")
	make_movie(f, "Annulus1_np20r1L5dp1", include_witnesses = True)

elif test == 264:
	generate("Annulus1_np20r2L5drp5", "Annulus1", 20, rad = 2, layers = 5, delta_r = .5)
	
elif test == 265:
	f = points_to_persistence_diagram("Annulus1_np20r2L5drp5", old_parameter_set, ds_rate = 4, num_divisions = 10, landmark_selector = "EST", use_twr = True, title = "Annulus1_np20r2L5drp5")
	make_movie(f, "Annulus1_np20r2L5drp5", include_witnesses = True)
	
elif test == 266:
	f = points_to_persistence_diagram("Annulus1_np20r2L5drp5", old_parameter_set, ds_rate = 4, max_filtration_param = -30, num_divisions = 10, landmark_selector = "EST", use_twr = True, title = "Annulus1_np20r2L5drp5")
	make_movie(f, "Annulus1_np20r2L5drp5", include_witnesses = True)

elif test == 267:
	f = points_to_persistence_diagram("Annulus1_np20r2L5drp5", old_parameter_set, ds_rate = 4, max_filtration_param = -30, num_divisions = 10, landmark_selector = "EST", use_twr = True, title = "Annulus1_np20r2L5drp5")
	make_movie(f, "Annulus1_np20r2L5drp5", include_witnesses = True) # with substituted values to test against "not twr"
	
elif test == 268:
	f = points_to_persistence_diagram("Annulus1_np20r2L5drp5", old_parameter_set, ds_rate = 4, num_divisions = 10, landmark_selector = "EST", use_twr = True, title = "Annulus1_np20r2L5drp5")
	make_movie(f, "Annulus1_np20r2L5drp5", include_witnesses = True) # with substituted values to test against "not twr"

elif test == 269:
	f = points_to_persistence_diagram("Annulus1_np20r2L5drp5", old_parameter_set, ds_rate = 4, num_divisions = 10, landmark_selector = "EST", title = "Annulus1_np20r2L5drp5")
	make_movie(f, "Annulus1_np20r2L5drp5", include_witnesses = True) # with substituted values to test against "not twr"
	
elif test == 270:
	f = points_to_persistence_diagram("Annulus1_np20r2L5drp5", old_parameter_set, ds_rate = 4, num_divisions = 10, landmark_selector = "EST", use_twr = True, title = "Annulus1_np20r2L5drp5")
	make_movie(f, "Annulus1_np20r2L5drp5", include_witnesses = True) 
	
elif test == 272:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, max_filtration_param = .3, landmark_selection = "EST", use_twr = True)
elif test == 273:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, max_filtration_param = .3, landmark_selector = "EST", use_twr = True)
elif test == 274:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set,landmark_selector = "EST", use_twr = True)
elif test == 275:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, max_filtration_param = .1, landmark_selector = "EST", use_twr = True)

elif test == 276:
	f = points_to_persistence_diagram("Annulus1_np20r2L5drp5", old_parameter_set, ds_rate = 4, num_divisions = 10, m2_d = 1, time_order_landmarks = 'True', title = "Annulus1_np20r2L5drp5")
	make_movie(f, "Annulus1_np20r2L5drp5", include_witnesses = True)

elif test == 277:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, m2_d = 1, time_order_landmarks = True)
	

elif test == 278:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, m2_d = 1)

elif test == 279:
	f = points_to_persistence_diagram("L96N22F5_x1_m2tau10", old_parameter_set, use_twr = True, landmark_selector = "EST", title = "twr_L96N22F5_x1_m2tau10")
	make_movie(f, "twr_L96N22F5_x1_m2tau10", include_witnesses = True)	
elif test == 280:
	f = points_to_persistence_diagram("L96N22F5_x1_m2tau10", old_parameter_set, m2_d = 1, title = "m2d_L96N22F5_x1_m2tau10")
	make_movie(f, "m2d_L96N22F5_x1_m2tau10", include_witnesses = True)	
elif test == 281:
	f = points_to_persistence_diagram("L96N22F5_x1_m2tau10", old_parameter_set, landmark_selector = "EST", title = "EST_L96N22F5_x1_m2tau10")
	make_movie(f, "EST_L96N22F5_x1_m2tau10", include_witnesses = True)	
	
elif test == 282:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, straight_VB = 1)
	
elif test == 283:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, d_cov = 10)
	
elif test == 284:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 100, d_cov = 10)
	
elif test == 285:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 400, d_cov = 10)
	
elif test == 286:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 100, d_cov = 50)
	
elif test == 287:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 100, d_cov = 100)
	
elif test == 288:																				# !^@(*^#  MIGHT HAVE FIXED LANDMARK INDEXING 
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 400, d_cov = 10)
	
elif test == 289:																				# !^@(*^#  MIGHT HAVE FIXED LANDMARK INDEXING, trying neg cov 
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 400, d_cov = -10)
	
 	
elif test == 290:																				# !^@(*^#  MIGHT HAVE FIXED LANDMARK INDEXING, trying neg cov 
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 400)   

	
elif test == 291:																				# !^@(*^#  CHANGED BACK
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 200, d_cov = -20)
	
	
elif test == 292:																				# !^@(*^#  CHANGED BACK
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 200, d_cov = 0)
	
elif test == 293:																				# !^@(*^#  CHANGED BACK
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 400, d_cov = -50)
	
elif test == 294:																				# !^@(*^#  CHANGED BACK
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 400, d_cov = 50)
	
elif test == 295:																				# !^@(*^#  CHANGED BACK
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 200, d_cov = 50)

elif test == 296:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 400, d_cov = 40)
elif test == 297:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 400, d_cov = -40)
elif test == 298:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 400, d_cov = 100)
elif test == 299:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 400, d_cov = 200)
elif test == 300:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 400, d_cov = 400)
	
elif test == 301:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, m2_d = 1) 
	
elif test == 302:
	make_worm_movies("L96N22F5_x1_m2tau10.txt", 3, old_parameter_set, d_cov = 10) 
elif test == 303:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, d_cov = 10)
	
elif test == 304:																	# SUNDAY'S DEBUGING 
	make_worm_movies("btc2milIC123.txt", 3 ,old_parameter_set)					# ran, made first movie fine - so quit

elif test == 305:																	# SUNDAY'S DEBUGING 
	make_worm_movies("L96N22F5_x1_m2tau10.txt", 3 ,old_parameter_set)			# ran, made first movie fine - keeping on to next, curious
	
elif test == 306:																	# SUNDAY'S DEBUGING 
	make_worm_movies("btc2milIC123.txt", 3 ,old_parameter_set, use_twr = True)			# ran, got error in 'get_persistence_diagram' - didn't get any 1-dim homology, so didn't have file for it ;/
																						## after reviewing code, its written really for evenly spaced in time landmarks because we look the ds_rate ahead from a witness temporally and only one id number ahead for a landmark ; can probably re-write. 
																						### moving on to run next test
																						
elif test == 307:																	# SUNDAY'S DEBUGING 
	make_worm_movies("btc2milIC123.txt", 3 ,old_parameter_set, landmark_selector = 'EST', use_twr = True)  # ran, really slow - checking video, seems really sparse - letting run, then test increasing max_filtration paramater manually...seems not to play nicely if at all with current heuristic

elif test == 317:																	# SUNDAY'S DEBUGING 
	make_worm_movies("btc2milIC123.txt", 3 ,old_parameter_set, landmark_selector = 'EST', use_twr = True, max_filtration_param = .1) # ran, really slowly - still very sparse - seems to make sense and good justification for not using; MAKE TEST TEXT FILE CASE TO ENSURE WORKING CORRECTLY. 																	
	
elif test == 308:																	# SUNDAY'S DEBUGING 
	make_worm_movies("L96N22F5_x1_m2tau10.txt", 3 ,old_parameter_set, use_twr = True)  # ran, got same error for not having text file, moved on

elif test == 309:																	# SUNDAY'S DEBUGING 
	make_worm_movies("L96N22F5_x1_m2tau10.txt", 3 ,old_parameter_set, landmark_selector = 'EST', use_twr = True, max_filtration_param = 1) # ran, very sparse - re-running with extended max_filtration_parameter - bumped up to .5, still very sparse, bump to 1. need to save results. 
	
elif test == 310:																	# SUNDAY'S DEBUGING 
	make_worm_movies("btc2milIC123.txt", 3 ,old_parameter_set, m2_d = 1)				# runs, doesn't seem to make much of a difference in filtration or persistence diagram - TWEAK CODE TO MAKE SURE ITS CHANGING THINGS*

elif test == 311:																	# SUNDAY'S DEBUGING 
	make_worm_movies("L96N22F5_x1_m2tau10.txt", 3 ,old_parameter_set, m2_d = 1)				# runs, doesn't seem to make much of a difference in filtration - but perhaps a little more than L63 with full embedding dimension
	
elif test == 312:																	# SUNDAY'S DEBUGING 
	make_worm_movies("btc2milIC123.txt", 3 ,old_parameter_set, d_cov = 10)					# SAME plotting error
	
elif test == 313:																	# SUNDAY'S DEBUGING 
	make_worm_movies("L96N22F5_x1_m2tau10.txt", 3 ,old_parameter_set, d_cov = 10)			# SAME plotting error
	
elif test == 314:																	# SUNDAY'S DEBUGING 
	make_worm_movies("btc2milIC123.txt", 3 ,old_parameter_set, d_cov = -10)					# runs, does not seem very different from CONTROL.Euclidean, PROGRAM SOMETHING TO CHECK ACTUALLY AFFECTING DISTANCES AND FILTRATION!!*!&&!
	
elif test == 315:																	# SUNDAY'S DEBUGING 
	make_worm_movies("L96N22F5_x1_m2tau10.txt", 3 ,old_parameter_set, d_cov = -10)			# ran, error about complex variables /Users/nicolesanderson/Software/Python/JTFworms/PythonScripts77/BuildComplexNEW2MESSWITH1022.py:380: ComplexWarning: Casting complex values to real discards the imaginary part eigs[l,:] = eig_val 
																							 #runs, again check to see different from Euclidean
elif test == 316:																	# SUNDAY'S DEBUGING 
	make_worm_movies("btc2milIC123.txt", 3 ,old_parameter_set, straighten_vb = 1)			# runs, doesn't seem much different from Euclidean/CONTROL. MAKE SOMETHING TO CHECK! 

elif test == 318:																	# SUNDAY'S DEBUGING 
	make_worm_movies("L96N22F5_x1_m2tau10.txt", 3 ,old_parameter_set, straighten_vb = 1)	# runs, doesn't seem much different from CONTROL. CHECK

elif test == 319:
	make_worm_movies("L96N22F5_x1_m2tau10.txt", 3, old_parameter_set, landmark_selector = 'EST', d_cov = -10) # MONDAY'S DEBUGING 
																												# runs, need to run CONTROL;CHECK
	
elif test == 320:
	make_worm_movies("L96N22F5_x1_m2tau10.txt", 3, old_parameter_set, landmark_selector = 'EST', m2_d = 1) # MONDAY'S DEBUGING
																												# runs, need to run CONTROL;CHECK
elif test == 321:
	make_worm_movies("L96N22F5_x1_m2tau10.txt", 3, old_parameter_set, landmark_selector = 'EST') # MONDAY'S DEBUGING
																										#runs, THIS IS THE EST CONTROL! COMPARE TO OTHERS!
	
elif test == 322:
	make_worm_movies("L96N22F5_x1_m2tau10.txt", 3, old_parameter_set, landmark_selector = 'EST', straighten_vb = 1) # MONDAY'S DEBUGING
																													# runs, need to run CONTROL;CHECK
																													
elif test == 323:
	make_worm_movies("L96N22F5_x1_m2tau10.txt", 3, old_parameter_set, landmark_selector = 'EST', d_orientation_amplify = 9) # TUESDAY'S EXPERIMENT																																													
																															
elif test == 324:
	make_worm_movies("L96N22F5_x1_m2tau10.txt", 3, old_parameter_set, d_orientation_amplify = 9) # TUESDAY'S EXPERIMENT
																									
elif test == 325:
	make_worm_movies("L96N22F5_x1_m2tau10.txt", 3, old_parameter_set, ds_rate = 400, landmark_selector = 'EST', d_hamiltonian = -1) # TUESDAY'S EXPERIMENT																																													
																													
elif test == 326:
	make_worm_movies("L96N22F5_x1_m2tau10.txt", 3, old_parameter_set, d_hamiltonian = -1) # TUESDAY'S EXPERIMENT
																									#completed.
			# ... here ... 

elif test == 327:
	make_worm_movies("L96N22F5_x1_m2tau10.txt", 3, old_parameter_set, d_hamiltonian = -10) # WEDNESDAY'S EXPERIMENT
																									#different from nH = -1 but not too different, bumping up
elif test == 328:
	make_worm_movies("L96N22F5_x1_m2tau10.txt", 3, old_parameter_set, d_orientation_amplify = -18) # WEDNESDAY'S EXPERIMENT
																									# too different (seems like bad, at least, very different PD) than O9, lowering
elif test == 329:
	make_worm_movies("L96N22F5_x1_m2tau10.txt", 3, old_parameter_set, d_hamiltonian = -20) # WEDNESDAY'S EXPERIMENT

elif test == 330:
	make_worm_movies("L96N22F5_x1_m2tau10.txt", 3, old_parameter_set, d_orientation_amplify = -12) # WEDNESDAY'S EXPERIMENT	
	
elif test == 331:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, use_twr = 'True', landmark_selector = 'EST', max_filtration_param = 1)		

elif test == 332:																	# SUNDAY'S DEBUGING 
	make_worm_movies("btc2milIC123.txt", 3 ,old_parameter_set, ds_rate = 400, d_cov = 10)					# SAME plotting error	
	
elif test == 333:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 400, d_cov = -10)			# TUESDAY'S DEBUGGING 
																											# still graph issues
elif test == 334:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 400, d_cov = 10)			# TUESDAY'S DEBUGGING

elif test == 335:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 400)			# TUESDAY'S DEBUGGING	
	
elif test == 336:																		# WEDNESDAY'S STEVIE NICKS DEBUGGING 
	make_worm_movies("btc2milIC123.txt", 3 ,old_parameter_set, ds_rate = 400, d_cov = 10)	

elif test == 337:
	make_worm_movies("btc2milIC123.txt", 3, old_parameter_set, ds_rate = 400, d_cov = -10)

elif test == 338:																		# DONE DEBUGGING! 
	make_worm_movies("btc2milIC123.txt", 2 ,old_parameter_set, ds_rate = 50, d_cov = 50)	

elif test == 339:
	make_worm_movies("btc2milIC123.txt", 2, old_parameter_set, ds_rate = 50, d_cov = -50)
	
elif test == 340:
		make_worm_movies("btc2milIC123.txt", 2, old_parameter_set, ds_rate = 50, d_cov = 100)

elif test == 341:
		make_worm_movies("btc2milIC123.txt", 2, old_parameter_set, ds_rate = 50, d_cov = -100) # I think that there may be too many landmarks making the low density in the outside rings still not fixed
		
elif test == 342:
	for i in xrange(10):
		make_worm_movies("btc2milIC123.txt", 2, old_parameter_set, ds_rate = -50, d_cov = 20*i)

elif test == 343:
	for i in xrange(10):
		make_worm_movies("btc2milIC123.txt", 2, old_parameter_set, ds_rate = -50, d_cov = -20*i)
		
elif test == 344:
	for i in xrange(10):
		make_worm_movies("btc2milIC123.txt", 2, old_parameter_set, ds_rate = -100, d_cov = 20*i)

elif test == 345:
	for i in xrange(3):
		make_worm_movies("btc2milIC123.txt", 2, old_parameter_set, ds_rate = 100*i+100)	# RUNS SUCCESSFULLY!
		
elif test == 346:
	for i in xrange(3):
		make_worm_movies('L63_x_m2_tau%s.txt' % str(i+2), 2, old_parameter_set, ds_rate = 400)
		
elif test == 347:
	for i in xrange(3):
		make_worm_movies('L63_x_m2_tau%s.txt' % str(i+2), 2, old_parameter_set, worm_length = 2000, ds_rate = 50)

elif test == 348:
	for i in xrange(24):
		make_worm_movies('L63_x_m2_tau%s.txt' % str(i+2), 2, old_parameter_set, ds_rate = 400)
	
elif test == 349:
	for i in xrange(24):
		make_worm_movies('L63_x_m2_tau%s.txt' % str(i+2), 2, old_parameter_set, ds_rate = 200)
		
elif test == 350:
	for i in xrange(23):
		make_worm_movies('L63_x_m2_tau%s.txt' % str(i+2), 2, old_parameter_set, ds_rate = 100)

elif test == 351:
	for i in xrange(23):
		make_worm_movies('L63_x_m2_tau%s.txt' % str(i+2), 2, old_parameter_set, ds_rate = 100, d_orientation_amplify = 9)
		
elif test == 352:
	for i in xrange(23):
		make_worm_movies('L63_x_m2_tau%s.txt' % str(i+2), 2, old_parameter_set, ds_rate = 100, d_use_hamiltonian = -1)
		
elif test == 353:
	make_worm_movies('L63_x_m2_tau20.txt', 2, old_parameter_set, ds_rate = 50, d_use_hamiltonian = -10)

elif test == 354:
	for i in xrange(20):
		f = points_to_persistence_diagram("L63_x_m2_tau%s" % str(i+2), old_parameter_set, title = 'L63_x_m2_NH5_tau%s' % str(i+2), d_use_hamiltonian = -4)
		make_movie(f, "NHamiltonian4_tau%s" % str(i+2), include_witnesses = True)
	make_PD_movie('this is holder a.', 'L63_x_m2_NH5_tau')
		
elif test == 355:
	for i in xrange(20):
		f = points_to_persistence_diagram("L63_x_m2_tau%s" % str(i+2), old_parameter_set, title = 'L63_x_m2_O15_tau%s' % str(i+2), d_orientation_amplify = 15)
		make_movie(f, "L63_x_m2_O15_tau%s" % str(i+2), include_witnesses = True)
	make_PD_movie('this is holder a.', 'L63_x_m2_O15_tau')
	
elif test == 356:
	for i in xrange(20):
		f = points_to_persistence_diagram("L63_x_m2_tau%s" % str(i+2), old_parameter_set, title = 'L63_x_m2_tau%s' % str(i+2))
		make_movie(f, "L63_x_m2_tau%s" % str(i+2), include_witnesses = True)
	make_PD_movie('this is holder a.', 'L63_x_m2_tau')
	
elif test == 357:
	make_filtration_succession('this is holder b.', 'L63_x_m2_tau') # RUNS, BUT NOT SUCCESSFULLY CREATING SEQUENCE OF MOVIES
	
elif test == 358:
	for i in xrange(20):
		f = points_to_persistence_diagram("L63_x_m2_tau%s" % str(i+2), old_parameter_set, landmark_selector = 'EST', title = 'L63_x_m2_EST_tau%s' % str(i+2))
		make_movie(f, "L63_x_m2_EST_tau%s" % str(i+2), include_witnesses = True)
	make_PD_movie('this is holder a.', 'L63_x_m2_EST_tau')
	
elif test == 359:												# HAVEN'T FOUND APPROPRIATE MAX_FILT TO GET DECENT VIDEO
	for i in xrange(20):
		f = points_to_persistence_diagram("L63_x_m2_tau%s" % str(i+2), old_parameter_set, landmark_selector = 'EST', max_filtration_param = 10, use_twr = True, title = 'L63_x_m2_EST_twr_tau%s' % str(i+2))
		make_movie(f, "L63_x_m2_EST_twr_tau%s" % str(i+2), include_witnesses = True)
	make_PD_movie('this is holder a.', 'L63_x_m2_EST_twr_tau')
	
elif test == 360:
	for i in xrange(20):
		f = points_to_persistence_diagram("L63_x_m2_tau%s" % str(i+2), old_parameter_set, d_cov = 50, title = 'L63_x_m2_dCOV50_tau%s' % str(i+2))
		make_movie(f, "L63_x_m2_dCov50_tau%s" % str(i+1), include_witnesses = True)
	make_PD_movie('this is holder a.', 'L63_x_m2_dCov50_tau')
	
elif test == 361:
	f = points_to_persistence_diagram("two_lines", old_parameter_set, ds_rate = 5, landmark_selector = 'EST', max_filtration_param = -20)
	make_movie(f, "two_lines", include_witnesses = True)
	
elif test == 362:
	f = points_to_persistence_diagram("two_lines", old_parameter_set, ds_rate = 5, landmark_selector = 'EST', use_twr = True, max_filtration_param = -20)
	make_movie(f, "two_lines_twr", include_witnesses = True)
	
elif test == 363:
	f = points_to_persistence_diagram("two_lines_p", old_parameter_set, ds_rate = 5, landmark_selector = 'EST', use_twr = True, max_filtration_param = -20)
	make_movie(f, "two_lines_p_twr", include_witnesses = True)
	
elif test == 364:
	f = points_to_persistence_diagram("two_lines_p", old_parameter_set, ds_rate = 5, landmark_selector = 'EST', max_filtration_param = -20)
	make_movie(f, "two_lines_p", include_witnesses = True)
	
elif test == 365:
	f = points_to_persistence_diagram("two_lines", old_parameter_set, ds_rate = 5, landmark_selector = 'EST', d_cov = 10)
	make_movie(f, "two_lines_dCov", include_witnesses = True)
elif test == 666:
	make_worm_movies('L63_x_m2_tau20.txt', 2, old_parameter_set, worm_length=10,ds_rate = 2,max_filtration_parameter=1,landmark_selector="EST",max_filtration_param=-3) #runs to error in plotting
	
elif test == 667:
	make_worm_movies('Annulus1_np20r1L5dp1.txt', 2, old_parameter_set, worm_length=20,ds_rate = 2,max_filtration_parameter=1,landmark_selector="EST",max_filtration_param=-3) #runs to error in plotting

elif test == 668:
	make_worm_movies('L63_x_m2_tau20.txt', 2, old_parameter_set, worm_length=10,ds_rate = 2,max_filtration_parameter=1,landmark_selector="EST",max_filtration_param=-3,d_use_hamiltonian=-3)
	
	