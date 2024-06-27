import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability_distribution = {}
    num_pages = len(corpus)

    # Determines if we get a random page or not based on damping factor
    choose_random_page = True if random.random() >= damping_factor else False
    if page not in corpus or len(corpus[page]) == 0 or choose_random_page:
        equal_probability = 1 / num_pages
        for key in corpus:
            probability_distribution[key] = equal_probability

    else:
        equal_probability = 1 / len(corpus[page])
        for page_link in corpus[page]:
            probability_distribution[page_link] = equal_probability

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_visit_count = {}
    for page in corpus:
        page_visit_count[page] = 0

    # Sets first page visited to be random
    random_page_probability = transition_model(corpus, 'random string not in corpus to get random page', damping_factor)
    curr_page = random.choice(list(random_page_probability.keys()))

    # Iterates n number of times to get page and update page visit count based on damping factor
    page_visit_count[curr_page] += 1
    for i in range(1, n):
        next_page_probability = transition_model(corpus, curr_page, damping_factor)
        next_page_distribution_possibilities = list(next_page_probability.keys())
        next_page_distribution_probabilities = [next_page_probability[page] for page in next_page_distribution_possibilities]

        curr_page = random.choices(next_page_distribution_possibilities, next_page_distribution_probabilities, k=1)[0]
        page_visit_count[curr_page] += 1

    page_rank = {}
    for page in page_visit_count:
        page_rank[page] = page_visit_count[page] / n
    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    threshold = .001
    prev_probabilities = {}
    curr_probabilities = {}

    # Starts every page out with an equal probability
    for page in corpus:
        prev_probabilities[page] = 1 / num_pages

    # First condition probability that remains a constant
    first_condition_probability = (1 - damping_factor) / num_pages
    while True:
        for curr_page in corpus:
            second_condition_probability = 0
            for page in corpus:
                # Considers probability if the page has a link outgoing to the current page we are calculating
                if curr_page in corpus[page]:
                    second_condition_probability += prev_probabilities[page] / len(corpus[page])
                # In cases where page has no links, treat page as having link to any page including itself
                elif len(corpus[page]) == 0:
                        second_condition_probability += prev_probabilities[page] / num_pages

            second_condition_probability *= damping_factor
            curr_probabilities[curr_page] = first_condition_probability + second_condition_probability

        max_difference = max([abs(curr_probabilities[i] - prev_probabilities[i]) for i in prev_probabilities])
        prev_probabilities = curr_probabilities.copy()

        # Breaks iterations when max
        if max_difference < threshold:
            break

    return curr_probabilities


if __name__ == "__main__":
    main()
