from chatterbot import ChatBot, filters
from chatterbot.trainers import ListTrainer

from conversations.smalltalk import train_smalltalk, farewells

DATABASE_FILE_NAME = "bot.sqlite3"

if __name__ == '__main__':
    bot = ChatBot(
        "WeatherChatBot",
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        logic_adapters=[
            "chatterbot.logic.MathematicalEvaluation",
            "conversations.weather_adapter.CurrentWeatherAdapter",
            "conversations.weather_adapter.WeatherForecastAdapter",
            {
                "import_path": "chatterbot.logic.BestMatch",
                "default_response": "I am sorry, but I do not understand.",
                "maximum_similarity_threshold": 0.90
            },
            {
                "import_path": "chatterbot.logic.TimeLogicAdapter",
                "negative": [
                    "current weather:",
                    "What is the weather now:",
                    "give me the weather:",
                    "what is the weather like:",
                    "thank you"
                ]
            }
        ],
        database_uri="sqlite:///" + DATABASE_FILE_NAME,
        filters=[filters.get_recent_repeated_responses]
    )

    trainer = ListTrainer(bot)
    train_smalltalk(trainer)

    run_loop = True
    farewells_lower = list(map(lambda x: x.lower(), farewells))
    print("Type something...")
    while run_loop:
        try:
            user_input = input("You > ")
            if user_input.lower() in farewells_lower:
                run_loop = False
            bot_response = bot.get_response(user_input)
            print(bot_response)
        except (KeyboardInterrupt, EOFError, SystemExit):
            print("Ending work...")
            run_loop = False
