"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def list_powerset(lst):
    """
    Get the power set of list 'lst'. 
    """
    result = set([()])
    for item in lst:
        temp_set = set()
        for subset in result:
            new_subset = list(subset)
            new_subset.append(item)
            temp_set.add(tuple(new_subset))
        result.update(temp_set)
    return result

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    max_index = max(hand)
    score_boxes = [0 for dummy_i in range(max_index + 1)]
    for item in hand:
        score_boxes[item] += item
    return max(score_boxes)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    die_outcomes = [index + 1 for index in range(num_die_sides)]
    all_sequences = gen_all_sequences(die_outcomes, num_free_dice)
    result = []
    for item in all_sequences:
        new_dice_list = list(held_dice)
        new_dice_list.extend(item)
        result.append(new_dice_list)
    size = len(result)
    exp_value = 0.0
    for item in result:
        exp_value += float(score(item)) / size
    return exp_value


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    power_set = list_powerset(list(hand))
    return power_set



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_num = len(hand)
    hold_dices = gen_all_holds(hand)
    max_value = -1
    for item in hold_dices:
        free_num = all_num - len(item)
        exp_value = expected_value(item, num_die_sides, free_num)
        if exp_value > max_value:
            max_value = exp_value
            dices_to_hold = item
    return (max_value, dices_to_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)


