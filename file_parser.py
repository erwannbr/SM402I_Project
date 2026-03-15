#read_automaton Erwann
#save ?

def read_automaton():
    automaton = {
        'alphabet': set(),
        'states': set(),
        'initials': set(),
        'finals': set(),
        'transitions': {}
    }
    i = 0
    j = 1
    file_path = 'automata.txt'
    found = False     

    with open(file_path, "r") as f:
        lines = f.readlines()

    automata_number = input("Which automaton do you want to read ? ").zfill(2)
    automata_number = automata_number.zfill(2)
                                                                                                                                                                                                                                                                                                                                                                                                                          

    while i < len(lines):
        line = lines[i].strip()

        if line.startswith(f"#ID:{automata_number}"):
            found = True
            i += 1
            break
        i += 1

    if not found:
        raise ValueError("Automaton not found")   
    
    while j < 6:
        line = lines[i].strip()

        if line.startswith("ALPHABET:"):
            symbols = line.split(":")[1]
            if symbols.strip():
                automaton['alphabet'] = set(s.strip() for s in symbols.split(","))
            j += 1

        elif line.startswith("STATES:"):
            states = line.split(":")[1]
            if states.strip():
                automaton['states'] = set(s.strip() for s in states.split(","))
            j += 1

        elif line.startswith("INITIALS:"):
            initials = line.split(":")[1]
            if initials.strip():
                automaton['initials'] = set(s.strip() for s in initials.split(","))
            j += 1

        elif line.startswith("TERMINALS:"):
            terminals = line.split(":")[1]
            if terminals.strip():
                automaton['finals'] = set(s.strip() for s in terminals.split(","))
            j += 1

        elif line.startswith("TRANSITIONS:"):
            transitions = line.split(":")[1]
            if transitions.strip():
                for trans in transitions.split("|"):
                    if trans.strip():
                        parts = trans.strip().split(",")
                        if len(parts) == 3:
                            automaton['transitions'].append(
                                (parts[0].strip(), parts[1].strip(), parts[2].strip())
                            )
            j += 1

        i += 1

    return automaton


def display_automata(automaton):
    header = "     |"
    for letter in sorted(automaton['alphabet']):
        header += f" {letter}   |"
    print("\n" + header)
    print("-" * len(header))

    for state in sorted(automaton['states']):
        prefix = " "
        if state in automaton['initials']:
            prefix += "I"
        if state in automaton['finals']:
            prefix += "T"

        line = f"{prefix:<5}{state} |"

        for letter in sorted(automaton['alphabet']):
            destinations = []
            for trans in automaton['transitions']:
                if trans[0] == state and trans[1] == letter:
                    destinations.append(trans[2])
            if destinations:
                dest_str = ",".join(destinations)
                line += f"{dest_str:^5}|"
            else:
                line += "     |"
        print(line)


if __name__ == "__main__":
    automaton = read_automaton()
    display_automata(automaton)
