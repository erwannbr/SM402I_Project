"""
Reads the automata.txt file and returns a dictionary representing the automaton.
"""
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

    while i < len(lines):
        line = lines[i].strip()
        if line.startswith(f"#ID:{automata_number}"):
            found = True
            i += 1
            break
        i += 1

    if not found:
        raise ValueError(f"Automaton #{automata_number} not found in file.")

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

    for state in automaton['states']:
        if state not in automaton['transitions']:
            automaton['transitions'][state] = {}

    return automaton