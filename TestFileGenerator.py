import math
import numpy as np

def rect(r, theta):
	x = r*math.cos(theta)
	y = r*math.sin(theta)
	return x,y

def generate(file_name, shape, number_of_points, **parameters):
	def get_param(key):
		result = parameters.get(key)
		if result is None:
			raise Exception("Must supply argument: '%s'" % key)
		return result
	def frange(start, stop, num_values):
		for i in xrange(num_values):
			yield float(stop - start)*float(i)/float(num_values) + float(start)
			
	f = open(file_name, "w")
	f.truncate()
	if shape == "Ellipse":
		rad_x = get_param("rad_x")
		rad_y = get_param("rad_y")
		for t in frange(0.0, 2.0*math.pi, number_of_points):
			f.write("%f %f\n" % (rad_x*math.cos(t), rad_y*math.sin(t)))
			
	elif shape == "Circle":
		rad = get_param("rad")
		for t in np.linspace(0, 2*np.pi, number_of_points):
			f.write("%f %f\n" % (rad*np.cos(t),rad*np.sin(t)))
			
	elif shape == "VarCircle":
		theta = [.01]
		while theta[-1] < 2*np.pi:
			next_theta = [theta[-1] + (np.sin(theta[-1]))**float(2)]
			theta = theta + next_theta
		for t in theta:
			f.write("%f %f\n" % (np.cos(t), np.sin(t)))
		
	elif shape == "Figure8":
		theta = np.linspace(0,2*np.pi, number_of_points)
		for t in theta:
			f.write("%f %f\n" % (np.cos(t), np.cos(t)*np.sin(t)))
	
	elif shape == "Annulus1":
		rad = get_param("rad")
		layers = get_param("layers")
		delta_r = get_param("delta_r")
		r = rad
		for i in range(1,layers+1):
			t = np.linspace(0, 2*np.pi, number_of_points + np.floor(2*np.pi*delta_r*(i-1)))
			for j in xrange(len(t)):
				f.write("%f %f\n" % (r*np.cos(t[j]),r*np.sin(t[j])))
			r = r + delta_r
			
	elif shape == "Annulus2":
		rad = get_param("rad")
		layers = get_param("layers")
		delta_r = get_param("delta_r")
		r = rad
		t = np.linspace(0, 2*np.pi, number_of_points)
		for i in range(1,layers+1):
			for j in xrange(len(t)):
				f.write("%f %f\n" % (r*np.cos(t[j]),r*np.sin(t[j])))
			r = r + delta_r
	
	elif shape == "Annulus3":
		rad = get_param("rad")
		layers = get_param("layers")
		delta_r = get_param("delta_r")
		r = rad
		for t in np.linspace(0, 2*np.pi, number_of_points):
			for i in range(1,layers+1):
				f.write("%f %f\n" % (r*np.cos(t),r*np.sin(t)))
				r = r + delta_r
			r = rad
	
	elif shape == "Superformula":
		a = parameters.get("a")
		b = parameters.get("b")
		if a is None:
			a = 1.0
		if b is None:
			b = 1.0
		m = float(get_param("m"))
		n1 = float(get_param("n1"))
		n2 = float(get_param("n2"))
		n3 = float(get_param("n3"))
		for theta in frange(0, math.pi*2, number_of_points):
			r = math.pow(math.pow(math.fabs(math.cos(m*theta/4.0)/a), n2) + math.pow(math.fabs(math.sin(m*theta/4.0)/b), n3), -1.0/n1)
			f.write("%f %f\n" % rect(r, theta))
	
	else:
		raise Exception("Not a valid shape name.")
	f.close()
	
	#Example of how to run: generate("Ellipse2000.txt", "Ellipse", 2000, rad_x = 10, rad_y = 5)
	