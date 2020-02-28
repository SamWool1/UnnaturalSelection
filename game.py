
class GameState(object):
	def __init__(self):
		self.sp_player = self.initialize_player()
		self.sp_ai = self.initialize_ai()
		self.environment =self.initialize_environment()

	def initialize_player(self):
		# Should hold logic for player-controlled species initialization
		print("initialize_player() has not been implemented yet")

	def initialize_ai(self):
		# Should hold logic for AI species initialization
		print("initialize_ai() has not been implemented yet")
		return [] # so execute doesn't crash while this is unimplemented

	def initialize_environment(self):
		# Should hold logic for environment initialization
		print("initialize_environment() has not been implemented yet")

	def is_over(self):
		# Should return whether or not a game is over or not, dependent upon
		# whether or completion conditions have been met
		print("is_over() is not implemented")

	def display_player_choices(self):
		# Should display the current state of the player species, how many evolution
		# points they have, and the potential evolutions that they can take from
		# the current species state
		print("display_player_choices() is not yet implemented")

	def modify_player(self, mod):
		# Should apply the chosen evolution of the player species
		print("modify_player() is not implemented")

	def modify_ai(self, mod, index):
		# Should apply the chosen evolution to the specified AI species ('index')
		print("modify_ai() is not implemented")

def execute_turn(state):
	for ai in state.sp_ai:
		state.modify_ai(simulate_ai_turn(ai), ai)
	playout()
	print_results()
	print("execute_turn() is not implemented")

def simulate_ai_turn(ai):
	# Should make the evolution choices for the AI controlled species
	print("simulate_ai_turn() is not implemented")

def playout():
	# Should simulate the interactions/competitions between all the species
	print("playout() is not implemented")

def print_results():
	# Should print the important information about the turn that just occured.
	# It's possible we want this to occur in execute_turn() and this function
	# is unnecessary
	print("print_results() is not implemented")

def read_input():
	# Should read player choice about which evolution to take, or any other
	# inputs we choose the allow the player to feed in, and ensure that it
	# is an appropriate input
	print("read_input() is not yet implemented")

if __name__ == "__main__":
	state = GameState()
	turn_counter = 20 # We may not want this, for now just here so the loop eventually terminates

	while not state.is_over() and turn_counter > 0:
		state.display_player_choices()
		mod = read_input()
		state.modify_player(mod)
		execute_turn(state)
		turn_counter -= 1

	print("Game over, thanks for playing")