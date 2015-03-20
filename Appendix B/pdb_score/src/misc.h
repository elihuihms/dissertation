#ifndef _misc_h_
#define _misc_h_

/* extracts a substring */
void substr( char* dest, char* source, int start, int len );

/* removes whitespace from an (editable) string */
char *trim( char *str );

#endif