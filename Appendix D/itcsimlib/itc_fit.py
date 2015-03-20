import sys

from scipy 	import array,dtype,optimize

class ITCFit:

#	def __init__(self,method='',maxfun=None,xtol=0.0001,ftol=0.0001,epsilon=None,step=None,scale=None,dGbounds=None,dHbounds=None,temp=None):
	def __init__(self, sim, **kwargs):
		self.sim	= sim
		self.nparams	= len(self.sim.dG)
		self.bounds = [(None,None)]*(self.nparams*3+2)
		self.method	= ''
		self.maxfun	= 1E3
		self.xtol	= 0.0001
		self.ftol	= 0.0001
		self.scale	= None
		self.epsilon	= None
		self.step	= None
		self.verbose	= False
		for key, value in kwargs.iteritems():
			setattr( self, key, value )
		assert self.method in ('','powell','basinhopping','tnc','bfgs')
		self.chisq	= 0.0

	def set_bounds(self, dG=None, dH=None, dCp=None, M=None, Q=None):
		if dG != None:
			assert len(dG[0]) == 2
			assert len(dG) == self.nparams
			for i in xrange(self.nparams):
				self.bounds[(0*self.nparams)+i] = dG[i]
		if dH != None:
			assert len(dH[0]) == 2
			assert len(dH) == self.nparams
			for i in xrange(self.nparams):
				self.bounds[(1*self.nparams)+i] = dH[i]
		if dCp != None:
			assert len(dCp[0]) == 2
			assert len(dCp) == self.nparams
			for i in xrange(self.nparams):
				self.bounds[(2*self.nparams)+i] = dCp[i]
		if M != None:
			self.bounds[-2] = M
		if Q != None:
			self.bounds[-1] = Q
		return self.bounds

	def fit(self, func, params, callback=None ):
		"""
		Use a user-defined fitting function
		"""
		if self.verbose:
			print "FITTING USER-DEFINED PARAMETERS USING \"%s\" MODEL" % (self.sim.model)

		ret = _fitter( func, params, (self.sim,), self, callback )

		if self.verbose:
			print "FITTING of USER-DEFINED PARAMETERS FINISHED:"
			for (i,f) in enumerate(ret[0]):
				print "  P_%i : %.5E" % (i,f)

		return( ret[0], ret[1] )

	def fit_dH(self):
		"""
		Find optimal dH values for all experimental datasets
		"""
		if self.verbose:
			print "FITTING dH PARAMETERS USING \"%s\" MODEL" % (self.sim.model)
			def _printer(x):
				sys.stdout.write("dH: ")
				for f in x:
					sys.stdout.write("%.5E " % f)
				sys.stdout.write("(%f)\n"%self.chisq);
				sys.stdout.flush()
		else:
			def _printer(x):
				return

		for i in xrange(self.sim.size):
			if self.sim.get_experiment(i).T != self.sim.get_experiment(0).T:
				print "ERROR:   Cannot fit experiments at more than one temperature without dCp"
				return
			if self.sim.get_experiment(i).T != self.sim.T_ref :
				print "WARNING: Experimental data is at different temperature (%.2fK) than T_ref (%.2fK)!" % (self.sim.get_experiment(0).T,self.sim.T_ref)

		ret = _fitter( _fit_H, self.sim.dH, (self.sim,), self, callback=_printer )

		if self.verbose:
			print "FITTING of dH FINISHED:"
			for (i,f) in enumerate(ret[0]):
				print "  dH(%.2f)_%i : %.5E" % (self.sim.T_ref,i,f)

		return (list(ret[0]),ret[1])

	def fit_dCp(self):
		if self.verbose:
			print "FITTING dCp PARAMETERS USING \"%s\" MODEL" % (self.sim.model)
			def _printer(x):
				sys.stdout.write("dCp: ")
				for f in x:
					sys.stdout.write("%.5E " % f)
				sys.stdout.write("(%f)\n"%self.chisq);
				sys.stdout.flush()
		else:
			def _printer(x):
				return

		ret = _fitter( _fit_dCp, self.sim.dCp, (self.sim,), self, callback=_printer )

		if self.verbose:
			print "FITTING OF dCp FINISHED:"
			for (i,f) in enumerate(ret[0]):
				print "  dCp_%i : %.5E" % (i,f)

		return (list(ret[0]),ret[1])

	def fit_dGdH(self):
		"""
		Find optimal dG and dH values for all experimental datasets
		"""

		if self.verbose:
			print "FITTING dG AND dH PARAMETERS USING \"%s\" MODEL:" % (self.sim.model)

			def _printer(x):
				sys.stdout.write("dG: ")
				for f in x[0:len(x)/2]:
					sys.stdout.write("%.5E " % f)
				sys.stdout.write("dH: ")
				for f in x[len(x)/2:]:
					sys.stdout.write("%.5E " % f)
				sys.stdout.write("(%f)\n"%self.chisq)
				sys.stdout.flush()
		else:
			def _printer(x):
				return

		for i in xrange(self.sim.size):
			if self.sim.get_experiment(i).T != self.sim.get_experiment(0).T:
				print "ERROR:   Cannot fit experiments at more than one temperature without dCp"
				return
			if self.sim.get_experiment(i).T != self.sim.T_ref :
				print "WARNING: Experimental data is at different temperature (%.2fK) than T_ref (%.2fK)!" % (self.sim.get_experiment(0).T,self.sim.T_ref)

		ret = _fitter( _fit_GH, list(self.sim.dG)+list(self.sim.dH), (self.sim,), self, callback=_printer )

		if self.verbose:
			print "FITTING OF dG and dH FINISHED:"
			for (i,f) in enumerate(ret[0][:len(self.sim.dG)]):
				print "  dG(%.2f)_%i : %.5E" % (self.sim.T_ref,i,f)
			for (i,f) in enumerate(ret[0][len(self.sim.dG):]):
				print "  dH(%.2f)_%i : %.5E" % (self.sim.T_ref,i,f)

		return (list(ret[0][:len(self.sim.dG)]), list(ret[0][len(self.sim.dG):]), ret[1])

	def fit_dGdHMQ(self):
		"""
		Find optimal dG and dH values for all experimental datasets
		"""

		if self.verbose:
			print "FITTING dG, dH, MACROMOLECULE CONCENTRATION, and HEAT OF DILUTION PARAMETERS USING \"%s\" MODEL:" % (self.sim.model)

			def _printer(x):
				sys.stdout.write("dG: ")
				for f in x[0:(len(x)-2)/2]:
					sys.stdout.write("%.5E " % f)
				sys.stdout.write("dH: ")
				for f in x[(len(x)-2)/2:len(x)-2]:
					sys.stdout.write("%.5E " % f)
				sys.stdout.write("M: %f%% " % (x[-2]*100.0) )
				sys.stdout.write("Q: %.5E " % (x[-1]) )
				sys.stdout.write("(%f)\n"%self.chisq)
				sys.stdout.flush()
		else:
			def _printer(x):
				return

		for i in xrange(self.sim.size):
			if self.sim.get_experiment(i).T != self.sim.get_experiment(0).T:
				print "ERROR:   Cannot fit experiments at more than one temperature without dCp"
				return
			if self.sim.get_experiment(i).T != self.sim.T_ref :
				print "WARNING: Experimental data is at different temperature (%.2fK) than T_ref (%.2fK)!" % (self.sim.get_experiment(0).T,self.sim.T_ref)

		ret = _fitter( _fit_GHMQ, list(self.sim.dG)+list(self.sim.dH)+[1.0,self.sim.get_experiment(0).dil_Q], (self.sim,), self, callback=_printer )

		if self.verbose:
			print "FITTING dG, dH, M AND Q FINISHED:"
			for (i,f) in enumerate(ret[0][0:len(self.sim.dG)]):
				print "  dG(%.2f)_%i : %.5E" % (self.sim.T_ref,i,f)
			for (i,f) in enumerate(ret[0][len(self.sim.dG):]):
				print "  dH(%.2f)_%i : %.5E" % (self.sim.T_ref,i,f)
			print "	M: %f%%" % (ret[0][-2])
			print "	Q: %.5E" % (ret[0][-1])

		return (list(ret[0][:len(self.sim.dG)]), list(ret[0][len(self.sim.dG):2*len(self.sim.dG)]), ret[0][-2], ret[0][-1], ret[1])

	def fit_dGdHdCp(self):
		"""
		Find optimal dG, dH, and dCp values for all experimental datasets
		"""

		if self.verbose:
			print "FITTING dG, dH, and dCp PARAMETERS USING \"%s\" MODEL:" % (self.sim.model)

			def _printer(x):
				sys.stdout.write("dG*: ")
				for f in x[0:len(x)/3]:
					sys.stdout.write("%.5E " % f)
				sys.stdout.write(" dH*: ")
				for f in x[len(x)/3:2*len(x)/3]:
					sys.stdout.write("%.5E " % f)
				sys.stdout.write(" dCp: ")
				for f in x[2*len(x)/3:]:
					sys.stdout.write("%.5E " % f)
				sys.stdout.write("(%f)\n"%self.chisq)
				sys.stdout.flush()
		else:
			def _printer(x):
				return

		ret = _fitter( _fit_GHC, list(self.sim.dG)+list(self.sim.dH)+list(self.sim.dCp), (self.sim,), self, callback=_printer )

		if self.verbose:
			print "FITTING OF dG, dH, AND dCp FINISHED:"
			for (i,f) in enumerate(ret[0][:len(self.sim.dG)]):
				print "  dG(%.2f)_%i : %.5E" % (self.sim.T_ref,i,f)
			for (i,f) in enumerate(ret[0][len(self.sim.dG):2*len(self.sim.dG)]):
				print "  dH(%.2f)_%i : %.5E" % (self.sim.T_ref,i,f)
			for (i,f) in enumerate(ret[0][2*len(self.sim.dG):]):
				print "  dCp_%i : %.5E" % (i,f)

		return (list(ret[0][:len(self.sim.dG)]), list(ret[0][len(self.sim.dG):2*len(self.sim.dG)]), list(ret[0][2*len(self.sim.dG):]), ret[1])

def _fitter(func, x0, args, fit, callback=None ):
	if fit.method == '':
		ret = optimize.fmin(
			func=func,
			x0=x0,
			args=(fit,)+args,
			xtol=fit.xtol,
			ftol=fit.ftol,
			disp=fit.verbose,
			maxfun=fit.maxfun,
			full_output=True,
			callback=callback,
		)
	elif fit.method == 'basinhopping':
		kwargs = {'method':'Powell','args':(fit,)+args}
		opt = optimize.basinhopping(
			func=func,
			x0=x0,
			minimizer_kwargs=kwargs,
			T=fit.temp,
			stepsize=fit.step,
			disp=fit.verbose
		)
		ret = opt.x,opt.fun
	elif fit.method == 'powell':
		ret = optimize.fmin_powell(
			func=func,
			x0=x0,
			args=(fit,)+args,
			xtol=fit.xtol,
			ftol=fit.ftol,
			disp=fit.verbose,
			maxfun=fit.maxfun,
			full_output=True,
			callback=callback,
		)
	elif fit.method == 'tnc':
		opt = optimize.fmin_tnc(
			func=func,
			x0=x0,
			args=(fit,)+args,
			approx_grad=True,
			maxfun=int(fit.maxfun),
			xtol=fit.xtol,
			ftol=fit.ftol,
			disp=fit.verbose)[0]
		ret = opt,func(x0,*args)
	elif fit.method == 'bfgs':
		ret = optimize.fmin_l_bfgs_b(
			func=func,
			x0=x0,
			args=(fit,)+args,
			approx_grad=True,
			maxfun=fit.maxfun,
			disp=fit.verbose)
	else:
		raise Exception('Unrecognized fitting algorithm')

	return ret

def _boundviolation(params,fit,dG=False,dH=False,dCp=False,M=False,Q=False):
	"""
	This is a really stupid function
	"""
	offset = 0
	if dG:
		for i in xrange(fit.nparams):
			if (fit.bounds[(fit.nparams*0)+i][0] != None and params[offset+i] < fit.bounds[(fit.nparams*0)+i][0]) or (fit.bounds[(fit.nparams*0)+i][1] != None and params[offset+i] > fit.bounds[(fit.nparams*0)+i][1]):
				if fit.verbose: print "dG bound violation"
				return True
		offset+=fit.nparams
	if dH:
		for i in xrange(fit.nparams):
			if (fit.bounds[(fit.nparams*1)+i][0] != None and params[offset+i] < fit.bounds[(fit.nparams*1)+i][0]) or (fit.bounds[(fit.nparams*1)+i][1] != None and params[offset+i] > fit.bounds[(fit.nparams*1)+i][1]):
				if fit.verbose: print "dH bound violation"
				return True
		offset+=fit.nparams
	if dCp:
		for i in xrange(fit.nparams):
			if (fit.bounds[(fit.nparams*2)+i][0] != None and params[offset+i] < fit.bounds[(fit.nparams*2)+i][0]) or (fit.bounds[(fit.nparams*2)+i][1] != None and params[offset+i] > fit.bounds[(fit.nparams*2)+i][1]):
				if fit.verbose: print "dCp bound violation"
				return True
		offset+=fit.nparams
	if M:
		if (fit.bounds[-2][0] != None and params[offset] < fit.bounds[-2][0]) or (fit.bounds[-2][1] != None and params[offset] > fit.bounds[-2][1]):
			if fit.verbose: print "M bound violation"
			return True
		offset+=1
	if Q:
		if (fit.bounds[-1][0] != None and params[offset] < fit.bounds[-1][0]) or (fit.bounds[-1][1] != None and params[offset] > fit.bounds[-1][1]):
			if fit.verbose: print "Q bound violation"
			return True
		offset+=1
	return False

def _fit_H(dH,fit,sim):
	if _boundviolation(dH,fit,dH=True):
		fit.chisq = sim.chisq()*2.0
	else:
		fit.chisq = sim.chisq( list(sim.dG) + list(dH) )
	return fit.chisq

def _fit_dCp(dCp,fit,sim):
	if _boundviolation(dCp,fit,dCp=True):
		fit.chisq = sim.chisq()*2.0
	else:
		# keep a copy of the old simulation parameters
		old_dCp	= sim.dCp[:]

		# update sim with specified test parameters
		sim.dCp = dCp

		# calculate the agreement with the new parameters
		# calling sim.chisq() w/o specified parameters will automatically calculate dG,dH for each experiment from sim's reference dG,dH,dCp
		fit.chisq = sim.chisq()

		# restore old params
		sim.dCp	= old_dCp
	return fit.chisq

def _fit_GH(dGdH,fit,sim):
	#print "\t".join(map(str,dGdH)),
	if _boundviolation(dGdH,fit,dG=True,dH=True):
		fit.chisq = sim.chisq()*2.0
	else:
		fit.chisq = sim.chisq( dGdH )
	#print fit.chisq
	return fit.chisq

def _fit_GHM(dGdHM,fit,sim):
	if _boundviolation(dGdHM,fit,dG=True,dH=True,M=True):
		fit.chisq = sim.chisq()*2.0
	else:
		# keep copy of original macromolecule concentration
		old_M = []
		for e in sim.get_experiments():
			old_M.append( e.M_conc[:] )

			# update macromolecule concentration
			e.M_conc	= array([ e.M_conc[i]*dGdHdMdQ[-2] for i in xrange(len(e.M_conc)) ],dtype('d'))

		fit.chisq = sim.chisq( dGdHM[:-1] )

		# reset original macromolecule concentration
		for e in sim.get_experiments():
			e.M_conc = old_M.pop(0)

	return fit.chisq

def _fit_GHQ(dGdHdQ,fit,sim):
	if _boundviolation(dGdHdQ,fit,dG=True,dH=True,Q=True):
		fit.chisq = sim.chisq()*2.0
	else:
		# keep copy of original heat of dilution
		old_Q = []
		for e in sim.get_experiments():
			old_Q.append( e.dil_Q )

			# update heat of dilution
			e.dil_Q = dGdHdQ[-1]

		fit.chisq = sim.chisq( dGdHdQ[:-1] )

		# reset original heat of dilution
		for e in sim.get_experiments():
			e.dil_Q = old_Q.pop(0)

	return fit.chisq

def _fit_GHMQ(dGdHdMdQ,fit,sim):
	if _boundviolation(dGdHdMdQ,fit,dG=True,dH=True,M=True,Q=True):
		fit.chisq = sim.chisq()*2.0
	else:
		# keep copy of original macromolecule concentration
		old_M, old_Q = [], []
		for e in sim.get_experiments():
			old_M.append( e.M_conc[:] )
			old_Q.append( e.dil_Q )

			# update macromolecule concentration
			e.M_conc	= array([ e.M_conc[i]*dGdHdMdQ[-2] for i in xrange(len(e.M_conc)) ],dtype('d'))
			e.dil_Q		= dGdHdMdQ[-1]

		fit.chisq = sim.chisq( dGdHdMdQ[:-2] )

		# reset original macromolecule concentration
		for e in sim.get_experiments():
			e.M_conc	= old_M.pop(0)
			e.dil_Q		= old_Q.pop(0)

	return fit.chisq

def _fit_GHC(dGdHdCp,fit,sim):
	#print " ".join(map(str,dGdHdCp)),
	if _boundviolation(dGdHdCp,fit,dG=True,dH=True,dCp=True):
		fit.chisq = sim.chisq()*2.0
	else:
		# keep a copy of the old simulation parameters
		old_dG	= sim.dG[:]
		old_dH	= sim.dH[:]
		old_dCp	= sim.dCp[:]

		# update sim with specified test parameters
		n = len(sim.dG)
		sim.dG	= dGdHdCp[:n]
		sim.dH	= dGdHdCp[n:2*n]
		sim.dCp = dGdHdCp[2*n:]

		# calculate the agreement with the new parameters
		# calling sim.chisq() w/o specified parameters will automatically calculate dG,dH for each experiment from sim's reference dG,dH,dCp
		fit.chisq = sim.chisq()

		# restore old params
		sim.dG	= old_dG
		sim.dH	= old_dH
		sim.dCp	= old_dCp

	return fit.chisq
