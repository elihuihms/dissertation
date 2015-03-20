def write_params_to_file( params, file, prefix='', postfix='', append=True ):
	if append:
		handle = open( file, 'a')
	else:
		handle = open( file, 'w')

	handle.write("%i	%s %f	%s	%s\n" % (i,str(fragment_combinations[i]),sse,str(dG),str(dH)))
	handle.close()

def read_params_from_file( file, col_start=0, col_end=3 ):
	handle = open( file, 'r' )

	ret = []
	for l in handle.readlines():
		fields = [f.replace(']','') for f in l.split('[')][col_start:col_end]
		ret.append( [ map(float,f.split(', ')) for f in fields ] )
	return ret

