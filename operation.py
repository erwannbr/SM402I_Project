# Functions:
# determinize Clem
# minimize ANAIS
# complement anais
# standardize houss
# completion amel


"""
Complete a deterministic automaton by adding a sink state "P" when some transitions are missing.
An automaton is complete if for every state and every symbol in the alphabet, there is a transition.
If a transition is missing, it is redirected to the sink state "P". The sink state then loops to itself for every symbol.
"""

def completion(automaton):

    states = set(automaton["states"])  # get state from automaton / use set() to make a copy so we don't modify
    alphabet = automaton["alphabet"] # get alphabet
    transitions = dict(automaton["transitions"]) # get transitions and copy them

    sink_state = "P"
    missing_transition_found = False

    for state in states:  # loop through every state
        for symbol in alphabet: # each state check every symbol of the alphabet
            if (state, symbol) not in transitions: # if transition does not exist
                transitions[(state, symbol)] = {sink_state} # add a transition to the sink state p
                missing_transition_found = True

    if missing_transition_found:
        automaton["states"].add(sink_state) # add sink state p to the set of states

        for symbol in alphabet:
            transitions[(sink_state, symbol)] = {sink_state} # add self-loops in sink state for every symbol

    automaton["transitions"] = transitions  # update transitions in automaton

    return automaton


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