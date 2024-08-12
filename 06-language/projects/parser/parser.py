import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP Conj VP | NP VP Conj NP VP

NP -> N | Det NP | AdjP NP | NP PP
VP -> V | V NP | AdvP VP | AdvP VP | V PP
AdjP -> Adj | Adj Adj
AdvP -> Adv
PP -> P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Tokenizes each element in sentence
    tokenized_words = nltk.tokenize.word_tokenize(sentence)

    # Creates list lowercase words from tokenized elements that only have alphabet characters in them
    processed_words = [word.lower() for word in tokenized_words if word.isalpha()]

    return processed_words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # Returns True value if "NP" exists within any child subtrees of current subtree
    def has_np_child(subtree):
        for child_subtree in subtree.subtrees():
            if child_subtree == subtree:
                continue
            elif child_subtree.label() == "NP":
                return True

        return False

    result = []

    # Iterates through subtrees that have a label of "NP"
    for subtree in tree.subtrees(lambda x: x.label() == "NP"):
        # Checks if subtrees children contains more "NP"
        if not has_np_child(subtree):
            result.append(subtree)

    return result


if __name__ == "__main__":
    main()
