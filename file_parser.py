"""
Reads an automaton from a file and returns it as a dictionary.
"""
def read_automaton():
    automaton = {
        'alphabet': set(),
        'states': set(),
        'initials': [],
        'finals': set(),
        'transitions': {}
    }
    
    file_path = 'automata.txt'
    # .zfill(2) matches your #03 or #04 image format
    target_id = input("Which automaton do you want to read? ").strip().zfill(2)
    found = False

    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Look for the ID header
        if line.startswith(f"#ID:{target_id}"):
            found = True
            i += 1
            # Continue reading until the next ID or end of file
            while i < len(lines):
                section_line = lines[i].strip()
                if not section_line or section_line.startswith("#ID:"):
                    break
                
                # Split key and value safely
                if ":" in section_line:
                    key, value = section_line.split(":", 1)
                    value = value.strip()

                    if key == "ALPHABET":
                        automaton['alphabet'] = set(s.strip() for s in value.split(",") if s.strip())
                    
                    elif key == "STATES":
                        automaton['states'] = set(s.strip() for s in value.split(",") if s.strip())
                        # Pre-initialize transitions for all states
                        for state in automaton['states']:
                            automaton['transitions'][state] = {symbol: set() for symbol in automaton['alphabet']}

                    elif key == "INITIALS":
                        automaton['initials'] = [s.strip() for s in value.split(",") if s.strip()]

                    elif key == "TERMINALS":
                        automaton['finals'] = set(s.strip() for s in value.split(",") if s.strip())

                    elif key == "TRANSITIONS":
                        # Logic for: src,symbol,dest | src,symbol,dest
                        for trans in value.split("|"):
                            parts = [p.strip() for p in trans.split(",")]
                            if len(parts) == 3:
                                src, sym, dest = parts
                                # Ensure the nested dictionary exists
                                if src not in automaton['transitions']:
                                    automaton['transitions'][src] = {}
                                if sym not in automaton['transitions'][src]:
                                    automaton['transitions'][src][sym] = set()
                                
                                automaton['transitions'][src][sym].add(dest)
                i += 1
            break # Exit the main loop once we've processed the specific ID
        i += 1

    if not found:
        print(f"Automaton #{target_id} not found.")
        return None

    return automaton