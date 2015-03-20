Scripts here perform processing on json arrays to remove structural duplicates or potentially clashing topologies.

Usage:

./combine_json *json > output.json

Should be self-explanatory.

./rm_duplicates.py <input.json> > output.json

Generates a 2D pointmap recreation of the each chain, and compares to to the other chains in the json file. Duplicates are removed, and only unique connectivities are printed to the console (redirect to a file to save).

./rm_neighbors.py <input.json> > output.json

Removes all json strings that have ATs existing at immediately neighboring TRAP binding sites. This is useful for preventing downstream steric clashes when adding ATs to TRAP with 11 potential AT binding sites.

./rm_clashes.py <input.json> <cutoff> > output.json

Generates a simplistic 2D projection of the binding parters, and will discard any chains which have a distance between components less than the provided cutoff.