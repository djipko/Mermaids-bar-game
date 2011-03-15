"""mermaids_bar.py Written by Nikola Dipanov (nikola.djipanov@gmail.com) 
This module is a python script representing a simulation of a game usually played in bars on Lamai Beach, Koh Samu, Thailand.
"""

import random, itertools, datetime
from collections import defaultdict
from optparse import OptionParser

class GameBoard(object):
	"""Class representing a gameboard"""
	def __init__(self, board_size = 9):
		self.board_size = board_size
		self.fields = [i for i in xrange(1, board_size + 1)]
		self.folding_seq = []
		self.game_over = False
	
	def is_folded(self, field):
		if field in xrange(1, self.board_size+1):
			return not field in self.fields
		else:
			raise ValueError, "Not a valid field!"
	
	def fold(self, field):
		if not self.is_folded(field) and not self.game_over:
			self.fields.remove(field)
			self.folding_seq.append(field)
			if not self.fields:
				self.game_over = True
		else:
			raise ValueError, "Not a valid field to fold!"
	
	def left_fields(self):
		return self.fields
	
	def folded_fields(self):
		return [f for f in xrange(1, self.board_size+1) if f not in self.fields]
	
	def give_up(self):
		self.game_over = True
	
	def game_won(self): 
		if self.game_over:
			return not self.fields
		else: 
			return False
	
	def play(self, strategy_func, verbose = False):
		d1, d2 = random.randint(1,6), random.randint(1,6) #Throw dice
		#Get only folding candidates from the current throw that are not folded yet 
		candidates = [c for c in [d1, d2, d1+d2] if c in self.left_fields()] 
		
		if candidates:	#if there are no foldable fields on the board the game is over
			#Chose the field based on the strategy chosen for the game
			field_to_fold = strategy_func(candidates)
			if verbose:
				print "Board: %s; Throw: %d, %d; Folded: %d" %(str(self), d1, d2, field_to_fold)
			#Fold the field
			self.fold(field_to_fold)
			if self.game_won():	#If this was the last folded field the game is won
				if verbose:
					print "Game Over. WON!!!"
				return
			#If the game is not over play another throw (recursively :) )
			self.play(strategy_func, verbose)
		else:
			if verbose:
				print "Board: %s; Throw: %d, %d; Folded: Nothing!\nGame Over. LOST!!!" %(str(self), d1, d2)
			self.give_up()
			return

	def __repr__(self):
		return " ".join([str(f) if f in self.fields else "x" for f in xrange(1, self.board_size+1)])

class Strategies(object):
	"""Class containing play strategies. All it's method's are classmethods 
	and all of them take a list of numbers and return a number contained 
	in this list thet is the choice for the next move. They are meant to be passed 
	as a second parameter to the play method of the GameBoard class above.
	This class is not meant to be instantiated.
	""" 
	
	def __new__(cls):
		raise NotImplementedError, "This class cannot be instantiated"
	
	def _calc_probabilities(seq):
		"""Functions that calculates probabilites for getting each of the numbers 
		in a sequence seq by throwing 2 6-sided dice. Can be generalised to """
		
		outcome_no = 36		#Number of possible outcomes when plating with 2d6
		max_result = 12		#Max number that can be thrown with 2d6
		outcomes = [o for o in itertools.product(xrange(1, 7), repeat=2)] #All possible outcomes of throwing 2d6 as a caretesian product
		probs = []
		for result in seq:
			if result < 1 or result > max_result:
				probs.append(0)
			else:
				def satisfies_result(outcome, res):
					"""Calculates if the oucome of the throw satisfieas the result""" 
					if sum(outcome) == res or res in outcome:
						return True
				probs.append(float(len([o for o in outcomes if satisfies_result(o, result)]))/float(outcome_no))
		return dict(zip(seq, probs))
	
	#Calculate all the probs immediately
	probs_dict = _calc_probabilities(xrange(1, 10))
	
	@classmethod
	def min_prob(cls, candidates):
		return min(candidates, key = lambda c: cls.probs_dict[c])
	
	#No need to define additional funtions to wrap simple min or max calls
	min_die = min
	max_die = max
	
	@staticmethod
	def rand_die(candidates): 
		return candidates[random.randint(0, len(candidates)-1)]

def main():
	#Get all of the methods of the strategies class
	strategies = [method_name for method_name in Strategies.__dict__ if hasattr(getattr(Strategies, method_name), "__call__") and not method_name.startswith("_")]

	parser = OptionParser()
	parser.add_option("-s", "--strategy", dest="strategy", help="Strategy to play. Can be one of the following: " + ", ".join(strategies), )
	parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
	parser.add_option("-n", type="int", dest="num", help="Number of games to play")
	parser.add_option("-f", "--full_stats", action="store_true", dest="full_stats", help="Print full stats.")
	parser.set_defaults(strategy=strategies[0], verbose=False, num=10, full_stats=False)
	
	options, args = parser.parse_args()
	
	if len(args) != 0:
		parser.error("Incorrect number of arguments")
		
	if options.strategy not in strategies:
		parser.error("option s: Unknown strategy")

	boards = []
	strategy_func = getattr(Strategies, options.strategy)
	start_time = datetime.datetime.now()
	for i in xrange(options.num): #Play a certain number of games so we can pull out some stats.
		board = GameBoard()
		board.play(strategy_func, options.verbose)
		boards.append(board)
	end_time = datetime.datetime.now()
	elapsed_time = end_time-start_time
	print "Stats after %d games with strategy %s:" %(options.num, options.strategy)
	won = [b for b in boards if b.game_won()]
	won_no = len(won)
	won_pcent = (float(won_no)/float(options.num))*100
	lost = [b for b in boards if not b.game_won()]
	lost_no = len(lost)
	lost_pcent = (float(lost_no)/float(options.num))*100
	print "Won: %d (%.1f%%), Lost: %d (%.1f%%)" %(won_no, won_pcent, lost_no, lost_pcent)
	print "Time elapsed: %s" %elapsed_time
	if options.full_stats:
		cnt_d = defaultdict(int)
		#Calculate the number of games lost according to the number of fields left
		for b in lost: 
			cnt_d[len(b.left_fields())] +=1
		#Calculate the percentge of lost games per each number of fields left
		pcnt_d = dict([( fields_no, (float(cnt_d[fields_no])/float(lost_no))*100 ) for fields_no in cnt_d])
		print "Lost games according to no. of fields left:"
		print ", ".join([ "%d: %d (%.1f%%)" %(fc, cnt_d[fc], pcnt_d[fc]) for fc in cnt_d])
		
if __name__ == "__main__":
	main()