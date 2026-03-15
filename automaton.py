# Predicate functions:
# is_deterministic HOUSS
# is_complete HOUSS
# is_standard HOUSS

def display_automata(FA):
    alphabet = sorted(list(FA['alphabet']))
    header = "      |"
    for letter in alphabet:
        header += f" {letter:^5}|"
    print("\n" + header)
    print("-" * len(header))

    for state in sorted(list(FA['states'])):
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
                dest_str = ",".join(sorted(list(destinations)))
                line += f"{dest_str:^6}|"
            else:
                line += "      |"
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