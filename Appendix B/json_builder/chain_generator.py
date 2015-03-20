from random import *

typePrimitive = []

def showInfo():
	print "chain_generator v. 0.006 - generates connectivity topologies for a specified system of (at the moment), two binders."
	return

def defineType(name,numSites,bindsTo,symmetric,maxCount):
	""" Convenience function that create a binding particle type """
		
	typePrimitive.append([name,numSites,bindsTo,symmetric,maxCount])
	return
	
def getTypes():
	""" Retrieves the primitive binding types specified by defineType() and formats them into an associative array that the binding model will utilize """
	
	translationTable = []
	for x in typePrimitive:
		translationTable.extend(x[0])
	
	id = 0
	types = []
	max = 0
	for x in typePrimitive:
		
		binds = []
		for y in x[2]:
			binds.append(translationTable.index(y))
		
		if (x[4] != False) and (x[4] > max):
			max = x[4]
			
		
		types.append({'name':x[0],'nSites':x[1],'binds':binds,'sym':x[3],'id':id,'max':x[4]})
		id+=1
	
	return (max,types)

def makeBinaryChains():
	""" Given two types of binding partners, generates a library of potential chain conformations """
	
	# retrieve the binding partner specifications
	(maxsize,types) = getTypes()
	
	# Do some basic argument checking for this model
	if (len(types) < 2):
		print "Number of defined types must equal two for binary chain calculations."
		return
	if (maxsize == 0):
		print "Must specify a valid maximum number for one or more components."
		return

	allChains = []
	newChainsA = [[]]
	newChainsB = []
	
	typeA = types[0]
	typeB = types[1]
	
	# start the chain with a single type A component
	addComponent(newChainsA[0],typeA,0,0)

	depth = 0
	for n in range(maxsize):
		depth+=1
		
		# go through all the chains created last iteration and append B components
		newChainsB = []
		for thisChain in newChainsA:

			# get a list of new available sites in the provided chain
			# by setting depth -1, we will only add to components added last round
			openSites = makeSiteList(thisChain,typeB,depth-1)
			
			# make all the descendants from the current chain and append them to the pool
			if (n == 0) and (typeA['sym']): #if the starting binder is symmetric, no need to start chains at all its sites
				newChainsB = newChainsB + fillSites(openSites,thisChain,typeB,-1)
			else:
				newChainsB = newChainsB + fillSites(openSites,thisChain,typeB,depth)
		
		print('n:'+str(n)+', '+str(len(newChainsB))+ ' chains created at depth '+str(depth))
		
		allChains = allChains + newChainsB
		
		depth+=1
		
		# add an additional component to all the previously modified chains
		newChainsA = []
		for thisChain in newChainsB:

			openSites = makeSiteList(thisChain,typeA,depth-1)
			newChainsA = newChainsA + fillSites(openSites,thisChain,typeA,depth)
			
		print('n:'+str(n)+', '+str(len(newChainsA))+ ' chains created at depth '+str(depth))
		
		allChains = allChains + newChainsA

	return allChains
	
def makeRandomChains( nChains=1 ):
	""" Makes a specified number of chains with random connectivities """
	
	# retrieve the binding partner specifications
	(maxsize,types) = getTypes()
		
	# array to hold finished, random chains
	allChains = []
	
	full = False	
	while( not full ):
		# array to hold the currently constructed chain
		newChain = []
		
		# start the chain with a connected TRAP+AT
		addComponent(newChain,types[0],0,0)
		addComponent(newChain,types[1],1,1)
		connectComponents(newChain,0,randint(0,types[0]['nSites']-1),1,randint(0,types[1]['nSites']-1))

		nTRAPs = 1
		nATs = 1
	
		while( (nTRAPs < types[0]['max']) or (nATs < types[1]['max']) ):
			
			index = nTRAPs + nATs
			
			if( (random() < 0.5) and (nTRAPs < types[0]['max']) ):
				list = makeSiteList(newChain,types[0],0)
				if(len(list) > 0):
					site = choice(list)
					addComponent(newChain,types[0],index,index)
					connectComponents(newChain,site[0],site[1],index,randint(0,types[0]['nSites']-1))
					nTRAPs += 1
			elif(nATs < types[1]['max']):
				list = makeSiteList(newChain,types[1],0)
				if(len(list) > 0):
					site = choice(list)
					addComponent(newChain,types[1],index,index)
					connectComponents(newChain,site[0],site[1],index,randint(0,types[1]['nSites']-1))
					nATs += 1
							
		allChains.append( Copy(newChain) )
		
		if( len(allChains) == nChains ):
			return allChains
	pass
pass	
	
def fillSites(sites,chain,type,depth):
	""" Creates a family of chains from a starting chain with available sites occupied by a specified binder type. (subject to the maximum number of allowed binders, naturally) """
	
	# count up the number of each component in the chain
	typecount = [0,0,0,0,0,0,0]
	for x in chain:
		typecount[x['type']] += 1
		
		# if we've exceeded the max value for any item, bail
		if( typecount[type['id']] >= type['max']) and (type['max'] != False):
			return []
			
	# the list that will contain all of the chains created from the provided chain
	daughterChains = []

	# pass on to the daughter chains a sitelist without the sites we're currently filling
	daughterSites = Copy(sites)

	# if depth is -1, this is a special flag that we are at the first binder, and we don't need to start chains at all of its sites
	if (depth == -1):
		sites = [[0,0]] #first site on the first binder
		depth = 1

	for coord in sites:
		# we are in the process of filling the coords, don't let the daughter process also fill them
		daughterSites.remove(coord)
		
		# if all sites on the new component are symmetrical, we only need to add it once
		if (type['sym']):
			max = 1
		else:
			max = type['nSites']
		
		# connect each new component at each of the possible sites of the new component
		for i in range(max):
			# make a copy of the existing chain
			newChain = Copy(chain)

			# create a new component in the new chain
			newComponent = addComponent(newChain,type,depth,i)
			
			# add it to the currently specified binding site
			connectComponents(newChain,coord[0],coord[1],len(newChain) -1,i)

			daughterChains.append(newChain)
			
			# now, starting with the newly-created chain, fill *those* sites
			daughterChains = daughterChains + fillSites(daughterSites,newChain,type,depth+1)
		
	return daughterChains

def makeSiteList(chain,type,depth):
	""" Generates a list of sites available to the specified binder type on the provided chain """

	# make a list of the available sites open to bind a given binderType
	sites = []
		
	for i in range(len(chain)):
		if (chain[i]['depth'] >= depth):
			if (chain[i]['type'] in type['binds']):
				for j in range(len(chain[i]['sites'])):
					if (chain[i]['sites'][j] == None):
						sites.append( [i,j] )
	
	return sites		
	
def addComponent(chain,type,depth,id):
	""" Appends a component of specified type to the chain array. """

	component = {'depth':depth,'type':type['id'],'name':type['name']+'.'+str(depth)+'.'+str(id),'sites':[]}
	for i in range(type['nSites']):
		component['sites'].append(None)
	chain.append(component)

	return

def connectComponents(chain,index1,site1,index2,site2):
	""" Tells two specified components in a given chain that they are bound to each other """
	
	chain[index1]['sites'][site1] = (index2*100)+site2
	chain[index2]['sites'][site2] = (index1*100)+site1
	
	return

def mkDotPlot(chains):

	nodelist1 = []
	nodelist2 = []
	edgelist = []
	
	s = ''
	i = 0
	for x in chains:
		for y in x:
		
			if (y['type'] == 0):
				nodelist1.append('T_'+str(i)+y['name'].replace('T.',''))
				
				for z in y['sites']:
					if(z != None):
						index = z/100
						locat = z%100
						edgelist.append('T_'+str(i)+y['name'].replace('T.','')+'--A_'+str(i)+x[index]['name'].replace('A.',''))

				
			else:
				nodelist2.append('A_'+str(i)+y['name'].replace('A.',''))
		i+=1
				
	nodelist1 = ' '.join(nodelist1)
	nodelist2 = ' '.join(nodelist2)
	edgelist = ";\n".join(edgelist)
	
	nodelist1 ="\t {node [width=1,height=1,shape=pentagon,style=filled,color=blue,fixedsize=true]"+nodelist1+"}\n"
	nodelist2 ="\t {node [width=0.5,height=0.5,shape=triangle,style=filled,color=red,fixedsize=true]"+nodelist2+"}\n"		
	s = "graph A {\n"
	s+= "layout=fdp;\n"
	s+= nodelist1
	s+= nodelist2
	s+= "edge [len=0.1];\n"
	s+= edgelist
	s+="}"
	
	return s


dignore = {str: None, unicode: None, int: None, type(None): None}

def Copy(obj):
    t = type(obj)

    if t in (list, tuple):
        if t == tuple:
            # Convert to a list if a tuple to 
            # allow assigning to when copying
            is_tuple = True
            obj = list(obj)
        else: 
            # Otherwise just do a quick slice copy
            obj = obj[:]
            is_tuple = False

        # Copy each item recursively
        for x in xrange(len(obj)):
            if type(obj[x]) in dignore:
                continue
            obj[x] = Copy(obj[x])

        if is_tuple: 
            # Convert back into a tuple again
            obj = tuple(obj)

    elif t == dict: 
        # Use the fast shallow dict copy() method and copy any 
        # values which aren't immutable (like lists, dicts etc)
        obj = obj.copy()
        for k in obj:
            if type(obj[k]) in dignore:
                continue
            obj[k] = Copy(obj[k])

    elif t in dignore: 
        # Numeric or string/unicode? 
        # It's immutable, so ignore it!
        pass 

    return obj