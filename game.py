
from Species import Species
from Species import traits
from Environment import Environment
from BT_Nodes import Selector, Sequence, Action, Check
from random import choice
from time import time
from math import floor

class GameState(object):
	def __init__(self):
		'''
		self.sp_player = self.initialize_player()
		self.sp_ai = [self.initialize_species([], 100, 1)] #start with just one ai opponent
		'''
		print("Initializing new game...")

		self.environment = self.initialize_environment()

		#self.all_sp = [Species([], 100, 2), Species([], 100, 1)]
		self.all_sp = [self.initialize_player(), self.initialize_species([], 100, 1)]
		self.player_index = 0
		self.player = self.all_sp[self.player_index]

		print()


	def initialize_player(self):
		# Should hold logic for player-controlled species initialization
		sp_player = Species([], 100, 2, "Player's species")
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

		maxSp = max(self.all_sp, key = lambda sp: sp.population_size)
		self.winner = maxSp

		for sp1 in self.all_sp:
			if maxSp.population_size < 100 + sp1.population_size:
				return False
		
		return True

	def display_player_choices(self):
		# Should display the current state of the player species, how many evolution
		# points they have, and the potential evolutions that they can take from
		# the current species state
		print("display_player_choices() is not yet implemented")

	def modify_species(self, mod, index):
		# Should apply the chosen evolution to the specified species (player is index 0)
		self.all_sp[index].add_trait(mod)


def evolve_player(state, mod):
	# Should evolve the species controlled by the player
	state.modify_species(mod, 0)

def read_input(state):
	# Environment stat print
	print("Environment currently has", int(state.environment.resources), "units worth of food")

	# Should read player choice about which evolution to take, or any other
	# inputs we choose the allow the player to feed in, and ensure that it
	# is an appropriate input

	# find all the evolution options for the species
	possible_evolutions = evolutions(state.all_sp[0])

	# print all information about the player species, AI species, and possible
	# evolutions to be selected
	print("Your species: ")
	print(state.all_sp[0])
	print("AI species: ")
	for ai in state.all_sp[1:]:
		print(ai)
	print("Your evolution options: ")
	for ev in possible_evolutions:
		print("Evolution: ", ev)
		print("    Cost: ", traits[ev]["cost"], "| Stats: ", traits[ev]["stats"])
	print("Points available:", state.all_sp[0].evo_points)

	while possible_evolutions:
		read = input("Choose an evolution for species or type 'quit' to quit ('none' for no evolution): ")
		if read in possible_evolutions or read == "quit" or read == "none":
			return read
		else:
			print()
			print("Please enter the name of one of the evolution options or type 'quit' to quit")

	print("No Evolution Options")

def evolutions(species):
	# Should find all the possible evolutions the species can take
	evolutions = []

	#filter through traits to get what the species doesnt already have, what the species can afford, and what the species has all the requirements for
	evolutions = list(
		filter(lambda trait: traits[trait]['requires'].issubset(species.traits), 
			filter(lambda trait: traits[trait]['cost'] <= species.evo_points, 
				filter(lambda trait: trait not in species.traits, traits.keys()))))

	return evolutions

def bt_evolve(state, species):
	root = Selector(name="Top Level Trait Selection")

	for priority in species.priorities:
		stat = Sequence(name="Stat " + priority)
		desirable = Check(is_desirable)
		evolve = Action(evolve_stat)
		stat.child_nodes = [desirable, evolve]
		root.child_nodes.append(stat)

	root.child_nodes.append(Action(no_evolution))
	root.execute(state, species)

# TODO: Placeholders for necessary logic for BT, for now return True as a default
#       so that everything will behave nice. May want to extract to a different file
def is_desirable(state, ai):
	return True

def evolve_stat(state, ai):
	return True

def no_evolution(state, ai):
	return True

def evolve_ai(state):
	# Should make the evolution choices for the AI controlled species

	evolution = random_evolve(state.all_sp[1])
	if evolution:
			state.modify_species(evolution, 1)  # can later implement different evolve functions for different ai species (ex: random evolution, greedy evolution, etc.)


def random_evolve(species):
	possible_evolutions = evolutions(species)

	if possible_evolutions:
		return choice(possible_evolutions)


def execute_turn(state):
	# Should simulate the interactions/competitions between all the species

	print("Executing Turn...")
	start_time = time()

	#Lotka Volterra competition model, works only for competition between two species right now
	# TODO Species hunting
	for sp in state.all_sp:
		pass

	# Environment grazing (determine ordering of who eats first by size)
	for sp in sorted(state.all_sp, key=lambda x: x.stats["size"]):
		eaten_amt = min(sp.consumption_rate * sp.population_size, state.environment.resources)
		state.environment.resources -= eaten_amt
		# sp.consume_food(eaten_amt)
		print(sp.name, "GRAZES FOR", int(sp.consume_food(eaten_amt)), "WORTH OF FOOD")

	# first species 
	species_to_remove = []
	for sp1 in state.all_sp:
		# Calculate base population change
		growth_rate = ( sp1.stats['birthrate'] - sp1.stats['deathrate'] ) / sp1.population_size

		#sum of competing species competition stats
		competition_denominator = 0

		#sum of population of competitotrs
		competitors_population = 0

		#amount of food gained from hunting
		hunted_food = 0

		# find species to compete with
		for sp2 in filter(lambda sp: sp != sp1, state.all_sp):

			#hunted_food += species_encounter(sp1, sp2)

			competition_denominator += sp2.stats['speed'] * (sp2.stats['attack'] + sp2.stats['defense'])
			
			competitors_population += sp2.population_size


		# formula for carrying capcity , modify as needed
		carrying_capacity = (state.environment.resources + hunted_food) / sp1.consumption_rate 

		# formula for competition constant , modify as needed
		competition_constant = sp1.stats['speed'] * (sp1.stats['attack'] + sp1.stats['defense']) / ( competition_denominator )
		
		# dN1/dt = (r * N1) * (1 - (N1 + c * N2) / K)
		population_change = (growth_rate) * sp1.population_size * (1 - (sp1.population_size + competition_constant * competitors_population)/carrying_capacity)

		'''
		print("c: ", competition_constant)
		print("K: ", carrying_capacity)
		print("dN/dt: " , population_change)
		'''

		# Apply population penalty for missing consumption goal
		consumption_penalty = sp1.use_food() / 2

		sp1.population_size -= floor(sp1.population_size * consumption_penalty)
		sp1.population_size += floor(population_change)

		if sp1.population_size <= 0:
			species_to_remove.append(sp1)
	
	# End game with player loss
	if state.all_sp[state.player_index] in species_to_remove:
		print('Player species has perished. Game over!')
		exit(1)
	
	# Remove dead species
	for sp in species_to_remove:
		state.all_sp.remove(sp)

	# Environment resource regain
	state.environment.resources += state.environment.resource_gain

	# Print execution time
	time_diff = floor(time() - start_time)
	if time_diff < 1:
		print("Executed in less than one second")
	else:
		print("Executed in", time_diff, "seconds")

	
	# Determines outcome of a species encountering and hunting another
	#
	# TODO: Modify to look through species array, determine a single prey species
	# which it can "hunt", dependent upon their attack power relative to the potential
	# prey species attack power
	def species_encounter(species_a, species_b):
		# Determine predator and prey
		predator, prey = None, None
		pred_rating_a = species_a.rand_sized_stat("attack")
		pred_rating_b = species_b.rand_sized_stat("attack")

		if (pred_rating_a < pred_rating_b):
			prey = species_a
			predator = species_b
		else:
			prey = species_b
			predator = species_a		
		pred_size_advntg = predator.stats["size"] / prey.stats["size"]

		# Calculate penalties for stealth, speed, defense checks
		penalties = {}
		penalties["stealth"] = max(prey.rand_sized_stat("stealth", True) - predator.rand_sized_stat("spotting", True), 0)
		penalties["speed"] = max(prey.rand_sized_stat("speed") - predator.rand_sized_stat("speed"), 0)
		penalties["defense"] = max(prey.rand_sized_stat("defense") - predator.rand_sized_stat("attack"), 0)

		# Calculate total overall penalty
		# TODO Will need testing and adjusting
		total_penalty = 0
		for _, penalty in penalties.items():
			total_penalty = (penalty * 10) + total_penalty

		# Reduce prey population, adjusted by penalty for failing checks and size, to represent hunting
		# Put cap on individuals hunted relative to amount of food needed by predators
		individuals_hunted = max(pred_size_advntg * predator.population_size - total_penalty, 0)
		prey.population_size = prey.population_size - individuals_hunted

		# Return inds hunted times prey size to represent food obtained
		return individuals_hunted * prey.stats["size"]

if __name__ == "__main__":
	state = GameState()
	max_turn = 10
	cur_turn = 0

	while not state.is_over() and cur_turn < max_turn:
		print("Turn ", cur_turn)
		# read player input
		mod = read_input(state)
		if mod == "quit":
			break

		if mod:
			# player chooses how to evolve their species
			evolve_player(state, mod)

		# a round is played with all the species
		for species in state.all_sp:
			if species != state.player:
				bt_evolve(state, species)

		cur_turn += 1
		print()


	print("Game over, thanks for playing")