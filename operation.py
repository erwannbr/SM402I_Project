from automaton import *
import copy

"""
Converts a non-deterministic FA into a complete deterministic FA using the subset-construction algorithm.
"""
def determinize(automaton):

    alphabet = automaton["alphabet"]
    final_states = automaton["finals"]
    transitions = automaton["transitions"]

    # BUG FIX: wrap the initial group in a frozenset so it is hashable
    initial_group = frozenset(automaton["initials"])

    dfa_states = [initial_group]
    dfa_final_states = []
    dfa_transitions = {}

    to_process = [initial_group]

    while to_process:
        current_group = to_process.pop(0)

        dfa_transitions[current_group] = {}

        # Mark as final if any member state is a final state
        if any(s in final_states for s in current_group):
            if current_group not in dfa_final_states:
                dfa_final_states.append(current_group)

        for symbol in alphabet:
            next_group = set()
            for state in current_group:
                # BUG FIX: guard against missing state/symbol in transitions
                if state in transitions and symbol in transitions[state]:
                    next_group.update(transitions[state][symbol])

            next_group = frozenset(next_group)  # hashable

            dfa_transitions[current_group][symbol] = next_group

            if next_group not in dfa_states:
                dfa_states.append(next_group)
                to_process.append(next_group)

    # Build human-readable state labels: "{1.2.3}" style
    def label(group):
        if not group:
            return "∅"
        return ".".join(sorted(str(s) for s in group))

    # Rebuild with string-keyed transitions for uniformity with the rest of
    # the program
    str_transitions = {}
    for group, trans in dfa_transitions.items():
        str_transitions[label(group)] = {
            sym: {label(target)} for sym, target in trans.items()
        }

    str_states = set(label(g) for g in dfa_states)
    str_finals = set(label(g) for g in dfa_final_states)
    str_initials = [label(initial_group)]

    print("\n--- DETERMINIZATION: state correspondence ---")
    for g in dfa_states:
        print(f"  New state '{label(g)}' ← original states {sorted(str(s) for s in g)}")

    return {
        "alphabet": alphabet,
        "states": str_states,
        "initials": str_initials,
        "finals": str_finals,
        "transitions": str_transitions
    }


"""
Complete a deterministic automaton by adding a sink state "P" when some transitions are missing.
An automaton is complete if for every state and every symbol in the alphabet, there is a transition.
If a transition is missing, it is redirected to the sink state "P". The sink state then loops to itself for every symbol.
"""
def completion(automaton):
    automaton = copy.deepcopy(automaton)

    states = set(automaton["states"])
    alphabet = automaton["alphabet"]
    transitions = automaton["transitions"]

    sink_state = "P"
    missing_transition_found = False

    for state in states:
        if state not in transitions:
            transitions[state] = {}
        for symbol in alphabet:
            if symbol not in transitions[state]:
                transitions[state][symbol] = {sink_state}
                missing_transition_found = True

    if missing_transition_found:
        automaton["states"].add(sink_state)
        transitions[sink_state] = {}
        for symbol in alphabet:
            transitions[sink_state][symbol] = {sink_state}
        print(f"Sink state '{sink_state}' added to complete the automaton.")
    else:
        print("Automaton is already complete — no sink state needed.")

    automaton["transitions"] = transitions
    return automaton


"""
Standardize a deterministic automaton by adding a new initial state
"""
def standardization(FA):
    if is_standard(FA):
        print("Automaton is already standard.")
        return FA

    new_FA = copy.deepcopy(FA)

    # Generate a fresh state name that does not clash with existing ones
    new_initial = "i0"
    while new_initial in new_FA["states"]:
        new_initial = new_initial + "_new"

    new_FA["states"].add(new_initial)
    new_FA["initials"] = [new_initial]
    new_FA["transitions"][new_initial] = {}

    # Copy transitions from all old initial states into the new one
    for init in FA["initials"]:
        for symbol in FA["alphabet"]:
            targets = FA["transitions"].get(init, {}).get(symbol, set())
            if targets:
                if symbol not in new_FA["transitions"][new_initial]:
                    new_FA["transitions"][new_initial][symbol] = set()
                new_FA["transitions"][new_initial][symbol].update(targets)

    # If any old initial state was final, the new one must be final too
    if any(s in FA["finals"] for s in FA["initials"]):
        new_FA["finals"].add(new_initial)

    print(f"Automaton standardized: new initial state '{new_initial}' created.")
    return new_FA


"""
Pretty-print one step of the minimization partition table.
"""
def _display_partition(partition, automaton, step):
    alphabet = sorted(list(automaton['alphabet']))
    print(f"\n  Partition at step {step}:")
    for i, group in enumerate(partition):
        print(f"    Group {i}: {sorted(str(s) for s in group)}")

    header = f"  {'State':<8}|"
    for letter in alphabet:
        header += f" {'→'+letter:<8}|"
    print("  " + "-" * (len(header) - 2))
    print(header)
    print("  " + "-" * (len(header) - 2))

    for i, group in enumerate(partition):
        for state in sorted(group, key=str):
            line = f"  {str(state):<8}|"
            for letter in alphabet:
                dest_set = automaton['transitions'].get(state, {}).get(letter, set())
                if dest_set:
                    dest = next(iter(dest_set))
                    # Find which group dest belongs to
                    dest_group = next(
                        (j for j, g in enumerate(partition) if dest in g), "?"
                    )
                    line += f" {'G'+str(dest_group):<8}|"
                else:
                    line += f" {'--':<8}|"
            print(line)
        print("  " + "-" * (len(header) - 2))


"""
Build the minimal DFA dict from the final Moore partition.
"""
def _build_minimal_dfa(automaton, final_partition):

    alphabet = sorted(automaton['alphabet'])
    n = len(final_partition)

    # Map each original state → its group index
    state_to_group = {}
    for idx, group in enumerate(final_partition):
        for s in group:
            state_to_group[s] = idx

    initial_original = automaton['initials'][0]
    initial_group = state_to_group[initial_original]

    final_groups = set()
    for idx, group in enumerate(final_partition):
        if any(s in automaton['finals'] for s in group):
            final_groups.add(idx)

    transitions = {}
    for idx, group in enumerate(final_partition):
        transitions[idx] = {}
        rep = next(iter(group))  # any representative
        for letter in alphabet:
            dest_set = automaton['transitions'].get(rep, {}).get(letter, set())
            if dest_set:
                dest = next(iter(dest_set))
                transitions[idx][letter] = {state_to_group[dest]}
            # (missing transitions remain absent — automaton should be complete
            #  before minimization, so this should not happen)

    print("\n--- MINIMIZATION: state correspondence ---")
    for idx, group in enumerate(final_partition):
        print(f"  New state {idx} ← {sorted(str(s) for s in group)}")

    return {
            'alphabet': automaton['alphabet'],
            'states': set(str(i) for i in range(n)), 
            'initials': [str(initial_group)],       
            'finals': set(str(f) for f in final_groups), 
            'transitions': {str(k): {sym: {str(v) for v in vals} for sym, vals in v_dict.items()} 
                            for k, v_dict in transitions.items()}
        }


"""
Minimizes a complete deterministic FA using Moore's partition refinement.
"""
def minimization(automaton):
    if not is_deterministic(automaton):
        print("Error: minimization requires a deterministic automaton.")
        return automaton
    if not is_complete(automaton):
        print("Error: minimization requires a complete automaton.")
        return automaton

    terminal_states = set(automaton['finals'])
    non_terminal_states = automaton['states'] - terminal_states

    teta_n = []
    if non_terminal_states:
        teta_n.append(frozenset(non_terminal_states))
    if terminal_states:
        teta_n.append(frozenset(terminal_states))

    step = 0
    _display_partition(teta_n, automaton, step)

    while True:
        step += 1
        teta_n_plus_1 = []

        for group in teta_n:
            patterns = {}
            for state in group:
                # Signature: tuple of destination-group indices, one per symbol
                sig = []
                for letter in sorted(automaton['alphabet']):
                    dest_set = automaton['transitions'].get(state, {}).get(letter, set())
                    if dest_set:
                        dest = next(iter(dest_set))
                        grp_idx = next(
                            (i for i, g in enumerate(teta_n) if dest in g), -1
                        )
                        sig.append(grp_idx)
                    else:
                        sig.append(-1)
                sig = tuple(sig)
                if sig not in patterns:
                    patterns[sig] = set()
                patterns[sig].add(state)

            for new_group in patterns.values():
                teta_n_plus_1.append(frozenset(new_group))

        _display_partition(teta_n_plus_1, automaton, step)

        # Stability check: same partition (as a set of frozensets)
        if set(teta_n_plus_1) == set(teta_n):
            break
        teta_n = teta_n_plus_1

    if len(teta_n) == len(automaton['states']):
        print("\nThe automaton is already minimal.")
    else:
        print(f"\nMinimization complete: {len(automaton['states'])} → {len(teta_n)} states.")

    return _build_minimal_dfa(automaton, teta_n)


"""
Builds the complement automaton by swapping final and non-final states.
Requires a complete deterministic automaton.
"""
def complement(automaton):
    if not is_deterministic(automaton):
        print("Error: complement requires a deterministic automaton.")
        return automaton
    if not is_complete(automaton):
        print("Error: complement requires a complete automaton.")
        return automaton

    comp = copy.deepcopy(automaton)
    comp['finals'] = automaton['states'] - automaton['finals']

    print("Complement automaton built (final ↔ non-final states swapped).")
    return comp
