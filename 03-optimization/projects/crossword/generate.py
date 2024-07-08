import sys
import copy

from crossword import *
from collections import deque


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Deep copy of domains to ensure consistent iteration of words in domain while as we remove words
        domains_copy = copy.deepcopy(self.domains)

        for var in domains_copy:
            for word in domains_copy[var]:
                # Removes word from variable if the word length does not equal the variable length (unary constraint)
                if len(word) != var.length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Return value describing if revision was made
        revision_made = False
        # Deep copy of domains to ensure consistent iteration of words in domain while as we remove words
        domains_copy = copy.deepcopy(self.domains)
        # Gets overlapping indices for x and y
        x_overlap, y_overlap = self.crossword.overlaps[x, y]

        for x_word in domains_copy[x]:
            no_value_matched = True
            for y_word in domains_copy[y]:
                if x_word[x_overlap] == y_word[y_overlap]:
                    no_value_matched = False
                    break # Breaks for loop since we only need one y_word match to ensure we keep x_word

            # If we iterate through all y_words without getting a value matched, then we revise and remove x_word
            if no_value_matched:
                self.domains[x].remove(x_word)
                revision_made = True

        return revision_made

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # If arc argument is None, initializes queue to have all arcs in problem
        if arcs == None:
            queue = deque([]) # Using deque here for O(1) pops at index 0
            for var_1 in self.domains:
                for var_2 in self.crossword.neighbors(var_1):
                    if self.crossword.overlaps[var_1, var_2] != None:
                        queue.append((var_1, var_2))
        else:
            queue = deque(arcs) # Using deque here for O(1) pops at index 0

        while len(queue) > 0:
            x, y = queue.popleft()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False

                # After revision, we cannot guarantee the neighbors to x are arc consistent so we append those arcs back to the queue to be processed
                for neighbor in self.crossword.neighbors(x):
                    if neighbor != y:
                        queue.append((neighbor, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment) == len(self.domains)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Returns false if there are any duplicates in assignment
        if len(assignment.values()) != len(set(assignment.values())):
            return False

        for var in assignment:
            # Checks unary constraints (correct length)
            if var.length != len(assignment[var]):
                return False

            # Checks binary constraints (conflicts with neighboring variables)
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    x_overlap, y_overlap = self.crossword.overlaps[var, neighbor]
                    if assignment[var][x_overlap] != assignment[neighbor][y_overlap]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        result = []
        for word in self.domains[var]:
            values_ruled_out = 0
            for neighbor_var in self.crossword.neighbors(var):
                # Skip every neighbor variable that has been already assigned to avoid duplicates
                if neighbor_var in assignment:
                    continue

                x_overlap, y_overlap = self.crossword.overlaps[var, neighbor_var]
                for neighbor_word in self.domains[neighbor_var]:
                    if word[x_overlap] != neighbor_word[y_overlap]:
                        values_ruled_out += 1

            result.append((values_ruled_out, word))

        # Sorts by values_ruled_out replaces each element (values_ruled_out, word) with just word
        result.sort()
        for i in range(len(result)):
            result[i] = result[i][1]

        return result

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        arr = []
        for var in self.domains:
            if var not in assignment:
                arr.append([len(self.domains[var]), var])

        # Sort based on remaining values in domain
        arr.sort(key=lambda x:x[0])
        # Returns variable that has the least remaining values in its domain
        return arr[0][1]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Base case - successfully completing assignment
        if len(self.domains) == len(assignment):
            return assignment

        # Iterates through every potential word on unassigned variable and recursively checks to see if there are any successful assignments
        unassigned_var = self.select_unassigned_variable(assignment)
        for word in self.domains[unassigned_var]:
            assignment[unassigned_var] = word
            if self.consistent(assignment):
                potential_assignment = self.backtrack(assignment)
                if potential_assignment is not None:
                    return potential_assignment

            # Deletes key value pair after we check all potential assignments
            del assignment[unassigned_var]

        # After iterating through all possible cases, we return None
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
