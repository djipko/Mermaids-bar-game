The module memaids.py is a python script representing a simulation of a game usually played in bars on Lamai Beach, Koh Samu, Thailand. I do not know the name of the game sadly.
Game is only played for fun, to pass the time while sipping cold drinks, and sometimes to help with the language barrier. No gambling is involved.

Rules of the game:
Game board consists of 9 foldable fields marked 1 through 9 and comes with 2 standard six sided dice. 
A turn consists of throwing the dice and folding a number that is either on one of the dice thrown or is the sum of both. 
You throw dice untill you cannot fold any more fields, in which case you loose the game, or untill you have folded all the fields in which case you win. 
You play a certain number of games in a row, and then your opponent (usually the waitres working at the bar) does the same, and the person who has more wins is the ultimate winner.

The program below simulates different strategies of choosing which field to fold. 

Note:
The obivous strategy was of course to fold firs the numbers that have the lowest probability to come up by throwing two dice (represented by the min_prob method below). 
By running the simulation with Python's pseudo random number generator in the random module, however this strategy turns out to be effective only about 8% of the time.
What is even more interesting is that if you do not apply this strategy ang go with folding the smallest number each throw (what a friend of mine did) or even a random number
the succes rate falls dramatically to about 2% (4 times!). Bar staff knows this, however non stochastic-savy "farang" (westerners) usually don't and this is why they keep loosing :).

Although I have not tried it, probability calculation should show that maximum probability of winning the game is about 8% as this number was the result of running 10**6 simulations.