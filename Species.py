
import json
import copy
import random

#a dictionary of traits
traits = {
    "arms": {
        "stats": {
            "attack": 1,
            "speed": 1,
            "stealth": 1,
            "size": 1
        },
		"requires": set([]),
        "cost": 2
    },
    "long arms": {
        "stats": {
            "attack": 2,
            "speed": 1,
            "stealth": 1,
            "size": 2
        },
        "requires": set([
		    "arms"
        ]),
        "cost": 4
	},
    "strong arms": {
        "stats": {
            "attack": 3,
            "stealth": -1,
            "size": 1
        },
        "requires": set([
		    "arms"
        ]),
        "cost": 4
	},
    "legs": {
        "stats": {
            "attack": 1,
            "speed": 1,
            "stealth": 1,
            "size": 1
        },
		"requires": set([]),
        "cost": 2
    },
    "long legs": {
        "stats": {
            "attack": 1,
            "speed": 3,
            "stealth": 1,
            "birthrate": -1,
            "size": 2
        },
        "requires": set([
		    "legs"
        ]),
        "cost": 4
	},
    "strong legs": {
        "stats": {
            "attack": 2,
            "speed": 3,
            "stealth": -2,
            "birthrate": -1,
            "size": 1
        },
        "requires": set([
		    "legs"
        ]),
        "cost": 4
	},
    "mouth": {
        "stats": {
            "attack": 1
        },
		"requires": set([]),
        "cost": 1
    },
    "teeth": {
        "stats": {
            "attack": 2
        },
		"requires": set([
            "mouth"
        ]),
        "cost": 1
    },
    "sharp teeth": {
        "stats": {
            "attack": 4
        },
        "requires": set([
		    "teeth"
        ]),
        "cost": 2
	},
    "poison": {
        "stats": {
            "attack": 4,
            "defense": 1
        },
        "requires": set([]),
        "cost": 10
	},
    "fur": {
        "stats": {
            "defense": 1,
            "stealth": 1
        },
		"requires": set([]),
        "cost": 1
    },
    "thick fur": {
        "stats": {
            "defense": 2,
            "stealth": 1
        },
		"requires": set([
            "fur"
        ]),
        "cost": 2
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
        "cost": 2
	},
    "compound eyes": {
        "stats": {
            "spotting": 10
        },
        "requires": set([
		    "good eyes"
        ]),
        "cost": 10
	},
    "night vision": {
        "stats": {
            "spotting": 5
        },
        "requires": set([
		    "eyes"
        ]),
        "cost": 4
	},
    "wings": {
        "stats": {
            "speed": 2,
            "size": 2
        },
		"requires": set([]),
        "cost": 2
    },
    "strong wings": {
        "stats": {
            "speed": 3,
            "stealth": 1,
            "size": 3
        },
        "requires": set([
		    "wings", "feathers"
        ]),
        "cost": 3
	},
    "light wings": {
        "stats": {
            "speed": 2,
            "stealth": 2
        },
        "requires": set([
		    "wings"
        ]),
        "cost": 3
	},
    "shell": {
        "stats": {
            "defense": 2,
            "size": 1
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
        "cost": 2
	},
    "claws": {
        "stats": {
            "attack": 2
        },
		"requires": set([
            "arms"
        ]),
        "cost": 1
    },
    "sharp claws": {
        "stats": {
            "attack": 4
        },
        "requires": set([
		    "claws"
        ]),
        "cost": 2
	},
    "camouflage": {
        "stats": {
            "stealth": 3
        },
		"requires": set([]),
        "cost": 2
    },
    "changable camouflage": {
        "stats": {
            "stealth": 5
        },
		"requires": set([
            "camouflage"
        ]),
        "cost": 5
    },
    "mimicry": {
        "stats": {
            "stealth": 2
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
        "cost": 2
	},
    "tail": {
        "stats": {
            "speed": 1,
            "stealth": 1
        },
		"requires": set([]),
        "cost": 2
    },
    "nose": {
        "stats": {
            "spotting": 1
        },
		"requires": set([]),
        "cost": 1
    },
    "good nose": {
        "stats": {
            "spotting": 3
        },
		"requires": set([
            "nose"
        ]),
        "cost": 2
    },
    "antenna": {
        "stats": {
            "spotting": 2
        },
		"requires": set([]),
        "cost": 1
    },
    "tough skin": {
        "stats": {
            "defense": 1
        },
		"requires": set([]),
        "cost": 1
    },
    "super tough skin": {
        "stats": {
            "defense": 3
        },
        "requires": set([
		    "tough skin"
        ]),
        "cost": 2
	},
    "feathers": {
        "stats": {
            "defense": 1,
            "speed": 1
        },
		"requires": set([]),
        "cost": 1
    },
    "pretty feathers": {
        "stats": {
            "birthrate": 2
        },
        "requires": set([
		    "feathers"
        ]),
        "cost": 5
	},
    "gorgeous feathers": {
        "stats": {
            "stealth": -2,
            "birthrate": 5
        },
        "requires": set([
		    "pretty feathers"
        ]),
        "cost": 5
	},
    "fluffy feathers": {
        "stats": {
            "defense": 2
        },
        "requires": set([
		    "feathers"
        ]),
        "cost": 3
	},
    "ultra fluffy feathers": {
        "stats": {
            "defense": 1,
            "stealth": 2,
        },
        "requires": set([
		    "fluffy feathers"
        ]),
        "cost": 5
	},
    "sleek feathers": {
        "stats": {
            "speed": 4
        },
        "requires": set([
		    "feathers"
        ]),
        "cost": 5
	},
    "echolocation": {
        "stats": {
            "spotting": 5
        },
        "requires": set([
		    "ears", "mouth"
        ]),
        "cost": 5
	},
    "scales": {
        "stats": {
            "defense": 1,
            "speed": 1,
            "stealth": 1
        },
		"requires": set([]),
        "cost": 2
    },
    "pretty scales": {
        "stats": {
            "defense": 1,
            "stealth": -1,
            "birthrate": 2
        },
		"requires": set([
            "scales"
        ]),
        "cost": 5
    },
    "nails": {
        "stats": {
            "attack": 1,
            "defense": 1,
        },
		"requires": set([
            "arms", "legs"
        ]),
        "cost": 1
    },
    "stinger": {
        "stats": {
            "attack": 3,
            "size": 1
        },
		"requires": set([]),
        "cost": 5
    },
    "whiskers": {
        "stats": {
            "stealth": 1,
            "spotting": 1
        },
		"requires": set([
            "fur"
        ]),
        "cost": 1
    },
    "mating call": {
        "stats": {
            "stealth": -5,
            "birthrate": 10
        },
		"requires": set([
            "mouth"
        ]),
        "cost": 5
    },
    "hibernate": {
        "stats": {
            "deathrate": -1
        },
		"requires": set([]),
        "cost": 5
    }   
}
"""
overpowered trait used for testing purposes
    "super saiyan": {
        "stats": {
            "attack": 100,
            "defense": 100,
            "speed": 100,
            "stealth": 100,
            "size": 100,
            "birthrate": 100,
            "deathrate": -100,
            "spotting": 100
        },
        "requires": set([]),
        "cost": 1
	}
"""

# Basic skeleton for Species class - feel free to modify as needed
class Species(object):
    # Stats and data on this species
    stats = {}  # Species stats
    population_size = 0
    consumption_rate = 1.  # Determines food needed + evo points gained
    traits = set([])  # List of traits for this species
    food_consumed = 0. # How much food has been consumed this turn
    food_needed = 100. # How much food is needed
    evo_points = 0 # How many points a species has to evolve

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
    # TODO Check for cost, return False if cost > evo points, else adjust evo points
    def add_trait(self, trait):
        if trait == "none":
            return True

        mod_stats = traits[trait]['stats']

        for stat in self.stats:
            if stat in mod_stats:
                self.stats[stat] = sum(d[stat] for d in [self.stats, mod_stats])

        self.traits.add(trait)
        return True

    # Returns {stat} * size, or -1 if {stat} invalid
    # If invert is true, stat's correlation to size is inverse (i.e. size goes up, stat goes down)
    def sized_stat(self, stat, invert=False):
        if stat not in self.stats.keys() or stat == "size":
            return -1
        else:
            if not invert:
                return self.stats[stat] * self.stats["size"]
            else:
                return self.stats[stat] / self.stats["size"]

    # Returns sized stat * random number between 0 and 1
    def rand_sized_stat(self, stat, invert=False):
        return self.sized_stat(stat, invert) * random.random()

    # Adds to food consumed this turn, negatively modified by consumption rate (size for now)
    def consume_food(self, food_amt):
        self.food_consumed = self.food_consumed + (food_amt / self.stats["size"])
    
    # Resets food consumed and adds appropriate evo points, returns a penalty (% of needed not reached)
    def use_food(self):
        penalty = max((self.food_needed - self.food_consumed) / 100, 0)
        # TODO "1" used for testing, determine if appropriate for final
        self.evo_points = (int(1 * self.stats["size"])) - (penalty * self.stats["size"]) + self.evo_points
        self.food_consumed = 0
        return penalty

    # TODO: stuff related to evo pts, death/birthrates, changing stats, and more
