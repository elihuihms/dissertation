import os
import shutil
import tempfile
import Tkinter as tk
import tkMessageBox
import tkFileDialog

from datetime import datetime

from .. exceptions				import *
from .. component_generation	import *
from .. plugin_functions		import *
from win_options				import *
from win_status					import *
from tools_plugin				import *

def makeComponentsFromWindow( w ):
	paths = w.componentPDBsList.get(0,tk.END)

	names = {}
	for p in paths:
		n = os.path.splitext(os.path.basename(p))[0]
		names[n] = [n]

	dirs = []
	type_counters = {}
	template = """# autogenerated by mesmer-gui
# %s

NAME	$0

""" % (datetime.now())
	for i in range(w.rowCounter):
		dirs.append( w.widgetRowFolders[i].get() )
		type	= w.widgetRowTypes[i].get()
		if(type in type_counters):
			type_counters[type]+=1
		else:
			type_counters[type]=0

		template+="%s%i\n%%%i\n\n" % (type,type_counters[type],i+1)

	try:
		data_files = match_data_files( names, dirs )
	except ComponentGenException as e:
		tkMessageBox.showerror("Error",e.msg,parent=w)
		return False

	tmp = tkFileDialog.asksaveasfilename(title='Save components folder:',parent=w,initialfile='components')
	if(tmp == ''):
		return False
	if(os.path.exists(tmp)):
		shutil.rmtree(tmp)

	try:
		os.mkdir(tmp)
	except OSError:
		tkMessageBox.showerror("Error","ERROR: Couldn't create component folder.",parent=w)
		return False

	try:
		write_component_files( names, data_files, template, tmp )
	except ComponentGenException as e:
		tkMessageBox.showerror("Error",e.msg,parent=w)
		return False

	tkMessageBox.showinfo("Success","%i component files were successfully written" % (len(names.keys())))
	return True

def pluginCalculator( w, plugin, pdbs, dir ):
	try:
		counter = plugin.calculator()
	except Exception as e:
		tkMessageBox.showerror("Error","Plugin \"%s\" reported an error.\n\n%s" % (plugin.name,e) )
		return

	if( counter < len(pdbs) ):
		w.CalcProgress.set("Progress: %i/%i" % (counter+1,len(pdbs)) )
		w.CurrentPDB.set( os.path.basename( pdbs[counter] ) )
		w.AfterID = w.after( plugin.respawn, pluginCalculator, *(w,plugin,pdbs,dir) )
	else:
		plugin.close()
		w.master.destroy()

def calcDataFromWindow( w, pdbs, pluginName ):

	# find the plugin matching the provided name
	plugin = None
	for p in w.calc_plugins:
		if( p.name == pluginName ):
			plugin = p
	if(plugin == None):
		return

	if( plugin.parser ): # get options for the plugin
		options = convertParserToOptions( plugin.parser )
		w.newWindow = tk.Toplevel(w.master)
		w.optWindow = OptionsWindow(w.newWindow,options)
		w.newWindow.transient(w)
		w.newWindow.focus_set()
		w.newWindow.grab_set()
		w.newWindow.wait_window()
		if w.optWindow.returncode > 0: # did user cancel the options window?
			return
	else:
		options = None

	dir = tkFileDialog.asksaveasfilename(title='Folder to save calculated data to:',parent=w, initialfile="%s_data" % (plugin.type) )
	if(dir == ''):
		return
	if(os.path.exists(dir)):
		shutil.rmtree(dir)
	try:
		os.mkdir(dir)
	except:
		tkMessageBox.showerror("Error","Could not create folder \"%s\"" % dir)
		return

	try:
		plugin.setup( pdbs, dir, options, w.prefs['cpu_count'] )
	except Exception as e:
		tkMessageBox.showerror("Error","Plugin reported a problem: %s" % (e))
		return

	# update the parent window row
	for i in range(w.rowCounter):
		if( w.widgetRowTypes[i].get() == plugin.type and w.widgetRowFolders[i].get() == '' ):
			w.widgetRowFolders[i].set( dir )
			break

	# open the status window
	w.newWindow = tk.Toplevel(w.master)
	w.statWindow = StatusWindow(w.newWindow,plugin.cancel,plugin.name)
	w.newWindow.focus_set()
	w.newWindow.grab_set()

	# set the timed callback function
	w.optWindow.AfterID = w.after( plugin.respawn, pluginCalculator, *(w.statWindow,plugin,pdbs,dir) )

	return w.newWindow



