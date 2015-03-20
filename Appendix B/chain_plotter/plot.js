var chainNum = 0;

function setupFileReader()
{
	if( window.File && window.FileReader && window.FileList && window.Blob )
	{
		document.getElementById('local_file').addEventListener('change', readLocalFile, false);
		document.body.addEventListener('keydown', keyDown, false );
	}
	else
		alert( "File APIs are not supported by this browser!" );
}
	
function readLocalFile(e)
{
	if( e.target.files[0] )
	{
		var reader = new FileReader();
		
		reader.onload = function(e)
		{
			window.chains = eval('('+e.target.result+')');

			if( window.chains.length < 1 )
				alert( "Error: file is not valid!" );
		}
		
		reader.readAsText( e.target.files[0] );
		window.setTimeout( 'setChainNum(0)', 10 );
		window.setTimeout( 'modifyChainNum(0)', 10 );
	}
	else
		alert( "File \""+file.name+"\" not read" );
	
}

function keyDown(event)
{
	if ((chainNum == 0) && (event.keyCode == 37))
		return;
	if ((chainNum == (window.chains.length-1)) && (event.keyCode == 39))
		return;

    if (event.keyCode == 39)
    	modifyChainNum(1);
    if (event.keyCode == 37)
    	modifyChainNum(-1);
    	
    return;
}

function modifyChainNum(increment)
{
	if ((chainNum == 0) && (increment < 0))
		return;
	if ((chainNum == (window.chains.length-1)) && (increment > 0))
		return;

	// update the chain # counter
	var e = document.getElementById('chainNumField');
	chainNum = parseInt(e.value) + increment;
	e.value = chainNum;
	
	var e = document.getElementById('chainNumIndication');
	e.innerHTML = '/'+(window.chains.length-1)
	
	var e = document.getElementById('chainRawText');
	e.value = JSON.stringify(window.chains[chainNum]);

	// plot the newly incremented chain
	clearCanvas();	
	plot();
	
	return;
}

function setChainNum()
{
	var e = document.getElementById('chainNumField');
	chainNum = e.value;
	
	clearCanvas();
	plot();
	
	return;
}

function clearCanvas()
{
	var canvas = document.getElementById('plotCanvas');
	var ctx = canvas.getContext('2d');
	ctx.save()
	ctx.setTransform(1,0,0,1,0,0);
	ctx.clearRect(0,0,canvas.width,canvas.height);
	ctx.restore();

	return;
}

function plot()
{
	var canvas = document.getElementById('plotCanvas');
	if (canvas.getContext)
	{
		var ctx = canvas.getContext('2d');
		
		setChainCoords( window.chains[chainNum],canvas.width/2,canvas.height/2 );
		
		for(var i=0; i<window.chains[chainNum].length; i++)
		{
			component = window.chains[chainNum][i];
			if(component.type == 0)
				drawTRAP(ctx,component.coords.x,component.coords.y,component.name);
			else
				drawAT(ctx,component.coords.x,component.coords.y,component.name);
		}
		
		/*
		var componentLists = makeComponentLists(canvas.width/2,canvas.height/2,window.chains[chainNum]);
		
		// now draw the two lists
		for (var i=0; i<componentLists[0].length; i++)
			drawTRAP(ctx,componentLists[0][i]['x'],componentLists[0][i]['y'],componentLists[0][i]['name']);
			
		for (var i=0; i<componentLists[1].length; i++)
			drawAT(ctx,componentLists[1][i]['x'],componentLists[1][i]['y'],componentLists[1][i]['name']);
		*/
	}
	return;
}

function setChainCoords( chain, startX, startY )
{
	chain[0].coords = []
	chain[0].coords.x = startX;
	chain[0].coords.y = startY;
	chain[0].coords.r = 0;
	
	seen = [];
	setComponentCoords( 0, chain, seen );
}

function setComponentCoords( parentID, chain, seen )
{
	var parent = chain[parentID];
	
	for(var i=0; i<parent.sites.length; i++)
	{
		if(parent.sites[i] != null)
		{
			childID = Math.floor(parent.sites[i] / 100);
			child = chain[ childID ];
			
			if(seen.indexOf(child) == -1)
			{
				seen.push(child);
				
				child.coords = [];
				child.coords.x = parent.coords.x + 35 * Math.cos( parent.coords.r + ( 2 * Math.PI * (i / parent.sites.length)) );
				child.coords.y = parent.coords.y + 35 * Math.sin( parent.coords.r + ( 2 * Math.PI * (i / parent.sites.length)) );
				child.coords.r = parent.coords.r + (2 * Math.PI * (i / parent.sites.length)) + Math.PI;
				
				setComponentCoords( childID, chain, seen );
			}
		}
	}
}

/*
function makeComponentLists(startX,startY,chain)
{

	// these arrays will hold all of the TRAP and ATs to eventually draw
	var TRAP_list = [];
	var AT_list = [];
	
	// find a TRAP as a starting point
	for (var i=0; i<chain.length; i++)
	{
		if (chain[i]['type'] == 0){
			var TRAP_list = [{'i':i,'name':window.chains[chainNum][i]['name'],'x':startX,'y':startY,'rot':0}];
			break;
		} 	
	}		
	
	// iterate until we've found all of the TRAPs and antiTRAPs
	while (true)
	{
		AT_list_len = AT_list.length;
		TRAP_list_len = TRAP_list.length;
		
		// from the newly discovered TRAPs, look for bound anti-TRAPs
		for (var i=0; i<TRAP_list.length; i++)
			AT_list = setBoundComponents(chain, TRAP_list[i], AT_list);
		
		// from the newly discovered anti-TRAPs, look for bound TRAPs
		for (var i=0; i<AT_list.length; i++)
			TRAP_list = setBoundComponents(chain, AT_list[i], TRAP_list);
	
		// if there were no new additions to either list, the loop will exit
		if ((AT_list_len == AT_list.length) && (TRAP_list_len == TRAP_list.length))
			break;
	}
	
	return [TRAP_list,AT_list];
}

function setBoundComponents(currChain, startComponent, list)
{
	// retrieve the component record from the chain
	var component = currChain[startComponent['i']];
	
	var nSites = component.sites.length;
	
	// iterate over all the component's binding sites
	for (var i=0; i<nSites; i++)
	{
		if (component['sites'][i] != null)
		{
			// get the bound partner's array index
			var index = Math.floor(component['sites'][i] / 100);
			alert(component.name+" "+nSites);
			// make sure we haven't already retrieved this particular component
			if (!isIndexInArray(list,index))
			{	
				// assign the bound partner's XY coordinates by going around the current component
				var x = startComponent['x'] + 35 * Math.cos( startComponent['rot'] + ( 2 * Math.PI * (i / nSites)) );
				var y = startComponent['y'] + 35 * Math.sin( startComponent['rot'] + ( 2 * Math.PI * (i / nSites)) );
				var r = Math.PI + startComponent['rot'] + (2 * Math.PI * (i / nSites));

				// append the new component to the list
				list.push({'i':index,'name':currChain[index]['name'],'x':x,'y':y,'rot':r});
			}
		}
	}
	
	return list;
}

function isIndexInArray(list, index)
{
	for(var i=0; i<list.length; i++)
		if (String(list[i]['i']) == String(index))
			return true;

	return false;
}
*/


function fillCircle(ctx, centerX, centerY, radius)
{
	ctx.beginPath();
	ctx.arc(centerX,centerY,radius,0,Math.PI*2,true);
	ctx.fill();
	
	return;
}

function drawTRAP(ctx,x,y,name)
{
	ctx.fillStyle='rgba(0,0,200,0.75)';
	fillCircle(ctx,x,y,30);
	
	var dim = ctx.measureText(name);
	ctx.fillStyle='black';
	ctx.fillText(name,x - (dim.width/2),y);
	
	return;
}

function drawAT(ctx,x,y,name)
{
	ctx.fillStyle='rgba(200,0,0,0.75)';
	fillCircle(ctx,x,y,15);
	
	var dim = ctx.measureText(name);
	ctx.fillStyle='black';
	ctx.fillText(name,x - (dim.width/2),y);
	
	return;
}