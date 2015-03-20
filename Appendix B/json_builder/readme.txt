This program creates a library of AT/TRAP connectivities at a given number of AT and TRAP components.

Usage:

./determinate<n> [# TRAP] (# AT)

Generates all possible TRAP-AT connectivities, assuming <n> sites on TRAP (either five or eleven).

Note: The number of AT is optional. Leaving out this value will result in the creation of chains with up to the maximum amount of ATs possible. (i.e. saturating all available TRAP sites for all configurations)

./random<n> [# TRAP] [# AT] [# chains]

Generates a specified number of chains with random TRAP-AT connectivities, assuming <n> sites on TRAP.

Both of these programs generate a JSON file (output.json) containing the topology for each created chain.

