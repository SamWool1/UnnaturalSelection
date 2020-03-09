import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    #if len(state.my_fleets()) >= 1:
        #return False
    print('attack')

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    #if len(state.my_fleets()) >= 1:
        #return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 3)
        

#calculate the weight of a node (planet) based on planet size, distance, and planet score
def calculate_planet_weight(state, source):
    planet_weights = {}
    
    for planet in state.not_my_planets():
        planet_weights[planet] = planet.growth_rate *10 - state.distance(source, planet.ID) - planet.num_ships
        #print(state.distance(source, planet.ID))
        #planet_weights[planet] = planet['growth_rate'] - distance(source, planet) - planet['num_ships']
        
    return planet_weights
    
#select planet with the highest weight as the target and send fleets to it
def attack_best_planet(state):
    #pick my strongest planet to send fleets
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    #strongest_planet = planet(strongest_planet)
    
    if not strongest_planet:
        return False
    
    #out of all the planets in the game, pick the one with the highest weight as the target
    all_planet_weights = calculate_planet_weight(state, strongest_planet.ID)
    #target_planet = max(all_planet_weights)
    maximum = -9999
    target_planet = ()
    for planet in all_planet_weights:
        if all_planet_weights[planet] > maximum:
            maximum = all_planet_weights[planet]
            target_planet = planet
    #return decision
    if not strongest_planet or not target_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, target_planet.ID, strongest_planet.num_ships / 2)
    

