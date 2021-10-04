#################################
#	   Introduction		#
#################################

This project was one completed in an AI class in which I was tasked to build the framework off of which two
agents in a game of chess would compete with each other.
The culmination of all we had learned that semester, this project was the successful implementation of an advanced
algorithm meant to incentivize taking pieces and protecting the king by planning out all possible move sets some _n_
moves in advance.
This was further refined using a time-limited minimax determiner with alpha-beta pruning and a heuristic evaluator.


#################################
#       Compiling & Running	#
#################################

You have been provided a bash script called `play.sh`, which compiles and runs your code; it also starts a game session between your AI and itself. DO NOT MODIFY THIS SCRIPT.
You can run `play.sh` using the following command format :

	./play.sh Joueur.<lang> Session_ID

Where `Joueur.<lang>` is the directory for the language you are coding in. An example of the above command for c++ would be :

	./play.sh Joueur.cpp AIisAwesome
