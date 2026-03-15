# Functions:
# determinize Clem
# minimize ANAIS
# standardize houss
# IMPORTATION
from automaton import *


def build_mcda (finite_automata, partition):
    mcda = {
        'alphabet' : finite_automata['alphabet'],
        'states':[],
        'initials':[],
        'terminals':[],
        'transitions':{}
    }
    for i in range(len(partition)):
        mcda['states'].append(i)
    for group_num, group_content in enumerate(partition):
        if finite_automata['initials'][0] in group_content:
            mcda['initials'] = [group_num]
            break

    for group_num, group_content in enumerate(partition):
        for state in group_content:
            if state in finite_automata['terminals']:
                mcda['terminals'].append(group_num)
                break

    for group_num, group_content in enumerate(partition):
        mcda['transitions'][group_num] = {}
        one_state_from_group = list(group_content)[0]
        for letter in mcda['alphabet']:
            past_destination = finite_automata['transitions'][one_state_from_group][letter][0]
            for target_num, target_content in enumerate(partition):
                if past_destination in target_content:
                    mcda['transitions'][group_num][letter] = [target_num]
                    break
    print ("\n --- CORRESPONDANCE TABLE (MCDA)")
    for num, content in enumerate(partition):
        print(f"New state {num}: correspond to previous state {sorted(list(content))}")
    return mcda

def display_partition (partition,finite_automata):
    print("Transitions table:")
    header = "State |"
    for letter in finite_automata['alphabet']:
        header = header + f"{letter} |"
    print(header)
    print("-"*len(header))

    for group_num, group_content in enumerate(partition):
        for state in sorted(list(group_content)):
            line = f"{state} |"
            for letter in finite_automata['alphabet']:
                destination = finite_automata['transistions'][state][letter][0]
                for target_num, target_content in enumerate(partition):
                    if destination in target_num:
                        line+= f"Group {target_num} |"
                        break
            print(line)
        print("-"*20)

    for group_num, group_content in enumerate(partition):
        print(f"Group {group_num} : {sorted(list(group_content))}")

def minimization(finite_automata):
    if is_deterministic(finite_automata) and is_complete(finite_automata):
        terminal_states = set(finite_automata['terminal'])
        non_terminal_states = set(finite_automata['non_terminal'])

        teta_n=[]
        if non_terminal_states: teta_n.append(non_terminal_states)
        if terminal_states: teta_n.append(terminal_states)

        while True:
            teta_n_plus_1=[]
            for group in teta_n:
                patterns={}
                for state in group:
                    target_partition = []
                    for letter in finite_automata['alphabet']:
                        target = finite_automata["transitions"][state][letter][0]
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
    return build_mcda (teta_n, finite_automata)

def complement(finite_automata):
    if is_deterministic(finite_automata) and is_complete(finite_automata):
        print("Building complement...")
        finite_automataComp = finite_automata.copy()
        new_terminal_states = []
        new_non_terminal_states = []
        for state in finite_automata['state']:
            if state not in finite_automata['terminal']:
                new_terminal_states.append(state)
            else:
                new_non_terminal_states.append(state)
        finite_automataComp['terminal'] = new_terminal_states
        finite_automataComp['non_terminal'] = new_non_terminal_states
        display_automata (finite_automataComp)

        word = input ("Enter a word to test or 'end' to stop:")
        while word!="end":
            if recognize_word(word, finite_automataComp):
                print (f"The word '{word}' is accepted by the complement")
            else:
                print(f"The word '{word}' is not accepted by the complement")
            word=input ("Enter a word to test or 'end' to stop:")

        return finite_automataComp


"""
Complete a deterministic automaton by adding a sink state "P" when some transitions are missing.
An automaton is complete if for every state and every symbol in the alphabet, there is a transition.
If a transition is missing, it is redirected to the sink state "P". The sink state then loops to itself for every symbol.
"""

def completion(automaton):

    states = set(automaton["states"])  
    alphabet = automaton["alphabet"]
    transitions = dict(automaton["transitions"]) 

    sink_state = "P"
    missing_transition_found = finite_automatalse

    for state in states: 
        for symbol in alphabet: 
            if (state, symbol) not in transitions: 
                transitions[(state, symbol)] = {sink_state} 
                missing_transition_found = True

    if missing_transition_found:
        automaton["states"].add(sink_state) 

        for symbol in alphabet:
            transitions[(sink_state, symbol)] = {sink_state}

    automaton["transitions"] = transitions

    return automaton

def standardization(FA):

    if is_standard(FA):
        print("Automaton already standard.")
        return FA

    new_FA = FA.copy()

    new_initial = max(FA["states"]) + 1

    new_FA["states"] = FA["states"] + [new_initial]
    new_FA["initial_states"] = [new_initial]

    new_FA["transitions"] = FA["transitions"].copy()

    # connect new initial state
    for init in FA["initial_states"]:
        for symbol in FA["alphabet"]:
            if (init, symbol) in FA["transitions"]:
                targets = FA["transitions"][(init, symbol)]

                new_FA["transitions"][(new_initial, symbol)] = targets

    print("Automaton has been standardized.")

    return new_FA
