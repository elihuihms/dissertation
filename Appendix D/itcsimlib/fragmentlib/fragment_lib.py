from scipy				import optimize,exp,finfo,float32

from ..itc_sim			import ITCSim
from ..itc_calc			import ITCCalc
from fragment_functions	import frag_count,return_unique,count,frag_xcount_dict

class ITCSimFragment(ITCSim):
	# make a custom class overwriting the setup_model method
	def setup_model(self,num_parameters,fragments,modelname='',nsites=11,exclusive=False):
		self.model=modelname
		for i in xrange(len(self.workers)):
			self.workers[i] = fragmentModel( self.in_Queue, self.out_Queue )
			self.workers[i].setup([num_parameters,fragments,nsites,exclusive])
			self.workers[i].start()
		return

#def get_combinations( max_fragment_size, num_parameters, rm_empty=True ):
#	fragments,fragment_combinations = [],[]
#
#	for i in xrange(1,max_fragment_size+1):
#		fragments.extend( return_unique( [chunk(list(c),i) for c in _configs] )[0] )
#
#	# remove empty site only fragments ?
#	if rm_empty:
#		for i in xrange(1,max_fragment_size+1):
#			index = fragments.index('0'*i)
#			del fragments[index]
#
#	def choose_iter(elements, length):
#		for i in xrange(len(elements)):
#			if length == 1:
#				yield (elements[i],)
#			else:
#				for next in choose_iter(elements[i+1:len(elements)], length-1):
#					yield (elements[i],) + next
#
#	# make sure all combinations have "1" ?
#	fragment_combinations = []
#	for c in list(choose_iter(fragments, num_parameters)):
#		if count(c,'1') > 0:
#			fragment_combinations.append( c )
#
#	return fragment_combinations

def make_configs( size ):
	ret = ['']*(2**size)
	s = "{0:0>%s}"%(size)
	for i in xrange(2**size):
		ret[i] = s.format("{0:b}".format(i))
	return ret

def get_fragment_combinations( min_fragment_size, max_fragment_size, num_parameters ):
	assert min_fragment_size == 1 or min_fragment_size % 2 == 1
	assert max_fragment_size == 1 or max_fragment_size % 2 == 1

	tmp = []
	for i in xrange(min_fragment_size/2,max_fragment_size/2+1):
		tmp.extend( return_unique( make_configs( i*2+1), linear=True )[0] )

	fragments = []
	for f in tmp:
		if list(f)[ len(f)/2 ] == '1':
			fragments.append( f )

	def choose_iter(elements, length):
		for i in xrange(len(elements)):
			if length == 1:
				yield (elements[i],)
			else:
				for next in choose_iter(elements[i+1:len(elements)], length-1):
					yield (elements[i],) + next

	fragment_combinations = []
	for c in list(choose_iter(fragments, num_parameters)):
		fragment_combinations.append( c )

	return fragment_combinations

class fragmentModel(ITCCalc):
	def setup(self,args):
		self.lib = fragmentModelLib()
		self.lib.setup(*args)

class fragmentModelLib:

	def close(self):
		return

	def setup(self,num_parameters,fragments,nsites=11,exclusive=False):
		self.num_parameters = num_parameters
		self.fragments = fragments
		self.exclusive = exclusive
		self._configs = make_configs(nsites)
		print "Current fragments: %s" % (str(self.fragments))
		if self.exclusive:
			print "Using exclusive fragment bookeeping"

		self.dG		= [0.0]*len(self._configs)
		self.dH		= [0.0]*len(self._configs)
		self.probs	= [0.0]*len(self._configs)
		self.bound	= [0]*len(self._configs)
		return

	def _set_energies(self, params, cutoff=-1E5):
		for i in xrange(2048):
			self.dG[i],self.dH[i] = 0.0,0.0
			self.bound[i] = count(self._configs[i],'1')

			if self.exclusive:
				for f,n in frag_xcount_dict( self._configs[i], self.fragments ).iteritems():
					j = self.fragments.index(f)
					self.dG[i] += params[j] * n
					self.dH[i] += params[self.num_parameters +j] * n

			else:
				for j in xrange(self.num_parameters):
					n = frag_count(self._configs[i], self.fragments[j])
					self.dG[i] += params[j] * n
					self.dH[i] += params[self.num_parameters +j] * n

#		print self.dG[1]
#		print self.dG[2047]

	def _set_probs(self, L_free, T):
		R = 8.3144621 # J/(K*mol)
		P_sum = 0
		for i in xrange(2048):
			self.probs[i] = exp( (-1 * self.dG[i]) / ( R * T ) ) * pow(L_free, self.bound[i])
			P_sum += self.probs[i]

		for i in xrange(2048):
			self.probs[i] /= P_sum

	def _getFree(self, P_tot, L_tot, T):
		assert L_tot > 0

		def _func(L_free):
			self._set_probs(L_free,T)
			total_bound = 0.0
			for i in xrange(2048):
				total_bound += self.probs[i] * self.bound[i] * P_tot
			return L_tot - (total_bound + L_free)

		# free ligand concentration is somewhere between zero and the total ligand conc
		return optimize.brentq( _func, finfo(float32).tiny, L_tot )

	def _getQ(self):
		ret = 0.0
		for i in xrange(2048):
			ret += self.probs[i] * self.dH[i]
		return ret

	def calc(self,n,M_conc,L_conc,Q_fit,params,T):
		self._set_energies( params._arr )
		for i in xrange(n):
			self._set_probs( self._getFree( M_conc._arr[i], L_conc._arr[i], T.value ), T.value )
			Q_fit._arr[i] = self._getQ()

		return 0











