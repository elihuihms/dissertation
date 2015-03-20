import os
try:
	#import matplotlib
	#matplotlib.use('Agg')
	import matplotlib.pyplot as pyplot
except:
	pyplot = None

from ctypes				import cdll,c_double
from math				import fabs
from multiprocessing	import cpu_count,Queue
from scipy				import array,dtype,zeros,genfromtxt

from itc_calc			import ITCCalc
from thermo				import *

class ITCExperiment:
	"""
	Encapsulates all the necessary data for a specific ITC experiment
	"""

	def __init__(
		self,
		title,
		T,
		V0,
		M0,
		L0,
		dQ_exp,
		I_vol,
		M_conc,
		L_conc,
		reverse,
		skip=[],
		ddQ_exp=[],
		dil_Q=0.0):

		self.npoints = len(dQ_exp)
		assert( self.npoints == len(I_vol) )
		assert( self.npoints == len(M_conc) )
		assert( self.npoints == len(L_conc) )

		self.title	= title
		self.T		= T
		self.V0		= V0
		self.P0		= M0
		self.L0		= L0
		self.I_vol	= I_vol
		self.M_conc	= M_conc
		self.L_conc	= L_conc
		self.reverse= reverse
		self.skip	= skip
		self.dil_Q	= dil_Q

		# convert raw data (in calories) to joules per mol of injectant
		if self.reverse:
			self.dQ_exp	= [J_from_cal(dQ_exp[i]/(self.I_vol[i]*self.M0)) for i in xrange(self.npoints)]
		else:
			self.dQ_exp	= [J_from_cal(dQ_exp[i]/(self.I_vol[i]*self.L0)) for i in xrange(self.npoints)]
		self.ddQ_exp	= map(J_from_cal,ddQ_exp)
		self.dQ_fit = []

		# if no ddQ data, use normalized RMSD goodness of fit instead
		if self.ddQ_exp == []:
			self.use_nrmsd = True
			self.spread = max(self.dQ_exp) - min(self.dQ_exp)
		else:
			self.use_nrmsd = False

	def set_params(self, **kwargs):
		for key, value in kwargs.iteritems():
			setattr( self, key, value )

	def show_plot(self,hardcopy=False,hardcopydir='.',hardcopyprefix='', hardcopytype='png'):
		"""
		Generate a plot of the experimental data, and a fit if available
		"""

		if pyplot == None: return
		if hardcopy: fig = pyplot.figure()

		pyplot.clf()
		pyplot.title(self.title)
		pyplot.ylabel("Joule/mol of injectant")

		if self.reverse:
			ratios = get_ratios(self.M_conc,self.L_conc)
			pyplot.xlabel("Molar Ratio (M/L)")
		else:
			ratios = get_ratios(self.L_conc,self.M_conc)
			pyplot.xlabel("Molar Ratio (L/M)")
		pyplot.scatter(ratios,self.dQ_exp,c='#DDDDDD')

		if len(self.dQ_fit) > 1:
			tmpx = [ ratios[i] for i in xrange(self.npoints) if i not in self.skip ]
			tmpy = [ self.dQ_fit[i] for i in xrange(self.npoints) if i not in self.skip ]
			pyplot.plot(tmpx,tmpy,c='r')

		if len(self.skip) > 0:
			tmpx = [ ratios[i] for i in self.skip ]
			tmpy = [ self.dQ_exp[i] for i in self.skip ]
			pyplot.scatter(tmpx,tmpy,c='g')

		pyplot.draw()
		if hardcopy:
			fig.savefig( os.path.join(hardcopydir,"%s%s.%s"%(hardcopyprefix,self.title,hardcopytype)), bbox_inches='tight')
			pyplot.close(fig)
		else:
			pyplot.show()

	def chisq(self, dQ_fit, writeback=False):
		if writeback:
			self.dQ_fit = dQ_fit[:]

		n,sum = len(dQ_fit), 0.0
		if self.use_nrmsd:
			for i in xrange(n):
				if i not in self.skip:
					sum += (self.dQ_exp[i] - dQ_fit[i])**2
			return sqrt( sum / (n -len(self.skip)) ) / self.spread
		else:
			for i in xrange(n):
				if i not in self.skip:
					sum += (self.dQ_exp[i] - dQ_fit[i])**2 / self.ddQ_exp[i]**2
			return sum / (n -len(self.skip))

class ITCSim:
	"""
	Contains all the necessary data and methods to collect experiments
	"""

	def __init__(self,T_ref=298.15,verbose=False,threads=None):
		self.T_ref	= T_ref # reference temperature
		self.dG		= []
		self.dH		= []
		self.dCp	= []
		self.size	= 0 # number of experiments
		self.experiments = []
		self.model	= None
		self.verbose = verbose

		self.in_Queue,self.out_Queue = Queue(),Queue()

		if threads==None or threads<1:
			threads = cpu_count()
		self.workers = [None] * threads

	def __del__(self):
		self.close()

	def setup_model(self,args):
		self.model = args[0]
		for i in xrange(len(self.workers)):
			self.workers[i] = ITCCalc( self.in_Queue, self.out_Queue )
			self.workers[i].setup(*args)
			self.workers[i].start()

	def close(self):
		# send term signal to workers
		for i in xrange(len(self.workers)):
			self.in_Queue.put( None )
		# make sure they're all shut down
		for i in xrange(len(self.workers)):
			if self.workers[i] != None:
				self.workers[i].join()
			self.workers[i] = None

	def get_experiment(self, index=0):
		return self.experiments[index]

	def get_experiments(self):
		return self.experiments

	def get_experiment_by_title(self, title):
		for E in self.experiments:
			if E.title==title:
				return E
		return None

	def get_experiments_by_temperature(self, temperature):
		ret = []
		for E in self.experiments:
			if E.T == temperature:
				ret.append(E)
		return ret

	def set_params(self, dG=None, dH=None, dCp=None ):
		"""
		Set the various initial parameters for the specified model
		"""

		if len(self.dG) > 0 and dG != None:
			assert( len(self.dG) == len(dG) )
		if len(self.dG) > 0 and dH != None:
			assert( len(self.dG) == len(dH) )
		if len(self.dG) > 0 and dCp != None:
			assert( len(self.dG) == len(dCp) )

		# note, dG & dH values are always at ref temp!
		if dG != None:
			self.dG		=	dG
		if dH != None:
			self.dH		=	dH
		if dCp != None:
			self.dCp	=	dCp

		return

	def add_experiment( self, title, T, V0, M0, L0, DQ, I_vol, reverse=False, skip=[], dil_Q=0.0 ):
		"""
		Add ITC data, along with the necessary experimental and instrument parameters necessary to generate fits
		Calculates the active concentration of protein and ligand at each point
		"""

		for E in self.experiments:
			if E.title == title:
				print "Experiment \"%s\" already present in this simulation" % (title)

		cM,cL = [0.0]*len(DQ),[0.0]*len(DQ)

		if reverse:
			cL[0] = L0
		else:
			cM[0] = M0

		for i in range(0,len(DQ)):
			dV = sum(I_vol[0:i])
			if reverse:
				#DQ[i] /= (I_vol[i]*M0) # normalize DQ per mol of injectant
				cL[i]	= L0 * ( (1-(dV/(2*V0))) / (1+(dV/(2*V0))) )
				cM_r	= (M0*dV/V0) * (1/(1+(dV/(2*V0)))) # concentration of macromolecule from previous injections
				cM[i]	= (M0*I_vol[i]/V0) + cM_r
			else:
				#DQ[i] /= (I_vol[i]*L0)
				cM[i]	= M0 * ( (1-(dV/(2*V0))) / (1+(dV/(2*V0))) )
				cL_r	= (L0*dV/V0) * (1/(1+(dV/(2*V0)))) # concentration of ligand from previous injections
				cL[i]	= (L0*I_vol[i]/V0) + cL_r

				# Ian's calculation of current ligand concentration. As footnoted in his thesis, this is INCORRECT!
				"""
				# % Concentration of injectant in cell assuming RID
				if i>0:
					cL_r = ( cL[i-1] * (V0-I_vol[i]) + (L0*I_vol[i]) ) / V0;
				else:
					cL_r = ( 0.00000 * (V0-I_vol[i]) + (L0*I_vol[i]) ) / V0;
				# % This value is reduced due to some displacement of injected material
				cL[i]	= cL_r*(1-I_vol[i]/2.0/V0)
				"""

		self.experiments.append(
			ITCExperiment(
				title	= title,
				T		= T,
				V0		= V0,
				M0		= M0,
				L0		= L0,
				dQ_exp	= array(DQ,dtype('d')),
				I_vol	= array(I_vol,dtype('d')),
				M_conc	= array(cM,dtype('d')),
				L_conc	= array(cL,dtype('d')),
				reverse	= reverse,
				skip	= skip,
				dil_Q	= dil_Q
			)
		)

		self.size +=1
		return

	def load_file( self, path, T, V0, M0, L0, reverse=False, skip=[], dil_Q=0.0, title=None):
		"""
		Read experimental ITC data from a file containing two columns: the observed deltaH and the injection volumes
		"""

		(DQ,I_vol) = genfromtxt( path, unpack=True, usecols=(0,1) )
		if title==None:
			title = os.path.splitext(os.path.basename(path))[0]
		self.add_experiment( title, T, V0, M0, L0, DQ, I_vol, reverse, skip, dil_Q)

	def make_plots(self,indices=None,hardcopy=False,hardcopydir='.',hardcopyprefix='',hardcopytype='png'):
		"""
		Generate plots for all experimental datasets
		"""
		for (i,E) in enumerate(self.experiments):
			if(indices==None) or (i in indices):
				E.show_plot(hardcopy,hardcopydir,hardcopyprefix,hardcopytype)

	def _submit_to_queue( self, params=None ):

		n = len(self.dG)
		for E in self.get_experiments():

			p = [0.0]*(n*2)
			if params==None: # use the current parameters in the sim
				for i in xrange(n):
					p[i]		= dG_vant_Hoff( self.dG[i], self.dH[i], self.dCp[i], E.T, self.T_ref )
					p[i+n]		= dH_vant_Hoff( self.dH[i], self.dCp[i], E.T, self.T_ref )
			else:
				assert( len(params) == len(self.dG)*2 )
				for i in xrange(n):
					p[i]		= dG_vant_Hoff( params[i], params[i+n], self.dCp[i], E.T, self.T_ref )
					p[i+n]		= dH_vant_Hoff( params[i+n], self.dCp[i], E.T, self.T_ref )

			# put the parameters for the experiment in the queue to calculate dQ
			self.in_Queue.put( (array(p,dtype('d')),E) )

		return

	def _retrieve_from_queue( self ):
		ret = []
		while len(ret) < self.size:
			ret.append( self.out_Queue.get(True) )

		return ret

	def update_fits( self ):
		"""
		Using the current model parameters, generate fits for all experimental datasets
		"""

		self._submit_to_queue( None )
		queue_contents = self._retrieve_from_queue()

		for (title,dQ) in queue_contents:
			E = self.get_experiment_by_title(title)
			E.dQ_fit = dQ

		return

	def chisq(self, params=None):
		"""
		Calculates either sum-squared of error between the experimental data for the simulation, either from the existing parameters or from a provided set of parameters
		"""

		self._submit_to_queue( params )
		queue_contents = self._retrieve_from_queue()

		ret = 0
		# match experiments and calculate discrepancy
		for (title,dQ) in queue_contents:
			E = self.get_experiment_by_title(title)
			ret += E.chisq(dQ,writeback=False)

		return ret


