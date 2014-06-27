"""
Cookie Clicker Simulator
"""

import simpleplot
import math
import random

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self, total_cookie_num = 0.0, current_cookie_num = 0.0, current_time = 0.0, cps = 1.0):
        self._total_cookie_num = total_cookie_num
        self._current_cookie_num = current_cookie_num
        self._current_time = current_time
        self._cps = cps
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        string = "\nTotal cookie number: " + str(self._total_cookie_num) + "\n"
        string += "Current cookie number: " + str(self._current_cookie_num) + "\n"
        string += "Current time: " + str(self._current_time) + "\n"
        string += "CPS: " + str(self._cps) + "\n"
        string += "History: " + str(self._history)
        return string
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookie_num
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies >= 0 and cookies > self._current_cookie_num:
            return math.ceil((cookies - self._current_cookie_num)/self._cps)
        else:
            return 0.0
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time > 0:
            self._current_time += time
            self._current_cookie_num += time * self._cps
            self._total_cookie_num += time * self._cps
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookie_num < cost:
            return
        self._current_cookie_num -= cost
        self._cps += additional_cps
        self._history.append((self._current_time, item_name, cost, self._total_cookie_num))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    build = build_info
    clicker = ClickerState()
    while clicker.get_time() <= duration:
        time_left = duration - clicker.get_time()
        item_name = strategy(clicker.get_cookies(), clicker.get_cps(), time_left, build_info)
        if item_name == None:
            break
        item_cost = build.get_cost(item_name)
        if clicker.time_until(item_cost) > time_left:
            break
        else:
            clicker.wait(clicker.time_until(item_cost))
            clicker.buy_item(item_name, item_cost, build.get_cps(item_name))
            build.update_item(item_name)
    clicker.wait(time_left)
    return clicker


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Cheap strategy
    """
    item_list = build_info.build_items()
    min_cost = float('Inf')
    item_to_select = None
    for item in item_list:
        cost = build_info.get_cost(item)
        if cost > cookies + cps * time_left:
            break
        if cost < min_cost:
            min_cost = cost
            item_to_select = item
    return item_to_select

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    Expensive strategy
    """
    item_list = build_info.build_items()
    max_cost = -1
    item_to_select = None
    for item in item_list:
        cost = build_info.get_cost(item)
        if cost > cookies + cps * time_left:
            break
        if cost > max_cost:
            max_cost = cost
            item_to_select = item
    return item_to_select

def strategy_best(cookies, cps, time_left, build_info):
    """
    Best(random) strategy
    """
    item_list = build_info.build_items()
    length = len(item_list)
    count = 0
    while True:
        count += 1
        if count >= 1000:
            return None
        index = random.randrange(length)
        item = item_list[index]
        cost = build_info.get_cost(item)
        if cost > cookies + cps * time_left:
            break
        return item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    # state = simulate_clicker(provided.BuildInfo(), time, strategy)
    state = simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 0.10000000000000001], 'Grandma': [100.0, 0.5]}, 1.15), 400, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor)
    #run_strategy("None", SIM_TIME, strategy_none)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    
