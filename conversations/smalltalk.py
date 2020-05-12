farewells = ["Bye", "Goodbye", "See you", "Have a nice day"]


def train_polite(trainer):
    user_sentences = ["Thank you", "Thanks"]
    answers = ["Nevermind", "You're welcome"]
    polite_combinations = [[i, j] for i in user_sentences for j in answers]
    for combination in polite_combinations:
        trainer.train(combination)
        

def train_greetings(trainer):
    greetings = ["Hey", "Hi", "Hello", "Welcome", "Good day"]
    greetings_combinations = [[i, j] for i in greetings for j in greetings]
    for combination in greetings_combinations:
        trainer.train(combination)


def train_farewells(trainer):
    farewells_combinations = [[i, j] for i in farewells for j in farewells]
    for combination in farewells_combinations:
        trainer.train(combination)


def train_howareyou(trainer):
    questions = ["How are you?", "How do you do?"]
    answers = ["Fine, what about you?", "Hmmm, not bad. How are you?", "Excellent, and you?"]
    user_communication = [["I'm fine", "I'm happy with that"], ["Not bad", "That is good"], ["Awful", "I'm sorry"]]
    howareyou_combinations = [[i, j] for i in questions for j in answers]
    for combination in howareyou_combinations:
        for user_case in user_communication:
            trainer.train(combination + user_case)


def train_jokes(trainer):
    questions = ["Make me laugh", "Tell a joke"]
    jokes = [
        "What is the longest word in the English language?\n'Smiles', because there is a"
        "mile between its first and last letters!",
        "Could you please call me a Taxi?\nYou're a taxi",
        "What's blue and smells like red paint?\nBlue paint"
    ]
    jokes_combinations = [[i, j] for i in questions for j in jokes]
    for combination in jokes_combinations:
        trainer.train(combination)


def train_smalltalk(trainer):
    train_polite(trainer)
    train_greetings(trainer)
    train_farewells(trainer)
    train_howareyou(trainer)
    train_jokes(trainer)
