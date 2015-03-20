oldChains = []

function changeFilter()
{
	// save the original chain array
	if (oldChains.length == 0)
		oldChains = chains;

	// update the chain filter
	var e = document.getElementById('chainFilterSize');
	
	// update the chains global
	chains = filterChains(oldChains,parseInt(e.value));
	
	// force a redraw
	modifyChainNum(0);

	return;
}

function filterChains( chains, cutoff )
{
	/* function checks all of the inter-component center distances and returns an array in which all chains that have the distance restraint violated are removed */
	
	var i,j,k;
	var dist;
	var componentLists = [];
	var list = [];
	
	// go through every chain
	for(i=0; i<chains.length; i++)
	{
		componentLists = makeComponentLists(0,0,chains[i]);
		
		// put all components in the same list
		checkList = componentLists[0].concat(componentLists[1]);
		
		// all chains innocent until proven guilty (at least once)
		goodChain = true;
		
		for(toggle=0; toggle<2; toggle++)
		
		// go through every component in the chain
		for(j=0; j<checkList.length; j++)
		{
			// compare against every other TRAP in the chain
			for(k=0; k<checkList.length; k++)
			{
				if(j != k)
				{
					dist = Math.sqrt(Math.pow(checkList[j]['x']-checkList[k]['x'],2)+Math.pow(checkList[j]['y']-checkList[k]['y'],2));
					
					if(dist < cutoff)
						goodChain = false;
				}
			}
		}
		
		if(goodChain)
			list.push(chains[i]);	
	}
	
	return list;
}