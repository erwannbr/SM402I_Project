from automaton import *
import copy
from graphviz import Digraph
import webbrowser
from pathlib import Path

"""
Converts a non-deterministic FA into a complete deterministic FA using the subset-construction algorithm.
"""


# ---------------------------------------------------------------------------
# DETERMINIZATION  (+ implicit completion via the sink state approach)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# EPSILON-CLOSURE  (helper for determinize)
# ---------------------------------------------------------------------------

def _epsilon_closure(states, transitions):
    """
    Returns all states reachable from `states` via epsilon ('e') transitions only.
    Iteratively expands the set until no new states are discovered.
    """
    closure = set(states)
    to_visit = list(states)

    while to_visit:
        current = to_visit.pop()
        #follow every epsilon transition out of current
        for target in transitions.get(current, {}).get("e", set()):
            if target not in closure:
                closure.add(target)
                to_visit.append(target)

    return frozenset(closure)


# ---------------------------------------------------------------------------
# DETERMINIZATION
# ---------------------------------------------------------------------------

def determinize(automaton):
    """
    Converts a non-deterministic FA (with or without epsilon transitions) into
    an equivalent deterministic FA using the subset-construction algorithm.

    Epsilon transitions (symbol 'e') are eliminated via epsilon-closure.
    The result is deterministic but NOT necessarily complete — call completion()
    separately if needed.
    """
    alphabet = automaton["alphabet"]
    final_states = automaton["finals"]
    transitions = automaton["transitions"]

    # 'e' is not a real input symbol — it is only used internally for epsilon-closure
    real_alphabet = [s for s in alphabet if s != "e"]

    #the initial group is the epsilon-closure of all original initial states.
    #frozenset is used so groups can be stored as dict keys (must be hashable).
    initial_group = _epsilon_closure(automaton["initials"], transitions)

    dfa_states = [initial_group]
    dfa_final_states = []
    dfa_transitions = {}
    to_process = [initial_group]

    while to_process:
        current_group = to_process.pop(0)
        dfa_transitions[current_group] = {}

        #the group is final if any of its member states was final in the original FA
        if any(s in final_states for s in current_group):
            if current_group not in dfa_final_states:
                dfa_final_states.append(current_group)

        for symbol in real_alphabet:
            #collect all states directly reachable by reading `symbol` from any state in the group
            raw_targets = set()
            for state in current_group:
                if state in transitions and symbol in transitions[state]:
                    raw_targets.update(transitions[state][symbol])

            #then expand with epsilon-closure (states reachable via 'e' after reading symbol)
            next_group = _epsilon_closure(raw_targets, transitions) if raw_targets else frozenset()

            dfa_transitions[current_group][symbol] = next_group

            #only add the group to the queue if it hasn't been seen yet
            if next_group not in dfa_states:
                dfa_states.append(next_group)
                to_process.append(next_group)

    #Label each group of states as "1.2.3" (dot-separated sorted members).
    #the empty group (no reachable state) is labelled "∅".
    def label(group):
        if not group:
            return "∅"
        return ".".join(sorted(str(s) for s in group))

    #rebuild the transition table with string keys,
    #consistent with the rest of the program
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
        "alphabet": set(real_alphabet),  # 'e' removed from the output alphabet
        "states": str_states,
        "initials": str_initials,
        "finals": str_finals,
        "transitions": str_transitions
    }


# ============================
# COMPLETION FUNCTION
# ============================

"""
Complete a deterministic automaton by adding a sink state "P" when some transitions are missing.
An automaton is complete if for every state and every symbol in the alphabet, there is a transition.
If a transition is missing, it is redirected to the sink state "P". The sink state then loops to itself for every symbol.
"""
def completion(automaton):

    automaton = copy.deepcopy(automaton) # make a deep copy so we don't modify the original automaton
    # get the main components of the automaton
    states = set(automaton["states"]) # copy of states
    alphabet = automaton["alphabet"] # symbols
    transitions = automaton["transitions"] # transitions 

    sink_state = "P" # name of the sink state (like in class)
    missing_transition_found = False  # used to know if we actually need to add P
    
    # go through every state
    for state in states:

        # if a state has no transitions at all, create an empty dict for it
        if state not in transitions:
            transitions[state] = {}

        # check all symbols for this state
        for symbol in alphabet:

            # if a transition is missing, send it to P
            if symbol not in transitions[state]:
                transitions[state][symbol] = {sink_state}
                missing_transition_found = True
    
    # if at least one transition was missing → we add the sink state
    if missing_transition_found:

        # add P to the set of states
        automaton["states"].add(sink_state)
        # create transitions for P 
        transitions[sink_state] = {}
         # P loops to itself for every symbol
        for symbol in alphabet:
            transitions[sink_state][symbol] = {sink_state}
        print(f"Sink state '{sink_state}' added to complete the automaton.")
    else:
        # nothing to do if already complete
        print("Automaton is already complete — no sink state needed.")
    
    # update transitions in the automaton
    automaton["transitions"] = transitions
    # return the completed automaton
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


def display_partition(partition, automaton, step):
    """Displays the current partition and transition table at a given minimization step."""
    alphabet = sorted(list(automaton['alphabet']))
    all_states = [s for group in partition for s in group]

    # Print each group and its members
    print(f"\n  Partition at step {step}:")
    for i, group in enumerate(partition):
        print(f"    Group {i}: {sorted(str(s) for s in group)}")

    # Dynamic column widths based on actual content
    # State column: longest state name + 2 for indentation
    state_col_w = max((len(str(s)) for s in all_states), default=5) + 2

    # Transition columns: "G<n>" labels, so width depends on number of groups
    max_group_label = len("G" + str(len(partition)))
    col_w = max(max_group_label, 2) + 2  # +2 for padding

    header = f"  {'State':<{state_col_w}}|"
    for letter in alphabet:
        header += f" {'→' + letter:<{col_w}}|"
    print("  " + "-" * (len(header) - 2))
    print(header)
    print("  " + "-" * (len(header) - 2))

    for i, group in enumerate(partition):
        # sort by string so mixed int/string state names display consistently
        for state in sorted(group, key=str):
            line = f"  {str(state):<{state_col_w}}|"
            for letter in alphabet:
                dest_set = automaton['transitions'].get(state, {}).get(letter, set())
                if dest_set:
                    dest = next(iter(dest_set))  # DFA: one destination only
                    # Show the group index of the destination, not the raw state name,
                    # because at this stage we reason in terms of groups, not states.
                    dest_group = next(
                        (j for j, g in enumerate(partition) if dest in g), "?"
                    )
                    line += f" {'G' + str(dest_group):<{col_w}}|"
                else:
                    line += f" {'--':<{col_w}}|"
            print(line)
        # Separator line between groups for readability
        print("  " + "-" * (len(header) - 2))


"""
Build the minimal DFA dict from the final Moore partition.
"""
def build_minimal_dfa(automaton, final_partition):

    alphabet = sorted(automaton['alphabet'])
    n = len(final_partition)

    # Maps each old state to the index of the group it ended up in.
    # Example: if state "0.1" is in group 2, then state_to_group["0.1"] == 2.
    state_to_group = {}
    for idx, group in enumerate(final_partition):
        for s in group:
            state_to_group[s] = idx
    # The new initial state is the group that contains the original initial state.
    initial_original = automaton['initials'][0]
    initial_group = state_to_group[initial_original]
    # A group is final if at least one of its original states was final.
    # Since the partition separates finals from non-finals, in practice either
    # all states in a group are final or none are — but `any()` is used defensively.
    final_groups = set()
    for idx, group in enumerate(final_partition):
        if any(s in automaton['finals'] for s in group):
            final_groups.add(idx)

    # Build transitions for the new automaton
    # All states in a group behave identically (that is what the partition guarantees),
    # so we only need to look at one representative state per group
    transitions = {}
    for idx, group in enumerate(final_partition):
        transitions[idx] = {}
        rep = next(iter(group))  # pick any state from the group as representative
        for letter in alphabet:
            dest_set = automaton['transitions'].get(rep, {}).get(letter, set())
            if dest_set:
                dest = next(iter(dest_set)) # DFA: exactly one destination
                # Translate the destination to its new group index
                transitions[idx][letter] = {state_to_group[dest]}
            # (missing transitions remain absent — automaton should be complete
            #  before minimization, so this should not happen)

    print("\n--- MINIMIZATION: state correspondence ---")
    for idx, group in enumerate(final_partition):
        print(f"  New state {idx} ← {sorted(str(s) for s in group)}")
    # Convert all state indices to strings so the returned structure is uniform
    # with the rest of the program (which uses string state labels throughout).
    return {
            'alphabet': automaton['alphabet'],
            'states': set(str(i) for i in range(n)), 
            'initials': [str(initial_group)],       
            'finals': set(str(f) for f in final_groups), 
            # Rewrite the transitions dict: int keys/values → string keys/values
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
    # Initial partition: finals vs non-finals (already distinguishable by definition).
    # frozenset is used because groups will be stored in a set for the stability
    # check below — plain sets are not hashable and can't be put inside a set.
    teta_n = []
    if non_terminal_states:
        teta_n.append(frozenset(non_terminal_states))
    if terminal_states:
        teta_n.append(frozenset(terminal_states))

    step = 0
    display_partition(teta_n, automaton, step)
    
    while True:
        step += 1
        teta_n_plus_1 = []

        for group in teta_n:
            patterns = {}
            for state in group:
                # Signature: tuple of destination-group indices for each symbol.
                # States with the same signature stay together; different → split.
                sig = []
                for letter in sorted(automaton['alphabet']):
                    dest_set = automaton['transitions'].get(state, {}).get(letter, set())
                    if dest_set:
                        dest = next(iter(dest_set)) # DFA: exactly one destination
                        grp_idx = next(
                            (i for i, g in enumerate(teta_n) if dest in g), -1
                        )
                        sig.append(grp_idx)
                    else:
                        sig.append(-1)
                sig = tuple(sig) # tuple so it can be used as a dict key
                if sig not in patterns:
                    patterns[sig] = set()
                patterns[sig].add(state)

            for new_group in patterns.values():
                teta_n_plus_1.append(frozenset(new_group)) # frozenset for hashability

        display_partition(teta_n_plus_1, automaton, step)

         # Stability check: compare as sets of frozensets to ignore ordering.
        # If the partition is unchanged, the algorithm has converged.
        if set(teta_n_plus_1) == set(teta_n):
            break
        teta_n = teta_n_plus_1

    if len(teta_n) == len(automaton['states']):
        print("\nThe automaton is already minimal.")
    else:
        print(f"\nMinimization complete: {len(automaton['states'])} → {len(teta_n)} states.")
    # Each group in the final partition becomes one state in the minimal DFA
    return build_minimal_dfa(automaton, teta_n)


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
    #The automaton MUST be DETERMINISTIC and COMPLETE.
    #To ensure every word follows exactly ONE unique path. 
    comp = copy.deepcopy(automaton)
    #We use deepcopy to create a fully independent object in memory so no modif on the original 
    comp['finals'] = automaton['states'] - automaton['finals']
    #Only final states has to be changed/swapped.
    #States, transitions and initial state remain the same.
    print("Complement automaton built (final and non-final states swapped).")
    display_automata(comp)
    word = input("Enter a word to test on the complement (or 'end' to stop): ").strip()
    while word != "end":
        if recognize_word(comp, word):
            print(f"  '{word}' is accepted by the complement.")
        else:
            print(f"  '{word}' is rejected by the complement.")
        word = input("Enter a word to test on the complement (or 'end' to stop): ").strip()
    return comp


import tempfile
import webbrowser
from pathlib import Path


import tempfile
import webbrowser
from pathlib import Path


def open_graphviz_graph(automaton, filename="automaton_graph"):
    """
    Build a Graphviz visualization of the automaton
    and open it in the browser.
    """

    dot = Digraph(format="png")
    dot.attr(rankdir="LR")   # left to right
    dot.attr("node", shape="circle")

    # fake start node
    dot.node("start", shape="none", label="")

    # states
    for state in automaton["states"]:
        state_name = str(state)

        if state in automaton["finals"]:
            dot.node(state_name, shape="doublecircle")
        else:
            dot.node(state_name, shape="circle")

    # initial arrows
    for init in automaton["initials"]:
        dot.edge("start", str(init))

    # transitions
    for src, trans in automaton["transitions"].items():
        for symbol, destinations in trans.items():
            for dest in destinations:
                dot.edge(str(src), str(dest), label=str(symbol))

    # render file
    output_path = dot.render(filename=filename, cleanup=True)

    # open generated image
    webbrowser.open(Path(output_path).resolve().as_uri())

    print(f"Graphviz graph opened: {output_path}")