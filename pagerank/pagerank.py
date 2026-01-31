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
    key = {}

    pages = round(float((1 - damping_factor) / len(corpus.keys())) , 5)
    for i in corpus.keys():
        key[i] = pages
    links = corpus[page]
    n = len(links)
    if  n == 0:
        for i in corpus.keys():
            key[i] += (damping_factor / len(corpus.keys()))
        return key
    for i in links:
        key[i] += (damping_factor / n)
    return key



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    key = {}
    random_number = random.randint(0, len(corpus.keys()) - 1)
    list_number = list(corpus.keys())[random_number]
    count = 0
    for i in corpus.keys():
        key[i] = 0
    while count < n :
        key[list_number] += 1
        count += 1
        rand = random.random()
        diction = transition_model(corpus, list_number, damping_factor)
        for i in diction:
            if diction[i] < rand:
                rand -= diction[i]
            else:
                list_number = i
                break
    normalize = sum(key.values())
    for i in key.keys():
        key[i] = round(key[i] / normalize , 5)
    return key
    

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_ranking = {}
    for i in corpus.keys():
        page_ranking[i] = float(1/len(corpus.keys()))
    
    stop = 0
    while not stop:
        top_ranking = {}
        stop = 1
        for i in page_ranking.keys():
            temp = page_ranking[i]
            top_ranking[i] = float((1-damping_factor)/ len(corpus.keys()))
            for page, link in corpus.items():
                if i in link:
                    top_ranking[i] += float(damping_factor * page_ranking[page]/len(link))
            if abs(temp - top_ranking[i]) > 0.001:   
                stop = 0
        for i in page_ranking.keys():
            page_ranking[i] = top_ranking[i]
    return page_ranking


if __name__ == "__main__":
    main()
