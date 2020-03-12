
from Species import Species
from Species import traits
from Environment import Environment
from BT_Nodes import Selector, Sequence, Action, Check
from random import choice
from time import time
from math import floor, ceil

class GameState(object):
	def __init__(self):
		'''
		self.sp_player = self.initialize_player()
		self.sp_ai = [self.initialize_species([], 100, 1)] #start with just one ai opponent
		'''
		print("Initializing new game...")

		self.environment = self.initialize_environment()

		#self.all_sp = [Species([], 100, 2), Species([], 100, 1)]
		# self.all_sp = [self.initialize_player(), self.initialize_species([], 100, 1)]
		self.all_sp = [self.initialize_player()]
		for _ in range(0, 3):
			sp = self.initialize_species([], 100, 1)
			self.all_sp.append(sp)
		self.player_index = 0
		self.player = self.all_sp[self.player_index]

		print()

	def initialize_player(self):
		# Should hold logic for player-controlled species initialization
		sp_player = Species([], 100, 1, "Player's species")
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

		if len(self.all_sp) == 1:
			return True

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
	species.curr_stat = -1
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
	num_sp = len(state.all_sp)
	num_loss = 0
	total_loss_mag = 0
	avg_loss_mag = 0

	ai.curr_stat += 1
	stat = ai.priorities[ai.curr_stat]
	for other in state.all_sp:
		if other == ai:
			continue
		if ai.stats[stat] < other.stats[stat]:
			num_loss += 1
			total_loss_mag += other.stats[stat] - ai.stats[stat]


	# Perform check
	if num_loss != 0:
		avg_loss_mag = total_loss_mag / num_loss
	# print("STAT:", stat, "LOSS MAG:", avg_loss_mag, "TOTAL LEN:", num_sp, "NUM LOSS:", num_loss) 

	MAG_THRESHOLD = 3 # Adjust if needed
	mag_check = avg_loss_mag > MAG_THRESHOLD
	loss_check = (num_sp/4) < num_loss < ((3*num_sp)/4)

	result = not (loss_check and mag_check) # Change to 'or' if needed
	# print("RESULT:", result)
	return result

def evolve_stat(state, ai):
	desired_stat = ai.priorities[ai.curr_stat]
	possible_evo_all = evolutions(species)

	possible_evo = {}
	for evo in possible_evo_all:
		if desired_stat in traits[evo]['stats']:
			possible_evo[evo] = traits[evo]

	print('WANT:', desired_stat)
	print('OPTIONS:', possible_evo)

	poss_evo_len = len(possible_evo)

	for _ in range(0, poss_evo_len):
		# Find best possible trait ignoring cost
		trait, stats = max(possible_evo.items(), key=lambda x: x[1]['stats'][desired_stat])
		print('TRY:', trait, stats)
		possible_evo.pop(trait)

		# Try to buy
		if ai.add_trait(trait):
			return True

	return False

def no_evolution(state, ai):
	ai.curr_stat += 1
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

	# Environment grazing (determine ordering of who eats first by size)
	for sp in sorted(state.all_sp, key=lambda x: x.stats["size"]):
		eaten_amt = min(sp.consumption_rate * sp.population_size, state.environment.resources)
		state.environment.resources -= eaten_amt
		sp.consume_food(eaten_amt)
		print(sp.name, "GRAZES FOR", floor(eaten_amt), "WORTH OF FOOD")


	# Simulate population changes with Lotka-Volterra Model
		# Predator-Prey Model: Each species selects random other for prey 
		# Interspeciic Model: Every species competes for natural resources 

	species_to_remove = []
	for sp1 in state.all_sp:
		
		# Calculate base population change
		growth_rate = ( sp1.stats['birthrate'] / 100 ) - ( sp1.stats['deathrate'] / 100 )

		# list of all species that sp1 can compete with
		competing_species = list(filter(lambda sp: sp != sp1, state.all_sp))

		# number of sp1 predators fed with prey
		predators_fed = 0

		''' 
		Lotka-Volterra Predator-Prey Model : 
			dN1/dt =  r1 * N1 -  e  * N1N2     
			dN2/dt = -m2 * N2 + e/c * N1N2 
				c : capture efficiency 
		'''

		# Assign predator
		predator = sp1

		# Determine possible preys
		pred_rating = predator.rand_sized_stat("attack")
		preys = list(filter(lambda prey: prey.rand_sized_stat("attack") < pred_rating, competing_species))

		# Choose random prey and hunt
		if preys:
			prey = choice(preys)

			# Calculate size advantage
			pred_size_advntg = predator.stats["size"] / prey.stats["size"]

			# Calculate penalties for stealth, speed, defense checks
			penalties = {}
			penalties["stealth"] = predator.rand_sized_stat("spotting", True) - prey.rand_sized_stat("stealth", True)
			penalties["speed"] = predator.rand_sized_stat("speed") - prey.rand_sized_stat("speed")
			penalties["defense"] = predator.rand_sized_stat("attack") - prey.rand_sized_stat("defense")

			# Calculate total capture_efficiency
			# TODO Might need testing and adjusting
			capture_efficiency = 0
			for _, penalty in penalties.items():
				capture_efficiency += penalty 
			capture_efficiency = (capture_efficiency + pred_size_advntg) / 10000 

			prey_killed = min(max((capture_efficiency) * prey.population_size * predator.population_size, 0), prey.population_size)
			prey.population_size -= prey_killed
			predators_fed = prey_killed * prey.stats["size"] / predator.consumption_rate

			if prey_killed > 0:
				print(predator.name, "hunted for", ceil(prey_killed), prey.name)
				print(prey.name, "fed", ceil(predators_fed), "of", predator.name)


		'''
		Lotka-Volterra Interspecific Competition Model : 
			dN1/dt = (r * N1) * (1 - (N1 + c * N2) / K)
				c : competition constant
				K : carrying capacity
		'''

		# Sum of competing species' competition stats
		competition_denominator = 0

		# Sum of population of competitotrs
		competitors_population = 0

		# Calculate competitors' stats 
		for sp2 in competing_species:

			competition_denominator += sp2.stats['speed'] * (sp2.stats['attack'] + sp2.stats['defense'])
			competitors_population += sp2.population_size

		# formula for carrying capcity , modify as needed
		carrying_capacity = ( state.environment.resources / sp1.consumption_rate ) + predators_fed

		# formula for competition constant , modify as needed
		competition_constant = sp1.stats['speed'] * (sp1.stats['attack'] + sp1.stats['defense']) / ( competition_denominator )
		
		# dN1/dt = (r * N1) * (1 - (N1 + c * N2) / K)
		if carrying_capacity == 0:
			carrying_capacity = 1
		population_change = (growth_rate) * sp1.population_size * (1 - (sp1.population_size + competition_constant * competitors_population)/carrying_capacity)
		
		'''
		print("c: ", competition_constant)
		print("K: ", carrying_capacity)
		print("dN/dt: " , population_change)
		'''

		# Apply population penalty for missing consumption goal
		consumption_penalty = sp1.use_food() / 2

		sp1.population_size -= sp1.population_size * consumption_penalty
		sp1.population_size += population_change

		if sp1.population_size <= 0 or sp2.population_size <= 0:
			species_to_remove.append(sp1)
	
	# End game with player loss
	if state.all_sp[state.player_index] in species_to_remove:
		print('Player species has perished. Game over!')
		exit(1)
	
	# Remove dead species
	for sp in species_to_remove:
		print(sp.name, "has perished!")
		state.all_sp.remove(sp)

	# Environment resource regain
	state.environment.resources += state.environment.resource_gain

	# Print execution time
	time_diff = floor(time() - start_time)
	if time_diff < 1:
		print("Executed in less than one second")
	else:
		print("Executed in", time_diff, "seconds")

def print_results():
	# Should print the important information about the turn that just occured.
	# It's possible we want this to occur in execute_turn() and this function
	# is unnecessary
	print("Updated species: ", list(map(lambda sp: int(floor(sp.population_size)), state.all_sp)))
	print("")

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

		# ai evolution
		for species in state.all_sp:
			if species != state.player:
				bt_evolve(state, species)

		# a round is played with all the species
		execute_turn(state)

		cur_turn += 1
		print()

	print("Winner: ", state.winner)
	print("Game over, thanks for playing")