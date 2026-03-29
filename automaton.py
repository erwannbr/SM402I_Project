"""
Display the automaton as a table.
"""


def display_automata(FA):
    alphabet = sorted(list(FA['alphabet']))
    states = sorted(list(FA['states']), key=lambda s: str(s))

    #compute dynamic column widths

    #width of the state column: longest state name + prefix ("→*" = 2 chars) + spacing
    state_col_w = max((len(str(s)) for s in states), default=1) + 3  # +3 for prefix + space

    #width of each transition column: wide enough for the longest destination string
    #and at least as wide as the symbol itself.
    def dest_str(state, letter):
        dests = FA['transitions'].get(state, {}).get(letter, set())
        if dests:
            return ",".join(sorted((str(d) for d in dests), key=str))
        return "--"

    col_widths = {}
    for letter in alphabet:
        max_dest = max((len(dest_str(s, letter)) for s in states), default=2)
        col_widths[letter] = max(max_dest, len(letter)) + 2  # +2 for padding

    #header
    header = f"{'':^{state_col_w}}|"
    for letter in alphabet:
        header += f" {letter:^{col_widths[letter]}}|"
    print("\n" + header)
    print("-" * len(header))

    #rows
    for state in states:
        prefix = ""
        if state in FA.get('initials', []):
            prefix += "I"
        if state in FA.get('finals', set()):
            prefix += "T"

        #right-align prefix, then left-align state name within the state column
        state_label = str(state)
        line = f"{prefix:>2} {state_label:<{state_col_w - 3}}|"

        for letter in alphabet:
            dests = FA['transitions'].get(state, {}).get(letter, set())
            if dests:
                cell = ",".join(sorted((str(d) for d in dests), key=str))
            else:
                cell = "--"
            line += f" {cell:^{col_widths[letter]}}|"

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
        print("Automaton is not standard, there is more than one initial state.")
        return False

    initial = FA["initials"][0]

    for state, state_transitions in FA["transitions"].items():
        for symbol, targets in state_transitions.items():
            if initial in targets:
                print(f"Automaton is not standard because transition from state {state} with symbol '{symbol}' goes to the initial state {initial}.")
                return False
    print("Automaton is standrad.")
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
                print(f"Automaton is not complete because state {state} has no transition")
                return False
            if symbol not in FA["transitions"][state]:
                print(f"Automaton is not complete, we have missing transition from state {state} with symbol '{symbol}'")
                return False

    print("Automaton is complete")
    return True


"""
Check if the automaton is deterministic
"""


def is_deterministic(FA):
    """An FA is deterministic if it has exactly one initial state and every
    transition leads to at most one state"""
    if len(FA["initials"]) != 1:
        print(f"Automaton is not deterministic: {len(FA['initials'])} initial states {FA['initials']}.")
        return False

    #collect all non-deterministic transitions before reporting
    conflicts = []
    for state, state_transitions in FA["transitions"].items():
        for symbol, targets in state_transitions.items():
            if len(targets) > 1:
                conflicts.append((state, symbol, targets))

    if conflicts:
        print("Automaton is not deterministic — multiple targets found:")
        for state, symbol, targets in conflicts:
            print(f"  State '{state}' on '{symbol}' → {sorted(str(t) for t in targets)}")
        return False

    print("Automaton is deterministic.")
    return True