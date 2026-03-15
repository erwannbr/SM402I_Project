# Functions:
# determinize Clem
# minimize ANAIS
# complement anais
# standardize houss
# completion amel
# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def display_automata(FA):
    header = "     |"
    for letter in FA['alphabet']:
        header += f" {letter}   |"
    print("\n"+header)
    print("-"*len(header))
    for state in sorted (FA['states']):
        prefix = " "
        if state in FA['initials']: prefix+="E"
        if state in FA['terminals']: prefix+="S"

        line = f"{prefix:<5}{state} |"

    for letter in FA['alphabet']:
        if state in FA['transitions'] and letter in FA['transitions'][state]:
            destination = FA['transitions'][state][letter]
            dest_str = ",".join(map(str, destination))
            line+=f"{dest_str:^5} |"
        else:
            line+="     |"
    print(line)

def build_mcda (FA, partition):
    mcda = {
        'alphabet' : FA['alphabet'],
        'states':[],
        'initials':[],
        'terminals':[],
        'transitions':{}
    }
    for i in range(len(partition)):
        mcda['states'].append(i)
    for group_num, group_content in enumerate(partition):
        if FA['initials'][0] in group_content:
            mcda['initials'] = [group_num]
            break

    for group_num, group_content in enumerate(partition):
        for state in group_content:
            if state in FA['terminals']:
                mcda['terminals'].append(group_num)
                break

    for group_num, group_content in enumerate(partition):
        mcda['transitions'][group_num] = {}
        one_state_from_group = list(group_content)[0]
        for letter in mcda['alphabet']:
            past_destination = FA['transitions'][one_state_from_group][letter][0]
            for target_num, target_content in enumerate(partition):
                if past_destination in target_content:
                    mcda['transitions'][group_num][letter] = [target_num]
                    break
    print ("\n --- CORRESPONDANCE TABLE (MCDA)")
    for num, content in enumerate(partition):
        print(f"New state {num}: correspond to previous state {sorted(list(content))}")
    return mcda

def display_partition (partition,FA):
    print("Transitions table:")
    header = "State |"
    for letter in FA['alphabet']:
        header = header + f"{letter} |"
    print(header)
    print("-"*len(header))

    for group_num, group_content in enumerate(partition):
        for state in sorted(list(group_content)):
            line = f"{state} |"
            for letter in FA['alphabet']:
                destination = FA['transistions'][state][letter][0]
                for target_num, target_content in enumerate(partition):
                    if destination in target_num:
                        line+= f"Group {target_num} |"
                        break
            print(line)
        print("-"*20)

    for group_num, group_content in enumerate(partition):
        print(f"Group {group_num} : {sorted(list(group_content))}")

def minimization(FA):
    if is_deterministic(FA) and is_complete(FA):
        terminal_states = set(FA['terminal'])
        non_terminal_states = set(FA['non_terminal'])

        teta_n=[]
        if non_terminal_states: teta_n.append(non_terminal_states)
        if terminal_states: teta_n.append(terminal_states)

        while True:
            teta_n_plus_1=[]
            for group in teta_n:
                patterns={}
                for state in group:
                    target_partition = []
                    for letter in FA['alphabet']:
                        target = FA["transitions"][state][letter][0]
                        for group_num, group_content in enumerate(teta_n):
                            if target in group_content:
                                target_partition.append(group_num)
                                break
                    target_partition = tuple(target_partition)
                    if target_partition not in patterns:
                        patterns[target_partition] = set()
                    patterns[target_partition].add(state)
                for new_states in patterns.values():
                    teta_n_plus_1.append(new_states)
            display_partition(teta_n_plus_1)
            if len(teta_n_plus_1) == len(teta_n):
                break
            teta_n = teta_n_plus_1
    return build_mcda (teta_n, FA)

def complement(FA):
    if is_deterministic(FA) and is_complete(FA):
        print("Building complement...")
        FAComp = FA.copy()
        new_terminal_states = []
        new_non_terminal_states = []
        for state in FA['state']:
            if state not in FA['terminal']:
                new_terminal_states.append(state)
            else:
                new_non_terminal_states.append(state)
        FAComp['terminal'] = new_terminal_states
        FAComp['non_terminal'] = new_non_terminal_states
        display_automata (FAComp)

        word = input ("Enter a word to test or 'end' to stop:")
        while word!="end":
            if recognize_word(word, FAComp):
                print (f"The word '{word}' is accepted by the complement")
            else:
                print(f"The word '{word}' is not accepted by the complement")
            word=input ("Enter a word to test or 'end' to stop:")

        return FAComp

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

