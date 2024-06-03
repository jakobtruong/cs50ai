from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Knowledge based on the structure
    # Character cannot be both a knight and a knave and a character must be one or the other
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # Knowledge based on what the character A said
    # Implications gathered by character A saying they are both a knight and a knave
    Implication(AKnight, And(AKnight, AKnave)), # Implication that whatever the knights says is the truth
    Implication(AKnave, Not(And(AKnight, AKnave))) # Implication that whataver is knave says is a lie
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Knowledge based on the structure
    # Character cannot be both a knight and a knave and a character must be one or the other
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # Knowledge based on what the character A said
    # Implications gathered from A saying that they are both knaves
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Knowledge based on the structureCharacter cannot be both a knight and a knave
    # Character cannot be both a knight and a knave and a character must be one or the other
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # Knowledge based on what the character A said
    # Implications gathered from A saying A and B are of the same kind
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))), # Implication that whatever the knights says is the truth
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))), # Implication that whataver is knave says is a lie

    # Knowledge based on what the character B said
    # Implications gathered from B saying A and B are of different kinds
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Knowledge based on the structure
    # Character cannot be both a knight and a knave and a character must be one or the other
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # Knowledge based on what the character A said
    # Either A says "I am a knight" or "I am a knave" but we don't know which one
    Or(
        And(
            Implication(AKnight, AKnight),
            Implication(AKnave, Not(AKnight))
        ),
        And(
            Implication(AKnight, AKnave),
            Implication(AKnave, Not(AKnave))
        )
    ),

    # Knowledge based on what the character B said
    # Implication that if B is a knight (tells the truth), says that A said that "I am a knave"
    Implication(BKnight, And(
        Implication(AKnight, AKnave),
        Implication(AKnave, Not(AKnave)
    ))),

    # If character B is a knave, then B saying A said something is not true therefore no implications can be gathered in this case

    # Implications gathered from character B saying C is a knave
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),

    # Knowledge based on what the character C said
    # Implications gathered from character C saying A is a knight
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
