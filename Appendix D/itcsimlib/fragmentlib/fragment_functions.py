from random import random
from math import floor

def chunk( a, size ):
	return ''.join( permute( a, int(random()*len(a)) )[0:size] )

def permute( a, i ):
	assert( i >= 0 )

	ret,n = a[:],len(a)
	for j in xrange(n):
		if( i+j >= n ):
			ret[ (i+j) % n ] = a[j]
		else:
			ret[i+j] = a[j]

	return ret

def reflect( a ):
	ret,n = a[:],len(a)
	for i in xrange(n):
		ret[ (n-1) -i ] = a[i]

	return ret

def slice( a, center, size ):
	assert len(a) > size
	assert size==1 or size%2==1

	return permute( permute(a,len(a)-center), int(size)/2 )[0:size]

def compare( a, b, mirror=True, linear=False ):
	n = len(a)

	def is_same(x,y):
		for z in xrange(n):
			if x[z] != y[z]:
				return False
		return True

	if linear:
		if is_same(a,b):
			return True
		elif  mirror and is_same( reflect(a), b ):
			return True
		return False

	for i in range(n):
		if is_same( a, permute(b,i) ):
			return True
		if mirror and is_same( reflect(a), permute(b,i) ):
			return True

	return False

def frag_count( config, fragment ):
	config = list(config)

	# start with the largest fragments
	ret,n = 0,len(fragment)
	for i in xrange(len(config)):

		if compare( list(fragment), slice(config,i,n), linear=True ):
			ret += 1

	return ret

def frag_count_dict( config, fragments ):
	# counts the number of occurrences of each odd-sized fragment
	ret = {}
	for f in fragments:
		ret[f] = 0

	# start with the largest fragments
	for f in sorted(fragments, key=len, reverse=True):
		ret[f] = frag_count( config, f )

	return ret

def frag_xcount_dict( config, fragments ):
	# counts the number of occurrences of each odd-sized fragment, unless it's already been counted as part of a larger fragment

	ret = {}
	for f in fragments:
		ret[f] = 0

	config = list(config)
	sorted_fragments = sorted(fragments, key=len, reverse=True)

	for i in xrange(len(config)):
		for f in sorted_fragments:
			if compare( list(f), slice(config,i,len(f)), linear=True ):
				ret[f] += 1
				break # stop looking for more fragments

	return ret

# this was the old count, which frequently OVERCOUNTS dGs
def count( a, b, mirror=True ):
	ret,n,k = 0,len(a),len(b)
	assert k < n

	c = ''.join( reflect( list(b) ) )
	if c == b: # b is symmetric
		mirror = False

	for i in xrange(n):
		if b == ''.join( permute( list(a),i)[0:k] ):
			ret +=1

		if mirror and c == ''.join( permute( list(a),i)[0:k] ):
			ret +=1

	return ret

def return_unique( configs, mirror=True, linear=False ):
	unique,counts = [configs[0]],{configs[0]:0}
	for c1 in configs:

		seen = False
		for c2 in unique:

			if compare(list(c1),list(c2),mirror,linear):
				counts[ c2 ] += 1
				seen = True
				break

		if not seen:
			unique.append(c1)
			counts[ c1 ] = 1

	return unique,counts
