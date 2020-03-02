
import json
import copy

#a dictionary of traits
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
            "attack": 2,
            "speed": 1,
            "stealth": 1
        },
        "requires": set([
		    "arms"
        ]),
        "cost": 1
	},
    "legs": {
        "stats": {
            "attack": 1,
            "speed": 1,
            "stealth": 1
        },
		"requires": set([]),
        "cost": 1
    },
    "long legs": {
        "stats": {
            "attack": 1,
            "speed": 2,
            "stealth": 1
        },
        "requires": set([
		    "legs"
        ]),
        "cost": 1
	},
    "teeth": {
        "stats": {
            "attack": 2
        },
		"requires": set([]),
        "cost": 1
    },
    "sharp teeth": {
        "stats": {
            "attack": 4
        },
        "requires": set([
		    "teeth"
        ]),
        "cost": 1
	},
    "fur": {
        "stats": {
            "defense": 1,
            "stealth": 1
        },
		"requires": set([]),
        "cost": 1
    },
    "horn": {
        "stats": {
            "attack": 2
        },
		"requires": set([]),
        "cost": 1
    },
    "eyes": {
        "stats": {
            "spotting": 1
        },
		"requires": set([]),
        "cost": 1
    },
    "good eyes": {
        "stats": {
            "spotting": 2
        },
        "requires": set([
		    "eyes"
        ]),
        "cost": 1
	},
    "compound eyes": {
        "stats": {
            "spotting": 4
        },
        "requires": set([
		    "eyes"
        ]),
        "cost": 1
	},
    "wings": {
        "stats": {
            "speed": 2
        },
		"requires": set([]),
        "cost": 1
    },
    "good wings": {
        "stats": {
            "speed": 3,
            "stealth": 1
        },
        "requires": set([
		    "wings"
        ]),
        "cost": 1
	},
    "shell": {
        "stats": {
            "defense": 2
        },
		"requires": set([]),
        "cost": 1
    },
    "hard shell": {
        "stats": {
            "defense": 4
        },
        "requires": set([
		    "shell"
        ]),
        "cost": 1
	},
    "claws": {
        "stats": {
            "attack": 2
        },
		"requires": set([]),
        "cost": 1
    },
    "sharp claws": {
        "stats": {
            "attack": 4
        },
        "requires": set([
		    "claws"
        ]),
        "cost": 1
	},
    "camouflage": {
        "stats": {
            "stealth": 3
        },
		"requires": set([]),
        "cost": 1
    },
    "ears": {
        "stats": {
            "spotting": 1
        },
		"requires": set([]),
        "cost": 1
    },
    "good ears": {
        "stats": {
            "spotting": 2
        },
        "requires": set([
		    "ears"
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
