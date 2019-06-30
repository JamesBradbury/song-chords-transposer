from collections import defaultdict

def most_common_animal(observed_items):
    known_animal_names = {"dog", "cat", "bear"}
    occurrences = defaultdict(int)
    for item in observed_items:
        if item in known_animal_names:
            print(item, "is known.")
        else:
            print(item, "is unknown.")
        occurrences[item] += 1
    return max(occurrences, key=occurrences.get)
