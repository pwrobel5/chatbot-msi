farewells = ["Na razie", "Miłego dnia", "Żegnam", "Do widzenia"]


def train_polite(trainer):
    user_sentences = ["Dziękuję", "Dzięki"]
    answers = ["Nie ma za co", "Drobiazg"]
    polite_combinations = [[i, j] for i in user_sentences for j in answers]
    for combination in polite_combinations:
        trainer.train(combination)


def train_greetings(trainer):
    greetings = ["Cześć", "Witam", "Dzień dobry"]
    greetings_combinations = [[i, j] for i in greetings for j in greetings]
    for combination in greetings_combinations:
        trainer.train(combination)


def train_farewells(trainer):
    farewells_combinations = [[i, j] for i in farewells for j in farewells]
    for combination in farewells_combinations:
        trainer.train(combination)


def train_howareyou(trainer):
    questions = ["Jak się masz?", "Co u ciebie?"]
    answers = ["W porządku, a ty?", "Hmmm, jako tako. A co u ciebie?", "Świetnie, a u ciebie jak tam?"]
    user_communication = [["W porządku", "Cieszę się"], ["OK", "Fajnie!"],
                          ["Benadziejnie", "Oooo, przykro mi"]]
    howareyou_combinations = [[i, j] for i in questions for j in answers]
    for combination in howareyou_combinations:
        for user_case in user_communication:
            trainer.train(combination + user_case)


def train_joke_responses(trainer):
    trainer.train(["Haha", "Dobre, co?"])


def train_smalltalk(trainer):
    train_polite(trainer)
    train_greetings(trainer)
    train_farewells(trainer)
    train_howareyou(trainer)
    train_joke_responses(trainer)
