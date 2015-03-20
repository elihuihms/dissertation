from numpy 				import linspace,logspace

class ITCGrid:

	def __init__(self, sim, fit):
		self.sim = sim
		self.fit = fit

	def grid_dG_fit_dH(self, dG_bounds, dH_bounds=None, dH_scale=None, printer=None, startindex=0, endindex=None, verbose=False):
		"""
		Optimizes dH from a grid of dG values
		"""
		count = dG_bounds[0][2]
		for i in xrange(1,len(dG_bounds)):
			count *= dG_bounds[i][2]

		if endindex != None and endindex <= count:
			count = endindex

		if verbose:
			print "FITTING dH PARAMETERS OVER %i dG GRID POINTS" % (count-startindex)

		for b in dG_bounds:
			if len(b) != 4:
				print "dG bounds must be a  list of (dG_low, dG_high, steps, logspace)"
				return

		self._make_grid( dG_bounds )

		# save old sim.dG for restoration later
		sim_dG = self.sim.dG

		dH_fits = []
		for i in xrange( startindex, count ):
			self.sim.dG = self._get_point( i )

			tmp = self.fit.fit_dH(self.sim,dH_bounds,dH_scale,verbose)
			dH_fits.append( (self.sim.dG, tmp) )

			if printer != None:
				printer( (self.sim.dG, tmp) )

		# restore original sim.dG
		self.sim.dG = sim_dG

		return dH_fits

	def _make_grid( self, bounds ):
		"""
		build a list of the values to test for each parameter
		"""

		self._grid_pts = []
		for (low,high,steps,logstep) in bounds:
			if logstep:
				self._grid_pts.append( logspace(low,high,steps) )
			else:
				self._grid_pts.append( linspace(low,high,steps) )

		return self._grid_pts

	def _get_point( self, index ):
		"""
		Given a multidimensional grid of points, provides a unique combination for a given iteration
		"""
		gridpt = []
		for i in range(len(self._grid_pts)):
			gridpt.append( self._grid_pts[i][ index % len(self._grid_pts[i]) ] )
			index /= len(self._grid_pts[i])

		return gridpt