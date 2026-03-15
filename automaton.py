# Predicate functions:
# is_deterministic HOUSS
# is_complete HOUSS
# is_standard HOUSS

def display_automata(FA):
    header = "     |"
    for letter in sorted(FA['alphabet']):
        header += f" {letter}   |"
    print("\n"+header)
    print("-"*len(header))
    for state in sorted (FA['states']):
        prefix = " "
        if state in FA['initials']: prefix+="I"
        if state in FA['finals']: prefix+="T"

        line = f"{prefix:<5}{state} |"

    for letter in sorted(FA['alphabet']):
        if state in FA['transitions'] and letter in FA['transitions'][state]:
            destination = FA['transitions'][state][letter]
            dest_str = ",".join(sorted(list(destination)))
            line+=f"{dest_str:^3} |"
        else:
            line+="     |"
    print(line)

"""
Check if a word is recognized by the automaton.
The function starts from the initial state/states, reads the word symbol by symbol, and follows the transitions.
At the end, if at least one current state is a final state, the word is accepted. Otherwise, it is rejected.
"""

def recognize_word(automaton, word):

    current_states = set(automaton["initial_states"])

    for symbol in word: 

        next_states = set()

        for state in current_states: 

            if (state, symbol) in automaton["transitions"]: 

                next_states.update(automaton["transitions"][(state, symbol)])

        current_states = next_states
    for state in current_states: 
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