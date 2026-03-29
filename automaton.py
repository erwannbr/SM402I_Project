# Predicate functions:
# is_deterministic HOUSS
# is_complete HOUSS
# is_standard HOUSS

"""
Display the automaton as a table.
"""
def display_automata(FA):
    alphabet = sorted(list(FA['alphabet']))
    header = "      |"
    for letter in alphabet:
        header += f" {letter:^5}|"
    print("\n" + header)
    print("-" * len(header))

    for state in sorted(str(s) for s in FA['states']):
        prefix = ""
        if state in FA.get('initials', []):
            prefix += "I"
        if state in FA.get('finals', []):
            prefix += "T"

        state_label = str(state)
        line = f"{prefix:>3} {state_label:<2} |"

        state_transitions = FA['transitions'].get(state, {})

        for letter in alphabet:
            destinations = state_transitions.get(letter, set())

            if destinations:
                dest_str = ",".join(sorted(str(d) for d in destinations))
                line += f"{dest_str:^6}|"
            else:
                line += "      |"
        print(line)

# ============================
# WORD RECOGNITION
# ============================

"""
Check if a word is recognized by the automaton.
The function starts from the initial state/states, reads the word symbol by symbol, and follows the transitions.
At the end, if at least one current state is a final state, the word is accepted. Otherwise, it is rejected.
"""

def recognize_word(automaton, word):
    
    # start from the initial state 
    current_states = set(automaton["initials"])
    
    # read the word one symbol at a time
    for symbol in word:

        # this will store the states we can reach after reading the symbol
        next_states = set()

        # check all current states
        for state in current_states:
            # make sure the state has transitions and the symbol exists
            if state in automaton["transitions"] and symbol in automaton["transitions"][state]:
                # add all reachable states
                next_states.update(automaton["transitions"][state][symbol])
        
        # move to the next states
        current_states = next_states

    # after reading the whole word, check if we reached a final state
    for state in current_states:
        if state in automaton["finals"]:
            return True
    
    # if no final state is reached → word is rejected
    return False

# ============================
# READ WORD FROM USER
# ============================

"""
Read a word from the user.
The user types a word in the terminal. The function returns the word.
Typing "end" stops the program.
"""

def read_word():
    # ask the user to type a word in the terminal
    word = input("Enter a word (or 'end' to stop): ")
    # return the word as a string
    return word


"""
Check if the automaton is standard
"""
def is_standard(FA):
    if len(FA["initials"]) != 1:
        return False

    initial = FA["initials"][0]

    for state, state_transitions in FA["transitions"].items():
        for symbol, targets in state_transitions.items():
            if initial in targets:
                return False

    return True


"""
Check if the automaton is complete
"""
def is_complete(FA):
    alphabet = FA["alphabet"]
    states = FA["states"]

    for state in states:
        for symbol in alphabet:
            if state not in FA["transitions"] or symbol not in FA["transitions"][state]:
                return False

    return True


"""
Check if the automaton is deterministic
"""
def is_deterministic(FA):
    if len(FA["initials"]) != 1:
        return False

    for state, state_transitions in FA["transitions"].items():
        for symbol, targets in state_transitions.items():
            if len(targets) > 1:
                return False

    return True