from file_parser import read_automaton
from automaton import display_automata, recognize_word, read_word, is_standard, is_deterministic, is_complete
from operation import standardization, determinize, completion, minimization, complement

def menu():
    print("\n" + "=" * 35)
    print("        Automaton Menu")
    print("=" * 35)
    print("1. Display automaton")
    print("2. Check properties (std / det / complete)")
    print("3. Standardize")
    print("4. Determinize & complete")
    print("5. Minimize")
    print("6. Complement")
    print("7. Test a word")
    print("8. Load another automaton")
    print("0. Exit")
    print("=" * 35)
    return input("Choose an option: ").strip()


def check_properties(fa):
    print(f"  Standard    : {'yes' if is_standard(fa) else 'no'}")
    print(f"  Deterministic: {'yes' if is_deterministic(fa) else 'no'}")
    print(f"  Complete    : {'yes' if is_complete(fa) else 'no'}")


def main():
    try:
        current_fa = read_automaton()
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    while True:
        choice = menu()

        if choice == "0":
            print("Goodbye.")
            break

        elif choice == "1":
            display_automata(current_fa)

        elif choice == "2":
            check_properties(current_fa)

        elif choice == "3":
            if is_standard(current_fa):
                print("Automaton is already standard — skipping.")
            else:
                current_fa = standardization(current_fa)
                display_automata(current_fa)

        elif choice == "4":
            # BUG FIX: guard against determinizing an already-deterministic FA
            # (the project spec says this must be treated as an error).
            if is_deterministic(current_fa):
                if is_complete(current_fa):
                    print("Automaton is already a complete DFA — nothing to do.")
                else:
                    print("Automaton is deterministic but not complete → completing.")
                    current_fa = completion(current_fa)
                    display_automata(current_fa)
            else:
                print("Automaton is non-deterministic → determinizing & completing.")
                current_fa = determinize(current_fa)
                display_automata(current_fa)

        elif choice == "5":
            if not is_deterministic(current_fa) or not is_complete(current_fa):
                print("Please obtain a complete deterministic FA first (option 4).")
            else:
                current_fa = minimization(current_fa)
                display_automata(current_fa)

        elif choice == "6":
            if not is_deterministic(current_fa) or not is_complete(current_fa):
                print("Please obtain a complete deterministic FA first (option 4).")
            else:
                comp_fa = complement(current_fa)
                display_automata(comp_fa)
                word = read_word()
                while word != "end":
                    if recognize_word(comp_fa, word):
                        print(f"  '{word}' is accepted by the complement.")
                    else:
                        print(f"  '{word}' is rejected by the complement.")
                    word = read_word()

        elif choice == "7":
            word = read_word()
            while word != "end":
                if recognize_word(current_fa, word):
                    print(f"  '{word}' is accepted.")
                else:
                    print(f"  '{word}' is rejected.")
                word = read_word()

        elif choice == "8":
            try:
                current_fa = read_automaton()
            except Exception as e:
                print(f"Error loading file: {e}")

        else:
            print("Unknown option — please try again.")


if __name__ == "__main__":
    main()
