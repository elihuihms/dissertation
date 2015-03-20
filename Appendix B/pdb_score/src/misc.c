#ifndef _stdlib_h_
#include <stdlib.h>
#endif

#ifndef _misc_h_
#include "misc.h"
#endif

/*	
	Author: E. Ihms
*/

void substr( char* dest, char* source, int start, int len )
{
	strncpy(dest, source+start, len);	
	dest[len] = 0;

	return;
}

char *trim( char *str )
{
	int i;
	int begin = 0;
	int end = strlen(str) -1;
	
	while (isspace( str[begin] ))
		begin++;
	while (isspace( str[end] ) && (end >= begin))
		end--;
	
	for (i = begin; i<= end; i++)
		str[i - begin] = str[i];
	
	str[i - begin] = '\0';
}