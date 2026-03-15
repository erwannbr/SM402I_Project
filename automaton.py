# Predicate functions:
# is_deterministic HOUSS
# is_complete HOUSS
# is_standard HOUSS

def display_automata(FA):
    header = "       |"
    for letter in sorted(FA['alphabet']):
        header += f" {letter}   |"
    print("\n" + header)
    print("-" * len(header))

    for state in sorted(FA['states']):
        prefix = " "
        if state in FA['initials']:
            prefix += "I"
        if state in FA['finals']:
            prefix += "T"

        line = f"{prefix:<5}{state} |"

        for letter in sorted(FA['alphabet']):
            destinations = []
            for trans in FA['transitions']:
                if trans[0] == state and trans[1] == letter:
                    destinations.append(trans[2])

            if len(destinations) > 1:
                return False


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


def is_standard(FA):

    if len(FA["initial_states"]) != 1:
        print("Automaton is not standard.")
        return False

    initial = FA["initial_states"][0]

    for (state, symbol), targets in FA["transitions"].items():
        if initial in targets:
            print("Automaton is not stadard")
            return False

    print("Automaton is standard.")
    return True

def is_complete(FA):
    alphabet = FA["alphabet"]
    states = FA["states"]

    for state in states:
        for symbol in alphabet:
            if (state, symbol) not in FA["transitions"]:
                print(f"Automaton is not complete")
                return False

    print("Automaton is complete.")
    return True

def is_deterministic(FA):

    if len(FA["initial_states"]) != 1:
        print("The automaton is not deterministic because there are many initial states.")
        return False

    for key in FA["transitions"]:
        targets = FA["transitions"][key]

        if len(targets) > 1:
            print(f"Automaton is not deterministic")
            return False

    print("Automaton is deterministic.")
    return True