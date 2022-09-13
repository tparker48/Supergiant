from planet import *
from constants import *
from inventory import *
from radar import *
from orbit import *


class GameState:
    window = None
    inventory = None
    radar = None

    extractors = 0

    game_log = ""

    def __init__(self, graphics_window):
        self.game_log = "Welcome!"
        self.window = graphics_window
        self.radar = Radar(graphics_window)
        self.inventory = Inventory(graphics_window)
        self.orbit = Orbit(graphics_window)

    def update(self):
        self.orbit.refresh_text()
    
    def search_planet(self, search_mode):
        if search_mode not in PLANET_SEARCH_FUEL_COSTS.keys():
            self.game_log = INVALID_COMMAND
            return

        if not self.inventory.can_find_planet(search_mode):
            self.game_log = NOT_ENOUGH_FUEL
            return

        self.radar.find_new_planet(search_mode)
        self.inventory.deduct_find_planet_cost(search_mode)
        planet_info = self.radar.found_planet.get_description()        
        self.game_log = FOUND_PLANET + ' ' + planet_info

    def buy_found_planet(self, name):
        if name == None:
            self.game_log = INVALID_COMMAND
            return
        
        if len(name) > 10:
            self.game_log = NAME_TOO_LONG
            return

        if self.radar.found_planet == None:
            self.game_log = NO_PLANET_TO_BUY
            return

        if not self.orbit.can_add_planet():
            self.game_log = ORBIT_CAPACITY_REACHED
            return

        cost = self.radar.found_planet.get_planet_cost()
        if not self.inventory.can_afford_planet(cost):
            self.game_log = CANT_AFFORD
            return
        
        self.inventory.deduct_credits(cost)
        self.radar.found_planet.name = name
        self.orbit.add_planet(self.radar.found_planet)
        self.radar.pop()
        self.game_log = BOUGHT_PLANET + ' ' + name

    def process_planets(self, no_arg):
        profit = self.orbit.process_all()
        self.inventory.add_credits(profit)
        self.game_log = PROCESSED_PLANETS + ' ' + str(profit) + ' credits'
    

    def purchase_auto_extractor(self, no_arg):
        cost = self.orbit.get_auto_extractor_cost()
        
        if cost > self.inventory.credits:
            self.game_log = CANT_AFFORD
            return
        
        self.inventory.deduct_credits(cost)
        self.orbit.add_extractor()
        self.game_log = BOUGHT_AUTO_EXTRACTOR
    
    def recycle_planet(self, planet_name):
        planet = self.orbit.get_planet(planet_name)

        if planet == None:
            self.game_log = NO_SUCH_PLANET + ' ' + planet_name
            return
        
        value = planet.get_planet_value()
        self.inventory.add_credits(value)
        self.orbit.remove_planet(planet_name)
        self.game_log = RECYCLED_PLANET + ' ' + str(value)

    def increase_orbit_capacity(self, no_arg):
        cost = self.orbit.get_capacity_increase_cost() # (self.capacity) * 50000
        
        if self.inventory.credits < cost:
            self.game_log = CANT_AFFORD
            return

        if self.orbit.max_capacity_reached():
            self.game_log = MAX_CAPACITY_REACHED
            return

        self.orbit.increase_capacity()
        self.inventory.deduct_credits(cost)
        self.game_log = INCREASED_CAPACITY

    def buy_fuel(self, amt):
        if not amt.isnumeric():
            self.game_log = INVALID_COMMAND
            return
        
        amt = int(amt)

        if not self.inventory.can_buy_fuel(amt):
            self.game_log = CANT_AFFORD
            return
        
        self.inventory.buy_fuel(amt)
        self.game_log = BOUGHT_FUEL + ' ' + str(amt)

    