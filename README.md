# Harvard University's CS50AI - Introduction to Artificial Intelligence with Python (2024)

> Please <strong>DO NOT</strong> use the source code directly, they are provided strictly for reference and knowledge sharing. Plagiarism is strictly prohibited by both the Harvard University and the edX platform. Please see CS50AI's [academic honesty policy](https://cs50.harvard.edu/ai/2024/honesty/) and [license](https://cs50.harvard.edu/ai/2024/license/) for additional details.

This course explores the concepts and algorithms at the foundation of modern artificial intelligence, diving into the ideas that give rise to technologies like game-playing engines, handwriting recognition, and machine translation. Through hands-on projects, students gain exposure to the theory behind graph search algorithms, classification, optimization, reinforcement learning, and other topics in artificial intelligence and machine learning as they incorporate them into their own Python programs. By course’s end, students emerge with experience in libraries for machine learning as well as knowledge of artificial intelligence principles that enable them to design intelligent systems of their own.

### Artificial Intelligence

Artificial Intelligence (AI) covers a range of techniques that appear as sentient behavior by the computer. For example, AI is used to recognize faces in photographs on your social media, beat the World’s Champion in chess, and process your speech when you speak to Siri or Alexa on your phone. This course will explore some of the ideas that make AI possible.

This course will explore ideas and topics that make artificial intelligence possible:

0. **[Search](#lecture-0---search)**: Finding a solution to a problem, like a navigator app that finds the best route from your origin to the destination, or like playing a game and figuring out the next move
1. **[Knowledge](#lecture-1---knowledge)**: Representing information and drawing inferences from it
2. **[Uncertainty](#lecture-2---uncertainty)**: Dealing with uncertain events using probability
3. **[Optimization](#lecture-3---optimization)**: Finding not only a correct way to solve a problem, but a better—or the best—way to solve it
4. **[Learning](#lecture-4---learning)**: Improving performance based on access to data and experience. For example, your email is able to distinguish spam from non-spam mail based on past experience
5. **[Neural Networks](#lecture-5---neural-networks)**: A program structure inspired by the human brain that is able to perform tasks effectively
6. **[Language](#lecture-6---language)**: Processing natural language, which is produced and understood by humans

### Setting Up Virtual Environment (Optional)
In case any readers of this are unfamiliar with virtual environments, it is generally recommended to set up virtual environments for each project to create an isolated python environment. Virtual environments are stable, reproducible, and portable while leaving just the necessary dependencies for the project to execute successfully. This can help avoid various environment and dependency conflicts that can vary from developer to developer.

To create the virtual environment, use the following command. The last argument (ex: '.venv') can be freely renamed to anything the user decides to name the virtual environment folder.

```bash
python3 -m venv .venv
```

To activate the virtual environment, use the following command.
```bash
source .venv/bin/activate
```

To deactivate the virtual environment, use `deactivate` in the terminal.

Using `which python3` can be useful for identifying and confirming where your current Python3 path is pointing to.

---
Finally, install necessary dependencies using the following command.
```bash
pip install -r requirements.txt
```


## Lecture 0 - [Search](00-Search)

This lecture explores algorithms used for navigating problem spaces. It starts with basic search techniques like breadth-first search (BFS) and depth-first search (DFS), and progresses to more advanced informed search algorithms such as A* and greedy search. This lecture emphasizes how search algorithms are used to solve problems by finding optimal paths or solutions.

**Key Concepts:** Problem representation, state spaces, search trees, exploration strategies, and heuristic functions.

### Projects

- [Degrees](00-Search/projects/degrees)
- [Tic-Tac-Toe](00-Search/projects/tictactoe)

## Lecture 1 - [Knowledge](01-Knowledge)

The focus of this lecture is on how knowledge is represented in AI systems and how reasoning is performed. It introduces propositional logic and predicate logic, explaining how these formal systems are used to represent facts and rules. The lecture shows how AI systems use logic to make decisions and solve problems based on given knowledge.

**Key Concepts:** Logical operators, truth tables, knowledge bases, inference rules, and logical reasoning.

### Projects

- [Knights](01-Knowledge/projects/knights)
- [Minesweeper](01-Knowledge/projects/minesweeper)

## Lecture 2 - [Uncertainty](02-Uncertainty)

This lecture provides an introduction to probabilistic models and statistical methods, which are crucial for handling uncertainty in AI. It covers concepts such as random variables, probability distributions, and Bayes' theorem. Demonstrates how probabilistic reasoning is applied in AI to make predictions and decisions based on uncertain or incomplete information.

**Key Concepts:** Probability theory, conditional probability, Bayesian inference, and statistical estimation.

### Projects

- [PageRank](02-Uncertainty/projects/pagerank)
- [Heredity](02-Uncertainty/projects/heredity)

## Lecture 3 - [Optimization](03-Optimization)

Explores optimization techniques used to improve AI models and algorithms. It focuses on methods for finding the best parameters or solutions within given constraints. This lecture illustrates how optimization algorithms are used to train models effectively and efficiently

**Key Concepts:** Gradient descent and its variants (stochastic gradient descent, mini-batch gradient descent), optimization for continuous and discrete problems, convergence criteria, and hyperparameter tuning.

### Projects

- [Crossword](03-Optimization/projects/crossword)

## Lecture 4 - [Learning](04-Learning)

Focuses on supervised learning, where models are trained using labeled data. The lecture covers various supervised learning algorithms including linear regression, logistic regression, and support vector machines (SVMs). This lecture goes into depth on how to build and evaluate models that predict outcomes based on input features.

**Key Concepts:** Training and testing datasets, model evaluation metrics, overfitting and underfitting, and cross-validation.

### Projects

- [Shopping](04-Learning/projects/shopping)
- [Nim](04-Learning/projects/nim)

## Lecture 5 - [Neural Networks](05-Neural-Networks)

This lecture dives into neural networks and deep learning, which are powerful tools for handling complex tasks. It covers the architecture of neural networks, including layers, activation functions, and backpropagation. Additionally, it explains how these neural networks are trained and used for tasks like image and speech recognition.

**Key Concepts:** Perceptrons, multi-layer perceptrons (MLPs), convolutional neural networks (CNNs), and recurrent neural networks (RNNs).

### Projects

- [Traffic](05-Neural-Networks/projects/traffic)

## Lecture 6 - [Language](06-Language)

This lecture focuses on natural language processing, enabling machines to understand and generate human language. It covers text processing techniques and various NLP models. Demonstrates how NLP techniques are applied in tasks like sentiment analysis and machine translation.

**Key Concepts:** Tokenization, part-of-speech tagging, named entity recognition, language modeling, and sequence-to-sequence models.

### Projects

- [Parser](06-Language/projects/parser)
- [Questions](06-Language/projects/questions)

## Certificate
[Certificate of Completion](https://cs50.harvard.edu/certificates/ca65df30-05cc-4b57-95c6-aafcb2ebdc8c)
