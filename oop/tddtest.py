from playerlib import player
import math




def main(input):
	"""
	>>> main(1)
	Nui
	Doe
	John
	Mayer

	"""
	allPlayers = [player(x) for x in ["Nui","Doe","John","Mayer"]]
	for x in allPlayers:
		print x.name
		
if __name__ == "__main__":
	import doctest
	doctest.testmod()
	