
from Species import Species
from Environment import Environment

class GameState(object):
	def __init__(self):
		self.sp_player = self.initialize_player()
		self.sp_ai = [self.initialize_species([], 100, 1)] #start with just one ai opponent

		self.all_sp = [self.sp_player] + self.sp_ai

		self.environment = self.initialize_environment()

	def initialize_player(self):
		# Should hold logic for player-controlled species initialization
		sp_player = self.initialize_species([], 100, 1)
		print("Created player species: ", sp_player)
		return sp_player


	def initialize_species(self, traits, population, consumption):
		# Should hold logic for species initialization
		sp = Species(traits, population, consumption)
		print("Created species: ", sp)
		return sp


	def initialize_environment(self):
		# Should hold logic for environment initialization
		env = Environment(1000)
		print("Created environment: ", env)
		return env

	def is_over(self):
		# Should return whether or not a game is over or not, dependent upon
		# whether or completion conditions have been met
		print("is_over() is not implemented")

	def display_player_choices(self):
		# Should display the current state of the player species, how many evolution
		# points they have, and the potential evolutions that they can take from
		# the current species state
		print("display_player_choices() is not yet implemented")

	def modify_species(self, mod, index):
		# Should apply the chosen evolution to the specified species (player is index 0)
		

		print("modify_species() is not implemented")

def evolve_player(state):
	
	#state.modify_species(read_input(), 0)

	print("evolve_player() is not implemented")

def read_input():
	# Should read player choice about which evolution to take, or any other
	# inputs we choose the allow the player to feed in, and ensure that it
	# is an appropriate input
	print("read_input() is not yet implemented")

def evolve_ai(state):
	# Should make the evolution choices for the AI controlled species

	for ai in state.sp_ai:
		random_evolve(ai)  # can later implement different evolve functions for different ai species (ex: random evolution, greedy evolution, etc.)

	print("evolve_ai() is not implemented")

def random_evolve(species):
	#state.modify_species(  , ai)
	print("random_evolve() is not implemented")



def execute_turn(state):
	# Should simulate the interactions/competitions between all the species

	#Lotka Volterra competition model, works only for competition between two species right now

	# first species 
	for sp1 in state.all_sp:
		growth_rate = ( sp1.stats['birthrate'] - sp1.stats['deathrate'] ) / sp1.population_size
		# temporary formula for carrying capcity(?)... should find what works best later
		carrying_capacity = state.environment.resources / sp1.consumption_rate 

		# second species to compete with
		for sp2 in filter(lambda sp: sp != sp1, state.all_sp):
			# temporary formula for constant... should find what works best later
			competition_constant = sp1.stats['speed'] * (sp1.stats['attack'] + sp1.stats['defense']) / ( sp2.stats['speed'] * (sp2.stats['attack'] + sp2.stats['defense']) )
			
			# dN1/dt = (r * N1) * (1 - (N1 + c * N2) / K)
			population_change = (growth_rate) * sp1.population_size * (1 - (sp1.population_size + competition_constant * sp2.population_size)/carrying_capacity)

			'''
			print("c: ", competition_constant)
			print("K: ", carrying_capacity)
			print("dN/dt: " , population_change)
			'''

			sp1.population_size += population_change

def print_results():
	# Should print the important information about the turn that just occured.
	# It's possible we want this to occur in execute_turn() and this function
	# is unnecessary
	print("Updated species: ", list(map(lambda sp: int(sp.population_size), state.all_sp)))

if __name__ == "__main__":
	state = GameState()
	turn_counter = 20 # We may not want this, for now just here so the loop eventually terminates

	while not state.is_over() and turn_counter > 0:

		# player chooses how to evolve their species
		evolve_player(state)

		# ai chooses how to evolve their species
		evolve_ai(state) 

		# a round is played with all the species
		execute_turn(state)

		# results of the round are printed to the player 
		print_results()

		turn_counter -= 1


	print("Game over, thanks for playing")