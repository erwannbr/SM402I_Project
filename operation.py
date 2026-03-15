# Functions:
# determinize Clem

import automaton


def determinize(automaton):
    alphabet = automaton["alphabet"]
    final_states = automaton["final_states"]
    transitions = automaton["transitions"]
    initial_state = automaton["initial_states"]

    dfa_states = [initial_state]
    dfa_final_states = []
    dfa_transitions = {}

    to_process = [initial_state]

    while to_process:
        current_state = to_process.pop(0)

        current_key = tuple(sorted(current_state)) 
        dfa_transitions[current_key] = {}

        for state in current_state:
            if state in final_states:
                if current_state not in dfa_final_states:
                    dfa_final_states.append(current_state)
                break

        for symbol in alphabet:
            next_state = set()

            for state in current_state:
                next_state.update(transitions[state][symbol])

            dfa_transitions[current_key][symbol] = next_state

            if next_state not in dfa_states:
                dfa_states.append(next_state)
                to_process.append(next_state)

    return {
        "alphabet": alphabet,
        "states": dfa_states,
        "initial_states": initial_state,
        "final_states": dfa_final_states,
        "transitions": dfa_transitions
    }

# minimize ANAIS
# complement anais
# standardize houss
# completion amel
