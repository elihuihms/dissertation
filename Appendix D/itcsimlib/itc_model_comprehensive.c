#include "itc_model_comprehensive.h"

int setupModelWorkspace( struct mWorkspace *w )
{
	/* initialize the root finder */
	w->fsolver_s = gsl_root_fsolver_alloc( gsl_root_fsolver_brent );
	w->fsolver_F.function = &getFree;

	w->bound[  0] =  0; // 00000000000
	w->bound[  1] =  1; // 00000000001
	w->bound[  2] =  2; // 00000000011
	w->bound[  3] =  2; // 00000000101
	w->bound[  4] =  3; // 00000000111
	w->bound[  5] =  2; // 00000001001
	w->bound[  6] =  3; // 00000001011
	w->bound[  7] =  4; // 00000001111
	w->bound[  8] =  2; // 00000010001
	w->bound[  9] =  3; // 00000010011
	w->bound[ 10] =  3; // 00000010101
	w->bound[ 11] =  4; // 00000010111
	w->bound[ 12] =  4; // 00000011011
	w->bound[ 13] =  5; // 00000011111
	w->bound[ 14] =  2; // 00000100001
	w->bound[ 15] =  3; // 00000100011
	w->bound[ 16] =  3; // 00000100101
	w->bound[ 17] =  4; // 00000100111
	w->bound[ 18] =  4; // 00000101011
	w->bound[ 19] =  4; // 00000101101
	w->bound[ 20] =  5; // 00000101111
	w->bound[ 21] =  4; // 00000110011
	w->bound[ 22] =  5; // 00000110111
	w->bound[ 23] =  6; // 00000111111
	w->bound[ 24] =  3; // 00001000011
	w->bound[ 25] =  3; // 00001000101
	w->bound[ 26] =  4; // 00001000111
	w->bound[ 27] =  3; // 00001001001
	w->bound[ 28] =  4; // 00001001011
	w->bound[ 29] =  4; // 00001001101
	w->bound[ 30] =  5; // 00001001111
	w->bound[ 31] =  4; // 00001010011
	w->bound[ 32] =  4; // 00001010101
	w->bound[ 33] =  5; // 00001010111
	w->bound[ 34] =  5; // 00001011011
	w->bound[ 35] =  5; // 00001011101
	w->bound[ 36] =  6; // 00001011111
	w->bound[ 37] =  4; // 00001100011
	w->bound[ 38] =  5; // 00001100111
	w->bound[ 39] =  5; // 00001101011
	w->bound[ 40] =  6; // 00001101111
	w->bound[ 41] =  6; // 00001110111
	w->bound[ 42] =  7; // 00001111111
	w->bound[ 43] =  3; // 00010001001
	w->bound[ 44] =  4; // 00010001011
	w->bound[ 45] =  5; // 00010001111
	w->bound[ 46] =  4; // 00010010011
	w->bound[ 47] =  4; // 00010010101
	w->bound[ 48] =  5; // 00010010111
	w->bound[ 49] =  4; // 00010011001
	w->bound[ 50] =  5; // 00010011011
	w->bound[ 51] =  5; // 00010011101
	w->bound[ 52] =  6; // 00010011111
	w->bound[ 53] =  4; // 00010100011
	w->bound[ 54] =  4; // 00010100101
	w->bound[ 55] =  5; // 00010100111
	w->bound[ 56] =  5; // 00010101011
	w->bound[ 57] =  5; // 00010101101
	w->bound[ 58] =  6; // 00010101111
	w->bound[ 59] =  5; // 00010110011
	w->bound[ 60] =  6; // 00010110111
	w->bound[ 61] =  6; // 00010111011
	w->bound[ 62] =  6; // 00010111101
	w->bound[ 63] =  7; // 00010111111
	w->bound[ 64] =  5; // 00011000111
	w->bound[ 65] =  5; // 00011001011
	w->bound[ 66] =  6; // 00011001111
	w->bound[ 67] =  6; // 00011010111
	w->bound[ 68] =  6; // 00011011011
	w->bound[ 69] =  7; // 00011011111
	w->bound[ 70] =  6; // 00011100111
	w->bound[ 71] =  7; // 00011101111
	w->bound[ 72] =  8; // 00011111111
	w->bound[ 73] =  4; // 00100100101
	w->bound[ 74] =  5; // 00100100111
	w->bound[ 75] =  5; // 00100101011
	w->bound[ 76] =  5; // 00100101101
	w->bound[ 77] =  6; // 00100101111
	w->bound[ 78] =  5; // 00100110011
	w->bound[ 79] =  6; // 00100110111
	w->bound[ 80] =  7; // 00100111111
	w->bound[ 81] =  5; // 00101001011
	w->bound[ 82] =  6; // 00101001111
	w->bound[ 83] =  5; // 00101010011
	w->bound[ 84] =  5; // 00101010101
	w->bound[ 85] =  6; // 00101010111
	w->bound[ 86] =  6; // 00101011011
	w->bound[ 87] =  6; // 00101011101
	w->bound[ 88] =  7; // 00101011111
	w->bound[ 89] =  6; // 00101100111
	w->bound[ 90] =  6; // 00101101011
	w->bound[ 91] =  6; // 00101101101
	w->bound[ 92] =  7; // 00101101111
	w->bound[ 93] =  6; // 00101110011
	w->bound[ 94] =  7; // 00101110111
	w->bound[ 95] =  7; // 00101111011
	w->bound[ 96] =  7; // 00101111101
	w->bound[ 97] =  8; // 00101111111
	w->bound[ 98] =  6; // 00110011011
	w->bound[ 99] =  7; // 00110011111
	w->bound[100] =  6; // 00110101011
	w->bound[101] =  7; // 00110101111
	w->bound[102] =  7; // 00110110111
	w->bound[103] =  7; // 00110111011
	w->bound[104] =  8; // 00110111111
	w->bound[105] =  7; // 00111001111
	w->bound[106] =  7; // 00111010111
	w->bound[107] =  8; // 00111011111
	w->bound[108] =  8; // 00111101111
	w->bound[109] =  9; // 00111111111
	w->bound[110] =  6; // 01010101011
	w->bound[111] =  7; // 01010101111
	w->bound[112] =  7; // 01010110111
	w->bound[113] =  8; // 01010111111
	w->bound[114] =  7; // 01011010111
	w->bound[115] =  7; // 01011011011
	w->bound[116] =  8; // 01011011111
	w->bound[117] =  8; // 01011101111
	w->bound[118] =  9; // 01011111111
	w->bound[119] =  8; // 01101101111
	w->bound[120] =  8; // 01101110111
	w->bound[121] =  9; // 01101111111
	w->bound[122] =  9; // 01110111111
	w->bound[123] =  9; // 01111011111
	w->bound[124] = 10; // 01111111111
	w->bound[125] = 11; // 11111111111

	w->weight[  0] =  1; // 00000000000
	w->weight[  1] = 11; // 00000000001
	w->weight[  2] = 11; // 00000000011
	w->weight[  3] = 11; // 00000000101
	w->weight[  4] = 11; // 00000000111
	w->weight[  5] = 11; // 00000001001
	w->weight[  6] = 22; // 00000001011
	w->weight[  7] = 11; // 00000001111
	w->weight[  8] = 11; // 00000010001
	w->weight[  9] = 22; // 00000010011
	w->weight[ 10] = 11; // 00000010101
	w->weight[ 11] = 22; // 00000010111
	w->weight[ 12] = 11; // 00000011011
	w->weight[ 13] = 11; // 00000011111
	w->weight[ 14] = 11; // 00000100001
	w->weight[ 15] = 22; // 00000100011
	w->weight[ 16] = 22; // 00000100101
	w->weight[ 17] = 22; // 00000100111
	w->weight[ 18] = 22; // 00000101011
	w->weight[ 19] = 11; // 00000101101
	w->weight[ 20] = 22; // 00000101111
	w->weight[ 21] = 11; // 00000110011
	w->weight[ 22] = 22; // 00000110111
	w->weight[ 23] = 11; // 00000111111
	w->weight[ 24] = 11; // 00001000011
	w->weight[ 25] = 22; // 00001000101
	w->weight[ 26] = 22; // 00001000111
	w->weight[ 27] = 11; // 00001001001
	w->weight[ 28] = 22; // 00001001011
	w->weight[ 29] = 22; // 00001001101
	w->weight[ 30] = 22; // 00001001111
	w->weight[ 31] = 22; // 00001010011
	w->weight[ 32] = 11; // 00001010101
	w->weight[ 33] = 22; // 00001010111
	w->weight[ 34] = 22; // 00001011011
	w->weight[ 35] = 11; // 00001011101
	w->weight[ 36] = 22; // 00001011111
	w->weight[ 37] = 11; // 00001100011
	w->weight[ 38] = 22; // 00001100111
	w->weight[ 39] = 11; // 00001101011
	w->weight[ 40] = 22; // 00001101111
	w->weight[ 41] = 11; // 00001110111
	w->weight[ 42] = 11; // 00001111111
	w->weight[ 43] = 11; // 00010001001
	w->weight[ 44] = 22; // 00010001011
	w->weight[ 45] = 11; // 00010001111
	w->weight[ 46] = 22; // 00010010011
	w->weight[ 47] = 22; // 00010010101
	w->weight[ 48] = 22; // 00010010111
	w->weight[ 49] = 11; // 00010011001
	w->weight[ 50] = 22; // 00010011011
	w->weight[ 51] = 22; // 00010011101
	w->weight[ 52] = 22; // 00010011111
	w->weight[ 53] = 11; // 00010100011
	w->weight[ 54] = 11; // 00010100101
	w->weight[ 55] = 22; // 00010100111
	w->weight[ 56] = 22; // 00010101011
	w->weight[ 57] = 22; // 00010101101
	w->weight[ 58] = 22; // 00010101111
	w->weight[ 59] = 22; // 00010110011
	w->weight[ 60] = 22; // 00010110111
	w->weight[ 61] = 22; // 00010111011
	w->weight[ 62] = 11; // 00010111101
	w->weight[ 63] = 22; // 00010111111
	w->weight[ 64] = 11; // 00011000111
	w->weight[ 65] = 22; // 00011001011
	w->weight[ 66] = 22; // 00011001111
	w->weight[ 67] = 22; // 00011010111
	w->weight[ 68] = 11; // 00011011011
	w->weight[ 69] = 22; // 00011011111
	w->weight[ 70] = 11; // 00011100111
	w->weight[ 71] = 22; // 00011101111
	w->weight[ 72] = 11; // 00011111111
	w->weight[ 73] = 11; // 00100100101
	w->weight[ 74] = 11; // 00100100111
	w->weight[ 75] = 22; // 00100101011
	w->weight[ 76] = 11; // 00100101101
	w->weight[ 77] = 22; // 00100101111
	w->weight[ 78] = 11; // 00100110011
	w->weight[ 79] = 22; // 00100110111
	w->weight[ 80] = 11; // 00100111111
	w->weight[ 81] = 22; // 00101001011
	w->weight[ 82] = 11; // 00101001111
	w->weight[ 83] = 11; // 00101010011
	w->weight[ 84] = 11; // 00101010101
	w->weight[ 85] = 22; // 00101010111
	w->weight[ 86] = 22; // 00101011011
	w->weight[ 87] = 22; // 00101011101
	w->weight[ 88] = 22; // 00101011111
	w->weight[ 89] = 22; // 00101100111
	w->weight[ 90] = 22; // 00101101011
	w->weight[ 91] = 11; // 00101101101
	w->weight[ 92] = 22; // 00101101111
	w->weight[ 93] = 22; // 00101110011
	w->weight[ 94] = 22; // 00101110111
	w->weight[ 95] = 22; // 00101111011
	w->weight[ 96] = 11; // 00101111101
	w->weight[ 97] = 22; // 00101111111
	w->weight[ 98] = 11; // 00110011011
	w->weight[ 99] = 11; // 00110011111
	w->weight[100] = 11; // 00110101011
	w->weight[101] = 22; // 00110101111
	w->weight[102] = 22; // 00110110111
	w->weight[103] = 11; // 00110111011
	w->weight[104] = 22; // 00110111111
	w->weight[105] = 11; // 00111001111
	w->weight[106] = 11; // 00111010111
	w->weight[107] = 22; // 00111011111
	w->weight[108] = 11; // 00111101111
	w->weight[109] = 11; // 00111111111
	w->weight[110] = 11; // 01010101011
	w->weight[111] = 11; // 01010101111
	w->weight[112] = 22; // 01010110111
	w->weight[113] = 11; // 01010111111
	w->weight[114] = 11; // 01011010111
	w->weight[115] = 11; // 01011011011
	w->weight[116] = 22; // 01011011111
	w->weight[117] = 22; // 01011101111
	w->weight[118] = 11; // 01011111111
	w->weight[119] = 11; // 01101101111
	w->weight[120] = 11; // 01101110111
	w->weight[121] = 11; // 01101111111
	w->weight[122] = 11; // 01110111111
	w->weight[123] = 11; // 01111011111
	w->weight[124] = 11; // 01111111111
	w->weight[125] =  1; // 11111111111

	return 0;
}

int freeModelWorkspace( struct mWorkspace w )
{
	gsl_root_fsolver_free( w.fsolver_s );
	return 0;
}

void setProbabilities( struct mWorkspace *w )
{
	/*

	from itcsimlib.fragmentlib	import *

	configs,counts = return_unique( make_configs(11), mirror=True, linear=False )
	for (i,c) in enumerate(configs):
		bound = c.count('1')
		#print "w->probs[%03s] = w->weight[%03s] * exp( (-1 * w->dG[%03s] * w->bound[%03s]) / (R * w->temp) ) * pow(w->Lfree,w->bound[%03s]); // %s" % (i,i,i,i,i,c)
		#print "w->bound[%03s] = %02s; // %s" %(i,bound,c)
		#print "w->weight[%03s] = %02s; // %s" %(i,counts[c],c)
	*/

	double	R = 8.3144621; // J/(K*mol)

	w->probs[  0] = w->weight[  0] * exp( (-1 * w->dG[  0] * w->bound[  0]) / (R * w->temp) ) * pow(w->Lfree,w->bound[  0]); // 00000000000
	w->probs[  1] = w->weight[  1] * exp( (-1 * w->dG[  1] * w->bound[  1]) / (R * w->temp) ) * pow(w->Lfree,w->bound[  1]); // 00000000001
	w->probs[  2] = w->weight[  2] * exp( (-1 * w->dG[  2] * w->bound[  2]) / (R * w->temp) ) * pow(w->Lfree,w->bound[  2]); // 00000000011
	w->probs[  3] = w->weight[  3] * exp( (-1 * w->dG[  3] * w->bound[  3]) / (R * w->temp) ) * pow(w->Lfree,w->bound[  3]); // 00000000101
	w->probs[  4] = w->weight[  4] * exp( (-1 * w->dG[  4] * w->bound[  4]) / (R * w->temp) ) * pow(w->Lfree,w->bound[  4]); // 00000000111
	w->probs[  5] = w->weight[  5] * exp( (-1 * w->dG[  5] * w->bound[  5]) / (R * w->temp) ) * pow(w->Lfree,w->bound[  5]); // 00000001001
	w->probs[  6] = w->weight[  6] * exp( (-1 * w->dG[  6] * w->bound[  6]) / (R * w->temp) ) * pow(w->Lfree,w->bound[  6]); // 00000001011
	w->probs[  7] = w->weight[  7] * exp( (-1 * w->dG[  7] * w->bound[  7]) / (R * w->temp) ) * pow(w->Lfree,w->bound[  7]); // 00000001111
	w->probs[  8] = w->weight[  8] * exp( (-1 * w->dG[  8] * w->bound[  8]) / (R * w->temp) ) * pow(w->Lfree,w->bound[  8]); // 00000010001
	w->probs[  9] = w->weight[  9] * exp( (-1 * w->dG[  9] * w->bound[  9]) / (R * w->temp) ) * pow(w->Lfree,w->bound[  9]); // 00000010011
	w->probs[ 10] = w->weight[ 10] * exp( (-1 * w->dG[ 10] * w->bound[ 10]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 10]); // 00000010101
	w->probs[ 11] = w->weight[ 11] * exp( (-1 * w->dG[ 11] * w->bound[ 11]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 11]); // 00000010111
	w->probs[ 12] = w->weight[ 12] * exp( (-1 * w->dG[ 12] * w->bound[ 12]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 12]); // 00000011011
	w->probs[ 13] = w->weight[ 13] * exp( (-1 * w->dG[ 13] * w->bound[ 13]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 13]); // 00000011111
	w->probs[ 14] = w->weight[ 14] * exp( (-1 * w->dG[ 14] * w->bound[ 14]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 14]); // 00000100001
	w->probs[ 15] = w->weight[ 15] * exp( (-1 * w->dG[ 15] * w->bound[ 15]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 15]); // 00000100011
	w->probs[ 16] = w->weight[ 16] * exp( (-1 * w->dG[ 16] * w->bound[ 16]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 16]); // 00000100101
	w->probs[ 17] = w->weight[ 17] * exp( (-1 * w->dG[ 17] * w->bound[ 17]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 17]); // 00000100111
	w->probs[ 18] = w->weight[ 18] * exp( (-1 * w->dG[ 18] * w->bound[ 18]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 18]); // 00000101011
	w->probs[ 19] = w->weight[ 19] * exp( (-1 * w->dG[ 19] * w->bound[ 19]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 19]); // 00000101101
	w->probs[ 20] = w->weight[ 20] * exp( (-1 * w->dG[ 20] * w->bound[ 20]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 20]); // 00000101111
	w->probs[ 21] = w->weight[ 21] * exp( (-1 * w->dG[ 21] * w->bound[ 21]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 21]); // 00000110011
	w->probs[ 22] = w->weight[ 22] * exp( (-1 * w->dG[ 22] * w->bound[ 22]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 22]); // 00000110111
	w->probs[ 23] = w->weight[ 23] * exp( (-1 * w->dG[ 23] * w->bound[ 23]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 23]); // 00000111111
	w->probs[ 24] = w->weight[ 24] * exp( (-1 * w->dG[ 24] * w->bound[ 24]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 24]); // 00001000011
	w->probs[ 25] = w->weight[ 25] * exp( (-1 * w->dG[ 25] * w->bound[ 25]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 25]); // 00001000101
	w->probs[ 26] = w->weight[ 26] * exp( (-1 * w->dG[ 26] * w->bound[ 26]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 26]); // 00001000111
	w->probs[ 27] = w->weight[ 27] * exp( (-1 * w->dG[ 27] * w->bound[ 27]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 27]); // 00001001001
	w->probs[ 28] = w->weight[ 28] * exp( (-1 * w->dG[ 28] * w->bound[ 28]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 28]); // 00001001011
	w->probs[ 29] = w->weight[ 29] * exp( (-1 * w->dG[ 29] * w->bound[ 29]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 29]); // 00001001101
	w->probs[ 30] = w->weight[ 30] * exp( (-1 * w->dG[ 30] * w->bound[ 30]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 30]); // 00001001111
	w->probs[ 31] = w->weight[ 31] * exp( (-1 * w->dG[ 31] * w->bound[ 31]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 31]); // 00001010011
	w->probs[ 32] = w->weight[ 32] * exp( (-1 * w->dG[ 32] * w->bound[ 32]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 32]); // 00001010101
	w->probs[ 33] = w->weight[ 33] * exp( (-1 * w->dG[ 33] * w->bound[ 33]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 33]); // 00001010111
	w->probs[ 34] = w->weight[ 34] * exp( (-1 * w->dG[ 34] * w->bound[ 34]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 34]); // 00001011011
	w->probs[ 35] = w->weight[ 35] * exp( (-1 * w->dG[ 35] * w->bound[ 35]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 35]); // 00001011101
	w->probs[ 36] = w->weight[ 36] * exp( (-1 * w->dG[ 36] * w->bound[ 36]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 36]); // 00001011111
	w->probs[ 37] = w->weight[ 37] * exp( (-1 * w->dG[ 37] * w->bound[ 37]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 37]); // 00001100011
	w->probs[ 38] = w->weight[ 38] * exp( (-1 * w->dG[ 38] * w->bound[ 38]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 38]); // 00001100111
	w->probs[ 39] = w->weight[ 39] * exp( (-1 * w->dG[ 39] * w->bound[ 39]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 39]); // 00001101011
	w->probs[ 40] = w->weight[ 40] * exp( (-1 * w->dG[ 40] * w->bound[ 40]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 40]); // 00001101111
	w->probs[ 41] = w->weight[ 41] * exp( (-1 * w->dG[ 41] * w->bound[ 41]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 41]); // 00001110111
	w->probs[ 42] = w->weight[ 42] * exp( (-1 * w->dG[ 42] * w->bound[ 42]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 42]); // 00001111111
	w->probs[ 43] = w->weight[ 43] * exp( (-1 * w->dG[ 43] * w->bound[ 43]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 43]); // 00010001001
	w->probs[ 44] = w->weight[ 44] * exp( (-1 * w->dG[ 44] * w->bound[ 44]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 44]); // 00010001011
	w->probs[ 45] = w->weight[ 45] * exp( (-1 * w->dG[ 45] * w->bound[ 45]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 45]); // 00010001111
	w->probs[ 46] = w->weight[ 46] * exp( (-1 * w->dG[ 46] * w->bound[ 46]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 46]); // 00010010011
	w->probs[ 47] = w->weight[ 47] * exp( (-1 * w->dG[ 47] * w->bound[ 47]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 47]); // 00010010101
	w->probs[ 48] = w->weight[ 48] * exp( (-1 * w->dG[ 48] * w->bound[ 48]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 48]); // 00010010111
	w->probs[ 49] = w->weight[ 49] * exp( (-1 * w->dG[ 49] * w->bound[ 49]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 49]); // 00010011001
	w->probs[ 50] = w->weight[ 50] * exp( (-1 * w->dG[ 50] * w->bound[ 50]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 50]); // 00010011011
	w->probs[ 51] = w->weight[ 51] * exp( (-1 * w->dG[ 51] * w->bound[ 51]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 51]); // 00010011101
	w->probs[ 52] = w->weight[ 52] * exp( (-1 * w->dG[ 52] * w->bound[ 52]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 52]); // 00010011111
	w->probs[ 53] = w->weight[ 53] * exp( (-1 * w->dG[ 53] * w->bound[ 53]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 53]); // 00010100011
	w->probs[ 54] = w->weight[ 54] * exp( (-1 * w->dG[ 54] * w->bound[ 54]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 54]); // 00010100101
	w->probs[ 55] = w->weight[ 55] * exp( (-1 * w->dG[ 55] * w->bound[ 55]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 55]); // 00010100111
	w->probs[ 56] = w->weight[ 56] * exp( (-1 * w->dG[ 56] * w->bound[ 56]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 56]); // 00010101011
	w->probs[ 57] = w->weight[ 57] * exp( (-1 * w->dG[ 57] * w->bound[ 57]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 57]); // 00010101101
	w->probs[ 58] = w->weight[ 58] * exp( (-1 * w->dG[ 58] * w->bound[ 58]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 58]); // 00010101111
	w->probs[ 59] = w->weight[ 59] * exp( (-1 * w->dG[ 59] * w->bound[ 59]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 59]); // 00010110011
	w->probs[ 60] = w->weight[ 60] * exp( (-1 * w->dG[ 60] * w->bound[ 60]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 60]); // 00010110111
	w->probs[ 61] = w->weight[ 61] * exp( (-1 * w->dG[ 61] * w->bound[ 61]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 61]); // 00010111011
	w->probs[ 62] = w->weight[ 62] * exp( (-1 * w->dG[ 62] * w->bound[ 62]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 62]); // 00010111101
	w->probs[ 63] = w->weight[ 63] * exp( (-1 * w->dG[ 63] * w->bound[ 63]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 63]); // 00010111111
	w->probs[ 64] = w->weight[ 64] * exp( (-1 * w->dG[ 64] * w->bound[ 64]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 64]); // 00011000111
	w->probs[ 65] = w->weight[ 65] * exp( (-1 * w->dG[ 65] * w->bound[ 65]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 65]); // 00011001011
	w->probs[ 66] = w->weight[ 66] * exp( (-1 * w->dG[ 66] * w->bound[ 66]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 66]); // 00011001111
	w->probs[ 67] = w->weight[ 67] * exp( (-1 * w->dG[ 67] * w->bound[ 67]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 67]); // 00011010111
	w->probs[ 68] = w->weight[ 68] * exp( (-1 * w->dG[ 68] * w->bound[ 68]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 68]); // 00011011011
	w->probs[ 69] = w->weight[ 69] * exp( (-1 * w->dG[ 69] * w->bound[ 69]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 69]); // 00011011111
	w->probs[ 70] = w->weight[ 70] * exp( (-1 * w->dG[ 70] * w->bound[ 70]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 70]); // 00011100111
	w->probs[ 71] = w->weight[ 71] * exp( (-1 * w->dG[ 71] * w->bound[ 71]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 71]); // 00011101111
	w->probs[ 72] = w->weight[ 72] * exp( (-1 * w->dG[ 72] * w->bound[ 72]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 72]); // 00011111111
	w->probs[ 73] = w->weight[ 73] * exp( (-1 * w->dG[ 73] * w->bound[ 73]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 73]); // 00100100101
	w->probs[ 74] = w->weight[ 74] * exp( (-1 * w->dG[ 74] * w->bound[ 74]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 74]); // 00100100111
	w->probs[ 75] = w->weight[ 75] * exp( (-1 * w->dG[ 75] * w->bound[ 75]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 75]); // 00100101011
	w->probs[ 76] = w->weight[ 76] * exp( (-1 * w->dG[ 76] * w->bound[ 76]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 76]); // 00100101101
	w->probs[ 77] = w->weight[ 77] * exp( (-1 * w->dG[ 77] * w->bound[ 77]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 77]); // 00100101111
	w->probs[ 78] = w->weight[ 78] * exp( (-1 * w->dG[ 78] * w->bound[ 78]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 78]); // 00100110011
	w->probs[ 79] = w->weight[ 79] * exp( (-1 * w->dG[ 79] * w->bound[ 79]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 79]); // 00100110111
	w->probs[ 80] = w->weight[ 80] * exp( (-1 * w->dG[ 80] * w->bound[ 80]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 80]); // 00100111111
	w->probs[ 81] = w->weight[ 81] * exp( (-1 * w->dG[ 81] * w->bound[ 81]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 81]); // 00101001011
	w->probs[ 82] = w->weight[ 82] * exp( (-1 * w->dG[ 82] * w->bound[ 82]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 82]); // 00101001111
	w->probs[ 83] = w->weight[ 83] * exp( (-1 * w->dG[ 83] * w->bound[ 83]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 83]); // 00101010011
	w->probs[ 84] = w->weight[ 84] * exp( (-1 * w->dG[ 84] * w->bound[ 84]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 84]); // 00101010101
	w->probs[ 85] = w->weight[ 85] * exp( (-1 * w->dG[ 85] * w->bound[ 85]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 85]); // 00101010111
	w->probs[ 86] = w->weight[ 86] * exp( (-1 * w->dG[ 86] * w->bound[ 86]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 86]); // 00101011011
	w->probs[ 87] = w->weight[ 87] * exp( (-1 * w->dG[ 87] * w->bound[ 87]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 87]); // 00101011101
	w->probs[ 88] = w->weight[ 88] * exp( (-1 * w->dG[ 88] * w->bound[ 88]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 88]); // 00101011111
	w->probs[ 89] = w->weight[ 89] * exp( (-1 * w->dG[ 89] * w->bound[ 89]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 89]); // 00101100111
	w->probs[ 90] = w->weight[ 90] * exp( (-1 * w->dG[ 90] * w->bound[ 90]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 90]); // 00101101011
	w->probs[ 91] = w->weight[ 91] * exp( (-1 * w->dG[ 91] * w->bound[ 91]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 91]); // 00101101101
	w->probs[ 92] = w->weight[ 92] * exp( (-1 * w->dG[ 92] * w->bound[ 92]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 92]); // 00101101111
	w->probs[ 93] = w->weight[ 93] * exp( (-1 * w->dG[ 93] * w->bound[ 93]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 93]); // 00101110011
	w->probs[ 94] = w->weight[ 94] * exp( (-1 * w->dG[ 94] * w->bound[ 94]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 94]); // 00101110111
	w->probs[ 95] = w->weight[ 95] * exp( (-1 * w->dG[ 95] * w->bound[ 95]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 95]); // 00101111011
	w->probs[ 96] = w->weight[ 96] * exp( (-1 * w->dG[ 96] * w->bound[ 96]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 96]); // 00101111101
	w->probs[ 97] = w->weight[ 97] * exp( (-1 * w->dG[ 97] * w->bound[ 97]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 97]); // 00101111111
	w->probs[ 98] = w->weight[ 98] * exp( (-1 * w->dG[ 98] * w->bound[ 98]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 98]); // 00110011011
	w->probs[ 99] = w->weight[ 99] * exp( (-1 * w->dG[ 99] * w->bound[ 99]) / (R * w->temp) ) * pow(w->Lfree,w->bound[ 99]); // 00110011111
	w->probs[100] = w->weight[100] * exp( (-1 * w->dG[100] * w->bound[100]) / (R * w->temp) ) * pow(w->Lfree,w->bound[100]); // 00110101011
	w->probs[101] = w->weight[101] * exp( (-1 * w->dG[101] * w->bound[101]) / (R * w->temp) ) * pow(w->Lfree,w->bound[101]); // 00110101111
	w->probs[102] = w->weight[102] * exp( (-1 * w->dG[102] * w->bound[102]) / (R * w->temp) ) * pow(w->Lfree,w->bound[102]); // 00110110111
	w->probs[103] = w->weight[103] * exp( (-1 * w->dG[103] * w->bound[103]) / (R * w->temp) ) * pow(w->Lfree,w->bound[103]); // 00110111011
	w->probs[104] = w->weight[104] * exp( (-1 * w->dG[104] * w->bound[104]) / (R * w->temp) ) * pow(w->Lfree,w->bound[104]); // 00110111111
	w->probs[105] = w->weight[105] * exp( (-1 * w->dG[105] * w->bound[105]) / (R * w->temp) ) * pow(w->Lfree,w->bound[105]); // 00111001111
	w->probs[106] = w->weight[106] * exp( (-1 * w->dG[106] * w->bound[106]) / (R * w->temp) ) * pow(w->Lfree,w->bound[106]); // 00111010111
	w->probs[107] = w->weight[107] * exp( (-1 * w->dG[107] * w->bound[107]) / (R * w->temp) ) * pow(w->Lfree,w->bound[107]); // 00111011111
	w->probs[108] = w->weight[108] * exp( (-1 * w->dG[108] * w->bound[108]) / (R * w->temp) ) * pow(w->Lfree,w->bound[108]); // 00111101111
	w->probs[109] = w->weight[109] * exp( (-1 * w->dG[109] * w->bound[109]) / (R * w->temp) ) * pow(w->Lfree,w->bound[109]); // 00111111111
	w->probs[110] = w->weight[110] * exp( (-1 * w->dG[110] * w->bound[110]) / (R * w->temp) ) * pow(w->Lfree,w->bound[110]); // 01010101011
	w->probs[111] = w->weight[111] * exp( (-1 * w->dG[111] * w->bound[111]) / (R * w->temp) ) * pow(w->Lfree,w->bound[111]); // 01010101111
	w->probs[112] = w->weight[112] * exp( (-1 * w->dG[112] * w->bound[112]) / (R * w->temp) ) * pow(w->Lfree,w->bound[112]); // 01010110111
	w->probs[113] = w->weight[113] * exp( (-1 * w->dG[113] * w->bound[113]) / (R * w->temp) ) * pow(w->Lfree,w->bound[113]); // 01010111111
	w->probs[114] = w->weight[114] * exp( (-1 * w->dG[114] * w->bound[114]) / (R * w->temp) ) * pow(w->Lfree,w->bound[114]); // 01011010111
	w->probs[115] = w->weight[115] * exp( (-1 * w->dG[115] * w->bound[115]) / (R * w->temp) ) * pow(w->Lfree,w->bound[115]); // 01011011011
	w->probs[116] = w->weight[116] * exp( (-1 * w->dG[116] * w->bound[116]) / (R * w->temp) ) * pow(w->Lfree,w->bound[116]); // 01011011111
	w->probs[117] = w->weight[117] * exp( (-1 * w->dG[117] * w->bound[117]) / (R * w->temp) ) * pow(w->Lfree,w->bound[117]); // 01011101111
	w->probs[118] = w->weight[118] * exp( (-1 * w->dG[118] * w->bound[118]) / (R * w->temp) ) * pow(w->Lfree,w->bound[118]); // 01011111111
	w->probs[119] = w->weight[119] * exp( (-1 * w->dG[119] * w->bound[119]) / (R * w->temp) ) * pow(w->Lfree,w->bound[119]); // 01101101111
	w->probs[120] = w->weight[120] * exp( (-1 * w->dG[120] * w->bound[120]) / (R * w->temp) ) * pow(w->Lfree,w->bound[120]); // 01101110111
	w->probs[121] = w->weight[121] * exp( (-1 * w->dG[121] * w->bound[121]) / (R * w->temp) ) * pow(w->Lfree,w->bound[121]); // 01101111111
	w->probs[122] = w->weight[122] * exp( (-1 * w->dG[122] * w->bound[122]) / (R * w->temp) ) * pow(w->Lfree,w->bound[122]); // 01110111111
	w->probs[123] = w->weight[123] * exp( (-1 * w->dG[123] * w->bound[123]) / (R * w->temp) ) * pow(w->Lfree,w->bound[123]); // 01111011111
	w->probs[124] = w->weight[124] * exp( (-1 * w->dG[124] * w->bound[124]) / (R * w->temp) ) * pow(w->Lfree,w->bound[124]); // 01111111111
	w->probs[125] = w->weight[125] * exp( (-1 * w->dG[125] * w->bound[125]) / (R * w->temp) ) * pow(w->Lfree,w->bound[125]); // 11111111111

	double	sum = 0;
	for(int i=0; i<126; i++)
		sum += w->probs[i];
	for(int i=0; i<126; i++)
		w->probs[i] /= sum;

	return;
}

double getFree( double Lfree, void *params )
{
	struct mWorkspace *w = (struct mWorkspace *)params;

	w->Lfree = Lfree;
	setProbabilities( w ); /* get the bound fraction of each protein state */

	double bound = 0; /* concentration of sites in bound state */
	for(int i=0; i<126; i++)
		bound += w->probs[i] * w->Ptot * w->bound[i];

	return w->Ltot - (bound + w->Lfree);
}

int setFree( struct mWorkspace *w )
{
	int status;
	int iter = 0, max_iter = 100;

	w->fsolver_F.params = w;
	gsl_root_fsolver_set( w->fsolver_s, &w->fsolver_F, 0, w->Ltot );

	double r,a,b;
	do
	{
		iter++;
		status = gsl_root_fsolver_iterate( w->fsolver_s );
		r = gsl_root_fsolver_root( w->fsolver_s );
		a = gsl_root_fsolver_x_lower( w->fsolver_s );
		b = gsl_root_fsolver_x_upper( w->fsolver_s );

		status = gsl_root_test_interval( a, b, 0.0, 0.0 );

	}while( status == GSL_CONTINUE && iter < max_iter );

	return status;
}