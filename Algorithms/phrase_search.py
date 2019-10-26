import re
from itertools import combinations
from difflib import SequenceMatcher as SM


def phrase_search(l_object_list: list, search_string: str) -> int:
    # format pattern to match {word} in strings
    format_pattern = re.compile('\{(\w*?)\}')
    # working with every object seperatly 
    for z_object in l_object_list:
        # Creating list of patterns to find match with search string
        patterns = []
        # Creating list of {words} to create patterns based on combination
        key_words = format_pattern.findall(z_object["phrase"])
        # If key words in object, we do magic
        if key_words:
            # we do not want to modify original object
            z_object_phrase = z_object["phrase"]
            # it's complicated to work with key words
            # therefore, we change them to indexes
            # yes, I could use func here, but readability of code is more important
            for i, key_word in enumerate(key_words):
                z_object_phrase = z_object_phrase.replace('{' + key_word + '}', '{' + str(i) + '}')
            # creating list of all possible combinations based on number of different key words
            slots_combinations = list(combinations(z_object["slots"], len(key_words)))
            # creating list of patterns
            for str_variations in slots_combinations:
                patterns.append(z_object_phrase.format(*str_variations))
        # if there are not key words, we just add phrase to pattern list
        else:
            patterns.append(z_object["phrase"])
        # Because we have list of patterns,
        #  we need to compare search_string with every string, not element of list
        # if [pattern for pattern in patterns if search_string in pattern]:
        # Because you asked for FuzzySearch, so let it be
        if [pt for pt in patterns if SM(None, search_string, pt).ratio() > 0.9]:
            return z_object['id']
    return 0


if __name__ == "__main__":
    """ 
    len(object) != 0
    object["id"] > 0
    0 <= len(object["phrase"]) <= 120
    0 <= len(object["slots"]) <= 50
    """
    object_list = [
        {"id": 1, "phrase": "Hello world!", "slots": []},
        {"id": 2, "phrase": "I wanna {pizza}", "slots": ["pizza", "BBQ", "pasta"]},
        {"id": 3, "phrase": "Give me your power", "slots": ["money", "gun"]},
        {"id": 4, "phrase": "I wanna {eat} and {drink}", "slots": ["pizza", "BBQ", "pepsi", "tea"]}
    ]

    assert phrase_search(object_list, 'I wanna pasta') == 2
    assert phrase_search(object_list, 'Give me your power') == 3
    assert phrase_search(object_list, 'Hello world!') == 1
    assert phrase_search(object_list, 'I wanna nothing') == 0
    assert phrase_search(object_list, 'Hello again world!') == 0
    assert phrase_search(object_list, 'I need your clothes, your boots & your motorcycle') == 0
