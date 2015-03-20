from ctypes				import cdll,c_double
from multiprocessing	import Process
from scipy				import dtype,zeros

from thermo				import dQ_calc

class ITCCalc(Process):
	def __init__(self,in_queue,out_queue):
		super(ITCCalc, self).__init__()
		self.iQ = in_queue
		self.oQ = out_queue
		self.daemon = True

	def setup(self,path,args):
		self.lib = cdll.LoadLibrary(path)
		self.lib.setup(*args)

	def run(self):
		for (params,experiment) in iter(self.iQ.get, None):
			n = len(experiment.dQ_exp)
			Q_fit = zeros(n,dtype('d'))

			self.lib.calc(
				n,
				experiment.M_conc.ctypes,
				experiment.L_conc.ctypes,
				Q_fit.ctypes,
				params.ctypes,
				c_double( experiment.T )
			)

			# normalize total heat content to macromolecule concentration in the cell volume
			for i in xrange(n):
				Q_fit[i] *= experiment.V0 * experiment.M_conc[i]

			# obtain the change in cell heat b/t each titration point
			dQ_fit = dQ_calc(Q_fit, experiment.V0, experiment.I_vol)

			for i in xrange(n):
				# incorrect normalization factor (to CHANGE in titration concentration) Ian used in his thesis:
				#if i==0:
				#	dQ_fit[i] /= experiment.V0*(experiment.L_conc[i] - 0.0)
				#else:
				#	dQ_fit[i] /= experiment.V0*(experiment.L_conc[i] - experiment.L_conc[i-1])

				# normalize by injected amount of material per this titration point
				# remove heat of ligand or macromolecule dilution
				if experiment.reverse:
					dQ_fit[i] /= experiment.M0 * experiment.I_vol[i]

					if i==0:
						dQ_fit[i] -= experiment.V0*(experiment.M_conc[i])*experiment.dil_Q
					else:
						dQ_fit[i] -= experiment.V0*(experiment.M_conc[i]-experiment.M_conc[i-1])*experiment.dil_Q
				else:
					dQ_fit[i] /= experiment.L0 * experiment.I_vol[i]

					if i==0:
						dQ_fit[i] -= experiment.V0*(experiment.L_conc[i])*experiment.dil_Q
					else:
						dQ_fit[i] -= experiment.V0*(experiment.L_conc[i]-experiment.L_conc[i-1])*experiment.dil_Q

			self.oQ.put( (experiment.title,dQ_fit) )

		self.lib.close()
		return