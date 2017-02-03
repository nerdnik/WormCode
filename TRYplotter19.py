import os
import os.path
from os import system
import timeit	
	
def make_PD_movie(holder_a, abrev_title, format_type = 1, persistence_plot_dimension = 1, framerate = 1.0, view = None, **overrides):	
		print 'holder_a = %s' % holder_a
		segment_title_base = '%s' % abrev_title
		movie_title = '%s' % abrev_title
		system("ffmpeg -hide_banner -loglevel panic -y -framerate %f -start_number 2 -i \"%s%%d_persistence_diagram.png\" -r 30 \"%s_movie.mp4\"" % (framerate, segment_title_base, movie_title))

def make_filtration_succession(holder_b, abrev_title, format_type = 1, persistence_plot_dimension = 1, framerate = 1.0, view = None, **overrides):
	print 'holder_b = %s' % holder_b
	segment_title_base = '%s' % abrev_title
	movie_title = '%s: Filtration Succession' % abrev_title
	system("ffmpeg -hide_banner -loglevel panic -y -framerate %f -start_number 2 -i \"%s%%d_movie.mp4\" -r 30 \"%s_movie.mp4\"" % (framerate, segment_title_base, movie_title))