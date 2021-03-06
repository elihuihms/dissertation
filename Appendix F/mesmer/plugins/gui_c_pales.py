import os
import argparse
import shutil

from subprocess				import Popen,PIPE

from lib.gui.plugin_objects import guiCalcPlugin
from lib.gui.tools_plugin	import makeStringFromOptions

class plugin(guiCalcPlugin):

	def __init__(self):
		self.name = 'RDC - PALES'
		self.version = '2014.09.09'
		self.type = 'RDC'
		self.respawn = 100

		self.parser = argparse.ArgumentParser(prog=self.name)
		self.parser.add_argument('-media',		choices=['Bicelles','Phage'] ,	default='Bicelles', help='Model of alignment media: Bicelles (Wall) or Phage (Rod)')
		self.parser.add_argument('-wv',			type=float,						default=0.05,		help='Liguid Crystal Concentration [mg/mL]')
		self.parser.add_argument('-dot',		type=int,						default=100,		help='Orientation Density (Sphere)')
		self.parser.add_argument('-digPsi',		type=int,						default=18,			help='Orientation Density (3rd angle)')
		self.parser.add_argument('-dGrid',		type=float,						default=0.2,		help='Grid Spacing [A]')
		self.parser.add_argument('-rM',			type=float,						default=20,			help='Half Model Thickness [A]')
		self.parser.add_
		#self.parser.add_argument('-lm',		default='',	help='Maximum order of harmonics (default 15)')
		#self.parser.add_argument('-fb',		default='',	help='Order of fibonacci grid(default 17)')
		self.parser.add_argument('-sm',		type=float,	default=0.5,	help='Maximum scattering vector')
		self.parser.add_argument('-ns',		type=int,	default=128,	help='# points in the computed curve')
		self.parser.add_argument('-dns',	type=float,	default=0.334,	help='Solvent density (default 0.334 e/A**3)')
		self.parser.add_argument('-dro',	type=float,	default=0.03,	help='Contrast of hydration shell (default 0.03 e/A**3)')
		self.parser.add_argument('-eh',		action='store_true', 		help='Account for explicit hydrogens')

	def setup(self, pdbs, dir, options, threads):
		self.pdbs	= pdbs
		self.dir	= dir
		self.options	= options
		self.threads	= threads
		self.counter	= 0
		self.state	= 0 # not busy
		self.currentPDB = ''

	def calculator(self):
		if(self.state >= self.threads):	#semaphore to check if we're still busy processing
			return
		self.state +=1

		pdb = os.path.abspath( self.pdbs[self.counter] )
		base = os.path.basename(pdb)
		name = os.path.splitext( os.path.basename(pdb) )[0]

		if not os.path.exists(pdb):
			raise Exception( "Could not find \"%s\"" % (pdb) )

		cmd = ['pales']
		cmd.extend( makeStringFromOptions(self.options).split() )
		cmd.append( pdb )

		try:
			pipe = Popen(cmd, cwd=self.dir, stdout=PIPE)
			pipe.wait()
		except OSError as e:
			if(e.errno == os.errno.ENOENT):
				raise Exception("Could not find \"pales\" executable. Perhaps it isn't installed?")
			else:
				raise e

		tmp = "%s%s%s00.int" % (self.dir,os.sep,name)
		if not os.path.exists(tmp):
			raise Exception( "Failed to calculate SAXS profile for \"%s\". CRYSOL output: %s" % (pdb,pipe.stdout.read()) )

		try:
			lines = open( tmp ).readlines()[1:-1]
			f = open( "%s%s%s.dat" % (self.dir,os.sep,name), 'w' )
			for l in lines:
				f.write( "%s\n" % ("\t".join( l.split()[0:2] ) ) )
			f.close()
		except:
			raise Exception( "Could not clean up CRYSOL profile \"%s\"" % (tmp) )

		os.remove("%s%s%s00.log" % (self.dir,os.sep,name) )
		os.remove("%s%s%s00.alm" % (self.dir,os.sep,name) )
		os.remove("%s%s%s00.int" % (self.dir,os.sep,name) )

		self.state -=1
		self.counter +=1
		return self.counter
