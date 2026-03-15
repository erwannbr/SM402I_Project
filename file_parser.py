#read_automaton Erwann
#save ?

def read_automaton():
    automaton = {
        'alphabet': set(),
        'states': set(),
        'initials': set(),
        'finals': set(),
        'transitions': []
    }
    i = 0
    j = 1
    file_path = 'automata.txt'
    found = False     

    with open(file_path, "r") as f:
        lines = f.readlines()

    automata_number = input("Which automaton do you want to read ? ")
                                                                                                                                                                                                                                                                                                                                                                                                                          

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
            symbols = line.split(" : ")
            if symbols:
                print(symbols)

read_automaton()
