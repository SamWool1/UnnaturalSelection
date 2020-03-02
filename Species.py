
import json
import copy

traits = {
    "arms": {
        "stats": {
            "attack": 1,
            "speed": 1,
            "stealth": 1
        },
		"requires": set([]),
        "cost": 1
      },
    "long arms": {
        "stats": {
            "attack": 1,
            "speed": 1,
            "stealth": 1
        },
        "requires": set([
		    "arms"
        ]),
        "cost": 1
	}
}

# Basic skeleton for Species class - feel free to modify as needed
class Species(object):
    # Stats and data on this species
    stats = {}  # Species stats
    population_size = 0
    consumption_rate = 1.  # Determines food needed + evo points gained
    traits = set([])  # List of traits for this species

    def __init__(self, initial_traits, initial_pop_size, initial_cons_rate):
        self.stats = {
            "attack": 1.,
            "defense": 1.,
            "speed": 1.,
            "stealth": 1.,
            "size": 1.,
            "birthrate": 20.,  # might not default to 1. in future
            "deathrate": 10.,  # same as above
            "spotting": 1.,
        } # This species' stats. Default to 1.

        self.traits = set([])

        self.population_size = initial_pop_size
        self.consumption_rate = initial_cons_rate
        
        for trait in self.traits:
            self.add_trait(trait)

    def __repr__(self):
        # method for string representing the species

        return ' '.join(["[", "Population:", str(self.population_size), ", Stats:", str(self.stats),  "]"])

    # Functions to modify this species
    # Add a trait and modify species according to what the trait is
    def add_trait(self, trait):
        mod_stats = traits[trait]['stats']

        for stat in self.stats:
            if stat in mod_stats:
                self.stats[stat] = sum(d[stat] for d in [self.stats, mod_stats])

        self.traits.add(trait)

    # TODO: stuff related to evo pts, death/birthrates, changing stats, and more
