#read_automaton Erwann
#save ?

def read_automaton():
    automaton = {
        'alphabet': set(),
        'states': set(),
        'initials': [],
        'finals': set(),
        'transitions': {}
    }
    i = 0
    file_path = 'automata.txt'
    found = False

    with open(file_path, "r") as f:
        lines = f.readlines()

    automata_number = input("Which automaton do you want to read? ").zfill(2)

    # Find the block starting with the requested ID
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith(f"#ID:{automata_number}"):
            found = True
            i += 1
            break
        i += 1

    if not found:
        raise ValueError(f"Automaton #{automata_number} not found in file.")

    # BUG FIX: the original loop used `for _ in range(5)` which stops after 5
    # lines regardless of how many fields remain; replaced with a content-driven
    # loop that stops at a blank line or the next #ID marker.
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("#ID:"):
            break

        if line.startswith("ALPHABET:"):
            symbols = line.split(":", 1)[1]
            if symbols.strip():
                automaton['alphabet'] = set(s.strip() for s in symbols.split(","))

        elif line.startswith("STATES:"):
            states = line.split(":", 1)[1]
            if states.strip():
                # BUG FIX: keep states as strings to stay consistent with
                # transitions (which are also keyed by the raw string from file).
                automaton['states'] = set(s.strip() for s in states.split(","))

        elif line.startswith("INITIALS:"):
            initials = line.split(":", 1)[1]
            if initials.strip():
                automaton['initials'] = [s.strip() for s in initials.split(",")]

        elif line.startswith("TERMINALS:"):
            terminals = line.split(":", 1)[1]
            if terminals.strip():
                automaton['finals'] = set(s.strip() for s in terminals.split(","))

        elif line.startswith("TRANSITIONS:"):
            transitions_str = line.split(":", 1)[1]
            if transitions_str.strip():
                for trans in transitions_str.split("|"):
                    parts = [p.strip() for p in trans.split(",")]
                    if len(parts) == 3:
                        src, sym, dest = parts
                        if src not in automaton['transitions']:
                            automaton['transitions'][src] = {}
                        if sym not in automaton['transitions'][src]:
                            automaton['transitions'][src][sym] = set()
                        automaton['transitions'][src][sym].add(dest)

        i += 1

    # BUG FIX: ensure every state has an entry in transitions (even if empty)
    # so that callers never get a KeyError when iterating over all states.
    for state in automaton['states']:
        if state not in automaton['transitions']:
            automaton['transitions'][state] = {}

    return automaton