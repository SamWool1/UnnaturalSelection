
from Species import Species
from Species import traits
from Environment import Environment
from random import choice

class GameState(object):
	def __init__(self):
		'''
		self.sp_player = self.initialize_player()
		self.sp_ai = [self.initialize_species([], 100, 1)] #start with just one ai opponent
		'''

		self.environment = self.initialize_environment()

		#self.all_sp = [Species([], 100, 2), Species([], 100, 1)]
		self.all_sp = [self.initialize_player(), self.initialize_species([], 100, 1)]


	def initialize_player(self):
		# Should hold logic for player-controlled species initialization
		sp_player = self.initialize_species([], 100, 2)
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
		#print("is_over() is not implemented")
		pass

	def display_player_choices(self):
		# Should display the current state of the player species, how many evolution
		# points they have, and the potential evolutions that they can take from
		# the current species state
		print("display_player_choices() is not yet implemented")

	def modify_species(self, mod, index):
		# Should apply the chosen evolution to the specified species (player is index 0)
		self.all_sp[index].add_trait(mod)


def evolve_player(state):
	# Should evolve the species controlled by the player

	mod = read_input(state)
	if mod:
		state.modify_species(mod, 0)

def read_input(state):
	# Should read player choice about which evolution to take, or any other
	# inputs we choose the allow the player to feed in, and ensure that it
	# is an appropriate input

	# find all the evolution options for the species
	possible_evolutions = evolutions(state.all_sp[0])

	while possible_evolutions:
		# print all the evolutions options for the species
		print("Evolution options: ")
		print(possible_evolutions)   # can add printing more info later
		evolution = input("Choose an evolution for species: ")
		if (evolution in possible_evolutions):
			return evolution
		else:
			print("Please enter the name of one of the evolution options")

	print("No Evolution Options")

def evolutions(species):
	# Should find all the possible evolutions the species can take
	evolutions = []

	#filter through traits to get what the species doesnt already have, what the species can afford, and what the species has all the requirements for
	evolutions = list(
		filter(lambda trait: traits[trait]['requires'].issubset(species.traits), 
			filter(lambda trait: traits[trait]['cost'] <= species.population_size, 
				filter(lambda trait: trait not in species.traits, traits.keys()))))

	#print("possible evolutions:", evolutions)
	#print("current traits: ", species.traits)

	return evolutions


def evolve_ai(state):
	# Should make the evolution choices for the AI controlled species

	evolution = random_evolve(state.all_sp[1])
	if evolution:
			state.modify_species(evolution, 1)  # can later implement different evolve functions for different ai species (ex: random evolution, greedy evolution, etc.)

	'''
	i = 1

	while i < len(state.all_sp):
		evolution = random_evolve(state.all_sp[i])
		if evolution:
			state.modify_species(evolution, i)  # can later implement different evolve functions for different ai species (ex: random evolution, greedy evolution, etc.)
		i += 1
		'''

def random_evolve(species):
	possible_evolutions = evolutions(species)

	if possible_evolutions:
		return choice(possible_evolutions)


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
	turn_counter = 2 # We may not want this, for now just here so the loop eventually terminates

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