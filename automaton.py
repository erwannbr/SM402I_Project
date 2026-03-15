# Utility functions:
# display_automaton Erwann
# recognize_word Amel
#
# Predicate functions:
# is_deterministic HOUSS
# is_complete HOUSS
# is_standard HOUSS


"""
Check if a word is recognized by the automaton.
The function starts from the initial state/states, reads the word symbol by symbol, and follows the transitions.
At the end, if at least one current state is a final state, the word is accepted. Otherwise, it is rejected.
"""

def recognize_word(automaton, word):

    current_states = set(automaton["initial_states"])# start from the initial state(s)

    for symbol in word: # read the word symbol by symbol

        next_states = set()# this will store the states reached after reading the symbol

        for state in current_states: # check all current states

            if (state, symbol) in automaton["transitions"]: # if transition exists for this state and symbol

                next_states.update(automaton["transitions"][(state, symbol)]) # add the states to next_states

        current_states = next_states # move to next states

    for state in current_states: # after reading the word, check if current state is final
        if state in automaton["final_states"]:
            return True

    return False



"""
Read a word from the user.
The user types a word in the terminal. The function returns the word.
Typing "end" stops the program.
"""

def read_word():

    word = input("Enter a word (or 'end' to stop): ")
    
    return word