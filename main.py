from chatterbot import ChatBot, filters
from chatterbot.trainers import ListTrainer

from conversations.smalltalk import train_smalltalk, farewells

DATABASE_FILE_NAME = "bot.sqlite3"

if __name__ == '__main__':
    bot = ChatBot(
        "WeatherChatBot",
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        input_adapter='chatterbot.input.TerminalAdapter',
        output_adapter='chatterbot.output.TerminalAdapter',
        logic_adapters=[
            "chatterbot.logic.MathematicalEvaluation",
            "conversations.weather_adapter.CurrentWeatherAdapter",
            "conversations.weather_adapter.WeatherForecastAdapter",
            "conversations.currency_adapter.CurrencyAdapter",
            "conversations.joke_adapter.JokeAdapter",
            "conversations.time_adapter.TimeAdapter",
            {
                "import_path": "chatterbot.logic.BestMatch",
                "default_response": "Przykro mi, ale nie rozumiem :(",
                "maximum_similarity_threshold": 0.90
            }
        ],
        database_uri="sqlite:///" + DATABASE_FILE_NAME,
        filters=[filters.get_recent_repeated_responses]
    )

    trainer = ListTrainer(bot)
    train_smalltalk(trainer)

    run_loop = True
    farewells_lower = list(map(lambda x: x.lower(), farewells))
    print("Napisz coś...")
    while run_loop:
        try:
            user_input = input("Zapytanie > ")
            if user_input.lower() in farewells_lower:
                run_loop = False
            bot_response = bot.get_response(user_input)
            print(bot_response)
        except (KeyboardInterrupt, EOFError, SystemExit):
            print("Kończymy pracę...")
            run_loop = False
