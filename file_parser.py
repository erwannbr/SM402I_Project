"""
Reads an automaton from a file and returns it as a dictionary.
"""
def read_automaton():
    #different variables
    found = False
    i = 0
    
    #define the automaton (diff states)
    automaton = {
        'alphabet': set(),
        'states': set(),
        'initials': [],
        'finals': set(),
        'transitions': {}
    }
    
    #name of the file where there is all the automatas
    file_path = 'automata.txt'
    #.zfill(2) matches your #03 or #04 image format, read the automaton at the reight line
    target_id = input("Which automaton do you want to read? ").strip().zfill(2)

    #try to open the file where there is all the files
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None

    #read the file line by line
    while i < len(lines):
        line = lines[i].strip()
        #Look for the ID header
        if line.startswith(f"#ID:{target_id}"):
            found = True
            i += 1
            #Continue reading until the next ID or end of file
            while i < len(lines):
                section_line = lines[i].strip()
                if not section_line or section_line.startswith("#ID:"):
                    break
                
                # Split key and value safely
                if ":" in section_line:
                    key, value = section_line.split(":", 1) #need to split in order to avoid errors
                    value = value.strip()
                    
                    #check the key, and cherche for the alphabet
                    if key == "ALPHABET":
                        automaton['alphabet'] = set(s.strip() for s in value.split(",") if s.strip())
                    
                    #checle for the states, key is "STATES"
                    elif key == "STATES":
                        automaton['states'] = set(s.strip() for s in value.split(",") if s.strip())
                        # Pre-initialize transitions for all states
                        for state in automaton['states']:
                            automaton['transitions'][state] = {symbol: set() for symbol in automaton['alphabet']}
                    
                    #check for the initials states
                    elif key == "INITIALS":
                        automaton['initials'] = [s.strip() for s in value.split(",") if s.strip()]

                    #check for the finals states
                    elif key == "TERMINALS":
                        automaton['finals'] = set(s.strip() for s in value.split(",") if s.strip())
                    
                    #check for the transitions
                    elif key == "TRANSITIONS":
                        #logic for: src,symbol,dest | src,symbol,dest
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
            break #exit the main loop once we've processed the specific ID
        i += 1

    #if the automaton was not found
    if not found:
        print(f"Automaton #{target_id} not found.")
        return None
    
    #return the autoamton as a dictionnary
    return automaton