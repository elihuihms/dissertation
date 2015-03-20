from scipy				import optimize,dtype,zeros,array
from ctypes				import c_double

from itc_sim			import ITCSim
from itc_calc			import ITCCalc
from thermo				import dQ_calc

class ITCCalcOpt(ITCCalc):

	def __init__(self, *args, **kwargs):
		# call parent constructor first
		super(ITCCalcOpt,self).__init__(*args, **kwargs)

		# hardcoded values for now
		self.M_bounds = (0.5,2)
		self.dH_bounds = (0.5,2)
		self.dQ_bounds = (-1,1)
		self.ftol = 1E+2
		self.xtol = 1E-3

	def run(self):
		for (params,experiment) in iter(self.iQ.get, None):

			DOF,M_i,dH_i,dQ_i = 0,0,0,0
			if experiment.optM:
				DOF+=1
			if experiment.optdH:
				dH_i += DOF
				DOF+=1
			if experiment.optdQ:
				dQ_i += DOF
				DOF+=1

			n = len(experiment.dQ_exp)
			def _target( x, x0=None, full_output=False ):
				Q_fit = zeros(n,dtype('d'))

				y, bound_violation = [1,1,0], False
				if experiment.optM:
					if DOF == 1:
						y[0] = x
					elif DOF > 1:
						y[0] = x[M_i]
					if y[0] < self.M_bounds[0] or y[0] > self.M_bounds[1]:
						bound_violation = True
						y[0] = 1

				if experiment.optdH:
					if DOF == 1:
						y[1] = x
					elif DOF > 1:
						y[1] = x[ dH_i ]
					if y[1] < self.dH_bounds[0] or y[1] > self.dH_bounds[1]:
						bound_violation = True
						y[1] = 1

				if experiment.optdQ:
					if DOF == 1:
						y[2] = x
					elif DOF > 1:
						y[2] = x[ dQ_i]
					if y[2] < self.dQ_bounds[0] or y[2] > self.dQ_bounds[1]:
						bound_violation = True
						y[2] = 0

				if x0 != None:
					y = x0

				# apply the correction factor to the macromolecule concentration
				M_conc = array([f * y[0] for f in experiment.M_conc],dtype('d'))

				# calculate the uncorrected dQ in the cell
				self.lib.calc(
					n,
					M_conc.ctypes,
					experiment.L_conc.ctypes,
					Q_fit.ctypes,
					params.ctypes,
					c_double( experiment.T )
				)

				# calculate total heat content in cell at each point
				for i in xrange(n):
					Q_fit[i] *= experiment.M_conc[i] * experiment.V0

				# obtain the change in heat b/t each titration point
				dQ_fit = dQ_calc(Q_fit, experiment.V0, experiment.I_vol)

				# calculate heat of dilution as a fraction of the last titration point heat
				dil_Q = y[2] * experiment.V0*(experiment.L_conc[-1]-experiment.L_conc[-2])

				for i in xrange(n):
					# normalize by injected amount of material per this titration point
					if experiment.reverse:
						dQ_fit[i] /= experiment.M0 * experiment.I_vol[i]
					else:
						dQ_fit[i] /= experiment.L0 * experiment.I_vol[i]

					# remove heat of ligand dilution
					# does this need to tied to experiment direction?
					if i==0:
						dQ_fit[i] -= experiment.V0*(experiment.L_conc[i])*experiment.dil_Q
					else:
						dQ_fit[i] -= experiment.V0*(experiment.L_conc[i]-experiment.L_conc[i-1])*experiment.dil_Q

				# does this need to tied to experiment direction?
				avg = sum(dQ_fit) / sum(experiment.L_conc)

				if experiment.optdQ:
					for i in xrange(n):
						if i==0:
							dQ_fit[i] -= experiment.V0*(experiment.L_conc[i])*(avg * y[2])
						else:
							dQ_fit[i] -= experiment.V0*(experiment.L_conc[i]-experiment.L_conc[i-1])*(avg * y[2])

				# apply the dQ scaling factor
				dQ_fit = [f * y[1] for f in dQ_fit]

				# obtain the chisquare agreement to the experimental data
				chisq = experiment.sse( dQ_fit )
				#print "%s %f " % (str(y),chisq)

				# if we have a boundary violation, upscale a non-violating chisq and return that
				if bound_violation:
					chisq *= 2

				# restore the original macromolecule concentration
				if experiment.optM:
					experiment.M_conc /= y[1]

				if full_output:
					return chisq, dQ_fit, avg
				else:
					return chisq

			opt = [1,1,0]
			if DOF == 1:
				if experiment.optM:
					x1,x2 = self.M_bounds[0],self.M_bounds[1]
				elif experiment.optdH:
					x1,x2 = self.dH_bounds[0],self.dH_bounds[1]
				elif experiment.optdQ:
					x1,x2 = self.dQ_bounds[0],self.dQ_bounds[1]

				tmp, chisq, ierr, numfunc = optimize.fminbound( _target, x1=x1, x2=x2, xtol=self.xtol, full_output=True )

				if experiment.optM:
					opt[0] = tmp
				if experiment.optdH:
					opt[1] = tmp
				if experiment.optdQ:
					opt[2] = tmp

			elif DOF > 1:
				x0 = [1] * DOF
				if experiment.optdQ:
					x0[ dQ_i ] = 0

				tmp, sse, a, b, c =  optimize.fmin( _target, x0=x0, full_output=True, disp=False, ftol=self.ftol, xtol=self.xtol)

				if experiment.optM: # unmux the optimized parameters
					opt[0] = tmp[M_i]
				if experiment.optdH:
					opt[1] = tmp[dH_i]
				if experiment.optdQ:
					opt[2] = tmp[dQ_i]

			# calculate dQ with these optimize parameters
			chisq,dQ_fit,avg = _target(opt,x0=opt,full_output=True)

			# restore dil_Q to proper scale
			opt[2] *= avg

			# hacky: check for special "opt_calc" flag on experiment
			try:
				if experiment.opt_calc:
					self.oQ.put( (experiment.title,dQ_fit,opt[0],opt[1],opt[2]) )
			except:
				self.oQ.put( (experiment.title,dQ_fit) )

		self.lib.close()
		return

class ITCSimOpt(ITCSim):
	def setup_model(self,args):
		self.model = args[0]
		for i in xrange(len(self.workers)):
			self.workers[i] = ITCCalcOpt( self.in_Queue, self.out_Queue )
			self.workers[i].setup(*args)
			self.workers[i].start()

	def update_fits( self ):
		if self.verbose:
			print "OPTIMIZING PER-EXPERIMENT VARIABLES"

		# hacky: set special "opt_calc" flag for experiment to return optimized parameters
		for E in self.get_experiments():
			E.opt_calc = True

		self._submit_to_queue( None )
		queue_contents = self._retrieve_from_queue()

		if self.verbose:
			print "OPTIMIZATION OF PER-EXPERIMENT VARIABLES CONCLUDED:"
			print "NAME	M	dH	dQ"

		for (title,dQ,Mx,dHx,dil_Q) in queue_contents:
			E = self.get_experiment_by_title(title)
			E.dQ_fit = dQ
			E.opt_values = (Mx,dHx,dil_Q) # hacky!
			E.opt_calc = False

			if self.verbose:
				print "%s	%f	%f	%f" % (E.title, Mx, dHx, dil_Q)

		return

	def get_opt_values( self, E ):
		try:
			return E.opt_values
		except:
			print "ERROR: Optimized per-experiment variables not available. Run update_fits()"

